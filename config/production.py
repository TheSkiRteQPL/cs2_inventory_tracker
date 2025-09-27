"""
Konfiguracja produkcyjna dla CS2 Inventory Tracker
"""

import os
from datetime import timedelta

class ProductionConfig:
    """Konfiguracja dla środowiska produkcyjnego"""

    # Flask Core
    SECRET_KEY = os.getenv('SECRET_KEY')  # MUSI być ustawiony w produkcji
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Steam API
    STEAM_API_KEY = os.getenv('STEAM_API_KEY')
    STEAM_WEB_API_URL = 'https://api.steampowered.com'

    # Price APIs
    CSGOSKINS_API_KEY = os.getenv('CSGOSKINS_API_KEY', '')
    PRICEMPIRE_API_KEY = os.getenv('PRICEMPIRE_API_KEY', '')
    STEAMWEBAPI_KEY = os.getenv('STEAMWEBAPI_KEY', '')

    # Session & Security
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 godzina

    # Bcrypt
    BCRYPT_LOG_ROUNDS = 15  # Wyższa wartość dla produkcji

    # Mail Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 'yes']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')

    # Redis & Celery
    REDIS_URL = os.getenv('REDIS_URL')
    CELERY_BROKER_URL = os.getenv('REDIS_URL')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL')

    # Application Settings
    ITEMS_PER_PAGE = 20
    PRICE_UPDATE_INTERVAL = 600  # 10 minut w produkcji
    MAX_STEAM_PROFILES = 5
    ENABLE_NOTIFICATIONS = True

    # Upload Settings
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    UPLOAD_FOLDER = '/var/www/cs2tracker/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = '/var/log/cs2tracker/app.log'

    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL')
    RATELIMIT_DEFAULT = "100 per hour"
