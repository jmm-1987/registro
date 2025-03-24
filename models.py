
from flask_sqlalchemy import SQLAlchemy

# Usamos una única instancia de SQLAlchemy
db = SQLAlchemy()

class Usuario(db.Model):  # Cambiado de db.Base a db.Model
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Empleado(db.Model):  # Cambiado de db.Base a db.Model
    __tablename__ = "empleado"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(10), nullable=False)
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



class Registro(db.Model):  # Cambiado de db.Base a db.Model
    __tablename__ = "registro"
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    fecha_hora_entrada = db.Column(db.DateTime, nullable=False)
    fecha_hora_salida = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.String, db.CheckConstraint("tipo IN ('Trabajo', 'Vacaciones', 'Ausencia', 'Baja')", name='check_tipo'), nullable=False)

    empleado = db.relationship('Empleado', backref=db.backref('registros', lazy=True))


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