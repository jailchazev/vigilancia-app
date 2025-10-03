from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Unidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    puestos = db.relationship('Puesto', backref='unidad', lazy=True)
    incidentes = db.relationship('Incidente', backref='unidad_rel', lazy=True)

class Puesto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    unidad_id = db.Column(db.Integer, db.ForeignKey('unidad.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # 'vigilante', 'supervisor', 'administrador'
    unidad_id = db.Column(db.Integer, db.ForeignKey('unidad.id'), nullable=False)
    puesto_id = db.Column(db.Integer, db.ForeignKey('puesto.id'), nullable=False)

    unidad = db.relationship('Unidad', backref='usuarios')
    puesto = db.relationship('Puesto', backref='usuarios')

class Reporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'ok', 'alerta', 'emergencia'
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    hora_reporte = db.Column(db.DateTime, default=datetime.utcnow)
    intervalo_inicio = db.Column(db.DateTime, nullable=False)
    dentro_intervalo = db.Column(db.Boolean, default=True)

    user = db.relationship('User', backref='reportes')

class Emergencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporte_id = db.Column(db.Integer, db.ForeignKey('reporte.id'), nullable=False)
    atendida = db.Column(db.Boolean, default=False)
    comentario = db.Column(db.Text)

    reporte = db.relationship('Reporte', backref='emergencia')

class Incidente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    unidad_id = db.Column(db.Integer, db.ForeignKey('unidad.id'), nullable=False)
    tipo = db.Column(db.String(100))
    lugar = db.Column(db.String(200))
    prioridad = db.Column(db.String(20))
    responsable = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    acciones = db.Column(db.Text)
    recomendaciones = db.Column(db.Text)
    estado = db.Column(db.String(20), default='abierto')  # 'abierto', 'cerrado', 'pendiente'
    requiere_seguimiento = db.Column(db.Boolean, default=False)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='incidentes')
    unidad_rel = db.relationship('Unidad', backref='incidentes_unidad')