from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash

from models import db, Empleado
from datetime import datetime

app = Flask(__name__)

def ruta_crear_empleado(app):
    @app.route('/crear_empleado', methods=['GET', 'POST'])
    def crear_empleado():
        if request.method == 'POST':
            # Obtener datos del formulario
            nombre = ""
            usuario = request.form['username']
            password = request.form['password']
            cargo = request.form['cargo']
            alias = request.form['alias']
            nombre_completo = request.form['nombre_completo']
            dni = request.form['dni']
            seguridad_social = request.form['seguridad_social']
            sede = request.form['sede']
            telefono = request.form['telefono']
            email = request.form['email']

            # Convertir las fechas en objetos datetime
            fecha_alta_str = request.form['fecha_alta']
            fecha_baja_str = request.form.get('fecha_baja', '')  # Puede ser una cadena vacía si no se proporciona

            # Convertir las cadenas a objetos datetime (si no están vacías)
            fecha_alta = datetime.strptime(fecha_alta_str, '%Y-%m-%d')

            # Si no se proporciona fecha_baja, asignamos un valor predeterminado (por ejemplo, None o una fecha futura)
            fecha_baja = datetime.strptime(fecha_baja_str, '%Y-%m-%d') if fecha_baja_str else None

            sabados = 'sabados' in request.form


            # Crear un nuevo empleado
            hashed_password = generate_password_hash(password)

            nuevo_empleado = Empleado(
                nombre=nombre,
                usuario=usuario,
                password=hashed_password,  # Aquí sí
                cargo=cargo,
                alias=alias,
                nombre_completo=nombre_completo,
                dni=dni,
                seguridad_social=seguridad_social,
                sede=sede,
                telefono=telefono,
                email=email,
                fecha_alta=fecha_alta,
                fecha_baja=fecha_baja,
                sabados=sabados,
                activo=True
            )


            # Guardar el empleado en la base de datos

            db.session.add(nuevo_empleado)
            db.session.commit()

            return redirect(url_for('empleados'))

        return render_template('crear_empleado.html')

    if __name__ == '__main__':
        app.run(debug=True)
