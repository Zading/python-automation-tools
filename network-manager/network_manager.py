#!/usr/bin/env python3
"""
Network Manager PRO - Herramienta completa de gestión de red
Incluye: escaneo de red, detección de puertos, y gestión de firewall
"""

import socket
import subprocess
import threading
import time
import ipaddress
import json
import csv
from queue import Queue
from datetime import datetime
import platform
import os
import sys

# =========================
# CONFIGURACIÓN
# =========================
SERVICIOS_COMUNES = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 135: "MSRPC", 139: "NetBIOS",
    143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
    1433: "MSSQL", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    5900: "VNC", 6379: "Redis", 8080: "HTTP-ALT", 8443: "HTTPS-ALT",
    27017: "MongoDB"
}

PUERTOS_COMUNES = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 
                   993, 995, 1433, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017]

PUERTOS_TOP_100 = [
    7, 9, 13, 21, 22, 23, 25, 26, 37, 53, 79, 80, 81, 88, 106, 110, 111, 113, 119,
    135, 139, 143, 144, 179, 199, 389, 427, 443, 444, 445, 465, 513, 514, 515, 543,
    544, 548, 554, 587, 631, 646, 873, 990, 993, 995, 1025, 1026, 1027, 1028, 1029,
    1110, 1433, 1720, 1723, 1755, 1900, 2000, 2001, 2049, 2121, 2717, 3000, 3128,
    3306, 3389, 3986, 4899, 5000, 5009, 5051, 5060, 5101, 5190, 5357, 5432, 5631,
    5666, 5800, 5900, 6000, 6646, 7070, 8000, 8008, 8009, 8080, 8081, 8443, 8888,
    9100, 9999, 10000, 32768, 49152, 49153, 49154, 49155, 49156, 49157
]

# =========================
# ESCANEO DE RED
# =========================
def obtener_redes_locales():
    """Obtiene las redes locales del sistema."""
    redes = []
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["ipconfig"], capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split('\n'):
                if "IPv4" in line or "Dirección IPv4" in line:
                    ip_str = line.split(':')[-1].strip()
                    try:
                        ip = ipaddress.IPv4Address(ip_str)
                        # Crear red /24
                        red = ipaddress.IPv4Network(f"{ip_str}/24", strict=False)
                        if red not in redes:
                            redes.append(red)
                    except:
                        pass
        else:
            result = subprocess.run(
                ["ip", "addr"], capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split('\n'):
                if "inet " in line and "127.0.0.1" not in line:
                    ip_str = line.split()[1].split('/')[0]
                    try:
                        ip = ipaddress.IPv4Address(ip_str)
                        red = ipaddress.IPv4Network(f"{ip_str}/24", strict=False)
                        if red not in redes:
                            redes.append(red)
                    except:
                        pass
    except:
        pass
    return redes


def ping_host(ip, timeout=1):
    """Hace ping a un host y retorna True si está activo."""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["ping", "-n", "1", "-w", str(timeout * 1000), str(ip)],
                capture_output=True, timeout=timeout + 1
            )
        else:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", str(timeout), str(ip)],
                capture_output=True, timeout=timeout + 1
            )
        return result.returncode == 0
    except:
        return False


def obtener_hostname(ip):
    """Intenta obtener el hostname de una IP."""
    try:
        hostname = socket.gethostbyaddr(str(ip))[0]
        return hostname
    except:
        return None


def escanear_red(red_cidr=None, threads=50, timeout=1):
    """Escanea una red para encontrar hosts activos."""
    if red_cidr is None:
        redes = obtener_redes_locales()
        if not redes:
            print("❌ No se pudieron detectar redes locales.")
            red_input = input("Ingresa la red a escanear (ej: 192.168.1.0/24): ").strip()
            try:
                red = ipaddress.IPv4Network(red_input, strict=False)
            except:
                print("❌ Red inválida.")
                return []
        else:
            print("\n📡 Redes locales detectadas:")
            for i, red in enumerate(redes, 1):
                print(f"  {i}. {red}")
            if len(redes) == 1:
                red = redes[0]
                print(f"\n✓ Usando red: {red}")
            else:
                choice = input(f"\nSelecciona red (1-{len(redes)}): ").strip()
                try:
                    red = redes[int(choice) - 1]
                except:
                    red = redes[0]
    else:
        try:
            red = ipaddress.IPv4Network(red_cidr, strict=False)
        except:
            print(f"❌ Red inválida: {red_cidr}")
            return []
    
    hosts = list(red.hosts())
    print(f"\n🔍 Escaneando {len(hosts)} hosts en {red}...")
    
    resultados = []
    q = Queue()
    lock = threading.Lock()
    progress = [0]
    
    for host in hosts:
        q.put(host)
    
    def worker():
        while True:
            try:
                host = q.get(timeout=1)
            except:
                break
            
            if ping_host(host, timeout):
                hostname = obtener_hostname(host)
                with lock:
                    resultados.append({
                        "ip": str(host),
                        "hostname": hostname or "Desconocido",
                        "activo": True
                    })
                    progress[0] += 1
                    print(f"\r✓ Hosts encontrados: {len(resultados)}/{progress[0]} escaneados", end='', flush=True)
            
            with lock:
                progress[0] += 1
                if progress[0] % 10 == 0:
                    print(f"\rEscaneando... {progress[0]}/{len(hosts)}", end='', flush=True)
            
            q.task_done()
    
    threads_list = []
    for _ in range(min(threads, len(hosts))):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads_list.append(t)
    
    q.join()
    print("\r" + " " * 60 + "\r", end='')
    
    return resultados


# =========================
# ESCANEO DE PUERTOS
# =========================
def obtener_banner(sock, port):
    """Intenta obtener un banner del servicio."""
    try:
        sock.settimeout(1)
        if port == 21:  # FTP
            return sock.recv(1024).decode(errors="ignore").strip()
        elif port == 22:  # SSH
            return sock.recv(1024).decode(errors="ignore").strip()
        elif port in [25, 587]:  # SMTP
            sock.send(b"EHLO test\r\n")
            return sock.recv(1024).decode(errors="ignore").strip()
        elif port in [80, 8080]:  # HTTP
            sock.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            banner = sock.recv(1024).decode(errors="ignore").strip()
            return banner.split("\n")[0] if "\n" in banner else banner
        elif port in [443, 8443]:
            return "HTTPS (SSL/TLS)"
        elif port == 3306:  # MySQL
            return sock.recv(1024).decode(errors="ignore").strip()
        else:
            sock.send(b"\r\n")
            banner = sock.recv(1024).decode(errors="ignore").strip()
            return banner[:100] if banner else None
    except:
        return None


def escanear_puerto(ip, port, resultados, banner=False, timeout=1.0):
    """Escanea un puerto y retorna True si está abierto."""
    start_time = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        
        if result == 0:
            response_time = (time.time() - start_time) * 1000
            info = {
                "port": port,
                "service": SERVICIOS_COMUNES.get(port, "Desconocido"),
                "banner": None,
                "response_time": round(response_time, 2)
            }
            
            if banner:
                info["banner"] = obtener_banner(sock, port)
            
            resultados.append(info)
            sock.close()
            return True
        sock.close()
        return False
    except:
        return False


def escanear_puertos_host(ip, puertos=None, banner=False, timeout=1.0, threads=100):
    """Escanea puertos en un host específico."""
    if puertos is None:
        puertos = PUERTOS_COMUNES
    
    resultados = []
    q = Queue()
    progress_lock = threading.Lock()
    progress_counter = [0]
    
    for port in puertos:
        q.put(port)
    
    def worker():
        while True:
            try:
                port = q.get(timeout=1)
            except:
                break
            escanear_puerto(ip, port, resultados, banner, timeout)
            with progress_lock:
                progress_counter[0] += 1
            q.task_done()
    
    threads_list = []
    for _ in range(min(threads, len(puertos))):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads_list.append(t)
    
    q.join()
    resultados.sort(key=lambda x: x["port"])
    return resultados


# =========================
# GESTIÓN DE FIREWALL (WINDOWS)
# =========================
def es_administrador():
    """Verifica si el script se ejecuta como administrador."""
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except:
        return False


def abrir_puerto_firewall(port, protocol="TCP", name=None):
    """Abre un puerto en el firewall de Windows."""
    if platform.system() != "Windows":
        print("❌ La gestión de firewall solo está disponible en Windows.")
        return False
    
    if not es_administrador():
        print("❌ Se requieren permisos de administrador para gestionar el firewall.")
        return False
    
    if name is None:
        name = f"Puerto_{port}_{protocol}"
    
    try:
        cmd = [
            "netsh", "advfirewall", "firewall", "add", "rule",
            f"name={name}",
            f"dir=in",
            "action=allow",
            f"protocol={protocol}",
            f"localport={port}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Puerto {port}/{protocol} abierto correctamente.")
            return True
        else:
            print(f"❌ Error al abrir puerto: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def cerrar_puerto_firewall(port, protocol="TCP"):
    """Cierra un puerto en el firewall de Windows."""
    if platform.system() != "Windows":
        print("❌ La gestión de firewall solo está disponible en Windows.")
        return False
    
    if not es_administrador():
        print("❌ Se requieren permisos de administrador para gestionar el firewall.")
        return False
    
    try:
        cmd = [
            "netsh", "advfirewall", "firewall", "delete", "rule",
            f"protocol={protocol}",
            f"localport={port}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Puerto {port}/{protocol} cerrado correctamente.")
            return True
        else:
            print(f"❌ Error al cerrar puerto: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def listar_reglas_firewall():
    """Lista las reglas del firewall de Windows."""
    if platform.system() != "Windows":
        print("❌ La gestión de firewall solo está disponible en Windows.")
        return []
    
    if not es_administrador():
        print("❌ Se requieren permisos de administrador para ver reglas del firewall.")
        return []
    
    try:
        cmd = ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        return result.stdout
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def ver_puertos_locales():
    """Muestra los puertos abiertos en el sistema local."""
    print("\n📊 Puertos abiertos en el sistema local:\n")
    try:
        if platform.system() == "Windows":
            cmd = ["netstat", "-an"]
        else:
            cmd = ["ss", "-tuln"]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        return result.stdout
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


# =========================
# EXPORTACIÓN DE RESULTADOS
# =========================
def exportar_json(datos, filename):
    """Exporta datos a formato JSON."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        print(f"✅ Datos exportados a {filename}")
        return True
    except Exception as e:
        print(f"❌ Error al exportar: {e}")
        return False


def exportar_csv(datos, filename):
    """Exporta datos a formato CSV."""
    try:
        if not datos:
            print("❌ No hay datos para exportar.")
            return False
        
        if isinstance(datos, list) and len(datos) > 0:
            keys = datos[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(datos)
            print(f"✅ Datos exportados a {filename}")
            return True
    except Exception as e:
        print(f"❌ Error al exportar: {e}")
        return False


# =========================
# MENÚ PRINCIPAL
# =========================
def menu_escanear_red():
    """Menú para escanear red."""
    print("\n" + "=" * 70)
    print("  🔍 ESCANEO DE RED")
    print("=" * 70)
    
    red_input = input("\nIngresa la red a escanear (Enter para auto-detectar): ").strip()
    red = red_input if red_input else None
    
    threads_input = input("Número de threads (Enter para 50): ").strip()
    threads = int(threads_input) if threads_input else 50
    
    timeout_input = input("Timeout por host en segundos (Enter para 1): ").strip()
    timeout = float(timeout_input) if timeout_input else 1.0
    
    resultados = escanear_red(red, threads, timeout)
    
    if resultados:
        print(f"\n✅ Se encontraron {len(resultados)} hosts activos:\n")
        for host in resultados:
            print(f"  • {host['ip']:15s} - {host['hostname']}")
        
        exportar = input("\n¿Exportar resultados? (json/csv/n): ").strip().lower()
        if exportar == "json":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            exportar_json(resultados, f"escaneo_red_{timestamp}.json")
        elif exportar == "csv":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            exportar_csv(resultados, f"escaneo_red_{timestamp}.csv")
    else:
        print("\n❌ No se encontraron hosts activos.")


def menu_escanear_puertos():
    """Menú para escanear puertos."""
    print("\n" + "=" * 70)
    print("  🔍 ESCANEO DE PUERTOS")
    print("=" * 70)
    
    print("\nOpciones de escaneo:")
    print("  1. Puertos comunes (22 puertos)")
    print("  2. Top 100 puertos")
    print("  3. Rango personalizado")
    
    opcion = input("\nSelecciona opción (1-3): ").strip()
    
    if opcion == "1":
        puertos = PUERTOS_COMUNES
    elif opcion == "2":
        puertos = PUERTOS_TOP_100
    elif opcion == "3":
        start = int(input("Puerto inicial: "))
        end = int(input("Puerto final: "))
        puertos = list(range(start, end + 1))
    else:
        puertos = PUERTOS_COMUNES
    
    host = input("\nIngresa IP o dominio a escanear: ").strip()
    if not host:
        print("❌ No se ingresó ninguna dirección.")
        return
    
    # Resolver dominio
    ip = host
    if not host.replace('.', '').isdigit():
        try:
            ip = socket.gethostbyname(host)
            print(f"✓ {host} -> {ip}")
        except:
            print(f"❌ No se pudo resolver {host}")
            return
    
    banner = input("\n¿Obtener banners? (s/n): ").strip().lower() in ['s', 'si', 'sí', 'y']
    timeout = float(input("Timeout (Enter para 1.0s): ").strip() or "1.0")
    threads = int(input("Threads (Enter para 100): ").strip() or "100")
    
    print(f"\n🔍 Escaneando {len(puertos)} puertos en {host}...")
    resultados = escanear_puertos_host(ip, puertos, banner, timeout, threads)
    
    if resultados:
        print(f"\n✅ Se encontraron {len(resultados)} puertos abiertos:\n")
        for info in resultados:
            print(f"  ✓ Puerto {info['port']:5d} - {info['service']:20s} ({info['response_time']}ms)")
            if info['banner']:
                banner_clean = info['banner'].replace('\n', ' ')[:60]
                print(f"      Banner: {banner_clean}")
        
        exportar = input("\n¿Exportar resultados? (json/csv/n): ").strip().lower()
        if exportar == "json":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            exportar_json(resultados, f"escaneo_puertos_{timestamp}.json")
        elif exportar == "csv":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            exportar_csv(resultados, f"escaneo_puertos_{timestamp}.csv")
    else:
        print("\n❌ No se encontraron puertos abiertos.")


def menu_gestionar_firewall():
    """Menú para gestionar firewall."""
    print("\n" + "=" * 70)
    print("  🔥 GESTIÓN DE FIREWALL")
    print("=" * 70)
    
    if platform.system() != "Windows":
        print("\n❌ La gestión de firewall solo está disponible en Windows.")
        return
    
    if not es_administrador():
        print("\n⚠️  ADVERTENCIA: Se requieren permisos de administrador.")
        print("   Por favor, ejecuta este script como administrador.")
        return
    
    print("\nOpciones:")
    print("  1. Abrir puerto")
    print("  2. Cerrar puerto")
    print("  3. Listar reglas del firewall")
    print("  4. Ver puertos locales abiertos")
    
    opcion = input("\nSelecciona opción (1-4): ").strip()
    
    if opcion == "1":
        port = int(input("Puerto a abrir: "))
        protocol = input("Protocolo (TCP/UDP, Enter para TCP): ").strip().upper() or "TCP"
        name = input("Nombre de la regla (Enter para auto): ").strip() or None
        abrir_puerto_firewall(port, protocol, name)
    
    elif opcion == "2":
        port = int(input("Puerto a cerrar: "))
        protocol = input("Protocolo (TCP/UDP, Enter para TCP): ").strip().upper() or "TCP"
        cerrar_puerto_firewall(port, protocol)
    
    elif opcion == "3":
        listar_reglas_firewall()
    
    elif opcion == "4":
        ver_puertos_locales()
    
    else:
        print("❌ Opción inválida.")


def menu_escanear_red_completo():
    """Escaneo completo: red + puertos en todos los hosts encontrados."""
    print("\n" + "=" * 70)
    print("  🔍 ESCANEO COMPLETO DE RED")
    print("=" * 70)
    print("\nEste modo escaneará la red y luego los puertos en cada host encontrado.")
    
    red_input = input("\nIngresa la red a escanear (Enter para auto-detectar): ").strip()
    red = red_input if red_input else None
    
    threads_red = int(input("Threads para escaneo de red (Enter para 50): ").strip() or "50")
    timeout_red = float(input("Timeout para ping (Enter para 1.0s): ").strip() or "1.0")
    
    print("\n" + "-" * 70)
    print("PASO 1: Escaneando red...")
    print("-" * 70)
    hosts = escanear_red(red, threads_red, timeout_red)
    
    if not hosts:
        print("\n❌ No se encontraron hosts activos.")
        return
    
    print(f"\n✅ Se encontraron {len(hosts)} hosts activos.")
    
    # Configurar escaneo de puertos
    print("\n" + "-" * 70)
    print("PASO 2: Configuración de escaneo de puertos")
    print("-" * 70)
    print("\nOpciones de escaneo de puertos:")
    print("  1. Puertos comunes (22 puertos)")
    print("  2. Top 100 puertos")
    print("  3. Rango personalizado")
    
    opcion = input("\nSelecciona opción (1-3): ").strip()
    if opcion == "1":
        puertos = PUERTOS_COMUNES
    elif opcion == "2":
        puertos = PUERTOS_TOP_100
    elif opcion == "3":
        start = int(input("Puerto inicial: "))
        end = int(input("Puerto final: "))
        puertos = list(range(start, end + 1))
    else:
        puertos = PUERTOS_COMUNES
    
    banner = input("\n¿Obtener banners? (s/n): ").strip().lower() in ['s', 'si', 'sí', 'y']
    timeout_port = float(input("Timeout por puerto (Enter para 1.0s): ").strip() or "1.0")
    threads_port = int(input("Threads por host (Enter para 50): ").strip() or "50")
    
    # Escanear puertos en cada host
    print("\n" + "-" * 70)
    print("PASO 3: Escaneando puertos en cada host...")
    print("-" * 70)
    
    resultados_completos = []
    for i, host in enumerate(hosts, 1):
        ip = host['ip']
        print(f"\n[{i}/{len(hosts)}] Escaneando {ip} ({host['hostname']})...")
        puertos_abiertos = escanear_puertos_host(ip, puertos, banner, timeout_port, threads_port)
        
        resultado_host = {
            "ip": ip,
            "hostname": host['hostname'],
            "puertos_abiertos": len(puertos_abiertos),
            "puertos": puertos_abiertos
        }
        resultados_completos.append(resultado_host)
        
        if puertos_abiertos:
            print(f"  ✓ {len(puertos_abiertos)} puertos abiertos encontrados")
        else:
            print(f"  ✗ No se encontraron puertos abiertos")
    
    # Mostrar resumen
    print("\n" + "=" * 70)
    print("  📊 RESUMEN DEL ESCANEO COMPLETO")
    print("=" * 70)
    
    total_puertos = sum(r['puertos_abiertos'] for r in resultados_completos)
    print(f"\nHosts escaneados: {len(resultados_completos)}")
    print(f"Total de puertos abiertos encontrados: {total_puertos}")
    
    print("\n" + "-" * 70)
    print("DETALLES POR HOST:")
    print("-" * 70)
    
    for resultado in resultados_completos:
        print(f"\n  📍 {resultado['ip']} ({resultado['hostname']})")
        if resultado['puertos']:
            for puerto_info in resultado['puertos']:
                print(f"    ✓ Puerto {puerto_info['port']:5d} - {puerto_info['service']:20s}")
                if puerto_info.get('banner'):
                    banner_clean = puerto_info['banner'].replace('\n', ' ')[:50]
                    print(f"        Banner: {banner_clean}")
        else:
            print("    ✗ No hay puertos abiertos")
    
    # Exportar resultados
    exportar = input("\n¿Exportar resultados? (json/csv/n): ").strip().lower()
    if exportar == "json":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exportar_json(resultados_completos, f"escaneo_completo_{timestamp}.json")
    elif exportar == "csv":
        # Aplanar datos para CSV
        datos_csv = []
        for resultado in resultados_completos:
            if resultado['puertos']:
                for puerto_info in resultado['puertos']:
                    datos_csv.append({
                        'ip': resultado['ip'],
                        'hostname': resultado['hostname'],
                        'puerto': puerto_info['port'],
                        'servicio': puerto_info['service'],
                        'banner': puerto_info.get('banner', ''),
                        'tiempo_respuesta': puerto_info.get('response_time', '')
                    })
            else:
                datos_csv.append({
                    'ip': resultado['ip'],
                    'hostname': resultado['hostname'],
                    'puerto': '',
                    'servicio': '',
                    'banner': '',
                    'tiempo_respuesta': ''
                })
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exportar_csv(datos_csv, f"escaneo_completo_{timestamp}.csv")


def menu_principal():
    """Menú principal del programa."""
    while True:
        print("\n" + "=" * 70)
        print("  🌐 NETWORK MANAGER PRO")
        print("=" * 70)
        print("\nOpciones:")
        print("  1. Escanear red (descubrir hosts activos)")
        print("  2. Escanear puertos de un host")
        print("  3. Escanear red completa (red + puertos en todos los hosts)")
        print("  4. Gestionar firewall (abrir/cerrar puertos)")
        print("  5. Ver puertos locales abiertos")
        print("  6. Salir")
        
        opcion = input("\nSelecciona una opción (1-6): ").strip()
        
        if opcion == "1":
            menu_escanear_red()
        elif opcion == "2":
            menu_escanear_puertos()
        elif opcion == "3":
            menu_escanear_red_completo()
        elif opcion == "4":
            menu_gestionar_firewall()
        elif opcion == "5":
            ver_puertos_locales()
        elif opcion == "6":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción inválida. Intenta de nuevo.")


# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

