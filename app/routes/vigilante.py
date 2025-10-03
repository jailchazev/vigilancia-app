from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from app.models import Reporte, Emergencia, db
from datetime import datetime, timedelta

vigilante_bp = Blueprint('vigilante', __name__)

def get_current_interval():
    now = datetime.utcnow()
    local_hour = (now.hour - 5) % 24  # Ajuste UTC-5 (Perú)
    minute = (now.minute // 30) * 30
    interval_start = now.replace(minute=minute, second=0, microsecond=0)
    return interval_start

@vigilante_bp.route('/reporte')
@login_required
def reporte():
    if current_user.rol != 'vigilante':
        return redirect(url_for('admin.dashboard'))
    intervalo = get_current_interval()
    return render_template('vigilante/reporte.html', intervalo=intervalo)

@vigilante_bp.route('/enviar_reporte', methods=['POST'])
@login_required
def enviar_reporte():
    data = request.get_json()
    tipo = data['tipo']
    lat = data.get('lat')
    lon = data.get('lon')

    intervalo_inicio = get_current_interval()
    now = datetime.utcnow()
    tolerancia_inicio = intervalo_inicio
    tolerancia_fin = intervalo_inicio + timedelta(minutes=5)
    dentro = tolerancia_inicio <= now <= tolerancia_fin

    reporte = Reporte(
        user_id=current_user.id,
        tipo=tipo,
        lat=lat,
        lon=lon,
        intervalo_inicio=intervalo_inicio,
        dentro_intervalo=dentro
    )
    db.session.add(reporte)
    db.session.commit()

    if tipo == 'emergencia':
        emergencia = Emergencia(reporte_id=reporte.id)
        db.session.add(emergencia)
        db.session.commit()

    return jsonify({'success': True, 'tipo': tipo, 'dentro': dentro})