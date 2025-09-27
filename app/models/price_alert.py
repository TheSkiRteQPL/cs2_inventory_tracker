"""
Model alertów cenowych dla CS2 Inventory Tracker
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db

class PriceAlert(db.Model):
    """Model alertu cenowego dla przedmiotów CS2"""

    __tablename__ = 'price_alerts'

    # Podstawowe informacje
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Przedmiot do śledzenia
    item_name = db.Column(db.String(255), nullable=False)
    market_name = db.Column(db.String(255))
    weapon_type = db.Column(db.String(50))
    skin_name = db.Column(db.String(100))
    wear_name = db.Column(db.String(30))
    quality = db.Column(db.String(30))

    # Warunki alertu
    target_price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(10), nullable=False)  # 'above', 'below', 'equals'
    tolerance = db.Column(db.Float, default=0.0)  # Tolerancja dla warunku 'equals'

    # Ustawienia alertu
    alert_type = db.Column(db.String(20), default='email')  # email, push, both
    repeat_interval = db.Column(db.Integer, default=0)  # Interwał powtarzania w godzinach (0 = jednorazowy)

    # Status i historia
    is_active = db.Column(db.Boolean, default=True)
    triggered_count = db.Column(db.Integer, default=0)
    last_triggered = db.Column(db.DateTime)
    last_price_check = db.Column(db.DateTime)
    last_known_price = db.Column(db.Float)

    # Metadane
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacje
    notifications = db.relationship('AlertNotification', backref='alert', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<PriceAlert {self.item_name} {self.condition} {self.target_price}$>'

    def check_condition(self, current_price):
        """
        Sprawdza czy warunek alertu został spełniony

        Args:
            current_price (float): Aktualna cena przedmiotu

        Returns:
            bool: True jeśli warunek spełniony
        """
        if not current_price or current_price <= 0:
            return False

        if self.condition == 'above':
            return current_price >= self.target_price
        elif self.condition == 'below':
            return current_price <= self.target_price
        elif self.condition == 'equals':
            tolerance = self.tolerance or (self.target_price * 0.02)  # 2% domyślna tolerancja
            return abs(current_price - self.target_price) <= tolerance

        return False

    def can_trigger(self):
        """
        Sprawdza czy alert może zostać wyzwolony
        (uwzględnia interwał powtarzania)

        Returns:
            bool: True jeśli alert może zostać wyzwolony
        """
        if not self.is_active:
            return False

        # Jeśli alert jednorazowy i już został wyzwolony
        if self.repeat_interval == 0 and self.triggered_count > 0:
            return False

        # Sprawdź interwał powtarzania
        if self.last_triggered and self.repeat_interval > 0:
            from datetime import timedelta
            time_since_last = datetime.utcnow() - self.last_triggered
            required_interval = timedelta(hours=self.repeat_interval)

            if time_since_last < required_interval:
                return False

        return True

    def trigger(self, current_price):
        """
        Wyzwala alert i zapisuje powiadomienie

        Args:
            current_price (float): Cena która wyzwoliła alert
        """
        if not self.can_trigger():
            return False

        # Aktualizuj statystyki alertu
        self.triggered_count += 1
        self.last_triggered = datetime.utcnow()
        self.last_known_price = current_price

        # Utwórz powiadomienie
        notification = AlertNotification(
            alert_id=self.id,
            triggered_price=current_price,
            message=self.generate_notification_message(current_price),
            notification_type=self.alert_type,
            triggered_at=datetime.utcnow()
        )

        db.session.add(notification)

        # Jeśli alert jednorazowy, dezaktywuj go
        if self.repeat_interval == 0:
            self.is_active = False

        db.session.commit()
        return True

    def generate_notification_message(self, current_price):
        """Generuje wiadomość powiadomienia"""
        condition_text = {
            'above': 'przekroczyła',
            'below': 'spadła poniżej',
            'equals': 'osiągnęła'
        }

        condition_desc = condition_text.get(self.condition, 'osiągnęła')

        return (f"🎯 Alert cenowy: {self.item_name} {condition_desc} "
                f"{self.target_price}$ (aktualna cena: {current_price}$)")

    def update_price_check(self, current_price):
        """Aktualizuje informacje o ostatnim sprawdzeniu ceny"""
        self.last_price_check = datetime.utcnow()
        self.last_known_price = current_price
        db.session.commit()

    def get_condition_display(self):
        """Zwraca czytelny opis warunku alertu"""
        condition_map = {
            'above': f'powyżej {self.target_price}$',
            'below': f'poniżej {self.target_price}$', 
            'equals': f'około {self.target_price}$'
        }
        return condition_map.get(self.condition, f'{self.target_price}$')

    def get_status_info(self):
        """Zwraca informacje o statusie alertu"""
        if not self.is_active:
            return {'status': 'inactive', 'description': 'Nieaktywny'}

        if self.repeat_interval == 0 and self.triggered_count > 0:
            return {'status': 'completed', 'description': 'Zakończony'}

        if self.can_trigger():
            return {'status': 'active', 'description': 'Aktywny'}
        else:
            next_check_hours = self.repeat_interval - (
                (datetime.utcnow() - self.last_triggered).total_seconds() / 3600
            ) if self.last_triggered else 0

            if next_check_hours > 0:
                return {
                    'status': 'waiting', 
                    'description': f'Oczekuje {next_check_hours:.1f}h do następnego sprawdzenia'
                }

        return {'status': 'active', 'description': 'Aktywny'}

    def to_dict(self):
        """Konwertuje obiekt na słownik (do API)"""
        return {
            'id': self.id,
            'item_name': self.item_name,
            'market_name': self.market_name,
            'weapon_type': self.weapon_type,
            'skin_name': self.skin_name,
            'wear_name': self.wear_name,
            'quality': self.quality,
            'target_price': self.target_price,
            'condition': self.condition,
            'condition_display': self.get_condition_display(),
            'tolerance': self.tolerance,
            'alert_type': self.alert_type,
            'repeat_interval': self.repeat_interval,
            'is_active': self.is_active,
            'status_info': self.get_status_info(),
            'triggered_count': self.triggered_count,
            'last_triggered': self.last_triggered.isoformat() if self.last_triggered else None,
            'last_price_check': self.last_price_check.isoformat() if self.last_price_check else None,
            'last_known_price': self.last_known_price,
            'created_at': self.created_at.isoformat()
        }

    @staticmethod
    def get_user_alerts(user_id, active_only=True):
        """Pobiera wszystkie alerty użytkownika"""
        query = PriceAlert.query.filter_by(user_id=user_id)
        if active_only:
            query = query.filter_by(is_active=True)
        return query.order_by(PriceAlert.created_at.desc()).all()

    @staticmethod
    def get_pending_alerts():
        """Pobiera wszystkie alerty oczekujące na sprawdzenie"""
        return PriceAlert.query.filter_by(is_active=True).all()

class AlertNotification(db.Model):
    """Model powiadomień alertów cenowych"""

    __tablename__ = 'alert_notifications'

    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.Integer, db.ForeignKey('price_alerts.id'), nullable=False)

    # Dane powiadomienia
    triggered_price = db.Column(db.Float, nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(20), nullable=False)  # email, push, both

    # Status dostarczenia
    is_sent = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime)
    delivery_status = db.Column(db.String(20), default='pending')  # pending, sent, failed
    error_message = db.Column(db.Text)

    # Metadane
    triggered_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<AlertNotification {self.id} - {self.delivery_status}>'

    def mark_as_sent(self):
        """Oznacza powiadomienie jako wysłane"""
        self.is_sent = True
        self.sent_at = datetime.utcnow()
        self.delivery_status = 'sent'
        db.session.commit()

    def mark_as_failed(self, error_message):
        """Oznacza powiadomienie jako nieudane"""
        self.delivery_status = 'failed'
        self.error_message = error_message
        db.session.commit()

    def to_dict(self):
        """Konwertuje obiekt na słownik (do API)"""
        return {
            'id': self.id,
            'triggered_price': self.triggered_price,
            'message': self.message,
            'notification_type': self.notification_type,
            'is_sent': self.is_sent,
            'delivery_status': self.delivery_status,
            'triggered_at': self.triggered_at.isoformat(),
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }

    @staticmethod
    def get_pending_notifications():
        """Pobiera wszystkie oczekujące powiadomienia"""
        return AlertNotification.query.filter_by(is_sent=False, delivery_status='pending').all()
