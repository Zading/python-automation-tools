"""
Script de diagnóstico para verificar el estado del sistema
"""

import os
import json
from todo_list import TodoList
from auth import AuthManager

print("="*60)
print("DIAGNÓSTICO DEL SISTEMA")
print("="*60)

# Verificar archivos
print("\n1. Verificando archivos...")
archivos = ["tareas.json", "usuarios.json"]
for archivo in archivos:
    if os.path.exists(archivo):
        print(f"   [OK] {archivo} existe")
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"      - Contiene {len(data)} elemento(s)")
        except Exception as e:
            print(f"   [ERROR] Error al leer {archivo}: {e}")
    else:
        print(f"   [INFO] {archivo} no existe (se creara automaticamente)")

# Verificar TodoList
print("\n2. Verificando TodoList...")
try:
    todo = TodoList("tareas.json")
    print(f"   [OK] TodoList inicializado correctamente")
    print(f"      - Tareas cargadas: {len(todo.tareas)}")
    print(f"      - Siguiente ID: {todo.contador_id}")
except Exception as e:
    print(f"   [ERROR] Error al inicializar TodoList: {e}")

# Verificar AuthManager
print("\n3. Verificando AuthManager...")
try:
    auth = AuthManager("usuarios.json")
    print(f"   [OK] AuthManager inicializado correctamente")
    print(f"      - Usuarios registrados: {len(auth.usuarios)}")
except Exception as e:
    print(f"   [ERROR] Error al inicializar AuthManager: {e}")

# Probar agregar tarea
print("\n4. Probando agregar tarea...")
try:
    todo = TodoList("tareas.json")
    resultado = todo.agregar_tarea("Tarea de prueba", "media")
    if resultado:
        print("   [OK] Tarea agregada correctamente")
    else:
        print("   [ERROR] Error al agregar tarea")
except Exception as e:
    print(f"   [ERROR] Excepcion al agregar tarea: {e}")
    import traceback
    traceback.print_exc()

# Verificar permisos de escritura
print("\n5. Verificando permisos de escritura...")
try:
    test_file = "test_write.tmp"
    with open(test_file, 'w') as f:
        f.write("test")
    os.remove(test_file)
    print("   [OK] Permisos de escritura OK")
except Exception as e:
    print(f"   [ERROR] Error de permisos: {e}")

print("\n" + "="*60)
print("DIAGNÓSTICO COMPLETADO")
print("="*60)

