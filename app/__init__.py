from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db').replace("postgres://", "postgresql://")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes.auth import auth_bp
    from app.routes.vigilante import vigilante_bp
    from app.routes.admin import admin_bp
    from app.routes.incidentes import incidentes_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(vigilante_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(incidentes_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app