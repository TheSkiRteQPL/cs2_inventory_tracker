"""
CS2 Inventory Tracker - Flask Application Factory
Inicjalizacja aplikacji z wszystkimi rozszerzeniami
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

# Inicjalizacja rozszerzeń Flask
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
csrf = CSRFProtect()

def create_app(config_name='development'):
    """
    Factory function do tworzenia aplikacji Flask

    Args:
        config_name (str): Nazwa konfiguracji ('development', 'production', 'testing')

    Returns:
        Flask: Skonfigurowana aplikacja Flask
    """
    app = Flask(__name__)

    # Ładowanie konfiguracji
    if config_name == 'development':
        from config.development import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'production':
        from config.production import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from config.development import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)

    # Inicjalizacja rozszerzeń z aplikacją
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Konfiguracja Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Zaloguj się, aby uzyskać dostęp do tej strony.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # Rejestracja Blueprint'ów
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.profile import profile_bp
    from app.routes.settings import settings_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Tworzenie tabel bazy danych
    with app.app_context():
        db.create_all()

    # Obsługa błędów
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app
