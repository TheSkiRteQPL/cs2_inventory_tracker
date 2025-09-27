"""
Model profilu Steam dla CS2 Inventory Tracker
"""

from datetime import datetime
import re
from flask_sqlalchemy import SQLAlchemy
from app import db

class SteamProfile(db.Model):
    """Model profilu Steam użytkownika"""

    __tablename__ = 'steam_profiles'

    # Podstawowe informacje
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Dane Steam
    steam_id64 = db.Column(db.String(20), nullable=False, index=True)
    steam_username = db.Column(db.String(100))
    profile_name = db.Column(db.String(100), nullable=False)  # Nazwa nadana przez użytkownika
    steam_url = db.Column(db.String(255))
    trade_url = db.Column(db.Text)

    # Avatar i profil
    avatar_url = db.Column(db.String(255))
    profile_visibility = db.Column(db.String(20), default='public')  # public, private, friends_only

    # Statystyki inwentarza
    last_inventory_update = db.Column(db.DateTime)
    inventory_value = db.Column(db.Float, default=0.0)
    items_count = db.Column(db.Integer, default=0)

    # Status i metadane
    is_active = db.Column(db.Boolean, default=True)
    is_primary = db.Column(db.Boolean, default=False)  # Główny profil użytkownika
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacje
    inventory_items = db.relationship('InventoryItem', backref='steam_profile', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<SteamProfile {self.profile_name} ({self.steam_id64})>'

    @staticmethod
    def extract_steam_id64(steam_input):
        """
        Wyodrębnia Steam ID64 z różnych formatów:
        - Steam URL: https://steamcommunity.com/profiles/76561198447630320
        - Steam ID URL: https://steamcommunity.com/id/username  
        - Trade URL: https://steamcommunity.com/tradeoffer/new/?partner=487364592&token=xxx
        - Bezpośredni Steam ID64: 76561198447630320
        """
        steam_input = steam_input.strip()

        # Bezpośredni Steam ID64
        if steam_input.isdigit() and len(steam_input) == 17:
            return steam_input

        # Steam Profile URL z ID64
        profile_match = re.search(r'steamcommunity\.com/profiles/(\d{17})', steam_input)
        if profile_match:
            return profile_match.group(1)

        # Trade URL - konwersja partner ID na Steam ID64
        trade_match = re.search(r'partner=(\d+)', steam_input)
        if trade_match:
            partner_id = int(trade_match.group(1))
            # Konwersja Account ID na Steam ID64
            steam_id64 = partner_id + 76561197960265728
            return str(steam_id64)

        # Steam ID URL - wymagałby dodatkowego API call
        id_match = re.search(r'steamcommunity\.com/id/([^/]+)', steam_input)
        if id_match:
            # Tutaj należałoby użyć Steam API do konwersji vanity URL na ID64
            return None  # Wymaga implementacji Steam API call

        return None

    @staticmethod
    def validate_steam_input(steam_input):
        """Waliduje format Steam ID/URL"""
        if not steam_input or not steam_input.strip():
            return False, "Steam ID/URL nie może być pusty"

        steam_id64 = SteamProfile.extract_steam_id64(steam_input)
        if not steam_id64:
            return False, "Nieprawidłowy format Steam ID/URL"

        return True, steam_id64

    def update_inventory_stats(self, items_count=None, total_value=None):
        """Aktualizuje statystyki inwentarza"""
        if items_count is not None:
            self.items_count = items_count
        if total_value is not None:
            self.inventory_value = total_value

        self.last_inventory_update = datetime.utcnow()
        db.session.commit()

    def get_inventory_value(self):
        """Zwraca aktualną wartość inwentarza"""
        return self.inventory_value or 0.0

    def get_steam_profile_url(self):
        """Zwraca pełny URL do profilu Steam"""
        return f"https://steamcommunity.com/profiles/{self.steam_id64}"

    def is_inventory_outdated(self, max_age_minutes=30):
        """Sprawdza czy inwentarz wymaga aktualizacji"""
        if not self.last_inventory_update:
            return True

        time_diff = datetime.utcnow() - self.last_inventory_update
        return time_diff.total_seconds() > (max_age_minutes * 60)

    def set_as_primary(self):
        """Ustawia ten profil jako główny dla użytkownika"""
        # Usuń status główny z innych profili tego użytkownika
        SteamProfile.query.filter_by(user_id=self.user_id, is_primary=True).update({'is_primary': False})

        # Ustaw ten profil jako główny
        self.is_primary = True
        db.session.commit()

    def to_dict(self):
        """Konwertuje obiekt na słownik (do API)"""
        return {
            'id': self.id,
            'profile_name': self.profile_name,
            'steam_id64': self.steam_id64,
            'steam_username': self.steam_username,
            'steam_url': self.get_steam_profile_url(),
            'avatar_url': self.avatar_url,
            'inventory_value': self.get_inventory_value(),
            'items_count': self.items_count,
            'last_update': self.last_inventory_update.isoformat() if self.last_inventory_update else None,
            'is_primary': self.is_primary,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }

    @staticmethod
    def get_user_profiles(user_id, active_only=True):
        """Pobiera wszystkie profile Steam użytkownika"""
        query = SteamProfile.query.filter_by(user_id=user_id)
        if active_only:
            query = query.filter_by(is_active=True)
        return query.order_by(SteamProfile.is_primary.desc(), SteamProfile.created_at.asc()).all()

    @staticmethod
    def find_by_steam_id64(steam_id64):
        """Znajduje profil po Steam ID64"""
        return SteamProfile.query.filter_by(steam_id64=steam_id64).first()
