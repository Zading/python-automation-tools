import argparse
import base64
import getpass
import hashlib
import hmac
import os
import secrets
import re
import sqlite3
import string
import sys
from datetime import datetime

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
except ImportError:  # pragma: no cover - runtime dependency check
    AESGCM = None
    Scrypt = None


DEFAULT_DB_NAME = "vault.db"
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_LENGTH = 32
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1


def require_crypto():
    if AESGCM is None or Scrypt is None:
        print(
            "Dependencia faltante: 'cryptography'.\n"
            "Instala con: pip install cryptography",
            file=sys.stderr,
        )
        sys.exit(1)


def utc_now():
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def derive_key(master_password, salt):
    kdf = Scrypt(salt=salt, length=KEY_LENGTH, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P)
    return kdf.derive(master_password.encode("utf-8"))


def key_check_value(key):
    return base64.b64encode(hmac.new(key, b"vault-check", hashlib.sha256).digest()).decode(
        "ascii"
    )


def encrypt_text(key, text):
    if text is None:
        return None
    aes = AESGCM(key)
    nonce = secrets.token_bytes(NONCE_SIZE)
    ciphertext = aes.encrypt(nonce, text.encode("utf-8"), None)
    return base64.b64encode(nonce + ciphertext).decode("ascii")


def decrypt_text(key, token):
    if token is None:
        return None
    raw = base64.b64decode(token.encode("ascii"))
    nonce = raw[:NONCE_SIZE]
    ciphertext = raw[NONCE_SIZE:]
    aes = AESGCM(key)
    return aes.decrypt(nonce, ciphertext, None).decode("utf-8")


def connect_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS vault_meta (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            salt BLOB NOT NULL,
            key_check TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            username TEXT,
            password_enc TEXT NOT NULL,
            notes_enc TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_entries_service ON entries(service)"
    )
    conn.commit()


def create_master_key(conn):
    print("Inicializando bóveda segura...")
    while True:
        master = getpass.getpass("Crea una contraseña maestra: ")
        confirm = getpass.getpass("Confirma la contraseña maestra: ")
        if master != confirm:
            print("No coinciden. Intenta de nuevo.")
            continue
        if len(master) < 10:
            print("La contraseña maestra debe tener al menos 10 caracteres.")
            continue
        break
    salt = secrets.token_bytes(SALT_SIZE)
    key = derive_key(master, salt)
    conn.execute(
        "INSERT INTO vault_meta (id, salt, key_check, created_at) VALUES (1, ?, ?, ?)",
        (sqlite3.Binary(salt), key_check_value(key), utc_now()),
    )
    conn.commit()
    print("Bóveda creada correctamente.")
    return key


def unlock_vault(conn):
    row = conn.execute("SELECT salt, key_check FROM vault_meta WHERE id = 1").fetchone()
    if row is None:
        return create_master_key(conn)
    salt = row["salt"]
    key_check = row["key_check"]
    for _ in range(3):
        master = getpass.getpass("Contraseña maestra: ")
        key = derive_key(master, salt)
        if hmac.compare_digest(key_check_value(key), key_check):
            return key
        print("Contraseña incorrecta.")
    print("Demasiados intentos fallidos.", file=sys.stderr)
    sys.exit(1)


def generate_password(
    length=16,
    use_upper=True,
    use_lower=True,
    use_digits=True,
    use_symbols=True,
    avoid_ambiguous=True,
):
    if length < 8:
        raise ValueError("La longitud mínima recomendada es 8.")
    symbols = "!@#$%^&*()-_=+[]{};:,.?/"
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    if avoid_ambiguous:
        for char in "O0Il1":
            upper = upper.replace(char, "")
            lower = lower.replace(char, "")
            digits = digits.replace(char, "")
    pools = []
    if use_upper:
        pools.append(upper)
    if use_lower:
        pools.append(lower)
    if use_digits:
        pools.append(digits)
    if use_symbols:
        pools.append(symbols)
    if not pools:
        raise ValueError("Debes seleccionar al menos un conjunto de caracteres.")
    if length < len(pools):
        raise ValueError("La longitud es demasiado corta para los conjuntos elegidos.")
    password_chars = [secrets.choice(pool) for pool in pools]
    all_chars = "".join(pools)
    password_chars += [secrets.choice(all_chars) for _ in range(length - len(pools))]
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def password_strength(password):
    length_score = min(len(password) * 4, 40)
    variety = 0
    variety += bool(re.search(r"[A-Z]", password))
    variety += bool(re.search(r"[a-z]", password))
    variety += bool(re.search(r"\d", password))
    variety += bool(re.search(r"[^A-Za-z0-9]", password))
    variety_score = variety * 15
    unique_score = min(len(set(password)) * 2, 20)
    score = length_score + variety_score + unique_score
    if score >= 80:
        level = "Fuerte"
    elif score >= 60:
        level = "Buena"
    elif score >= 40:
        level = "Media"
    else:
        level = "Débil"
    return min(score, 100), level


def prompt_password(confirm=True):
    while True:
        pwd = getpass.getpass("Contraseña: ")
        if not confirm:
            return pwd
        check = getpass.getpass("Confirma la contraseña: ")
        if pwd == check:
            return pwd
        print("No coinciden. Intenta de nuevo.")


def add_entry(conn, key, args):
    password = args.password
    if args.generate:
        password = generate_password(length=args.length)
    if password is None:
        password = prompt_password()
    notes = args.notes or ""
    encrypted_password = encrypt_text(key, password)
    encrypted_notes = encrypt_text(key, notes) if notes else None
    now = utc_now()
    conn.execute(
        """
        INSERT INTO entries (service, username, password_enc, notes_enc, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (args.service, args.username, encrypted_password, encrypted_notes, now, now),
    )
    conn.commit()
    print("Entrada guardada.")


def list_entries(conn):
    rows = conn.execute(
        "SELECT id, service, username, updated_at FROM entries ORDER BY updated_at DESC"
    ).fetchall()
    if not rows:
        print("No hay contraseñas guardadas.")
        return
    print(f"{'ID':<4} {'Servicio':<24} {'Usuario':<24} {'Actualizado'}")
    print("-" * 70)
    for row in rows:
        service = (row["service"] or "")[:23]
        username = (row["username"] or "")[:23]
        print(f"{row['id']:<4} {service:<24} {username:<24} {row['updated_at']}")


def get_entry(conn, key, args):
    if args.id:
        row = conn.execute("SELECT * FROM entries WHERE id = ?", (args.id,)).fetchone()
    else:
        row = conn.execute(
            "SELECT * FROM entries WHERE service = ?", (args.service,)
        ).fetchone()
    if row is None:
        print("Entrada no encontrada.")
        return
    password = decrypt_text(key, row["password_enc"])
    notes = decrypt_text(key, row["notes_enc"])
    print(f"ID: {row['id']}")
    print(f"Servicio: {row['service']}")
    print(f"Usuario: {row['username'] or ''}")
    print(f"Contraseña: {password}")
    if notes:
        print(f"Notas: {notes}")


def update_entry(conn, key, args):
    row = conn.execute("SELECT * FROM entries WHERE id = ?", (args.id,)).fetchone()
    if row is None:
        print("Entrada no encontrada.")
        return
    username = args.username if args.username is not None else row["username"]
    if args.generate:
        password = generate_password(length=args.length)
    elif args.password:
        password = args.password
    elif args.prompt:
        password = prompt_password()
    else:
        password = decrypt_text(key, row["password_enc"])
    notes = args.notes if args.notes is not None else decrypt_text(key, row["notes_enc"])
    encrypted_password = encrypt_text(key, password)
    encrypted_notes = encrypt_text(key, notes) if notes else None
    conn.execute(
        """
        UPDATE entries
        SET username = ?, password_enc = ?, notes_enc = ?, updated_at = ?
        WHERE id = ?
        """,
        (username, encrypted_password, encrypted_notes, utc_now(), args.id),
    )
    conn.commit()
    print("Entrada actualizada.")


def delete_entry(conn, args):
    conn.execute("DELETE FROM entries WHERE id = ?", (args.id,))
    conn.commit()
    print("Entrada eliminada.")


def suggest_password(args):
    pwd = generate_password(length=args.length)
    score, level = password_strength(pwd)
    print(f"Sugerencia: {pwd}")
    print(f"Fuerza estimada: {level} ({score}/100)")


def create_parser():
    parser = argparse.ArgumentParser(
        description="Generador y gestor seguro de contraseñas."
    )
    parser.add_argument(
        "--db",
        default=DEFAULT_DB_NAME,
        help="Ruta del archivo de la bóveda (por defecto vault.db).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Inicializa la bóveda.")

    suggest = subparsers.add_parser("suggest", help="Sugerir una contraseña fuerte.")
    suggest.add_argument("--length", type=int, default=20)

    generate = subparsers.add_parser("generate", help="Crear una contraseña.")
    generate.add_argument("--length", type=int, default=16)
    generate.add_argument("--no-upper", action="store_true")
    generate.add_argument("--no-lower", action="store_true")
    generate.add_argument("--no-digits", action="store_true")
    generate.add_argument("--no-symbols", action="store_true")
    generate.add_argument("--allow-ambiguous", action="store_true")

    add = subparsers.add_parser("add", help="Guardar una contraseña.")
    add.add_argument("--service", required=True)
    add.add_argument("--username")
    add.add_argument("--password")
    add.add_argument("--notes")
    add.add_argument("--generate", action="store_true")
    add.add_argument("--length", type=int, default=16)

    subparsers.add_parser("list", help="Listar contraseñas guardadas.")

    get = subparsers.add_parser("get", help="Mostrar una contraseña.")
    group = get.add_mutually_exclusive_group(required=True)
    group.add_argument("--id", type=int)
    group.add_argument("--service")

    update = subparsers.add_parser("update", help="Actualizar una contraseña.")
    update.add_argument("--id", type=int, required=True)
    update.add_argument("--username")
    update.add_argument("--password")
    update.add_argument("--notes")
    update.add_argument("--generate", action="store_true")
    update.add_argument("--prompt", action="store_true")
    update.add_argument("--length", type=int, default=16)

    delete = subparsers.add_parser("delete", help="Eliminar una contraseña.")
    delete.add_argument("--id", type=int, required=True)

    return parser


def main():
    require_crypto()
    parser = create_parser()
    args = parser.parse_args()
    db_path = os.path.abspath(args.db)
    conn = connect_db(db_path)
    init_db(conn)

    if args.command == "init":
        _ = unlock_vault(conn)
        return

    if args.command in {"add", "list", "get", "update", "delete"}:
        key = unlock_vault(conn)
    else:
        key = None

    if args.command == "suggest":
        suggest_password(args)
    elif args.command == "generate":
        password = generate_password(
            length=args.length,
            use_upper=not args.no_upper,
            use_lower=not args.no_lower,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            avoid_ambiguous=not args.allow_ambiguous,
        )
        score, level = password_strength(password)
        print(f"Contraseña: {password}")
        print(f"Fuerza estimada: {level} ({score}/100)")
    elif args.command == "add":
        add_entry(conn, key, args)
    elif args.command == "list":
        list_entries(conn)
    elif args.command == "get":
        get_entry(conn, key, args)
    elif args.command == "update":
        update_entry(conn, key, args)
    elif args.command == "delete":
        delete_entry(conn, args)


if __name__ == "__main__":
    main()
