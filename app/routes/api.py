from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import Unidad, Puesto, db

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/puestos/<int:unidad_id>')
def puestos_por_unidad(unidad_id):
    puestos = Puesto.query.filter_by(unidad_id=unidad_id).all()
    return jsonify([{'id': p.id, 'nombre': p.nombre} for p in puestos])