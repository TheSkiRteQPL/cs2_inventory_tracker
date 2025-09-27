"""
Model użytkownika dla CS2 Inventory Tracker
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """Model użytkownika aplikacji"""

    __tablename__ = 'users'

    # Podstawowe informacje
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Profil użytkownika
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    avatar_filename = db.Column(db.String(100))

    # Ustawienia
    timezone = db.Column(db.String(50), default='UTC')
    language = db.Column(db.String(5), default='pl')
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=True)

    # Metadane
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)

    # Relacje
    steam_profiles = db.relationship('SteamProfile', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    price_alerts = db.relationship('PriceAlert', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

    @property
    def password(self):
        """Zabezpieczenie przed odczytem hasła"""
        raise AttributeError('Hasło nie może być odczytane')

    @password.setter
    def password(self, password):
        """Szyfrowanie hasła przy ustawianiu"""
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Sprawdzanie poprawności hasła"""
        return check_password_hash(self.password_hash, password)

    def get_full_name(self):
        """Zwraca pełne imię i nazwisko"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def get_avatar_url(self):
        """Zwraca URL avatara użytkownika"""
        if self.avatar_filename:
            return f"/static/uploads/avatars/{self.avatar_filename}"
        return "/static/img/default_avatar.png"

    def update_last_login(self):
        """Aktualizuje czas ostatniego logowania"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def get_total_inventory_value(self):
        """Oblicza łączną wartość wszystkich inwentarzy użytkownika"""
        total_value = 0.0
        for profile in self.steam_profiles:
            total_value += profile.get_inventory_value()
        return total_value

    def get_active_alerts_count(self):
        """Zwraca liczbę aktywnych alertów cenowych"""
        return self.price_alerts.filter_by(is_active=True).count()

    def to_dict(self):
        """Konwertuje obiekt na słownik (do API)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.get_full_name(),
            'avatar_url': self.get_avatar_url(),
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'steam_profiles_count': self.steam_profiles.count(),
            'active_alerts_count': self.get_active_alerts_count(),
            'total_inventory_value': self.get_total_inventory_value()
        }

    @staticmethod
    def find_by_email(email):
        """Znajduje użytkownika po adresie email"""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_username(username):
        """Znajduje użytkownika po nazwie użytkownika"""
        return User.query.filter_by(username=username).first()
