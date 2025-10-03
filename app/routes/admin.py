from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models import Reporte, User, Unidad, Emergencia, db
from datetime import datetime, timedelta
from collections import defaultdict

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.rol not in ['administrador', 'supervisor']:
        return redirect(url_for('vigilante.reporte'))
    return render_template('admin/dashboard.html')

@admin_bp.route('/monitoreo')
@login_required
def monitoreo():
    return render_template('admin/monitoreo.html')

@admin_bp.route('/api/monitoreo')
@login_required
def api_monitoreo():
    # Lógica simplificada: solo reportes de hoy
    hoy = datetime.utcnow().date()
    reportes = Reporte.query.filter(db.cast(Reporte.hora_reporte, db.Date) == hoy).all()
    usuarios = {r.user_id: r.user for r in reportes}
    unidades = defaultdict(lambda: defaultdict(list))

    for r in reportes:
        u = r.user.unidad.nombre
        key = f"{r.user.nombre}|{r.user.puesto.nombre}"
        unidades[u][key].append({
            'hora': r.hora_reporte.strftime('%H:%M'),
            'tipo': r.tipo,
            'dentro': r.dentro_intervalo,
            'intervalo': r.intervalo_inicio.strftime('%H:%M')
        })

    return jsonify(unidades)

@admin_bp.route('/mapa')
@login_required
def mapa():
    return render_template('admin/mapa.html')

@admin_bp.route('/api/usuarios_activos')
@login_required
def api_usuarios_activos():
    # Último reporte en las últimas 2 horas
    limite = datetime.utcnow() - timedelta(hours=2)
    reportes = Reporte.query.filter(Reporte.hora_reporte > limite).all()
    usuarios = []
    vistos = set()
    for r in reportes:
        if r.user_id not in vistos and r.lat and r.lon:
            usuarios.append({
                'nombre': r.user.nombre,
                'unidad': r.user.unidad.nombre,
                'puesto': r.user.puesto.nombre,
                'lat': r.lat,
                'lon': r.lon
            })
            vistos.add(r.user_id)
    return jsonify(usuarios)