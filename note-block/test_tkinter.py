"""Script de prueba para verificar que Tkinter funciona"""
import tkinter as tk
from tkinter import messagebox

print("Iniciando prueba de Tkinter...")

try:
    root = tk.Tk()
    root.title("Prueba de Tkinter")
    root.geometry("400x300")
    
    # Asegurar que la ventana esté visible
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.focus_force()
    
    label = tk.Label(root, text="¡Tkinter funciona correctamente!", 
                    font=('Arial', 14), pady=20)
    label.pack()
    
    button = tk.Button(root, text="Cerrar", command=root.quit, 
                      font=('Arial', 12), padx=20, pady=10)
    button.pack()
    
    print("Ventana creada. Deberías ver una ventana con el mensaje.")
    print("Si no la ves, verifica:")
    print("1. Que no esté minimizada en la barra de tareas")
    print("2. Que no esté detrás de otras ventanas")
    print("3. Presiona Alt+Tab para cambiar entre ventanas")
    
    root.mainloop()
    print("Ventana cerrada correctamente.")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    input("Presiona Enter para salir...")






















