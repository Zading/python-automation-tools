# Script que monitorea y organiza automáticamente los archivos descargados
import os
import sys
import shutil
import time
from pathlib import Path

# Importaciones de watchdog (instalar con: pip install watchdog)
try:
    from watchdog.observers import Observer  # type: ignore
    from watchdog.events import FileSystemEventHandler  # type: ignore
except ImportError:
    print("[ERROR] El modulo 'watchdog' no esta instalado.")
    print("Instala con: pip install watchdog")
    sys.exit(1)

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Obtener la carpeta de Descargas (compatible con Windows y diferentes configuraciones)
def obtener_carpeta_descargas():
    """Obtiene la ruta de la carpeta de Descargas"""
    carpeta_objetivo = Path.home() / "Downloads"  # Inglés
    if not carpeta_objetivo.exists():
        carpeta_objetivo = Path.home() / "Descargas"  # Español
    if not carpeta_objetivo.exists():
        # Intentar obtener desde variables de entorno
        carpeta_objetivo = Path(os.path.expanduser("~/Downloads"))
        if not carpeta_objetivo.exists():
            carpeta_objetivo = Path(os.path.expanduser("~/Descargas"))
    
    if not carpeta_objetivo.exists():
        raise FileNotFoundError("No se encontró la carpeta de Descargas")
    
    return carpeta_objetivo

# Diccionario de extensiones por categoría
EXTENSIONES_CATEGORIA = {
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

def obtener_categoria(archivo):
    """Determina la categoría de un archivo según su extensión"""
    extension = archivo.suffix.lower()
    
    # Si el archivo NO tiene extensión, lo mandamos a "Otros"
    if extension == "":
        return "Otros"
    
    # Buscar la categoría según la extensión
    for categoria, extensiones in EXTENSIONES_CATEGORIA.items():
        if extension in extensiones:
            return categoria
    
    # Si no tiene categoría encontrada (extensión desconocida), va a "Otros"
    return "Otros"

def organizar_archivo(archivo_path, carpeta_objetivo):
    """Organiza un archivo moviéndolo a su carpeta correspondiente"""
    archivo = Path(archivo_path)
    
    # Ignorar si no es un archivo o si ya está en una carpeta de categoría
    if not archivo.is_file():
        return False
    
    # Ignorar archivos que ya están en carpetas de categoría
    if archivo.parent.name in EXTENSIONES_CATEGORIA.keys() or archivo.parent.name == "Otros":
        return False
    
    categoria = obtener_categoria(archivo)
    
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
        
        # Esperar un momento para asegurar que el archivo esté completamente descargado
        # (útil para descargas grandes que aún están en progreso)
        time.sleep(0.5)
        
        # Verificar que el archivo existe y no está siendo usado
        if not archivo.exists():
            return False
        
        # Intentar mover el archivo
        shutil.move(str(archivo), str(archivo_destino))
        try:
            ruta_destino = str(archivo_destino)
            print(f"[OK] Organizado: {archivo.name}")
            print(f"     Movido a: {ruta_destino}")
        except UnicodeEncodeError:
            nombre_archivo = archivo.name.encode('ascii', 'ignore').decode()
            ruta_destino = str(archivo_destino).encode('ascii', 'ignore').decode()
            print(f"[OK] Organizado: {nombre_archivo}")
            print(f"     Movido a: {ruta_destino}")
        return True
    except PermissionError:
        # El archivo aún está siendo descargado o usado
        return False
    except FileNotFoundError:
        # El archivo ya no existe (puede haber sido movido o eliminado)
        return False
    except Exception as e:
        try:
            print(f"[ERROR] Error al organizar {archivo.name}: {e}")
        except UnicodeEncodeError:
            print(f"[ERROR] Error al organizar archivo: {e}")
        return False

class OrganizadorHandler(FileSystemEventHandler):
    """Manejador de eventos para organizar archivos automáticamente"""
    
    def __init__(self, carpeta_objetivo):
        self.carpeta_objetivo = carpeta_objetivo
        self.archivos_procesando = set()  # Para evitar procesar el mismo archivo múltiples veces
    
    def on_created(self, event):
        """Se ejecuta cuando se crea un nuevo archivo"""
        try:
            if event.is_directory:
                return
            
            archivo_path = Path(event.src_path)
            
            # Verificar que el archivo existe
            if not archivo_path.exists():
                return
            
            # Ignorar archivos temporales
            if archivo_path.name.startswith('.') or archivo_path.name.startswith('~'):
                return
            
            # Ignorar archivos que ya están en carpetas de categoría
            if archivo_path.parent.name in EXTENSIONES_CATEGORIA.keys() or archivo_path.parent.name == "Otros":
                return
            
            # Evitar procesar el mismo archivo múltiples veces
            if str(archivo_path) in self.archivos_procesando:
                return
            
            self.archivos_procesando.add(str(archivo_path))
            
            # Esperar un poco para que la descarga se complete
            time.sleep(2)
            
            # Verificar nuevamente que el archivo existe
            if not archivo_path.exists():
                self.archivos_procesando.discard(str(archivo_path))
                return
            
            # Organizar el archivo
            if organizar_archivo(archivo_path, self.carpeta_objetivo):
                # Remover de la lista después de un tiempo
                time.sleep(1)
                self.archivos_procesando.discard(str(archivo_path))
            else:
                # Si falla, remover después de más tiempo para reintentar
                time.sleep(3)
                self.archivos_procesando.discard(str(archivo_path))
        except Exception as e:
            # Manejar cualquier error en el evento
            try:
                print(f"[ERROR] Error en evento: {e}")
            except:
                print("[ERROR] Error en evento (no se pudo mostrar detalles)")

def iniciar_monitoreo():
    """Inicia el monitoreo automático de la carpeta de Descargas"""
    try:
        carpeta_objetivo = obtener_carpeta_descargas()
        try:
            print(f"[INFO] Monitoreando carpeta: {carpeta_objetivo}")
            print("[INFO] El organizador automatico esta activo. Presiona Ctrl+C para detener.")
        except UnicodeEncodeError:
            print(f"[INFO] Monitoreando carpeta: {str(carpeta_objetivo)}")
            print("[INFO] El organizador automatico esta activo. Presiona Ctrl+C para detener.")
        print("-" * 60)
        
        # Crear el manejador de eventos
        event_handler = OrganizadorHandler(carpeta_objetivo)
        
        # Crear el observador
        observer = Observer()
        observer.schedule(event_handler, str(carpeta_objetivo), recursive=False)
        
        # Iniciar el observador
        observer.start()
        
        # Organizar archivos existentes al inicio
        print("[INFO] Organizando archivos existentes...")
        archivos_existentes = [f for f in carpeta_objetivo.iterdir() if f.is_file()]
        for archivo in archivos_existentes:
            organizar_archivo(archivo, carpeta_objetivo)
        print("[OK] Archivos existentes organizados.\n")
        
        # Mantener el script ejecutándose
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n[INFO] Deteniendo el organizador automatico...")
            observer.stop()
        
        observer.join()
        print("[OK] Organizador detenido correctamente.")
        
    except FileNotFoundError as e:
        print(f"[ERROR] Error: {e}")
        input("Presiona Enter para salir...")
        exit(1)
    except KeyboardInterrupt:
        print("\n[INFO] Deteniendo el organizador automatico...")
        exit(0)
    except Exception as e:
        print(f"[ERROR] Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")
        exit(1)

if __name__ == "__main__":
    iniciar_monitoreo()

