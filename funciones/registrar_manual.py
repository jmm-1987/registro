import pytz
from flask import redirect, url_for, request, flash
from flask_login import current_user, login_required
from datetime import datetime
from models import db, Registro


madrid = pytz.timezone('Europe/Madrid')
def ruta_registrar_manual(app):
    @app.route('/registrar_manual', methods=['POST'])
    @login_required
    def registrar_manual():
        tipo = request.form.get('tipo')
        hora_entrada = request.form.get('hora_entrada')
        hora_salida = request.form.get('hora_salida')


        try:
            nuevo_registro = Registro(
                empleado_id=current_user.id,
                fecha_hora_entrada=hora_entrada,
                fecha_hora_salida=hora_salida,
                tipo=tipo
            )

            db.session.add(nuevo_registro)
            db.session.commit()
            flash('✅ Entrada registrada correctamente.', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error al registrar la entrada: {e}', 'error')
            print(f"Error en registrar_entrada: {e}")

        return redirect(url_for('movil'))