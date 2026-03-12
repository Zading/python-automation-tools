"""
Sistema de autenticación para la aplicación de tareas
"""

import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session, redirect, url_for, flash


class AuthManager:
    """Gestor de autenticación de usuarios"""
    
    def __init__(self, archivo_usuarios: str = "usuarios.json"):
        """
        Inicializa el gestor de autenticación
        
        Args:
            archivo_usuarios: Nombre del archivo donde se guardan los usuarios
        """
        self.archivo_usuarios = archivo_usuarios
        self.usuarios = self.cargar_usuarios()
    
    def cargar_usuarios(self) -> dict:
        """
        Carga los usuarios desde el archivo JSON
        
        Returns:
            Diccionario de usuarios
        """
        if os.path.exists(self.archivo_usuarios):
            try:
                with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def guardar_usuarios(self):
        """Guarda los usuarios en el archivo JSON"""
        try:
            with open(self.archivo_usuarios, 'w', encoding='utf-8') as f:
                json.dump(self.usuarios, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error al guardar usuarios: {e}")
    
    def registrar_usuario(self, username: str, password: str, email: str = "") -> tuple:
        """
        Registra un nuevo usuario
        
        Args:
            username: Nombre de usuario
            password: Contraseña (se hasheará)
            email: Email del usuario (opcional)
        
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        username = username.strip().lower()
        
        # Validaciones
        if not username:
            return False, "El nombre de usuario no puede estar vacío"
        
        if not password or len(password) < 4:
            return False, "La contraseña debe tener al menos 4 caracteres"
        
        if username in self.usuarios:
            return False, "El nombre de usuario ya existe"
        
        # Crear usuario
        self.usuarios[username] = {
            "username": username,
            "password_hash": generate_password_hash(password),
            "email": email.strip(),
            "fecha_registro": self._obtener_fecha_actual()
        }
        
        self.guardar_usuarios()
        return True, "Usuario registrado exitosamente"
    
    def verificar_login(self, username: str, password: str) -> tuple:
        """
        Verifica las credenciales de un usuario
        
        Args:
            username: Nombre de usuario
            password: Contraseña
        
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        username = username.strip().lower()
        
        if not username or not password:
            return False, "Usuario y contraseña son requeridos"
        
        if username not in self.usuarios:
            return False, "Usuario o contraseña incorrectos"
        
        usuario = self.usuarios[username]
        
        if check_password_hash(usuario['password_hash'], password):
            return True, "Login exitoso"
        else:
            return False, "Usuario o contraseña incorrectos"
    
    def obtener_usuario(self, username: str) -> dict:
        """
        Obtiene la información de un usuario (sin la contraseña)
        
        Args:
            username: Nombre de usuario
        
        Returns:
            Diccionario con información del usuario o None
        """
        username = username.strip().lower()
        if username in self.usuarios:
            usuario = self.usuarios[username].copy()
            usuario.pop('password_hash', None)  # No devolver la contraseña
            return usuario
        return None
    
    def _obtener_fecha_actual(self) -> str:
        """Obtiene la fecha actual en formato string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def login_required(f):
    """
    Decorador para proteger rutas que requieren autenticación
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Por favor, inicia sesión para acceder a esta página', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


