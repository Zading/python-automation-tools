# Block de Notas

Aplicación de block de notas con interfaz gráfica desarrollada con Tkinter.

## 🚀 Características

- ✅ **Crear notas**: Crea nuevas notas con título y contenido
- ✅ **Editar notas**: Modifica notas existentes
- ✅ **Eliminar notas**: Borra notas que ya no necesites
- ✅ **Buscar notas**: Busca por título o contenido
- ✅ **Categorías**: Organiza tus notas en categorías (Personal, Trabajo, Estudio, Recordatorios, Otros)
- ✅ **Fechas automáticas**: Registra fecha de creación y última modificación
- ✅ **Estadísticas**: Muestra el total de notas y distribución por categoría
- ✅ **Persistencia**: Guarda automáticamente en archivo JSON

## 📋 Requisitos

- Python 3.6 o superior
- Tkinter (incluido en la mayoría de instalaciones de Python)

## 🎯 Uso

### Ejecutar la aplicación

```bash
python notas.py
```

### Funcionalidades

1. **Crear una nueva nota**:
   - Haz clic en el botón "Nueva Nota"
   - Escribe el título y contenido
   - Selecciona una categoría
   - Haz clic en "Guardar"

2. **Editar una nota**:
   - Selecciona una nota de la lista
   - Modifica el título o contenido
   - Haz clic en "Guardar"

3. **Eliminar una nota**:
   - Selecciona la nota que deseas eliminar
   - Haz clic en "Eliminar"
   - Confirma la eliminación

4. **Buscar notas**:
   - Escribe en el campo "Buscar"
   - La lista se filtra automáticamente

## 💾 Almacenamiento

Las notas se guardan automáticamente en el archivo `notas.json` en la misma carpeta del script.

## 🎨 Interfaz

La aplicación tiene una interfaz dividida en:

- **Panel izquierdo**: Lista de notas con búsqueda
- **Panel derecho**: Editor de notas con título, categoría y contenido
- **Panel inferior**: Estadísticas de tus notas

## 🔧 Estructura de datos

Cada nota se guarda con la siguiente estructura:

```json
{
  "titulo": "Título de la nota",
  "contenido": "Contenido de la nota",
  "categoria": "Personal",
  "fecha_creacion": "2024-01-15T10:30:00",
  "fecha_modificacion": "2024-01-15T10:30:00"
}
```

## 📝 Notas

- Las notas se guardan automáticamente al hacer clic en "Guardar"
- La búsqueda es en tiempo real
- Las fechas se muestran en formato legible
- Las estadísticas se actualizan automáticamente






















