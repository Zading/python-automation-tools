"""
Aplicación de Lista de Tareas (To-Do List)
Permite gestionar tareas: agregar, listar, completar, eliminar y buscar
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class TodoList:
    """Clase para gestionar la lista de tareas"""
    
    def __init__(self, archivo_datos: str = "tareas.json"):
        """
        Inicializa la lista de tareas
        
        Args:
            archivo_datos: Nombre del archivo donde se guardan las tareas
        """
        self.archivo_datos = archivo_datos
        self.tareas = self.cargar_tareas()
        self.contador_id = self._obtener_siguiente_id()
    
    def _obtener_siguiente_id(self) -> int:
        """Obtiene el siguiente ID disponible para una nueva tarea"""
        if not self.tareas:
            return 1
        return max(tarea['id'] for tarea in self.tareas) + 1
    
    def cargar_tareas(self) -> List[Dict]:
        """
        Carga las tareas desde el archivo JSON
        
        Returns:
            Lista de tareas
        """
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def guardar_tareas(self):
        """Guarda las tareas en el archivo JSON"""
        try:
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(self.tareas, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error al guardar las tareas: {e}")
            raise
        except Exception as e:
            print(f"Error inesperado al guardar: {e}")
            raise
    
    def agregar_tarea(self, descripcion: str, prioridad: str = "media") -> bool:
        """
        Agrega una nueva tarea a la lista
        
        Args:
            descripcion: Descripción de la tarea
            prioridad: Prioridad de la tarea (alta, media, baja)
        
        Returns:
            True si se agregó correctamente, False en caso contrario
        """
        try:
            if not descripcion or not descripcion.strip():
                # No usar print con emojis en Windows
                return False
            
            # Validar y normalizar prioridad
            prioridad = prioridad.strip().lower() if prioridad else "media"
            if prioridad not in ["alta", "media", "baja"]:
                prioridad = "media"
            
            nueva_tarea = {
                "id": self.contador_id,
                "descripcion": descripcion.strip(),
                "completada": False,
                "prioridad": prioridad,
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "fecha_completada": None
            }
            
            self.tareas.append(nueva_tarea)
            self.contador_id += 1
            self.guardar_tareas()
            # No usar print con emojis para evitar errores de codificación en Windows
            return True
        except Exception as e:
            # Log del error sin emojis
            print(f"Error al agregar tarea: {e}")
            return False
    
    def listar_tareas(self, mostrar_completadas: bool = True, filtro_prioridad: Optional[str] = None):
        """
        Lista todas las tareas
        
        Args:
            mostrar_completadas: Si True, muestra también las tareas completadas
            filtro_prioridad: Filtra por prioridad (alta, media, baja) o None para todas
        """
        tareas_filtradas = self.tareas.copy()
        
        # Filtrar por prioridad si se especifica
        if filtro_prioridad:
            tareas_filtradas = [t for t in tareas_filtradas if t['prioridad'] == filtro_prioridad]
        
        # Filtrar completadas si no se quieren mostrar
        if not mostrar_completadas:
            tareas_filtradas = [t for t in tareas_filtradas if not t['completada']]
        
        if not tareas_filtradas:
            print("📝 No hay tareas para mostrar")
            return
        
        # Ordenar: primero pendientes, luego completadas; dentro de cada grupo por prioridad
        orden_prioridad = {"alta": 1, "media": 2, "baja": 3}
        tareas_filtradas.sort(key=lambda x: (x['completada'], orden_prioridad.get(x['prioridad'], 3)))
        
        print("\n" + "="*60)
        print("📋 LISTA DE TAREAS")
        print("="*60)
        
        for tarea in tareas_filtradas:
            estado = "✅" if tarea['completada'] else "⏳"
            prioridad_icono = {
                "alta": "🔴",
                "media": "🟡",
                "baja": "🟢"
            }
            icono_prioridad = prioridad_icono.get(tarea['prioridad'], "⚪")
            
            print(f"\n{estado} [{tarea['id']}] {icono_prioridad} {tarea['descripcion']}")
            print(f"   Prioridad: {tarea['prioridad'].upper()}")
            print(f"   Creada: {tarea['fecha_creacion']}")
            
            if tarea['completada'] and tarea['fecha_completada']:
                print(f"   Completada: {tarea['fecha_completada']}")
        
        print("\n" + "="*60)
        print(f"Total: {len(tareas_filtradas)} tarea(s)")
        print("="*60 + "\n")
    
    def completar_tarea(self, id_tarea: int) -> bool:
        """
        Marca una tarea como completada
        
        Args:
            id_tarea: ID de la tarea a completar
        
        Returns:
            True si se completó correctamente, False en caso contrario
        """
        tarea = self._buscar_tarea_por_id(id_tarea)
        
        if not tarea:
            # No usar print con emojis para evitar errores de codificación
            return False
        
        if tarea['completada']:
            # La tarea ya está completada
            return False
        
        tarea['completada'] = True
        tarea['fecha_completada'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.guardar_tareas()
        return True
    
    def eliminar_tarea(self, id_tarea: int) -> bool:
        """
        Elimina una tarea de la lista
        
        Args:
            id_tarea: ID de la tarea a eliminar
        
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        tarea = self._buscar_tarea_por_id(id_tarea)
        
        if not tarea:
            # No usar print con emojis para evitar errores de codificación
            return False
        
        descripcion = tarea['descripcion']
        self.tareas.remove(tarea)
        self.guardar_tareas()
        return True
    
    def buscar_tareas(self, termino: str):
        """
        Busca tareas que contengan el término especificado
        
        Args:
            termino: Término de búsqueda
        """
        termino_lower = termino.lower()
        tareas_encontradas = [
            t for t in self.tareas
            if termino_lower in t['descripcion'].lower()
        ]
        
        if not tareas_encontradas:
            print(f"🔍 No se encontraron tareas con el término '{termino}'")
            return
        
        print(f"\n🔍 Resultados de búsqueda para '{termino}':")
        print("="*60)
        
        for tarea in tareas_encontradas:
            estado = "✅" if tarea['completada'] else "⏳"
            prioridad_icono = {
                "alta": "🔴",
                "media": "🟡",
                "baja": "🟢"
            }
            icono_prioridad = prioridad_icono.get(tarea['prioridad'], "⚪")
            
            print(f"{estado} [{tarea['id']}] {icono_prioridad} {tarea['descripcion']}")
        
        print("="*60 + "\n")
    
    def estadisticas(self):
        """Muestra estadísticas de las tareas"""
        total = len(self.tareas)
        completadas = sum(1 for t in self.tareas if t['completada'])
        pendientes = total - completadas
        
        prioridades = {"alta": 0, "media": 0, "baja": 0}
        for tarea in self.tareas:
            if not tarea['completada']:
                prioridades[tarea['prioridad']] += 1
        
        print("\n" + "="*60)
        print("📊 ESTADÍSTICAS")
        print("="*60)
        print(f"Total de tareas: {total}")
        print(f"✅ Completadas: {completadas}")
        print(f"⏳ Pendientes: {pendientes}")
        
        if total > 0:
            porcentaje = (completadas / total) * 100
            print(f"📈 Progreso: {porcentaje:.1f}%")
        
        print("\nTareas pendientes por prioridad:")
        print(f"  🔴 Alta: {prioridades['alta']}")
        print(f"  🟡 Media: {prioridades['media']}")
        print(f"  🟢 Baja: {prioridades['baja']}")
        print("="*60 + "\n")
    
    def _buscar_tarea_por_id(self, id_tarea: int) -> Optional[Dict]:
        """
        Busca una tarea por su ID
        
        Args:
            id_tarea: ID de la tarea
        
        Returns:
            Diccionario de la tarea o None si no se encuentra
        """
        for tarea in self.tareas:
            if tarea['id'] == id_tarea:
                return tarea
        return None


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*60)
    print("📝 GESTOR DE TAREAS - MENÚ PRINCIPAL")
    print("="*60)
    print("1. Agregar tarea")
    print("2. Listar todas las tareas")
    print("3. Listar tareas pendientes")
    print("4. Completar tarea")
    print("5. Eliminar tarea")
    print("6. Buscar tareas")
    print("7. Ver estadísticas")
    print("8. Salir")
    print("="*60)


def main():
    """Función principal del programa"""
    todo = TodoList()
    
    print("✨ ¡Bienvenido al Gestor de Tareas! ✨")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSelecciona una opción (1-8): ").strip()
            
            if opcion == "1":
                descripcion = input("📝 Ingresa la descripción de la tarea: ").strip()
                print("\nPrioridades disponibles:")
                print("  1. Alta")
                print("  2. Media (por defecto)")
                print("  3. Baja")
                prioridad_opcion = input("Selecciona la prioridad (1-3, Enter para media): ").strip()
                
                prioridad_map = {"1": "alta", "2": "media", "3": "baja"}
                prioridad = prioridad_map.get(prioridad_opcion, "media")
                
                todo.agregar_tarea(descripcion, prioridad)
            
            elif opcion == "2":
                todo.listar_tareas(mostrar_completadas=True)
            
            elif opcion == "3":
                todo.listar_tareas(mostrar_completadas=False)
            
            elif opcion == "4":
                todo.listar_tareas(mostrar_completadas=False)
                try:
                    id_tarea = int(input("Ingresa el ID de la tarea a completar: "))
                    todo.completar_tarea(id_tarea)
                except ValueError:
                    print("❌ Error: Debes ingresar un número válido")
            
            elif opcion == "5":
                todo.listar_tareas(mostrar_completadas=True)
                try:
                    id_tarea = int(input("Ingresa el ID de la tarea a eliminar: "))
                    confirmar = input(f"¿Estás seguro de eliminar la tarea {id_tarea}? (s/n): ").strip().lower()
                    if confirmar == 's':
                        todo.eliminar_tarea(id_tarea)
                    else:
                        print("❌ Operación cancelada")
                except ValueError:
                    print("❌ Error: Debes ingresar un número válido")
            
            elif opcion == "6":
                termino = input("🔍 Ingresa el término de búsqueda: ").strip()
                if termino:
                    todo.buscar_tareas(termino)
                else:
                    print("❌ Error: El término de búsqueda no puede estar vacío")
            
            elif opcion == "7":
                todo.estadisticas()
            
            elif opcion == "8":
                print("\n👋 ¡Gracias por usar el Gestor de Tareas! ¡Hasta pronto! 👋\n")
                break
            
            else:
                print("❌ Opción no válida. Por favor, selecciona una opción del 1 al 8.")
        
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta pronto! 👋\n")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()



