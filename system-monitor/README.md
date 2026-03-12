# Monitor del Sistema - Tiempo Real

Monitor de sistema en consola que muestra información en tiempo real sobre el rendimiento de tu computadora. Diseñado para ser ligero, eficiente y fácil de usar.

## 📋 Características

- **Monitoreo en tiempo real** de recursos del sistema
- **Interfaz en consola** optimizada y sin efectos de cascada
- **Colores ANSI** para indicar estados (verde/amarillo/rojo)
- **Bajo consumo de recursos** - sin dependencias pesadas
- **Actualización suave** - sin parpadeos ni efectos visuales molestos
- **Información completa** de CPU, RAM, Disco, Red, Temperatura y Procesos

## 🎯 Información Mostrada

### Recursos del Sistema
- **CPU**: Porcentaje de uso, número de núcleos, frecuencia
- **RAM**: Porcentaje de uso, memoria usada/total/disponible
- **Disco**: Porcentaje de uso, espacio usado/total/libre
- **Temperatura**: Temperatura del CPU con indicador de estado (si está disponible)
- **Red**: Velocidad de envío/recepción en tiempo real y totales acumulados

### Información del Sistema
- Sistema operativo y versión
- Tiempo de actividad (uptime)
- Número de procesos activos
- Número de hilos en ejecución

### Top Procesos
- Los 5 procesos que más CPU consumen
- Información detallada: PID, nombre, CPU%, RAM%, memoria utilizada

## 🚀 Requisitos

- Python 3.6 o superior
- Biblioteca `psutil`

## 📦 Instalación

1. Asegúrate de tener Python instalado:
```bash
python --version
```

2. Instala la dependencia necesaria:
```bash
pip install psutil
```

**Nota para Windows (Temperatura opcional):**
Si deseas monitorear la temperatura en Windows, también necesitas instalar `wmi`:
```bash
pip install wmi
```

## 💻 Uso

Ejecuta el monitor simplemente con:

```bash
python monitor.py
```

El monitor se actualizará automáticamente cada segundo mostrando toda la información del sistema.

Para salir, presiona `CTRL+C`.

## 🎨 Indicadores de Color

El monitor utiliza colores ANSI para indicar el estado de los recursos:

### CPU, RAM y Disco:
- 🟢 **Verde**: Uso normal (0-50%)
- 🟡 **Amarillo**: Uso moderado (50-80%)
- 🔴 **Rojo**: Uso alto/crítico (>80%)

### Temperatura:
- 🟢 **Verde**: Normal (<60°C)
- 🟡 **Amarillo oscuro**: Moderado (60-70°C)
- 🟡 **Amarillo**: Alto (70-80°C)
- 🔴 **Rojo**: Crítico (>80°C)

## 📊 Ejemplo de Salida

```
================================================================================
                    MONITOR DEL SISTEMA - TIEMPO REAL
================================================================================
Fecha/Hora: 2024-01-15 14:30:25
Presiona CTRL+C para salir

CPU:  25.3% | Núcleos: 8 | Frecuencia: 3200 MHz
RAM:  45.2% | Usada:    8.50 GB | Total:   16.00 GB | Disponible:    8.75 GB
Disco: 62.1% | Usado:  500.25 GB | Total:  1000.00 GB | Libre:   380.50 GB
Temperatura CPU:  45.5°C | Estado: Normal
Red - Enviado:   125.50 KB/s (    1.25 GB total)
Red - Recibido:   250.75 KB/s (    2.50 GB total)
Red - Total:      3.75 GB

Sistema - OS: Windows 10 | Tiempo activo: 2h 15m 30s
Procesos activos: 156 | Hilos: 1245

================================================================================
TOP 5 PROCESOS POR CPU
================================================================================
PID      Nombre                     CPU %    RAM %    Memoria        
--------------------------------------------------------------------------------
1234     chrome.exe                   15.2%    8.5%     1.25 GB        
5678     code.exe                     8.3%    5.2%     850.50 MB       
9012     python.exe                   5.1%    2.1%     320.25 MB       
3456     explorer.exe                 3.2%    1.8%     180.75 MB       
7890     firefox.exe                  2.5%    4.3%     650.00 MB       

================================================================================
Actualizando cada 1.0s...
```

## ⚙️ Configuración

Puedes modificar el intervalo de actualización editando la variable `update_interval` en el método `__init__` de la clase `MonitorConsola`:

```python
self.update_interval = 1.0  # segundos (cambiar según necesidad)
```

## 🔧 Compatibilidad

- ✅ **Windows** (7, 8, 10, 11)
- ✅ **Linux** (distribuciones principales)
- ✅ **macOS** (versiones recientes)

### Notas de Compatibilidad:

- **Temperatura en Windows**: Requiere la biblioteca `wmi` (opcional). Si no está instalada, el monitor funcionará normalmente pero no mostrará temperatura.
- **Temperatura en Linux**: Funciona automáticamente si el sistema tiene sensores disponibles (`/sys/class/thermal/`).
- **Temperatura en macOS**: Funciona automáticamente si hay sensores disponibles.

## 🛠️ Estructura del Código

```
Monitor_sistema/
├── monitor.py          # Código principal del monitor
└── README.md           # Este archivo
```

### Clases y Métodos Principales:

- **`MonitorConsola`**: Clase principal que gestiona todo el monitoreo
  - `__init__()`: Inicializa variables y configuración
  - `mostrar_monitor()`: Bucle principal de actualización
  - `obtener_temperatura()`: Obtiene temperatura del sistema
  - `obtener_top_procesos()`: Lista procesos por consumo de CPU
  - `formatear_bytes()`: Convierte bytes a formato legible
  - `obtener_color_ansi()`: Retorna códigos de color según estado

## 📝 Características Técnicas

- **Sin dependencias pesadas**: Solo usa `psutil` (y opcionalmente `wmi` en Windows)
- **Actualización eficiente**: Usa códigos ANSI para actualizar sin limpiar toda la pantalla
- **Manejo de errores**: Gestión robusta de excepciones
- **Formato legible**: Valores formateados de manera clara y comprensible
- **Bajo consumo**: Optimizado para usar mínimos recursos del sistema

## 🐛 Solución de Problemas

### El monitor no muestra temperatura
- **Windows**: Instala `wmi` con `pip install wmi`
- **Linux/macOS**: Verifica que tu sistema tenga sensores de temperatura disponibles

### Los colores no se muestran
- Algunas terminales no soportan códigos ANSI. El monitor funcionará pero sin colores.

### El monitor se actualiza muy lento
- Reduce el `update_interval` en el código (valores menores = más rápido)

### Error de permisos
- En algunos sistemas, puede requerir permisos de administrador para acceder a cierta información.

## 🔮 Mejoras Futuras Posibles

- [ ] Exportar datos a archivo CSV
- [ ] Alertas cuando los recursos superen umbrales
- [ ] Historial de uso de recursos
- [ ] Configuración mediante archivo de configuración
- [ ] Soporte para múltiples discos
- [ ] Información de GPU (si está disponible)

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y personal.

## 👤 Autor

Desarrollado como parte del curso de Python.

## 🙏 Agradecimientos

- **psutil**: Biblioteca increíble para monitoreo de sistema en Python
- Comunidad de Python por las herramientas y recursos disponibles

---

**¡Disfruta monitoreando tu sistema!** 🚀

