# 📝 Gestor de Tareas (To-Do List)

Una aplicación de consola en Python para gestionar tus tareas diarias de manera eficiente.

## ✨ Características

- ✅ **Agregar tareas** con descripción y prioridad (alta, media, baja)
- 📋 **Listar tareas** (todas o solo pendientes)
- ✅ **Completar tareas** y marcar como finalizadas
- 🗑️ **Eliminar tareas** que ya no necesites
- 🔍 **Buscar tareas** por término de búsqueda
- 📊 **Ver estadísticas** de tu progreso
- 💾 **Persistencia de datos** - Las tareas se guardan automáticamente en un archivo JSON

## 🚀 Uso

### Ejecutar la aplicación

```bash
python todo_list.py
```

### Opciones del menú

1. **Agregar tarea**: Crea una nueva tarea con descripción y prioridad
2. **Listar todas las tareas**: Muestra todas las tareas (completadas y pendientes)
3. **Listar tareas pendientes**: Muestra solo las tareas que aún no has completado
4. **Completar tarea**: Marca una tarea como completada
5. **Eliminar tarea**: Elimina una tarea de la lista
6. **Buscar tareas**: Busca tareas que contengan un término específico
7. **Ver estadísticas**: Muestra estadísticas de tu progreso
8. **Salir**: Cierra la aplicación

## 📁 Estructura de datos

Las tareas se guardan en el archivo `tareas.json` con la siguiente estructura:

```json
[
  {
    "id": 1,
    "descripcion": "Completar proyecto Python",
    "completada": false,
    "prioridad": "alta",
    "fecha_creacion": "2024-01-15 10:30:00",
    "fecha_completada": null
  }
]
```

## 🎯 Prioridades

- 🔴 **Alta**: Tareas importantes y urgentes
- 🟡 **Media**: Tareas normales (por defecto)
- 🟢 **Baja**: Tareas que pueden esperar

## 💡 Ejemplo de uso

```
📝 GESTOR DE TAREAS - MENÚ PRINCIPAL
============================================================
1. Agregar tarea
2. Listar todas las tareas
3. Listar tareas pendientes
4. Completar tarea
5. Eliminar tarea
6. Buscar tareas
7. Ver estadísticas
8. Salir
============================================================

Selecciona una opción (1-8): 1
📝 Ingresa la descripción de la tarea: Estudiar Python
✅ Tarea agregada: Estudiar Python
```

## 🔧 Requisitos

- Python 3.6 o superior
- No se requieren librerías externas (usa solo la biblioteca estándar)

## 📝 Notas

- Las tareas se guardan automáticamente después de cada operación
- El archivo `tareas.json` se crea automáticamente en el mismo directorio que el script
- Puedes editar el archivo JSON manualmente si lo deseas, pero ten cuidado con la estructura




