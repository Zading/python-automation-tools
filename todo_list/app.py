"""
Aplicación Web de Lista de Tareas usando Flask
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from todo_list import TodoList
from auth import AuthManager, login_required
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para sesiones

# Instancias globales
todo = TodoList("tareas.json")
auth = AuthManager("usuarios.json")


@app.route('/')
@login_required
def index():
    """Página principal - Lista todas las tareas"""
    mostrar_completadas = request.args.get('mostrar_completadas', 'true').lower() == 'true'
    filtro_prioridad = request.args.get('prioridad', None)
    
    # Obtener todas las tareas
    tareas = todo.tareas.copy()
    
    # Filtrar por prioridad si se especifica
    if filtro_prioridad:
        tareas = [t for t in tareas if t['prioridad'] == filtro_prioridad]
    
    # Filtrar completadas si no se quieren mostrar
    if not mostrar_completadas:
        tareas = [t for t in tareas if not t['completada']]
    
    # Ordenar: primero pendientes, luego completadas; dentro de cada grupo por prioridad
    orden_prioridad = {"alta": 1, "media": 2, "baja": 3}
    tareas.sort(key=lambda x: (x['completada'], orden_prioridad.get(x['prioridad'], 3)))
    
    # Calcular estadísticas
    total = len(todo.tareas)
    completadas = sum(1 for t in todo.tareas if t['completada'])
    pendientes = total - completadas
    porcentaje = (completadas / total * 100) if total > 0 else 0
    
    return render_template('index.html', 
                         tareas=tareas,
                         total=total,
                         completadas=completadas,
                         pendientes=pendientes,
                         porcentaje=round(porcentaje, 1),
                         mostrar_completadas=mostrar_completadas,
                         filtro_prioridad=filtro_prioridad)


@app.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar_tarea():
    """Agregar una nueva tarea"""
    if request.method == 'POST':
        try:
            descripcion = request.form.get('descripcion', '').strip()
            prioridad = request.form.get('prioridad', 'media').strip()
            
            if not descripcion:
                flash('❌ La descripción no puede estar vacía', 'error')
                return redirect(url_for('agregar_tarea'))
            
            # Validar prioridad
            if prioridad not in ["alta", "media", "baja"]:
                prioridad = "media"
            
            resultado = todo.agregar_tarea(descripcion, prioridad)
            if resultado:
                flash('✅ Tarea agregada correctamente', 'success')
            else:
                flash('❌ Error al agregar la tarea', 'error')
            
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'❌ Error inesperado: {str(e)}', 'error')
            app.logger.error(f'Error al agregar tarea: {str(e)}', exc_info=True)
            return redirect(url_for('agregar_tarea'))
    
    return render_template('agregar.html')


@app.route('/completar/<int:id_tarea>', methods=['POST'])
@login_required
def completar_tarea(id_tarea):
    """Completar una tarea"""
    if todo.completar_tarea(id_tarea):
        flash('✅ Tarea completada', 'success')
    else:
        flash('❌ Error al completar la tarea', 'error')
    
    return redirect(url_for('index'))


@app.route('/eliminar/<int:id_tarea>', methods=['POST'])
@login_required
def eliminar_tarea(id_tarea):
    """Eliminar una tarea"""
    if todo.eliminar_tarea(id_tarea):
        flash('🗑️ Tarea eliminada', 'success')
    else:
        flash('❌ Error al eliminar la tarea', 'error')
    
    return redirect(url_for('index'))


@app.route('/buscar', methods=['GET', 'POST'])
@login_required
def buscar_tareas():
    """Buscar tareas"""
    if request.method == 'POST':
        termino = request.form.get('termino', '').strip()
        if not termino:
            flash('❌ El término de búsqueda no puede estar vacío', 'error')
            return redirect(url_for('index'))
        
        termino_lower = termino.lower()
        tareas_encontradas = [
            t for t in todo.tareas
            if termino_lower in t['descripcion'].lower()
        ]
        
        return render_template('buscar.html', 
                             tareas=tareas_encontradas,
                             termino=termino)
    
    return redirect(url_for('index'))


@app.route('/estadisticas')
@login_required
def estadisticas():
    """Mostrar estadísticas"""
    total = len(todo.tareas)
    completadas = sum(1 for t in todo.tareas if t['completada'])
    pendientes = total - completadas
    porcentaje = (completadas / total * 100) if total > 0 else 0
    
    prioridades = {"alta": 0, "media": 0, "baja": 0}
    for tarea in todo.tareas:
        if not tarea['completada']:
            prioridades[tarea['prioridad']] += 1
    
    return render_template('estadisticas.html',
                         total=total,
                         completadas=completadas,
                         pendientes=pendientes,
                         porcentaje=round(porcentaje, 1),
                         prioridades=prioridades)


@app.route('/api/tareas', methods=['GET'])
@login_required
def api_tareas():
    """API endpoint para obtener todas las tareas en JSON"""
    return jsonify(todo.tareas)


# ==================== RUTAS DE AUTENTICACIÓN ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    # Si ya está logueado, redirigir al inicio
    if 'username' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        exito, mensaje = auth.verificar_login(username, password)
        
        if exito:
            session['username'] = username
            flash(f'¡Bienvenido, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash(mensaje, 'error')
    
    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de nuevos usuarios"""
    # Si ya está logueado, redirigir al inicio
    if 'username' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirmar_password = request.form.get('confirmar_password', '')
        email = request.form.get('email', '').strip()
        
        # Validar que las contraseñas coincidan
        if password != confirmar_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('registro.html')
        
        exito, mensaje = auth.registrar_usuario(username, password, email)
        
        if exito:
            flash(mensaje + '. Ahora puedes iniciar sesión', 'success')
            return redirect(url_for('login'))
        else:
            flash(mensaje, 'error')
    
    return render_template('registro.html')


@app.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    username = session.get('username', 'Usuario')
    session.clear()
    flash(f'¡Hasta pronto, {username}!', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

