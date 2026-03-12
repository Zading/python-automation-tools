# 🌐 Network Manager PRO

Herramienta completa de gestión de red que integra escaneo de red, detección de puertos y gestión de firewall en una sola aplicación. Diseñada para administradores de red, profesionales de seguridad y usuarios avanzados.

## ✨ Características Principales

### 🔍 Escaneo de Red
- **Detección automática de redes**: Identifica automáticamente las redes locales del sistema
- **Escaneo paralelo**: Utiliza múltiples threads para escanear hosts rápidamente
- **Resolución de hostnames**: Obtiene nombres de dispositivos mediante DNS inverso
- **Múltiples formatos**: Soporta CIDR, rangos personalizados y detección automática
- **Progreso en tiempo real**: Muestra el progreso del escaneo con estadísticas

### 🔍 Escaneo de Puertos
- **Múltiples modos de escaneo**: Puertos comunes, top 100, rango personalizado
- **Obtención de banners**: Detecta banners de servicios (FTP, SSH, HTTP, SMTP, MySQL, etc.)
- **Escaneo paralelo**: Usa threading para escanear múltiples puertos simultáneos
- **Información detallada**: Muestra tiempo de respuesta, servicio identificado y banners
- **Resolución de dominios**: Acepta tanto direcciones IP como nombres de dominio

### 🔍 Escaneo Completo de Red
- **Escaneo combinado**: Escanea la red y luego los puertos en todos los hosts encontrados
- **Auditoría completa**: Ideal para análisis de seguridad exhaustivos
- **Resultados consolidados**: Genera un reporte completo con todos los hallazgos

### 🔥 Gestión de Firewall (Windows)
- **Abrir puertos**: Crea reglas en el firewall de Windows para abrir puertos específicos
- **Cerrar puertos**: Elimina reglas del firewall para cerrar puertos
- **Listar reglas**: Muestra todas las reglas configuradas en el firewall
- **Ver puertos locales**: Muestra los puertos abiertos en el sistema local
- **Soporte TCP/UDP**: Gestiona tanto protocolos TCP como UDP

### 📊 Funciones Adicionales
- **Exportación de resultados**: Guarda resultados en formato JSON o CSV
- **Interfaz interactiva**: Menú intuitivo y fácil de usar
- **Verificación de permisos**: Detecta si se ejecuta con permisos de administrador
- **Multiplataforma**: Funciona en Windows, Linux y macOS (algunas funciones son específicas de Windows)

## 📋 Requisitos

- **Python 3.6 o superior**
- **Sistema Operativo**: Windows (recomendado para gestión de firewall), Linux, macOS
- **Permisos**: 
  - Permisos de red para escaneo
  - Permisos de administrador para gestión de firewall (Windows)

### Dependencias

Este script utiliza **únicamente librerías estándar de Python**, no requiere instalación de paquetes externos:
- `socket`
- `subprocess`
- `threading`
- `ipaddress`
- `json`
- `csv`
- `platform`
- `os`
- `sys`

## 🚀 Instalación

No requiere instalación. Solo descarga el archivo y ejecútalo:

```bash
python network_manager.py
```

O en sistemas Unix/Linux:

```bash
python3 network_manager.py
```

### Ejecución como Administrador (Windows)

Para usar las funciones de gestión de firewall, ejecuta el script como administrador:

1. Abre PowerShell o CMD como administrador
2. Navega al directorio del script
3. Ejecuta: `python network_manager.py`

## 📖 Guía de Uso

### Menú Principal

Al ejecutar el script, verás el siguiente menú:

```
======================================================================
  🌐 NETWORK MANAGER PRO
======================================================================

Opciones:
  1. Escanear red (descubrir hosts activos)
  2. Escanear puertos de un host
  3. Escanear red completa (red + puertos en todos los hosts)
  4. Gestionar firewall (abrir/cerrar puertos)
  5. Ver puertos locales abiertos
  6. Salir
```

### 1. Escanear Red

Esta función descubre todos los hosts activos en una red.

**Características:**
- Detección automática de redes locales
- Escaneo paralelo con múltiples threads
- Resolución de hostnames
- Exportación de resultados

**Ejemplo de uso:**
```
Selecciona opción: 1

Ingresa la red a escanear (Enter para auto-detectar): 192.168.1.0/24
Número de threads (Enter para 50): 50
Timeout por host en segundos (Enter para 1): 1

🔍 Escaneando 254 hosts en 192.168.1.0/24...
✓ Hosts encontrados: 5/254 escaneados

✅ Se encontraron 5 hosts activos:

  • 192.168.1.1      - router.local
  • 192.168.1.10     - servidor.local
  • 192.168.1.50     - laptop.local
  • 192.168.1.100    - Desconocido
  • 192.168.1.150    - smartphone.local

¿Exportar resultados? (json/csv/n): json
✅ Datos exportados a escaneo_red_20251217_143022.json
```

### 2. Escanear Puertos

Esta función escanea los puertos abiertos en un host específico.

**Opciones de escaneo:**
1. **Puertos comunes** (22 puertos más usados)
   - SSH, HTTP, HTTPS, FTP, MySQL, RDP, etc.
   - Ideal para escaneos rápidos

2. **Top 100 puertos**
   - Los 100 puertos más comunes
   - Balance entre velocidad y cobertura

3. **Rango personalizado**
   - Permite especificar puerto inicial y final
   - Útil para escanear rangos específicos

**Ejemplo de uso:**
```
Selecciona opción: 2

Opciones de escaneo:
  1. Puertos comunes (22 puertos)
  2. Top 100 puertos
  3. Rango personalizado

Selecciona opción (1-3): 1

Ingresa IP o dominio a escanear: scanme.nmap.org
✓ scanme.nmap.org -> 45.33.32.156

¿Obtener banners? (s/n): s
Timeout (Enter para 1.0s): 1.0
Threads (Enter para 100): 100

🔍 Escaneando 22 puertos en scanme.nmap.org...

✅ Se encontraron 3 puertos abiertos:

  ✓ Puerto    22 - SSH                 (245.3ms)
      Banner: SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13

  ✓ Puerto    80 - HTTP                (156.7ms)
      Banner: HTTP/1.1 200 OK

  ✓ Puerto  9929 - Desconocido         (189.2ms)

¿Exportar resultados? (json/csv/n): csv
✅ Datos exportados a escaneo_puertos_20251217_143045.csv
```

### 3. Escanear Red Completa

Esta función realiza un escaneo completo: primero descubre todos los hosts activos en la red y luego escanea los puertos en cada uno de ellos. Ideal para auditorías de seguridad completas.

**Características:**
- Escaneo de red automático
- Escaneo de puertos en todos los hosts encontrados
- Reporte consolidado con todos los hallazgos
- Exportación de resultados detallados

**Ejemplo de uso:**
```
Selecciona opción: 3

======================================================================
  🔍 ESCANEO COMPLETO DE RED
======================================================================

Este modo escaneará la red y luego los puertos en cada host encontrado.

Ingresa la red a escanear (Enter para auto-detectar): 192.168.1.0/24
Threads para escaneo de red (Enter para 50): 50
Timeout para ping (Enter para 1.0s): 1.0

----------------------------------------------------------------------
PASO 1: Escaneando red...
----------------------------------------------------------------------
🔍 Escaneando 254 hosts en 192.168.1.0/24...
✅ Se encontraron 5 hosts activos.

----------------------------------------------------------------------
PASO 2: Configuración de escaneo de puertos
----------------------------------------------------------------------
Opciones de escaneo de puertos:
  1. Puertos comunes (22 puertos)
  2. Top 100 puertos
  3. Rango personalizado

Selecciona opción (1-3): 1

¿Obtener banners? (s/n): s
Timeout por puerto (Enter para 1.0s): 1.0
Threads por host (Enter para 50): 50

----------------------------------------------------------------------
PASO 3: Escaneando puertos en cada host...
----------------------------------------------------------------------

[1/5] Escaneando 192.168.1.1 (router.local)...
  ✓ 3 puertos abiertos encontrados

[2/5] Escaneando 192.168.1.10 (servidor.local)...
  ✓ 5 puertos abiertos encontrados

...

======================================================================
  📊 RESUMEN DEL ESCANEO COMPLETO
======================================================================

Hosts escaneados: 5
Total de puertos abiertos encontrados: 18

----------------------------------------------------------------------
DETALLES POR HOST:
----------------------------------------------------------------------

  📍 192.168.1.1 (router.local)
    ✓ Puerto    80 - HTTP
    ✓ Puerto   443 - HTTPS
    ✓ Puerto  8080 - HTTP-ALT

  📍 192.168.1.10 (servidor.local)
    ✓ Puerto    22 - SSH
    ✓ Puerto    80 - HTTP
    ✓ Puerto  3306 - MySQL
    ...

¿Exportar resultados? (json/csv/n): json
✅ Datos exportados a escaneo_completo_20251217_143100.json
```

### 4. Gestionar Firewall

Esta función permite gestionar el firewall de Windows (requiere permisos de administrador).

**Opciones:**
1. **Abrir puerto**: Crea una regla para permitir tráfico en un puerto específico
2. **Cerrar puerto**: Elimina la regla que permite tráfico en un puerto
3. **Listar reglas**: Muestra todas las reglas configuradas
4. **Ver puertos locales**: Muestra los puertos abiertos en el sistema

**Ejemplo de uso:**
```
Selecciona opción: 3

======================================================================
  🔥 GESTIÓN DE FIREWALL
======================================================================

Opciones:
  1. Abrir puerto
  2. Cerrar puerto
  3. Listar reglas del firewall
  4. Ver puertos locales abiertos

Selecciona opción (1-4): 1

Puerto a abrir: 8080
Protocolo (TCP/UDP, Enter para TCP): TCP
Nombre de la regla (Enter para auto): Servidor_Web_Local

✅ Puerto 8080/TCP abierto correctamente.
```

**⚠️ Importante:**
- Solo funciona en Windows
- Requiere permisos de administrador
- Los cambios afectan el firewall del sistema

### 5. Ver Puertos Locales

Muestra los puertos abiertos y conexiones activas en el sistema local.

**Ejemplo de salida:**
```
📊 Puertos abiertos en el sistema local:

Active Connections

  Proto  Local Address          Foreign Address        State
  TCP    0.0.0.0:80             0.0.0.0:0             LISTENING
  TCP    0.0.0.0:443            0.0.0.0:0             LISTENING
  TCP    0.0.0.0:3389           0.0.0.0:0             LISTENING
  TCP    127.0.0.1:3306         0.0.0.0:0             LISTENING
  ...
```

## 📊 Formatos de Exportación

### JSON
Los resultados se exportan en formato JSON estructurado:

```json
[
  {
    "ip": "192.168.1.1",
    "hostname": "router.local",
    "activo": true
  },
  {
    "ip": "192.168.1.10",
    "hostname": "servidor.local",
    "activo": true
  }
]
```

### CSV
Los resultados se exportan en formato CSV compatible con Excel y otras herramientas:

```csv
ip,hostname,activo
192.168.1.1,router.local,True
192.168.1.10,servidor.local,True
```

## 🔧 Servicios Reconocidos

El escáner reconoce automáticamente los siguientes servicios comunes:

| Puerto | Servicio | Puerto | Servicio |
|--------|----------|--------|----------|
| 20 | FTP-DATA | 443 | HTTPS |
| 21 | FTP | 445 | SMB |
| 22 | SSH | 993 | IMAPS |
| 23 | Telnet | 995 | POP3S |
| 25 | SMTP | 1433 | MSSQL |
| 53 | DNS | 3306 | MySQL |
| 80 | HTTP | 3389 | RDP |
| 110 | POP3 | 5432 | PostgreSQL |
| 135 | MSRPC | 5900 | VNC |
| 139 | NetBIOS | 6379 | Redis |
| 143 | IMAP | 8080 | HTTP-ALT |
| | | 8443 | HTTPS-ALT |
| | | 27017 | MongoDB |

## 🎯 Casos de Uso

### Auditoría de Seguridad
```bash
# 1. Escanear la red para encontrar todos los dispositivos
# 2. Escanear puertos en cada dispositivo encontrado
# 3. Identificar servicios expuestos
# 4. Exportar resultados para análisis
```

### Configuración de Servidor
```bash
# 1. Verificar qué puertos están abiertos localmente
# 2. Abrir puertos necesarios en el firewall
# 3. Verificar que los puertos estén accesibles desde otros hosts
```

### Monitoreo de Red
```bash
# 1. Escanear la red periódicamente
# 2. Comparar resultados para detectar nuevos dispositivos
# 3. Identificar cambios en la topología de red
```

### Desarrollo de Aplicaciones
```bash
# 1. Verificar puertos disponibles para desarrollo
# 2. Abrir puertos temporales para testing
# 3. Cerrar puertos después de las pruebas
```

## ⚙️ Configuración Avanzada

### Optimización de Velocidad

**Escaneo de red:**
- Aumenta el número de threads (hasta 100-200)
- Reduce el timeout (0.5-1.0 segundos)
- Escanea solo rangos específicos

**Escaneo de puertos:**
- Usa más threads (100-200)
- Reduce el timeout (0.5-1.0 segundos)
- Desactiva la obtención de banners

### Optimización de Precisión

**Escaneo de red:**
- Aumenta el timeout para redes lentas (2-3 segundos)
- Reduce el número de threads para evitar saturación

**Escaneo de puertos:**
- Aumenta el timeout (2-3 segundos)
- Activa la obtención de banners
- Usa rangos específicos en lugar de todos los puertos

## 🔒 Consideraciones de Seguridad

⚠️ **Importante**: Este script está diseñado para uso legítimo únicamente:

- ✅ Solo escanea sistemas que te pertenecen o tienes autorización para escanear
- ✅ El escaneo de puertos puede ser detectado por sistemas de seguridad
- ✅ Algunos servicios pueden registrar intentos de conexión
- ✅ Respeta las políticas de seguridad de la red
- ✅ Los cambios en el firewall afectan la seguridad del sistema

### Buenas Prácticas

1. **Permisos**: Siempre obtén autorización antes de escanear redes
2. **Firewall**: Revisa cuidadosamente antes de abrir puertos
3. **Logs**: Los escaneos pueden quedar registrados en logs del sistema
4. **Red**: Considera el impacto en el ancho de banda de la red

## 🐛 Solución de Problemas

### El escaneo es muy lento
- Reduce el timeout
- Aumenta el número de threads
- Escanea rangos más pequeños
- Desactiva la obtención de banners

### No se detectan hosts en la red
- Verifica que la red sea correcta
- Aumenta el timeout si la red es lenta
- Verifica que los hosts respondan a ping
- Algunos hosts pueden tener ping deshabilitado

### No se pueden abrir/cerrar puertos
- Verifica que ejecutes el script como administrador
- Solo funciona en Windows
- Verifica que el firewall de Windows esté activo
- Revisa los mensajes de error para más detalles

### No se resuelven los dominios
- Verifica la conexión a Internet
- Comprueba que el DNS esté funcionando
- Intenta usar la IP directamente

### Errores de permisos
- En Windows, ejecuta como administrador
- En Linux/macOS, algunos comandos pueden requerir sudo
- Verifica los permisos del usuario

## 📚 Estructura del Código

```
network_manager.py
├── CONFIGURACIÓN
│   ├── SERVICIOS_COMUNES: Diccionario de puertos y servicios
│   ├── PUERTOS_COMUNES: Lista de 22 puertos más usados
│   └── PUERTOS_TOP_100: Lista de top 100 puertos
│
├── ESCANEO DE RED
│   ├── obtener_redes_locales(): Detecta redes locales
│   ├── ping_host(): Hace ping a un host
│   ├── obtener_hostname(): Resuelve hostname
│   └── escanear_red(): Escanea una red completa
│
├── ESCANEO DE PUERTOS
│   ├── obtener_banner(): Obtiene banners de servicios
│   ├── escanear_puerto(): Escanea un puerto individual
│   └── escanear_puertos_host(): Escanea múltiples puertos
│
├── GESTIÓN DE FIREWALL
│   ├── es_administrador(): Verifica permisos
│   ├── abrir_puerto_firewall(): Abre un puerto
│   ├── cerrar_puerto_firewall(): Cierra un puerto
│   ├── listar_reglas_firewall(): Lista reglas
│   └── ver_puertos_locales(): Muestra puertos locales
│
├── EXPORTACIÓN
│   ├── exportar_json(): Exporta a JSON
│   └── exportar_csv(): Exporta a CSV
│
└── MENÚ
    ├── menu_principal(): Menú principal
    ├── menu_escanear_red(): Menú de escaneo de red
    ├── menu_escanear_puertos(): Menú de escaneo de puertos
    └── menu_gestionar_firewall(): Menú de firewall
```

## 🚧 Posibles Mejoras Futuras

- [ ] Soporte para gestión de firewall en Linux (iptables/ufw)
- [ ] Soporte para gestión de firewall en macOS (pfctl)
- [ ] Escaneo UDP (más complejo)
- [ ] Detección de versiones de servicios
- [ ] Escaneo de múltiples hosts simultáneos
- [ ] Comparación de resultados entre escaneos
- [ ] Modo verbose con más detalles
- [ ] Filtros por tipo de servicio
- [ ] Integración con bases de datos de vulnerabilidades
- [ ] Interfaz gráfica (GUI)
- [ ] Modo de línea de comandos (CLI) con argumentos
- [ ] Notificaciones cuando se detecten cambios

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y legítimo.

## 👤 Autor

Desarrollado como parte del curso de Python.

---

**Nota**: Este script es una herramienta educativa y profesional. Úsalo de manera responsable y ética. Siempre obtén autorización antes de escanear redes o sistemas que no te pertenecen.

## 📞 Soporte

Si encuentras problemas o tienes sugerencias:
1. Revisa la sección de "Solución de Problemas"
2. Verifica que cumplas con los requisitos
3. Asegúrate de tener los permisos necesarios

---

**Versión**: 1.0  
**Última actualización**: Diciembre 2025

