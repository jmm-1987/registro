from flask import redirect, url_for, request, flash
from flask_login import current_user, login_required
from datetime import datetime
from models import db, Registro

def ruta_registrar_entrada(app):
    @app.route('/registrar_entrada', methods=['POST'])
    @login_required
    def registrar_entrada():
        tipo = request.form.get('tipo')
        print(current_user.id)
        print(tipo)

        try:
            nuevo_registro = Registro(
                empleado_id=current_user.id,
                fecha_hora_entrada=datetime.now().isoformat(),
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