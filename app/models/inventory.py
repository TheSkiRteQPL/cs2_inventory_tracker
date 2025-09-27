"""
Model inwentarza i przedmiotów CS2 dla CS2 Inventory Tracker
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db

class InventoryItem(db.Model):
    """Model przedmiotu w inwentarzu CS2"""

    __tablename__ = 'inventory_items'

    # Podstawowe informacje
    id = db.Column(db.Integer, primary_key=True)
    steam_profile_id = db.Column(db.Integer, db.ForeignKey('steam_profiles.id'), nullable=False)

    # Dane przedmiotu
    asset_id = db.Column(db.String(20), nullable=False)  # Steam Asset ID
    class_id = db.Column(db.String(20), nullable=False)   # Steam Class ID
    instance_id = db.Column(db.String(20))               # Steam Instance ID

    # Informacje o przedmiocie
    name = db.Column(db.String(255), nullable=False)
    market_name = db.Column(db.String(255))
    type_name = db.Column(db.String(100))

    # Szczegóły CS2
    weapon_type = db.Column(db.String(50))      # AK-47, AWP, Karambit, etc.
    skin_name = db.Column(db.String(100))       # Redline, Dragon Lore, etc.
    wear_name = db.Column(db.String(30))        # Factory New, Minimal Wear, etc.
    wear_value = db.Column(db.Float)            # 0.0 - 1.0

    # Rzadkość i jakość
    rarity = db.Column(db.String(30))           # Consumer, Industrial, Mil-Spec, etc.
    rarity_color = db.Column(db.String(10))     # Hex color code
    quality = db.Column(db.String(30))          # Normal, StatTrak, Souvenir

    # Wartość i ceny
    current_price = db.Column(db.Float, default=0.0)
    last_price_update = db.Column(db.DateTime)
    purchase_price = db.Column(db.Float)        # Cena zakupu (jeśli znana)

    # Obrazek i opis
    icon_url = db.Column(db.String(255))
    inspect_url = db.Column(db.Text)
    description = db.Column(db.Text)

    # Stickers i dodatki
    stickers = db.Column(db.JSON)  # Lista naklejek w formacie JSON
    name_tag = db.Column(db.String(100))

    # Status i metadane
    is_tradeable = db.Column(db.Boolean, default=True)
    is_marketable = db.Column(db.Boolean, default=True)
    quantity = db.Column(db.Integer, default=1)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacje
    price_history = db.relationship('PriceHistory', backref='item', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<InventoryItem {self.name} ({self.current_price}$)>'

    def get_full_name(self):
        """Zwraca pełną nazwę przedmiotu"""
        if self.weapon_type and self.skin_name:
            full_name = f"{self.weapon_type} | {self.skin_name}"
            if self.wear_name:
                full_name += f" ({self.wear_name})"
            if self.quality and self.quality != 'Normal':
                full_name = f"{self.quality} {full_name}"
            return full_name
        return self.name or self.market_name

    def get_rarity_info(self):
        """Zwraca informacje o rzadkości przedmiotu"""
        rarity_map = {
            'Consumer Grade': {'color': '#b0c3d9', 'level': 1},
            'Industrial Grade': {'color': '#5e98d9', 'level': 2}, 
            'Mil-Spec Grade': {'color': '#4b69ff', 'level': 3},
            'Restricted': {'color': '#8847ff', 'level': 4},
            'Classified': {'color': '#d32ce6', 'level': 5},
            'Covert': {'color': '#eb4b4b', 'level': 6},
            'Contraband': {'color': '#e4ae39', 'level': 7}
        }

        return rarity_map.get(self.rarity, {'color': '#b0c3d9', 'level': 1})

    def get_wear_info(self):
        """Zwraca informacje o zużyciu przedmiotu"""
        if not self.wear_value:
            return {'category': 'Unknown', 'percentage': 0}

        wear_ranges = [
            (0.00, 0.07, 'Factory New'),
            (0.07, 0.15, 'Minimal Wear'),
            (0.15, 0.38, 'Field-Tested'),
            (0.38, 0.45, 'Well-Worn'),
            (0.45, 1.00, 'Battle-Scarred')
        ]

        for min_val, max_val, category in wear_ranges:
            if min_val <= self.wear_value < max_val:
                percentage = ((self.wear_value - min_val) / (max_val - min_val)) * 100
                return {'category': category, 'percentage': round(percentage, 2)}

        return {'category': 'Unknown', 'percentage': 0}

    def calculate_profit_loss(self):
        """Oblicza zysk/stratę względem ceny zakupu"""
        if not self.purchase_price or not self.current_price:
            return None

        profit = self.current_price - self.purchase_price
        percentage = (profit / self.purchase_price) * 100

        return {
            'profit': profit,
            'percentage': round(percentage, 2),
            'is_profit': profit > 0
        }

    def get_price_trend(self, days=7):
        """Pobiera trend cenowy dla określonej liczby dni"""
        from datetime import timedelta

        start_date = datetime.utcnow() - timedelta(days=days)
        history = self.price_history.filter(
            PriceHistory.recorded_at >= start_date
        ).order_by(PriceHistory.recorded_at.asc()).all()

        if len(history) < 2:
            return {'trend': 'stable', 'change': 0.0, 'percentage': 0.0}

        first_price = history[0].price
        last_price = history[-1].price
        change = last_price - first_price
        percentage = (change / first_price) * 100 if first_price > 0 else 0

        trend = 'rising' if change > 0 else 'falling' if change < 0 else 'stable'

        return {
            'trend': trend,
            'change': round(change, 2),
            'percentage': round(percentage, 2),
            'data_points': len(history)
        }

    def update_price(self, new_price, source='unknown'):
        """Aktualizuje cenę przedmiotu i zapisuje historię"""
        old_price = self.current_price
        self.current_price = new_price
        self.last_price_update = datetime.utcnow()

        # Zapisz historię cen
        if old_price != new_price:
            price_history = PriceHistory(
                item_id=self.id,
                price=new_price,
                source=source,
                recorded_at=datetime.utcnow()
            )
            db.session.add(price_history)

        db.session.commit()

    def to_dict(self):
        """Konwertuje obiekt na słownik (do API)"""
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'name': self.get_full_name(),
            'market_name': self.market_name,
            'weapon_type': self.weapon_type,
            'skin_name': self.skin_name,
            'wear_name': self.wear_name,
            'wear_value': self.wear_value,
            'wear_info': self.get_wear_info(),
            'rarity': self.rarity,
            'rarity_info': self.get_rarity_info(),
            'quality': self.quality,
            'current_price': self.current_price,
            'last_price_update': self.last_price_update.isoformat() if self.last_price_update else None,
            'profit_loss': self.calculate_profit_loss(),
            'price_trend_7d': self.get_price_trend(7),
            'icon_url': self.icon_url,
            'inspect_url': self.inspect_url,
            'is_tradeable': self.is_tradeable,
            'is_marketable': self.is_marketable,
            'quantity': self.quantity,
            'stickers': self.stickers,
            'name_tag': self.name_tag
        }

class PriceHistory(db.Model):
    """Model historii cen przedmiotów"""

    __tablename__ = 'price_history'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)

    price = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(50), default='steam_market')  # steam_market, csgoskins, pricempire, etc.
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<PriceHistory {self.price}$ at {self.recorded_at}>'

    def to_dict(self):
        """Konwertuje obiekt na słownik (do API)"""
        return {
            'price': self.price,
            'source': self.source,
            'recorded_at': self.recorded_at.isoformat()
        }
