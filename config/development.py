"""
Konfiguracja rozwojowa dla CS2 Inventory Tracker
"""

import os
from datetime import timedelta

class DevelopmentConfig:
    """Konfiguracja dla środowiska rozwojowego"""

    # Flask Core
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = True
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///cs2_tracker_dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Wyświetlanie zapytań SQL w konsoli

    # Steam API
    STEAM_API_KEY = os.getenv('STEAM_API_KEY', '')
    STEAM_WEB_API_URL = 'https://api.steampowered.com'

    # Price APIs
    CSGOSKINS_API_KEY = os.getenv('CSGOSKINS_API_KEY', '')
    PRICEMPIRE_API_KEY = os.getenv('PRICEMPIRE_API_KEY', '')
    STEAMWEBAPI_KEY = os.getenv('STEAMWEBAPI_KEY', '')

    # Session & Security
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    # Bcrypt
    BCRYPT_LOG_ROUNDS = 12

    # Mail Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 'yes']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME', 'noreply@cs2tracker.com')

    # Redis & Celery
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # Application Settings
    ITEMS_PER_PAGE = 20
    PRICE_UPDATE_INTERVAL = 300  # 5 minut
    MAX_STEAM_PROFILES = 5
    ENABLE_NOTIFICATIONS = True

    # Upload Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'app/static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Logging
    LOG_LEVEL = 'DEBUG'
    LOG_FILE = 'logs/cs2_tracker_dev.log'
