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
    # No necesitamos cargar un usuario real para el acceso de "javier"
    return None  # No devolvemos ningún usuario real, ya que no usamos la base de datos

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Login especial para "javier"
        if username == "javier" and password == "javier":
            class FakeUser:
                id = 1
                username = "javier"
                is_authenticated = True
                is_active = True
                is_anonymous = False

                def get_id(self):
                    return str(self.id)

            login_user(FakeUser())
            return redirect(url_for('index'))

        # Login normal con base de datos
        empleado = Empleado.query.filter_by(usuario=username).first()

        if empleado:
            if empleado.check_password(password):  # ← CORRECTO
                login_user(empleado)
                return redirect(url_for('index'))
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
#@login_required
def index():
    return render_template('index.html')

@app.route('/empleados')
#@login_required
def empleados():
    empleados_list = Empleado.query.all()  # Obtiene todos los empleados
    return render_template('empleados.html', empleados=empleados_list)

@app.route('/consultar_horarios')
@login_required
def consultar_horarios():
    empleados_list = Empleado.query.all()
    registros = Registro.query.options(joinedload(Registro.empleado)).all()
    return render_template('consultar_horarios.html', empleados=empleados_list, registros=registros)

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
