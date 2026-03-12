"""
Script de demostración del gestor de tareas
Simula algunas operaciones para mostrar cómo funciona
"""

from todo_list import TodoList
import os
import sys

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def demo():
    """Demostración de las funcionalidades del gestor de tareas"""
    
    # Usar un archivo de prueba para no afectar las tareas reales
    archivo_demo = "tareas_demo.json"
    
    # Limpiar archivo de demo si existe
    if os.path.exists(archivo_demo):
        os.remove(archivo_demo)
    
    print("="*60)
    print("DEMOSTRACION DEL GESTOR DE TAREAS")
    print("="*60)
    
    # Crear instancia con archivo de demo
    todo = TodoList(archivo_demo)
    
    print("\n1. Agregando algunas tareas de ejemplo...\n")
    
    # Agregar tareas de ejemplo
    todo.agregar_tarea("Estudiar Python - Clases y objetos", "alta")
    todo.agregar_tarea("Comprar ingredientes para la cena", "media")
    todo.agregar_tarea("Llamar a mama", "alta")
    todo.agregar_tarea("Leer un capitulo del libro", "baja")
    todo.agregar_tarea("Hacer ejercicio", "media")
    
    print("\n" + "="*60)
    print("2. Listando todas las tareas...")
    print("="*60)
    todo.listar_tareas(mostrar_completadas=True)
    
    print("\n" + "="*60)
    print("3. Completando una tarea (ID 1)...")
    print("="*60)
    todo.completar_tarea(1)
    
    print("\n" + "="*60)
    print("4. Listando solo tareas pendientes...")
    print("="*60)
    todo.listar_tareas(mostrar_completadas=False)
    
    print("\n" + "="*60)
    print("5. Buscando tareas con 'Python'...")
    print("="*60)
    todo.buscar_tareas("Python")
    
    print("\n" + "="*60)
    print("6. Completando otra tarea (ID 3)...")
    print("="*60)
    todo.completar_tarea(3)
    
    print("\n" + "="*60)
    print("7. Ver estadisticas...")
    print("="*60)
    todo.estadisticas()
    
    print("\n" + "="*60)
    print("8. Listando todas las tareas finales...")
    print("="*60)
    todo.listar_tareas(mostrar_completadas=True)
    
    print("\n" + "="*60)
    print("Demostracion completada!")
    print("="*60)
    print(f"\nLas tareas se guardaron en: {archivo_demo}")
    print("Puedes eliminar este archivo si quieres limpiar la demo\n")

if __name__ == "__main__":
    demo()

