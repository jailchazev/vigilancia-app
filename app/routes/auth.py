from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User, Unidad, Puesto
from app import db
from flask_login import login_user, logout_user, current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        codigo = request.form['codigo']
        unidad_id = request.form['unidad']
        puesto_id = request.form['puesto']

        user = User.query.filter_by(codigo=codigo, unidad_id=unidad_id, puesto_id=puesto_id).first()
        if user:
            login_user(user)
            session['unidad_id'] = unidad_id
            session['puesto_id'] = puesto_id
            if user.rol == 'vigilante':
                return redirect(url_for('vigilante.reporte'))
            else:
                return redirect(url_for('admin.dashboard'))
        else:
            flash('Credenciales incorrectas', 'danger')
    unidades = Unidad.query.all()
    return render_template('login.html', unidades=unidades)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))