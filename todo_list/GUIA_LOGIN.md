# 🔐 Guía de Prueba del Sistema de Login

## 🚀 Pasos para Probar

### 1. Acceder a la Aplicación

Abre tu navegador (Edge) y ve a:
```
http://127.0.0.1:5000
```

**Resultado esperado:** Deberías ver la página de **Login** (todas las rutas están protegidas ahora).

---

### 2. Crear una Nueva Cuenta

1. En la página de login, haz clic en **"Registrarse aquí"** (enlace al final del formulario)
2. Completa el formulario de registro:
   - **Nombre de Usuario:** (mínimo 3 caracteres) - Ejemplo: `juan`
   - **Email:** (opcional) - Ejemplo: `juan@email.com`
   - **Contraseña:** (mínimo 4 caracteres) - Ejemplo: `1234`
   - **Confirmar Contraseña:** Debe coincidir con la contraseña
3. Haz clic en **"Crear Cuenta"**

**Resultado esperado:** 
- Mensaje verde: "Usuario registrado exitosamente. Ahora puedes iniciar sesión"
- Redirección automática a la página de login

---

### 3. Iniciar Sesión

1. En la página de login, ingresa tus credenciales:
   - **Nombre de Usuario:** El que acabas de crear
   - **Contraseña:** La contraseña que usaste
2. Haz clic en **"Iniciar Sesión"**

**Resultado esperado:**
- Mensaje verde: "¡Bienvenido, [tu_usuario]!"
- Redirección a la página principal con tus tareas
- En la barra de navegación verás: **"👤 [tu_usuario]"** y **"Cerrar Sesión"**

---

### 4. Probar las Funcionalidades Protegidas

Ahora que estás logueado, puedes:
- ✅ Ver la lista de tareas
- ✅ Agregar nuevas tareas
- ✅ Completar tareas
- ✅ Eliminar tareas
- ✅ Buscar tareas
- ✅ Ver estadísticas

---

### 5. Probar la Protección de Rutas

1. Haz clic en **"Cerrar Sesión"** en la barra de navegación
2. Intenta acceder directamente a: `http://127.0.0.1:5000`

**Resultado esperado:**
- Mensaje: "Por favor, inicia sesión para acceder a esta página"
- Redirección automática a la página de login
- **No puedes acceder a ninguna funcionalidad sin estar logueado**

---

### 6. Probar Validaciones

#### En el Registro:
- Intenta crear un usuario con menos de 3 caracteres → Error
- Intenta crear una contraseña con menos de 4 caracteres → Error
- Intenta crear un usuario que ya existe → Error: "El nombre de usuario ya existe"
- Intenta que las contraseñas no coincidan → Error: "Las contraseñas no coinciden"

#### En el Login:
- Intenta iniciar sesión con usuario incorrecto → Error: "Usuario o contraseña incorrectos"
- Intenta iniciar sesión con contraseña incorrecta → Error: "Usuario o contraseña incorrectos"
- Deja campos vacíos → Error de validación del navegador

---

## 📁 Archivos Creados

Después de crear tu primera cuenta, se creará el archivo:
- `usuarios.json` - Contiene todos los usuarios registrados (con contraseñas hasheadas)

---

## 🔒 Seguridad

- ✅ Las contraseñas se guardan con hash (nunca en texto plano)
- ✅ Las rutas están protegidas con el decorador `@login_required`
- ✅ Las sesiones son seguras usando Flask sessions
- ✅ Validación de datos en frontend y backend

---

## 🎯 Pruebas Adicionales

### Crear Múltiples Usuarios
1. Cierra sesión
2. Crea otra cuenta con diferente nombre de usuario
3. Inicia sesión con la nueva cuenta
4. Verás que cada usuario tiene su propia sesión

### Persistencia de Sesión
1. Inicia sesión
2. Cierra el navegador completamente
3. Abre el navegador de nuevo y ve a `http://127.0.0.1:5000`
4. **Nota:** La sesión se pierde al cerrar el navegador (comportamiento normal en desarrollo)

---

## ✅ Checklist de Pruebas

- [ ] Ver página de login al acceder sin estar logueado
- [ ] Crear una cuenta nueva exitosamente
- [ ] Iniciar sesión con credenciales correctas
- [ ] Ver nombre de usuario en la barra de navegación
- [ ] Acceder a todas las funcionalidades estando logueado
- [ ] Cerrar sesión correctamente
- [ ] Verificar que no se puede acceder sin login
- [ ] Probar validaciones de registro (usuario corto, contraseña corta, etc.)
- [ ] Probar validaciones de login (credenciales incorrectas)

---

¡Disfruta probando el sistema de login! 🎉


