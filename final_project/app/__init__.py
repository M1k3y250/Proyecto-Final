from flask import Flask, g, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_principal import Principal, Identity, identity_changed, identity_loaded, RoleNeed
from flask_security import current_user
from config import Config

# Inicialización de extensiones
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
principal = Principal()  # Flask-Principal necesita inicializarse

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)  # Flask-Principal se enlaza a la app

    # Registrar blueprints
    from app.routes import main
    from app.auth_routes import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    # Cargar los roles del usuario actual a la identidad
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        if hasattr(current_user, 'role'):
            identity.provides.add(RoleNeed(current_user.role.name))

    # Establecer la identidad antes de cada petición (necesario para roles_accepted)
    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            identity_changed.send(
                current_app._get_current_object(),
                identity=Identity(current_user.id)
            )

    return app
