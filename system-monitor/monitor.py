import psutil
import time
import os
import platform
from datetime import datetime

class MonitorConsola:
    def __init__(self):
        # Variables para red
        self.last_net_sent = 0
        self.last_net_recv = 0
        self.last_net_time = time.time()
        
        # Variables para temperatura
        self.temp_available = False
        
        # Configuración
        self.update_interval = 5.0  # segundos
        
    def limpiar_pantalla(self):
        """Limpia la pantalla según el sistema operativo"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mover_cursor_inicio(self):
        """Mueve el cursor al inicio y limpia desde ahí hasta el final"""
        print('\033[H\033[J', end='')
    
    def formatear_bytes(self, bytes_value):
        """Formatea bytes a formato legible"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
    
    def obtener_temperatura(self):
        """Obtiene la temperatura del sistema si está disponible"""
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                if 'coretemp' in temps:
                    cpu_temps = temps['coretemp']
                    if cpu_temps:
                        return cpu_temps[0].current
                elif 'cpu_thermal' in temps:
                    return temps['cpu_thermal'][0].current
                elif 'k10temp' in temps:
                    return temps['k10temp'][0].current
                elif 'acpitz' in temps:
                    return temps['acpitz'][0].current
                else:
                    for key, values in temps.items():
                        if values:
                            return values[0].current
        except (AttributeError, KeyError, IndexError):
            try:
                if platform.system() == 'Windows':
                    try:
                        import wmi
                        w = wmi.WMI(namespace="root\\wmi")
                        temperature_info = w.MSAcpi_ThermalZoneTemperature()[0]
                        temp_kelvin = temperature_info.CurrentTemperature / 10.0
                        temp_celsius = temp_kelvin - 273.15
                        return temp_celsius
                    except ImportError:
                        pass
            except:
                pass
        return None
    
    def obtener_top_procesos(self, n=5):
        """Obtiene los N procesos que más CPU consumen"""
        procesos = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info']):
            try:
                pinfo = proc.info
                if pinfo['cpu_percent'] is not None and pinfo['cpu_percent'] > 0:
                    procesos.append({
                        'pid': pinfo['pid'],
                        'name': pinfo['name'][:25],
                        'cpu': pinfo['cpu_percent'],
                        'ram': pinfo['memory_percent'],
                        'mem': pinfo['memory_info'].rss
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        procesos.sort(key=lambda x: x['cpu'], reverse=True)
        return procesos[:n]
    
    def obtener_color_ansi(self, valor, tipo='cpu'):
        """Retorna código ANSI para colores en consola"""
        reset = '\033[0m'
        if tipo == 'cpu' or tipo == 'ram' or tipo == 'disk':
            if valor > 80:
                return '\033[91m'  # Rojo
            elif valor > 50:
                return '\033[93m'  # Amarillo
            else:
                return '\033[92m'  # Verde
        elif tipo == 'temp':
            if valor > 80:
                return '\033[91m'  # Rojo
            elif valor > 70:
                return '\033[93m'  # Amarillo
            elif valor > 60:
                return '\033[33m'  # Amarillo oscuro
            else:
                return '\033[92m'  # Verde
        return reset
    
    def mostrar_monitor(self):
        """Muestra el monitor en consola"""
        # Limpiar pantalla solo una vez al inicio
        self.limpiar_pantalla()
        primera_vez = True
        
        while True:
            try:
                # Después de la primera vez, solo mover el cursor al inicio
                if not primera_vez:
                    self.mover_cursor_inicio()
                else:
                    primera_vez = False
                
                # Encabezado
                print("=" * 80)
                print("  MONITOR DEL SISTEMA - TIEMPO REAL".center(80))
                print("=" * 80)
                print(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("Presiona CTRL+C para salir\n")
                
                # CPU
                cpu_percent = psutil.cpu_percent(interval=None)
                cpu_cores = psutil.cpu_count()
                color_cpu = self.obtener_color_ansi(cpu_percent, 'cpu')
                reset = '\033[0m'
                
                freq_info = ""
                try:
                    freq = psutil.cpu_freq()
                    if freq and freq.current:
                        freq_info = f" | Frecuencia: {freq.current:.0f} MHz"
                except:
                    pass
                
                print(f"{color_cpu}CPU: {cpu_percent:5.1f}%{reset} | Núcleos: {cpu_cores}{freq_info}")
                
                # RAM
                ram = psutil.virtual_memory()
                ram_percent = ram.percent
                ram_used = ram.used
                ram_total = ram.total
                ram_available = ram.available
                color_ram = self.obtener_color_ansi(ram_percent, 'ram')
                print(f"{color_ram}RAM: {ram_percent:5.1f}%{reset} | Usada: {self.formatear_bytes(ram_used):>10} | Total: {self.formatear_bytes(ram_total):>10} | Disponible: {self.formatear_bytes(ram_available):>10}")
                
                # Disco
                if platform.system() == 'Windows':
                    disk_path = 'C:\\'
                else:
                    disk_path = '/'
                
                try:
                    disk = psutil.disk_usage(disk_path)
                    disk_percent = disk.percent
                    disk_used = disk.used
                    disk_total = disk.total
                    disk_free = disk.free
                    color_disk = self.obtener_color_ansi(disk_percent, 'disk')
                    print(f"{color_disk}Disco: {disk_percent:5.1f}%{reset} | Usado: {self.formatear_bytes(disk_used):>10} | Total: {self.formatear_bytes(disk_total):>10} | Libre: {self.formatear_bytes(disk_free):>10}")
                except Exception:
                    print("Disco: No disponible")
                
                # Temperatura
                temp = self.obtener_temperatura()
                if temp is not None:
                    self.temp_available = True
                    color_temp = self.obtener_color_ansi(temp, 'temp')
                    estado = "Crítico" if temp > 80 else "Alto" if temp > 70 else "Moderado" if temp > 60 else "Normal"
                    print(f"{color_temp}Temperatura CPU: {temp:5.1f}°C{reset} | Estado: {estado}")
                else:
                    if not self.temp_available:
                        print("Temperatura: No disponible")
                
                # Red
                net = psutil.net_io_counters()
                current_time = time.time()
                time_diff = current_time - self.last_net_time
                
                if time_diff > 0:
                    sent_speed = (net.bytes_sent - self.last_net_sent) / time_diff
                    recv_speed = (net.bytes_recv - self.last_net_recv) / time_diff
                    
                    print(f"Red - Enviado: {sent_speed/1024:8.2f} KB/s ({self.formatear_bytes(net.bytes_sent):>10} total)")
                    print(f"Red - Recibido: {recv_speed/1024:8.2f} KB/s ({self.formatear_bytes(net.bytes_recv):>10} total)")
                    print(f"Red - Total: {self.formatear_bytes(net.bytes_sent + net.bytes_recv):>10}")
                    
                    self.last_net_sent = net.bytes_sent
                    self.last_net_recv = net.bytes_recv
                    self.last_net_time = current_time
                else:
                    print(f"Red - Enviado: {self.formatear_bytes(net.bytes_sent):>10} | Recibido: {self.formatear_bytes(net.bytes_recv):>10}")
                
                # Sistema
                boot_time = datetime.fromtimestamp(psutil.boot_time())
                uptime = datetime.now() - boot_time
                hours = int(uptime.total_seconds() // 3600)
                minutes = int((uptime.total_seconds() % 3600) // 60)
                seconds = int(uptime.total_seconds() % 60)
                
                procesos = psutil.pids()
                try:
                    thread_count = sum(p.num_threads() for p in psutil.process_iter() if p.is_running())
                except:
                    thread_count = 0
                
                print(f"\nSistema - OS: {platform.system()} {platform.release()} | Tiempo activo: {hours}h {minutes}m {seconds}s")
                print(f"Procesos activos: {len(procesos)} | Hilos: {thread_count}")
                
                # Top procesos
                print("\n" + "=" * 80)
                print("TOP 5 PROCESOS POR CPU")
                print("=" * 80)
                print(f"{'PID':<8} {'Nombre':<25} {'CPU %':<8} {'RAM %':<8} {'Memoria':<15}")
                print("-" * 80)
                
                top_procesos = self.obtener_top_procesos(5)
                for proc in top_procesos:
                    print(f"{proc['pid']:<8} {proc['name']:<25} {proc['cpu']:>6.1f}% {proc['ram']:>6.1f}% {self.formatear_bytes(proc['mem']):>15}")
                
                print("\n" + "=" * 80)
                print(f"Actualizando cada {self.update_interval}s...")
                
                time.sleep(self.update_interval)
                
            except KeyboardInterrupt:
                print("\n\nMonitor finalizado. ¡Hasta luego! 🚀")
                break
            except Exception as e:
                print(f"\nError: {e}")
                time.sleep(1)


def main():
    monitor = MonitorConsola()
    monitor.mostrar_monitor()


if __name__ == "__main__":
    main()
