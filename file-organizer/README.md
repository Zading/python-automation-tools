# Organizador Automático de Archivos

Este proyecto organiza automáticamente los archivos descargados en tu carpeta de Descargas, clasificándolos por tipo en carpetas correspondientes.

## 📋 Características

- ✅ Organización automática al descargar archivos
- ✅ Clasificación por categorías (Imágenes, Documentos, Audio, Video, etc.)
- ✅ Manejo de archivos duplicados
- ✅ Monitoreo en tiempo real de la carpeta de Descargas
- ✅ Compatible con Windows (Downloads/Descargas)

## 🚀 Instalación

1. **Instalar la dependencia necesaria:**
   ```bash
   pip install -r requirements.txt
   ```
   
   O directamente:
   ```bash
   pip install watchdog
   ```

## 📖 Uso

### Modo Manual (Una sola vez)
Ejecuta el script `organizar.py` para organizar los archivos existentes:
```bash
python organizar.py
```

### Modo Automático (Monitoreo continuo)
Ejecuta el script `organizar_auto.py` para monitorear y organizar automáticamente:
```bash
python organizar_auto.py
```

O simplemente haz doble clic en `iniciar_organizador.bat` (Windows)

El script se mantendrá ejecutándose y organizará automáticamente cualquier archivo que descargues. Presiona `Ctrl+C` para detenerlo.

## 📁 Categorías de Archivos

Los archivos se organizan en las siguientes carpetas:

- **Imagenes**: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .svg, .webp
- **Documentos**: .pdf, .doc, .docx, .odt, .txt, .rtf, .xls, .xlsx, .ppt, .pptx, .csv
- **Audio**: .mp3, .wav, .aac, .ogg, .flac, .m4a, .wma
- **Video**: .mp4, .avi, .mov, .wmv, .flv, .mkv, .webm, .mpeg
- **Comprimidos**: .zip, .rar, .tar, .gz, .bz2, .7z, .xz
- **Instaladores**: .exe, .msi, .dmg, .deb, .rpm, .pkg, .apk, .bat, .sh
- **Programacion**: .py, .ipynb, .java, .c, .cpp, .js, .html, .css, .php, .rb, .go, .ts
- **Discos**: .iso, .img, .bin, .cue, .vmdk, .vdi, .ova
- **Redes**: .pkt, .pka, .pcap, .pcapng
- **Otros**: Archivos sin extensión o con extensiones desconocidas

## 🔧 Ejecutar al Iniciar Windows

Para que el organizador se ejecute automáticamente al iniciar Windows:

1. Presiona `Win + R` y escribe `shell:startup`
2. Crea un acceso directo al archivo `iniciar_organizador.bat`
3. O crea un acceso directo a `pythonw.exe` con el argumento: `"ruta\completa\organizar_auto.py"`

**Nota:** Usa `pythonw.exe` en lugar de `python.exe` para que no aparezca una ventana de consola.

## ⚠️ Notas Importantes

- El script espera 1 segundo después de detectar un archivo nuevo para asegurar que la descarga se complete
- Si un archivo está siendo usado por otro programa, el script lo reintentará automáticamente
- Los archivos que ya están en carpetas de categoría no se moverán (evita bucles infinitos)
- Si un archivo con el mismo nombre ya existe en el destino, se agregará un número al nombre

## 🛠️ Solución de Problemas

**Error: "No se encontró la carpeta de Descargas"**
- Verifica que tu carpeta de Descargas exista
- El script busca en: `Downloads` (inglés) y `Descargas` (español)

**Error: "ModuleNotFoundError: No module named 'watchdog'"**
- Ejecuta: `pip install watchdog`

**El archivo no se organiza inmediatamente**
- El script espera 1 segundo para asegurar que la descarga se complete
- Para archivos muy grandes, puede tomar más tiempo






















