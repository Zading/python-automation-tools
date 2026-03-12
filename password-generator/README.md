# Generador y Gestor Seguro de Contraseñas

Herramienta en consola para **sugerir**, **crear** y **administrar** contraseñas de forma segura usando cifrado AES-GCM y una contraseña maestra.

## ✅ Características

- **Sugerencias de contraseñas fuertes** con evaluación de fuerza
- **Generación personalizable** (longitud, símbolos, dígitos, etc.)
- **Bóveda cifrada** con contraseña maestra
- **Gestión completa**: guardar, listar, ver, actualizar y eliminar
- **Almacenamiento local** en SQLite (archivo `vault.db`)

## 📦 Requisitos

- Python 3.8+
- Biblioteca `cryptography`

Instalación:
```bash
pip install cryptography
```

## 🚀 Uso rápido

Desde la carpeta del proyecto:
```bash
python password_manager.py init
python password_manager.py suggest
python password_manager.py generate --length 18
```

## 🔐 Administrar contraseñas (bóveda)

```bash
python password_manager.py add --service Gmail --username user@gmail.com --generate
python password_manager.py list
python password_manager.py get --id 1
python password_manager.py update --id 1 --prompt
python password_manager.py delete --id 1
```

## ⚙️ Opciones útiles

- Generación sin símbolos:
```bash
python password_manager.py generate --no-symbols
```

- Cambiar ubicación de la bóveda:
```bash
python password_manager.py --db "C:\ruta\mi_boveda.db" list
```

## 🧩 Estructura

```
Generador_contrasenas/
├── password_manager.py
└── README.md
```

## 🛡️ Notas de seguridad

- La contraseña maestra **no se guarda** en texto plano.
- Cada entrada se cifra con **AES-GCM** usando una clave derivada con **scrypt**.
- No compartas tu `vault.db`.

---

Desarrollado como parte del curso de Python.
