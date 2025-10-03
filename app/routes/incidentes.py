from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Incidente, Unidad, db
from datetime import datetime

incidentes_bp = Blueprint('incidentes', __name__)

@incidentes_bp.route('/reportar_incidente', methods=['GET', 'POST'])
@login_required
def reportar_incidente():
    if request.method == 'POST':
        unidad = current_user.unidad
        # Generar número
        ultimo = Incidente.query.filter_by(unidad_id=unidad.id).order_by(Incidente.id.desc()).first()
        num = 1 if not ultimo else int(ultimo.numero.split('-')[1]) + 1
        codigo = f"O{unidad.nombre[:3].upper()}-{num:04d}"

        incidente = Incidente(
            numero=codigo,
            user_id=current_user.id,
            unidad_id=unidad.id,
            tipo=request.form['tipo'],
            lugar=request.form['lugar'],
            prioridad=request.form['prioridad'],
            responsable=request.form['responsable'],
            descripcion=request.form['descripcion'],
            acciones=request.form['acciones'],
            recomendaciones=request.form['recomendaciones'],
            requiere_seguimiento=request.form.get('requiere_seguimiento') == 'on',
            lat=float(request.form['lat']) if request.form['lat'] else None,
            lon=float(request.form['lon']) if request.form['lon'] else None,
            fecha=datetime.strptime(request.form['fecha'], '%Y-%m-%dT%H:%M')
        )
        db.session.add(incidente)
        db.session.commit()
        flash('Reporte de incidente registrado con éxito', 'success')
        return redirect(url_for('incidentes.reportar_incidente'))

    return render_template('admin/incidente_form.html')