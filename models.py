from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Usamos una única instancia de SQLAlchemy
db = SQLAlchemy()

class Empleado(UserMixin, db.Model):  # Modificamos el modelo Empleado para que herede UserMixin
    __tablename__ = "empleado"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Aseguramos que la contraseña sea suficientemente larga
    cargo = db.Column(db.String(30), nullable=False)
    alias = db.Column(db.String, nullable=False)
    nombre_completo = db.Column(db.String, nullable=False)
    dni = db.Column(db.String, nullable=True)
    seguridad_social = db.Column(db.String, nullable=True)
    sede = db.Column(db.String, db.CheckConstraint("sede IN ('Merida', 'Navalmoral')", name='check_sede'), nullable=True)
    telefono = db.Column(db.String(9), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    fecha_alta = db.Column(db.DateTime, nullable=False)
    fecha_baja = db.Column(db.DateTime, nullable=True)
    sabados = db.Column(db.Boolean, nullable=False)
    activo = db.Column(db.Boolean, nullable=False)

    # Métodos requeridos por Flask-Login:

    def is_active(self):
        return self.activo  # Retorna si el empleado está activo

    def get_id(self):
        return str(self.id)  # Asegúrate de devolver el id como cadena

    def is_authenticated(self):
        return True  # Si el usuario está autenticado, devuelve True

    def is_anonymous(self):
        return False  # Si el usuario no es anónimo, devuelve False

    def check_password(self, password):
        """Método para comprobar la contraseña del empleado."""
        return check_password_hash(self.password, password)

    # Método para crear un nuevo empleado
    @staticmethod
    def create_empleado(usuario, password, **kwargs):
        """Crear un nuevo empleado con contraseña hasheada."""
        hashed_password = generate_password_hash(password)
        new_empleado = Empleado(usuario=usuario, password=hashed_password, **kwargs)
        db.session.add(new_empleado)
        db.session.commit()
        return new_empleado


class Registro(db.Model):
    __tablename__ = "registro"
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    fecha_hora_entrada = db.Column(db.DateTime, nullable=False)
    fecha_hora_salida = db.Column(db.DateTime, nullable=True)
    tipo = db.Column(db.String, db.CheckConstraint("tipo IN ('Trabajo', 'Vacaciones', 'Ausencia', 'Baja')", name='check_tipo'), nullable=False)

    empleado = db.relationship('Empleado', backref='registros')


class Foto(db.Model):
    __tablename__ = 'foto'

    id = db.Column(db.Integer, primary_key=True)
    empleado = db.Column(db.String(255), nullable=False)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    ruta = db.Column(db.String(255), nullable=False)

class Documento(db.Model):
    __tablename__ = 'documento'

    id = db.Column(db.Integer, primary_key=True)
    empleado = db.Column(db.String(255), nullable=False)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    ruta = db.Column(db.String(255), nullable=False)
