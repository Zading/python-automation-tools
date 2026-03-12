# 📝 Gestor de Tareas Web - Flask

Una aplicación web moderna para gestionar tus tareas diarias, desarrollada con Flask.

## ✨ Características

- 🌐 **Interfaz Web Moderna** - Diseño responsive y atractivo
- ✅ **Gestión Completa de Tareas** - Agregar, completar, eliminar y buscar
- 🎨 **Prioridades Visuales** - Alta (🔴), Media (🟡), Baja (🟢)
- 📊 **Estadísticas en Tiempo Real** - Progreso y distribución de tareas
- 🔍 **Búsqueda Rápida** - Encuentra tareas fácilmente
- 💾 **Persistencia de Datos** - Guardado automático en JSON
- 📱 **Responsive Design** - Funciona en móviles, tablets y desktop

## 🚀 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

O instalar Flask manualmente:

```bash
pip install Flask
```

### 2. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 📁 Estructura del Proyecto

```
todo_list/
├── app.py                 # Aplicación Flask principal
├── todo_list.py           # Clase TodoList (lógica de negocio)
├── requirements.txt       # Dependencias del proyecto
├── tareas.json           # Archivo de datos (se crea automáticamente)
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página principal
│   ├── agregar.html      # Formulario para agregar tareas
│   ├── buscar.html       # Resultados de búsqueda
│   └── estadisticas.html # Página de estadísticas
└── static/               # Archivos estáticos
    ├── css/
    │   └── style.css     # Estilos CSS
    └── js/
        └── main.js       # JavaScript
```

## 🎯 Funcionalidades

### Página Principal (`/`)
- Lista todas las tareas
- Filtros por prioridad y estado (completadas/pendientes)
- Búsqueda rápida
- Estadísticas resumidas
- Acciones: completar y eliminar tareas

### Agregar Tarea (`/agregar`)
- Formulario para crear nuevas tareas
- Selección de prioridad
- Validación de campos

### Buscar Tareas (`/buscar`)
- Búsqueda por término
- Resultados destacados
- Mismas acciones que la lista principal

### Estadísticas (`/estadisticas`)
- Total de tareas
- Tareas completadas vs pendientes
- Progreso general con barra visual
- Distribución por prioridad

## 🔧 Configuración

### Cambiar el puerto

Edita `app.py` y modifica la última línea:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Modo de desarrollo vs producción

**Desarrollo** (con debug activado):
```python
app.run(debug=True)
```

**Producción** (sin debug):
```python
app.run(debug=False)
```

Para producción, considera usar un servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 Uso de la API

La aplicación incluye un endpoint API para obtener todas las tareas en formato JSON:

```
GET /api/tareas
```

Respuesta:
```json
[
  {
    "id": 1,
    "descripcion": "Estudiar Python",
    "completada": false,
    "prioridad": "alta",
    "fecha_creacion": "2024-01-15 10:30:00",
    "fecha_completada": null
  }
]
```

## 🎨 Personalización

### Colores

Edita `static/css/style.css` y modifica las variables CSS:

```css
:root {
    --primary-color: #4f46e5;
    --success-color: #10b981;
    --danger-color: #ef4444;
    /* ... */
}
```

### Fuentes

La aplicación usa Google Fonts (Poppins). Puedes cambiarla en `templates/base.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=TuFuente&display=swap" rel="stylesheet">
```

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask'"

```bash
pip install Flask
```

### El servidor no inicia

Verifica que el puerto 5000 no esté en uso:
- Windows: `netstat -ano | findstr :5000`
- Linux/Mac: `lsof -i :5000`

### Los cambios no se reflejan

Asegúrate de tener `debug=True` en `app.py` para recarga automática.

## 📚 Tecnologías Utilizadas

- **Flask** - Framework web de Python
- **HTML5** - Estructura
- **CSS3** - Estilos modernos con variables CSS
- **JavaScript** - Interactividad
- **JSON** - Almacenamiento de datos

## 🔐 Seguridad

⚠️ **Nota importante**: Esta aplicación está diseñada para uso local o en entornos controlados. Para producción:

1. Cambia `app.secret_key` por una clave segura
2. Desactiva el modo debug
3. Usa HTTPS
4. Implementa autenticación si es necesario
5. Valida y sanitiza todas las entradas del usuario

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Siéntete libre de:
- Reportar bugs
- Sugerir nuevas funcionalidades
- Enviar pull requests

---

¡Disfruta gestionando tus tareas! 🎉




