from flask import render_template, request, redirect, url_for
from models import db, Empleado
from datetime import datetime

def ruta_editar_empleado(app):
    @app.route('/editar_empleado/<int:id>', methods=['GET', 'POST'])
    def editar_empleado(id):
        empleado = Empleado.query.get(id)  # Obtener el empleado específico por su ID
        if not empleado:
            return redirect(url_for('empleados'))  # Si no existe, redirigir a la lista de empleados

        if request.method == 'POST':
            # Si es un POST, actualizamos el empleado con los datos del formulario
            empleado.nombre_completo = request.form['nombre_completo']
            empleado.alias = request.form['alias']
            empleado.cargo = request.form['cargo']
            empleado.sede = request.form['sede']
            empleado.dni = request.form['dni']
            empleado.email = request.form['email']

            # Guardar los cambios en la base de datos
            db.session.commit()
            return redirect(url_for('empleados'))  # Redirigir de nuevo a la lista de empleados

        return render_template('editar_empleado.html', empleado=empleado)
