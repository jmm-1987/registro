import pytz
from flask import request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from models import db, Registro

madrid = pytz.timezone('Europe/Madrid')

def ruta_registrar_salida(app):
    @app.route('/registrar_salida', methods=['POST'])
    @login_required
    def registrar_salida():
        try:
            # Buscar el último registro sin salida del empleado
            registro = Registro.query.filter_by(
                empleado_id=current_user.id,
                fecha_hora_salida=None
            ).order_by(Registro.fecha_hora_entrada.desc()).first()

            if not registro:
                flash('⚠️ No hay ninguna entrada activa para registrar salida.', 'error')
                return redirect(url_for('movil'))

            # Registrar hora de salida
            registro.fecha_hora_salida = datetime.now(madrid)
            db.session.commit()
            flash('✅ Salida registrada correctamente.', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error al registrar salida: {e}', 'error')

        return redirect(url_for('movil'))
