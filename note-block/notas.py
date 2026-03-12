"""
Block de Notas - Aplicación con interfaz gráfica usando Tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import datetime
import json
import os
from pathlib import Path

class BlockDeNotas:
    # Temas prediseñados
    TEMAS = {
        'Oscuro': {
            'fondo': '#2b2b2b',
            'panel': '#3c3c3c',
            'texto': '#ffffff',
            'texto_secundario': '#b0b0b0',
            'boton': '#4a9eff',
            'boton_hover': '#5aaeff',
            'boton_peligro': '#ff4444',
            'entrada': '#1e1e1e',
            'lista': '#252525',
            'lista_seleccion': '#4a9eff',
            'accento': '#00d4ff',
            'exito': '#4caf50',
            'advertencia': '#ff9800'
        },
        'Claro': {
            'fondo': '#f5f5f5',
            'panel': '#ffffff',
            'texto': '#212121',
            'texto_secundario': '#757575',
            'boton': '#2196F3',
            'boton_hover': '#42a5f5',
            'boton_peligro': '#f44336',
            'entrada': '#ffffff',
            'lista': '#fafafa',
            'lista_seleccion': '#2196F3',
            'accento': '#00BCD4',
            'exito': '#4CAF50',
            'advertencia': '#FF9800'
        },
        'Azul': {
            'fondo': '#1a237e',
            'panel': '#283593',
            'texto': '#e3f2fd',
            'texto_secundario': '#90caf9',
            'boton': '#3f51b5',
            'boton_hover': '#5c6bc0',
            'boton_peligro': '#e91e63',
            'entrada': '#3949ab',
            'lista': '#303f9f',
            'lista_seleccion': '#5c6bc0',
            'accento': '#00e5ff',
            'exito': '#4caf50',
            'advertencia': '#ffc107'
        },
        'Verde': {
            'fondo': '#1b5e20',
            'panel': '#2e7d32',
            'texto': '#e8f5e9',
            'texto_secundario': '#a5d6a7',
            'boton': '#4caf50',
            'boton_hover': '#66bb6a',
            'boton_peligro': '#f44336',
            'entrada': '#388e3c',
            'lista': '#2e7d32',
            'lista_seleccion': '#66bb6a',
            'accento': '#76ff03',
            'exito': '#4caf50',
            'advertencia': '#ff9800'
        },
        'Púrpura': {
            'fondo': '#4a148c',
            'panel': '#6a1b9a',
            'texto': '#f3e5f5',
            'texto_secundario': '#ce93d8',
            'boton': '#9c27b0',
            'boton_hover': '#ab47bc',
            'boton_peligro': '#e91e63',
            'entrada': '#7b1fa2',
            'lista': '#6a1b9a',
            'lista_seleccion': '#ab47bc',
            'accento': '#e1bee7',
            'exito': '#4caf50',
            'advertencia': '#ff9800'
        },
        'Naranja': {
            'fondo': '#e65100',
            'panel': '#f57c00',
            'texto': '#fff3e0',
            'texto_secundario': '#ffcc80',
            'boton': '#ff9800',
            'boton_hover': '#ffb74d',
            'boton_peligro': '#f44336',
            'entrada': '#fb8c00',
            'lista': '#f57c00',
            'lista_seleccion': '#ffb74d',
            'accento': '#ffd54f',
            'exito': '#4caf50',
            'advertencia': '#ff9800'
        }
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Block de Notas")
        self.root.geometry("900x700")
        
        # Ruta de archivos
        self.archivo_datos = Path(__file__).parent / "notas.json"
        self.archivo_config = Path(__file__).parent / "config.json"
        
        # Cargar configuración
        self.tema_actual = self.cargar_configuracion()
        self.colores = self.TEMAS.get(self.tema_actual, self.TEMAS['Oscuro']).copy()
        
        self.root.configure(bg=self.colores['fondo'])
        
        # Lista de notas
        self.notas = []
        self.nota_actual = None
        
        # Cargar notas existentes
        self.cargar_notas()
        
        # Crear menú
        self.crear_menu()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Actualizar lista
        self.actualizar_lista()
    
    def cargar_configuracion(self):
        """Carga la configuración guardada"""
        if self.archivo_config.exists():
            try:
                with open(self.archivo_config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('tema', 'Oscuro')
            except:
                return 'Oscuro'
        return 'Oscuro'
    
    def guardar_configuracion(self):
        """Guarda la configuración"""
        try:
            config = {'tema': self.tema_actual}
            with open(self.archivo_config, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar configuración: {e}")
            return False
    
    def crear_menu(self):
        """Crea la barra de menú"""
        menubar = tk.Menu(self.root, bg=self.colores['panel'], fg=self.colores['texto'],
                         activebackground=self.colores['boton'], 
                         activeforeground=self.colores['texto'])
        self.root.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0, bg=self.colores['panel'], 
                              fg=self.colores['texto'],
                              activebackground=self.colores['boton'],
                              activeforeground=self.colores['texto'])
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nueva Nota", command=self.nueva_nota, 
                                accelerator="Ctrl+N")
        menu_archivo.add_command(label="Guardar", command=self.guardar_nota, 
                                accelerator="Ctrl+S")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Eliminar Nota", command=self.eliminar_nota, 
                                accelerator="Ctrl+D")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.root.quit, 
                                accelerator="Ctrl+Q")
        
        # Menú Editar
        menu_editar = tk.Menu(menubar, tearoff=0, bg=self.colores['panel'], 
                             fg=self.colores['texto'],
                             activebackground=self.colores['boton'],
                             activeforeground=self.colores['texto'])
        menubar.add_cascade(label="Editar", menu=menu_editar)
        menu_editar.add_command(label="Limpiar Editor", command=self.limpiar_editor, 
                               accelerator="Ctrl+L")
        menu_editar.add_separator()
        menu_editar.add_command(label="Buscar", command=self.focus_busqueda, 
                               accelerator="Ctrl+F")
        
        # Menú Ver (Temas)
        menu_ver = tk.Menu(menubar, tearoff=0, bg=self.colores['panel'], 
                         fg=self.colores['texto'],
                         activebackground=self.colores['boton'],
                         activeforeground=self.colores['texto'])
        menubar.add_cascade(label="Ver", menu=menu_ver)
        
        # Submenú de Temas
        menu_temas = tk.Menu(menu_ver, tearoff=0, bg=self.colores['panel'], 
                           fg=self.colores['texto'],
                           activebackground=self.colores['boton'],
                           activeforeground=self.colores['texto'])
        menu_ver.add_cascade(label="Tema", menu=menu_temas)
        
        # Variable para los radio buttons
        self.tema_var_menu = tk.StringVar(value=self.tema_actual)
        
        for tema in self.TEMAS.keys():
            menu_temas.add_radiobutton(
                label=tema,
                variable=self.tema_var_menu,
                value=tema,
                command=lambda t=tema: self.cambiar_tema(t)
            )
        
        # Menú Configuración
        menu_config = tk.Menu(menubar, tearoff=0, bg=self.colores['panel'], 
                            fg=self.colores['texto'],
                            activebackground=self.colores['boton'],
                            activeforeground=self.colores['texto'])
        menubar.add_cascade(label="Configuración", menu=menu_config)
        menu_config.add_command(label="Abrir Configuración", command=self.abrir_configuracion)
        
        # Atajos de teclado
        self.root.bind('<Control-n>', lambda e: self.nueva_nota())
        self.root.bind('<Control-s>', lambda e: self.guardar_nota())
        self.root.bind('<Control-d>', lambda e: self.eliminar_nota())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-l>', lambda e: self.limpiar_editor())
        self.root.bind('<Control-f>', lambda e: self.focus_busqueda())
    
    def focus_busqueda(self):
        """Enfoca el campo de búsqueda"""
        if hasattr(self, 'busqueda_entry'):
            self.busqueda_entry.focus()
    
    def cambiar_tema(self, tema):
        """Cambia el tema de la aplicación"""
        if tema in self.TEMAS:
            self.tema_actual = tema
            self.colores = self.TEMAS[tema].copy()
            self.guardar_configuracion()
            self.aplicar_tema()
            messagebox.showinfo("Tema cambiado", f"Tema cambiado a: {tema}")
    
    def aplicar_tema(self):
        """Aplica el tema actual a todos los widgets"""
        # Recrear la interfaz con el nuevo tema
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.configure(bg=self.colores['fondo'])
        self.crear_menu()
        self.crear_interfaz()
        self.actualizar_lista()
        if self.nota_actual is not None:
            self.cargar_nota_en_editor()
        
        # Actualizar variable del menú
        if hasattr(self, 'tema_var_menu'):
            self.tema_var_menu.set(self.tema_actual)
    
    def abrir_configuracion(self):
        """Abre la ventana de configuración"""
        ventana_config = tk.Toplevel(self.root)
        ventana_config.title("Configuración")
        ventana_config.geometry("400x300")
        ventana_config.configure(bg=self.colores['panel'])
        ventana_config.transient(self.root)
        ventana_config.grab_set()
        
        # Centrar ventana
        ventana_config.update_idletasks()
        x = (ventana_config.winfo_screenwidth() // 2) - (ventana_config.winfo_width() // 2)
        y = (ventana_config.winfo_screenheight() // 2) - (ventana_config.winfo_height() // 2)
        ventana_config.geometry(f"+{x}+{y}")
        
        # Frame principal
        frame = tk.Frame(ventana_config, bg=self.colores['panel'], padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(frame, text="⚙️ Configuración", 
                         bg=self.colores['panel'], fg=self.colores['accento'],
                         font=('Arial', 16, 'bold'))
        titulo.pack(pady=(0, 20))
        
        # Selección de tema
        tema_label = tk.Label(frame, text="Tema:", 
                             bg=self.colores['panel'], fg=self.colores['texto'],
                             font=('Arial', 11, 'bold'))
        tema_label.pack(anchor=tk.W, pady=(0, 10))
        
        tema_var = tk.StringVar(value=self.tema_actual)
        for tema in self.TEMAS.keys():
            rb = tk.Radiobutton(frame, text=tema, variable=tema_var, value=tema,
                              bg=self.colores['panel'], fg=self.colores['texto'],
                              selectcolor=self.colores['boton'],
                              activebackground=self.colores['panel'],
                              activeforeground=self.colores['texto'],
                              font=('Arial', 10))
            rb.pack(anchor=tk.W, padx=20)
        
        # Botones
        btn_frame = tk.Frame(frame, bg=self.colores['panel'])
        btn_frame.pack(pady=(20, 0))
        
        def aplicar_cambio():
            if tema_var.get() != self.tema_actual:
                self.cambiar_tema(tema_var.get())
            ventana_config.destroy()
        
        btn_aplicar = tk.Button(btn_frame, text="Aplicar", command=aplicar_cambio,
                               bg=self.colores['exito'], fg=self.colores['texto'],
                               font=('Arial', 10, 'bold'), relief=tk.FLAT, bd=0,
                               padx=20, pady=5, cursor='hand2')
        btn_aplicar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = tk.Button(btn_frame, text="Cancelar", command=ventana_config.destroy,
                                 bg=self.colores['texto_secundario'], fg=self.colores['texto'],
                                 font=('Arial', 10, 'bold'), relief=tk.FLAT, bd=0,
                                 padx=20, pady=5, cursor='hand2')
        btn_cancelar.pack(side=tk.LEFT, padx=5)
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica de la aplicación"""
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colores['fondo'], padx=10, pady=10)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # === Panel izquierdo: Lista de notas ===
        left_frame = tk.LabelFrame(main_frame, text="📝 Mis Notas", 
                                  bg=self.colores['panel'], fg=self.colores['accento'],
                                  font=('Arial', 11, 'bold'), padx=10, pady=10)
        left_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        
        # Barra de búsqueda
        search_frame = tk.Frame(left_frame, bg=self.colores['panel'])
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        search_label = tk.Label(search_frame, text="🔍 Buscar:", 
                               bg=self.colores['panel'], fg=self.colores['texto'],
                               font=('Arial', 10))
        search_label.grid(row=0, column=0, padx=(0, 5))
        self.busqueda_var = tk.StringVar()
        self.busqueda_var.trace('w', lambda *args: self.buscar_notas())
        self.busqueda_entry = tk.Entry(search_frame, textvariable=self.busqueda_var, 
                                       width=20, bg=self.colores['entrada'], 
                                       fg=self.colores['texto'],
                                       insertbackground=self.colores['texto'],
                                       font=('Arial', 10),
                                       relief=tk.FLAT, bd=2)
        self.busqueda_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Lista de notas con scrollbar
        list_frame = tk.Frame(left_frame, bg=self.colores['panel'])
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        scrollbar = tk.Scrollbar(list_frame, bg=self.colores['panel'],
                                activebackground=self.colores['boton'],
                                troughcolor=self.colores['entrada'])
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.lista_notas = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, 
                                      font=('Arial', 10), selectmode=tk.SINGLE,
                                      bg=self.colores['lista'], fg=self.colores['texto'],
                                      selectbackground=self.colores['lista_seleccion'],
                                      selectforeground=self.colores['texto'],
                                      relief=tk.FLAT, bd=2,
                                      highlightthickness=0)
        self.lista_notas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.lista_notas.bind('<<ListboxSelect>>', self.seleccionar_nota)
        
        scrollbar.config(command=self.lista_notas.yview)
        
        # Botones del panel izquierdo
        btn_frame = tk.Frame(left_frame, bg=self.colores['panel'])
        btn_frame.grid(row=2, column=0, pady=(10, 0))
        
        btn_nueva = tk.Button(btn_frame, text="✨ Nueva Nota", command=self.nueva_nota, 
                             width=18, bg=self.colores['boton'], fg=self.colores['texto'],
                             font=('Arial', 9, 'bold'), relief=tk.FLAT, bd=0,
                             activebackground=self.colores['boton_hover'],
                             activeforeground=self.colores['texto'],
                             cursor='hand2', padx=5, pady=5)
        btn_nueva.grid(row=0, column=0, padx=2)
        
        btn_eliminar = tk.Button(btn_frame, text="🗑️ Eliminar", command=self.eliminar_nota, 
                                width=18, bg=self.colores['boton_peligro'], 
                                fg=self.colores['texto'],
                                font=('Arial', 9, 'bold'), relief=tk.FLAT, bd=0,
                                activebackground='#ff6666',
                                activeforeground=self.colores['texto'],
                                cursor='hand2', padx=5, pady=5)
        btn_eliminar.grid(row=0, column=1, padx=2)
        
        # === Panel derecho: Editor de notas ===
        right_frame = tk.LabelFrame(main_frame, text="✏️ Editor", 
                                   bg=self.colores['panel'], fg=self.colores['accento'],
                                   font=('Arial', 11, 'bold'), padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(4, weight=1)
        
        # Título de la nota
        titulo_label = tk.Label(right_frame, text="📌 Título:", 
                               bg=self.colores['panel'], fg=self.colores['texto'],
                               font=('Arial', 10, 'bold'))
        titulo_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.titulo_var = tk.StringVar()
        self.titulo_entry = tk.Entry(right_frame, textvariable=self.titulo_var, 
                                     font=('Arial', 12, 'bold'),
                                     bg=self.colores['entrada'], fg=self.colores['texto'],
                                     insertbackground=self.colores['texto'],
                                     relief=tk.FLAT, bd=2)
        self.titulo_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Categoría
        cat_frame = tk.Frame(right_frame, bg=self.colores['panel'])
        cat_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        cat_frame.columnconfigure(1, weight=1)
        
        cat_label = tk.Label(cat_frame, text="🏷️ Categoría:", 
                            bg=self.colores['panel'], fg=self.colores['texto'],
                            font=('Arial', 10, 'bold'))
        cat_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.categoria_var = tk.StringVar()
        categoria_combo = ttk.Combobox(cat_frame, textvariable=self.categoria_var, 
                                      values=["Personal", "Trabajo", "Estudio", "Recordatorios", "Otros"],
                                      state="readonly", width=15)
        categoria_combo.grid(row=0, column=1, sticky=tk.W)
        categoria_combo.set("Personal")
        
        # Configurar estilo del combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground=self.colores['entrada'],
                       background=self.colores['entrada'], foreground=self.colores['texto'],
                       borderwidth=0)
        
        # Contenido de la nota
        contenido_label = tk.Label(right_frame, text="📄 Contenido:", 
                                  bg=self.colores['panel'], fg=self.colores['texto'],
                                  font=('Arial', 10, 'bold'))
        contenido_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.contenido_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, 
                                                        font=('Arial', 11), 
                                                        height=15, width=50,
                                                        bg=self.colores['entrada'], 
                                                        fg=self.colores['texto'],
                                                        insertbackground=self.colores['texto'],
                                                        relief=tk.FLAT, bd=2)
        self.contenido_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.rowconfigure(4, weight=1)
        
        # Información de fecha
        self.fecha_label = tk.Label(right_frame, text="", font=('Arial', 8), 
                                   bg=self.colores['panel'], fg=self.colores['texto_secundario'])
        self.fecha_label.grid(row=5, column=0, sticky=tk.W, pady=(5, 0))
        
        # Botones de acción
        action_frame = tk.Frame(right_frame, bg=self.colores['panel'])
        action_frame.grid(row=6, column=0, pady=(10, 0))
        
        btn_guardar = tk.Button(action_frame, text="💾 Guardar", command=self.guardar_nota, 
                               width=18, bg=self.colores['exito'], fg=self.colores['texto'],
                               font=('Arial', 9, 'bold'), relief=tk.FLAT, bd=0,
                               activebackground='#5cbf60',
                               activeforeground=self.colores['texto'],
                               cursor='hand2', padx=5, pady=5)
        btn_guardar.grid(row=0, column=0, padx=5)
        
        btn_limpiar = tk.Button(action_frame, text="🧹 Limpiar", command=self.limpiar_editor, 
                               width=18, bg=self.colores['advertencia'], fg=self.colores['texto'],
                               font=('Arial', 9, 'bold'), relief=tk.FLAT, bd=0,
                               activebackground='#ffa726',
                               activeforeground=self.colores['texto'],
                               cursor='hand2', padx=5, pady=5)
        btn_limpiar.grid(row=0, column=1, padx=5)
        
        # === Panel inferior: Estadísticas ===
        stats_frame = tk.LabelFrame(main_frame, text="📊 Estadísticas", 
                                    bg=self.colores['panel'], fg=self.colores['accento'],
                                    font=('Arial', 10, 'bold'), padx=10, pady=10)
        stats_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 0))
        
        self.stats_label = tk.Label(stats_frame, text="", font=('Arial', 9),
                                   bg=self.colores['panel'], fg=self.colores['texto'])
        self.stats_label.grid(row=0, column=0, sticky=tk.W)
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()
    
    def cargar_notas(self):
        """Carga las notas desde el archivo JSON"""
        if self.archivo_datos.exists():
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    self.notas = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar notas: {e}")
                self.notas = []
        else:
            self.notas = []
    
    def guardar_notas(self):
        """Guarda las notas en el archivo JSON"""
        try:
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(self.notas, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar notas: {e}")
            return False
    
    def actualizar_lista(self):
        """Actualiza la lista de notas en el panel izquierdo"""
        self.lista_notas.delete(0, tk.END)
        
        busqueda = self.busqueda_var.get().lower()
        
        for nota in self.notas:
            titulo = nota.get('titulo', 'Sin título')
            if busqueda in titulo.lower() or busqueda in nota.get('contenido', '').lower():
                # Mostrar título con fecha
                fecha = nota.get('fecha_creacion', '')
                if fecha:
                    try:
                        fecha_obj = datetime.fromisoformat(fecha)
                        fecha_str = fecha_obj.strftime('%d/%m/%Y')
                    except:
                        fecha_str = fecha
                else:
                    fecha_str = 'Sin fecha'
                
                categoria = nota.get('categoria', 'Sin categoría')
                self.lista_notas.insert(tk.END, f"{titulo} [{categoria}] - {fecha_str}")
    
    def buscar_notas(self):
        """Filtra las notas según la búsqueda"""
        self.actualizar_lista()
    
    def seleccionar_nota(self, event):
        """Carga la nota seleccionada en el editor"""
        seleccion = self.lista_notas.curselection()
        if seleccion:
            indice = seleccion[0]
            # Encontrar la nota real considerando el filtro
            busqueda = self.busqueda_var.get().lower()
            notas_filtradas = [n for n in self.notas 
                             if busqueda in n.get('titulo', '').lower() or 
                                busqueda in n.get('contenido', '').lower()]
            
            if indice < len(notas_filtradas):
                self.nota_actual = self.notas.index(notas_filtradas[indice])
                self.cargar_nota_en_editor()
    
    def cargar_nota_en_editor(self):
        """Carga la nota actual en el editor"""
        if self.nota_actual is not None and self.nota_actual < len(self.notas):
            nota = self.notas[self.nota_actual]
            self.titulo_var.set(nota.get('titulo', ''))
            self.contenido_text.delete('1.0', tk.END)
            self.contenido_text.insert('1.0', nota.get('contenido', ''))
            self.categoria_var.set(nota.get('categoria', 'Personal'))
            
            # Mostrar fecha
            fecha_creacion = nota.get('fecha_creacion', '')
            fecha_modificacion = nota.get('fecha_modificacion', '')
            
            info_fecha = f"Creada: {fecha_creacion}"
            if fecha_modificacion and fecha_modificacion != fecha_creacion:
                info_fecha += f" | Modificada: {fecha_modificacion}"
            
            self.fecha_label.config(text=info_fecha)
    
    def nueva_nota(self):
        """Crea una nueva nota"""
        self.limpiar_editor()
        self.nota_actual = None
        self.busqueda_var.set("")
        self.actualizar_lista()
    
    def limpiar_editor(self):
        """Limpia el editor"""
        self.titulo_var.set("")
        self.contenido_text.delete('1.0', tk.END)
        self.categoria_var.set("Personal")
        self.fecha_label.config(text="")
        self.nota_actual = None
    
    def guardar_nota(self):
        """Guarda la nota actual"""
        titulo = self.titulo_var.get().strip()
        contenido = self.contenido_text.get('1.0', tk.END).strip()
        categoria = self.categoria_var.get()
        
        if not titulo:
            messagebox.showwarning("Advertencia", "Por favor ingresa un título para la nota.")
            return
        
        fecha_actual = datetime.now().isoformat()
        
        if self.nota_actual is not None and self.nota_actual < len(self.notas):
            # Actualizar nota existente
            self.notas[self.nota_actual]['titulo'] = titulo
            self.notas[self.nota_actual]['contenido'] = contenido
            self.notas[self.nota_actual]['categoria'] = categoria
            self.notas[self.nota_actual]['fecha_modificacion'] = fecha_actual
            mensaje = "Nota actualizada correctamente."
        else:
            # Crear nueva nota
            nueva_nota = {
                'titulo': titulo,
                'contenido': contenido,
                'categoria': categoria,
                'fecha_creacion': fecha_actual,
                'fecha_modificacion': fecha_actual
            }
            self.notas.append(nueva_nota)
            self.nota_actual = len(self.notas) - 1
            mensaje = "Nota guardada correctamente."
        
        if self.guardar_notas():
            messagebox.showinfo("Éxito", mensaje)
            self.actualizar_lista()
            self.cargar_nota_en_editor()
            self.actualizar_estadisticas()
    
    def eliminar_nota(self):
        """Elimina la nota seleccionada"""
        if self.nota_actual is None:
            messagebox.showwarning("Advertencia", "Por favor selecciona una nota para eliminar.")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar esta nota?"):
            del self.notas[self.nota_actual]
            if self.guardar_notas():
                messagebox.showinfo("Éxito", "Nota eliminada correctamente.")
                self.limpiar_editor()
                self.actualizar_lista()
                self.actualizar_estadisticas()
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas mostradas"""
        total = len(self.notas)
        categorias = {}
        for nota in self.notas:
            cat = nota.get('categoria', 'Sin categoría')
            categorias[cat] = categorias.get(cat, 0) + 1
        
        stats_text = f"Total de notas: {total}"
        if categorias:
            stats_text += " | "
            stats_text += " | ".join([f"{cat}: {count}" for cat, count in categorias.items()])
        
        self.stats_label.config(text=stats_text)


def main():
    try:
        root = tk.Tk()
        # Asegurar que la ventana esté en primer plano
        root.lift()
        root.attributes('-topmost', True)
        root.after_idle(root.attributes, '-topmost', False)
        root.focus_force()
        
        app = BlockDeNotas(root)
        print("Block de Notas iniciado correctamente")
        print("Si no ves la ventana, verifica que no esté minimizada o detrás de otras ventanas")
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")


if __name__ == "__main__":
    main()

