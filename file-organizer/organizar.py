# Script que organiza los archivos existentes en la carpeta de "Descargas"
import os
import shutil
from pathlib import Path

# Obtener la carpeta de Descargas (compatible con Windows y diferentes configuraciones)
carpeta_objetivo = Path.home() / "Downloads"  # Inglés
if not carpeta_objetivo.exists():
    carpeta_objetivo = Path.home() / "Descargas"  # Español
if not carpeta_objetivo.exists():
    # Intentar obtener desde variables de entorno
    carpeta_objetivo = Path(os.path.expanduser("~/Downloads"))
    if not carpeta_objetivo.exists():
        carpeta_objetivo = Path(os.path.expanduser("~/Descargas"))

if not carpeta_objetivo.exists():
    print(f"Error: No se encontró la carpeta de Descargas.")
    print(f"Buscada en: {Path.home() / 'Downloads'} y {Path.home() / 'Descargas'}")
    exit(1)

print(f"Organizando archivos en: {carpeta_objetivo}")

# Se crea un diccionario con las extensiones a evaluar y sus diferentes categorias
extensiones_categoria = {
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
    "Documentos": [".pdf", ".doc", ".docx", ".odt", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a", ".wma"],
    "Video": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv", ".webm", ".mpeg"],
    "Comprimidos": [".zip", ".rar", ".tar", ".gz", ".bz2", ".7z", ".xz"],
    "Instaladores": [".exe", ".msi", ".dmg", ".deb", ".rpm", ".pkg", ".apk", ".bat", ".sh"],
    "Programacion": [".py", ".ipynb", ".java", ".c", ".cpp", ".js", ".html", ".css", ".php", ".rb", ".go", ".ts"],
    "Discos": [".iso", ".img", ".bin", ".cue", ".vmdk", ".vdi", ".ova"],
    "Redes": [".pkt", ".pka", ".pcap", ".pcapng"],
    "Otros": [".ics", ".torrent", ".lnk"]
}

archivos_procesados = 0
archivos_errores = 0

for archivo in carpeta_objetivo.iterdir():
    if archivo.is_file():
        extension = archivo.suffix.lower()
        categoria = None

        # Si el archivo NO tiene extensión, lo mandamos a "Otros"
        if extension == "":
            categoria = "Otros"
        else:
            # Buscar la categoría según la extensión
            for cat, extensiones in extensiones_categoria.items():
                if extension in extensiones:
                    categoria = cat
                    break

        # Si no tiene categoría encontrada (extensión desconocida), va a "Otros"
        if categoria is None:
            categoria = "Otros"

        try:
            # Crear la carpeta si no existe
            carpeta_destino = carpeta_objetivo / categoria
            carpeta_destino.mkdir(exist_ok=True)

            # Verificar si el archivo ya existe en el destino
            archivo_destino = carpeta_destino / archivo.name
            if archivo_destino.exists():
                # Si existe, agregar un número al nombre
                contador = 1
                nombre_base = archivo.stem
                while archivo_destino.exists():
                    nuevo_nombre = f"{nombre_base}_{contador}{archivo.suffix}"
                    archivo_destino = carpeta_destino / nuevo_nombre
                    contador += 1

            # Mover el archivo
            shutil.move(str(archivo), str(archivo_destino))
            archivos_procesados += 1
            print(f"✓ Movido: {archivo.name} -> {categoria}/")
        except Exception as e:
            archivos_errores += 1
            print(f"✗ Error al mover {archivo.name}: {e}")

# Se arroja mensaje de finalización
print(f"\n{'='*50}")
print(f"Organización completada.")
print(f"Archivos procesados: {archivos_procesados}")
if archivos_errores > 0:
    print(f"Archivos con errores: {archivos_errores}")
print(f"{'='*50}")
 
