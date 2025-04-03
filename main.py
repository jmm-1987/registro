from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from models import db, Empleado, Registro  # Usamos Empleado directamente
from funciones.crear_empleado import ruta_crear_empleado
from funciones.editar_empleado import ruta_editar_empleado
from funciones.registrar_entrada import ruta_registrar_entrada
from funciones.registrar_salida import ruta_registrar_salida
from sqlalchemy.orm import joinedload

app = Flask(__name__)

# Configuración de la base de datos
app.config['SECRET_KEY'] = '78587fgrtyth'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para evitar advertencias

# Inicializar la extensión SQLAlchemy y Flask-Login
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirige al login si no está autenticado

# Rutas relacionadas con empleados
ruta_crear_empleado(app)
ruta_editar_empleado(app)
ruta_registrar_entrada(app)
ruta_registrar_salida(app)

# Crear las tablas antes de iniciar la aplicación (manual)
with app.app_context():
    db.create_all()

# Cargar el usuario por su ID (función requerida por Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return Empleado.query.get(int(user_id))


# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        empleado = Empleado.query.filter_by(usuario=username).first()

        if empleado:
            if empleado.check_password(password):
                login_user(empleado)

                # 👇 Lógica para redirigir según el usuario
                if empleado.usuario == "superuser":
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('movil'))

            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash('Nombre de usuario no encontrado', 'error')

    return render_template('login.html')



# Ruta para cerrar sesión
@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/empleados')
@login_required
def empleados():
    empleados_list = Empleado.query.all()  # Obtiene todos los empleados
    return render_template('empleados.html', empleados=empleados_list)

@app.route('/consultar_horarios')
@login_required
def consultar_horarios():
    # Obtener los filtros desde la URL
    empleado_id = request.args.get('empleado_id', type=int)
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')

    # Iniciar la consulta base
    query = Registro.query.options(joinedload(Registro.empleado))

    # Aplicar filtros dinámicamente
    if empleado_id:
        query = query.filter(Registro.empleado_id == empleado_id)

    if fecha_desde:
        fecha_desde_dt = datetime.strptime(fecha_desde, '%Y-%m-%d')
        query = query.filter(Registro.fecha_hora_entrada >= fecha_desde_dt)

    if fecha_hasta:
        fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d')
        # Ajustar al final del día
        fecha_hasta_dt = fecha_hasta_dt.replace(hour=23, minute=59, second=59)
        query = query.filter(Registro.fecha_hora_entrada <= fecha_hasta_dt)

    registros_filtrados = query.order_by(Registro.fecha_hora_entrada.desc()).all()

    empleados = Empleado.query.all()

    return render_template('consultar_horarios.html',
        registros=registros_filtrados,
        empleados=empleados,
        filtro_empleado_id=empleado_id,
        filtro_fecha_desde=fecha_desde,
        filtro_fecha_hasta=fecha_hasta
    )
@app.route('/movil')
@login_required
def movil():
    entrada = Registro.query.filter_by(
        empleado_id=current_user.id,
        fecha_hora_salida=None
    ).order_by(Registro.fecha_hora_entrada.desc()).first()

    hora_entrada = entrada.fecha_hora_entrada.isoformat() if entrada else None
    return render_template("movil.html", hora_entrada=hora_entrada)

@app.route('/consultar_registro')
def consultar_registro():
    return 'Página de Consultar Registro'

if __name__ == '__main__':
    app.run(debug=True)
