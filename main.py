from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Empleado, Usuario, Registro  # Suponiendo que tienes un modelo de Usuario
from funciones.crear_empleado import ruta_crear_empleado
from funciones.editar_empleado import ruta_editar_empleado
from funciones.registrar_entrada import ruta_registrar_entrada
from funciones.registrar_salida import ruta_registrar_salida

app = Flask(__name__)

# Configuración de la base de datos
app.config['SECRET_KEY'] = '78587fgrtyth'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para evitar advertencias

# Inicializar la extensión SQLAlchemy y Flask-Login
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # Redirige al login si no está autenticado

ruta_crear_empleado(app)
ruta_editar_empleado(app)
ruta_registrar_entrada(app)
ruta_registrar_salida(app)


# Crear las tablas antes de iniciar la aplicación (manual)
with app.app_context():
    db.create_all()



    def __repr__(self):
        return f"<Usuario {self.username}>"

# Cargar el usuario por su ID (función requerida por Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar que el usuario es 'javier' para pruebas
        if username == "javier" and password == "javier":
            # Si es el usuario "javier", iniciar sesión directamente
            # Aquí puedes realizar el login sin necesidad de buscarlo en la base de datos
            # Esto es solo para pruebas
            user = Usuario.query.filter_by(username='javier').first()  # Obtener el usuario "javier" de la base de datos
            if not user:
                # Si el usuario "javier" no existe, puedes crear uno (por ejemplo, al inicio del desarrollo)
                user = Usuario(username="javier", password=generate_password_hash("javier"))
                db.session.add(user)
                db.session.commit()


            login_user(user)
            return redirect(url_for('index'))  # Redirige a la página principal después del login

        # Buscar al usuario en la base de datos para otros usuarios
        user = Usuario.query.filter_by(username=username).first()

        # Verificar si la contraseña coincide usando el hash almacenado
        if user and password == user.password:
            login_user(user)  # Iniciar sesión del usuario
            return redirect(url_for('movil'))  # Redirige a la página principal después del login
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'error')  # Si las credenciales son incorrectas

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
    # Obtener todos los empleados de la base de datos
    empleados_list = Empleado.query.all()  # Obtiene todos los empleados
    return render_template('empleados.html', empleados=empleados_list)

@app.route('/movil')
@login_required
def movil():
    # Buscar el último registro sin salida para este usuario
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
