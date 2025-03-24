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
            empleado.seguridad_social = request.form['seguridad_social']
            empleado.telefono = request.form['telefono']
            empleado.email = request.form['email']
            empleado.sabados = 'sabados' in request.form  # Check si el checkbox 'sabados' está seleccionado
            empleado.activo = 'activo' in request.form  # Check si el checkbox 'activo' está seleccionado
            # Convertir la cadena de fecha a un objeto datetime.date
            fecha_alta_str = request.form['fecha_alta']
            fecha_alta = datetime.strptime(fecha_alta_str, '%Y-%m-%d').date()
            fecha_baja_str = request.form['fecha_baja']
            fecha_baja = datetime.strptime(fecha_baja_str, '%Y-%m-%d').date()

            # Si es un POST, actualizamos el empleado con los datos del formulario
            empleado.dni = request.form['dni']
            empleado.fecha_alta = fecha_alta  # Asignar el objeto date
            empleado.fecha_baja = fecha_baja

            # Guardar los cambios en la base de datos
            db.session.commit()
            return redirect(url_for('empleados'))  # Redirigir de nuevo a la lista de empleados

        return render_template('editar_empleado.html', empleado=empleado)
