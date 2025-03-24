from flask import Flask, render_template
from models import db, Empleado, Registro
from funciones.crear_empleado import ruta_crear_empleado
from funciones.editar_empleado import ruta_editar_empleado



app = Flask(__name__)


# Configuración de la base de datos
app.config['SECRET_KEY'] = '78587fgrtyth'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para evitar advertencias

# Inicializar la extensión SQLAlchemy
db.init_app(app)

ruta_crear_empleado(app)
ruta_editar_empleado(app)

# Crear las tablas antes de iniciar la aplicación (manual)
with app.app_context():
    db.create_all()  # Crea las tablas en la base de datos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/empleados')
def empleados():
    # Obtener todos los empleados de la base de datos
    empleados_list = Empleado.query.all()  # Obtiene todos los empleados
    return render_template('empleados.html', empleados=empleados_list)


@app.route('/consultar_registro')
def consultar_registro():
    return 'Página de Consultar Registro'

if __name__ == '__main__':
    app.run(debug=True)
