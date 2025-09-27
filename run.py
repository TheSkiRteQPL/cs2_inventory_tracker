#!/usr/bin/env python3
"""
CS2 Inventory Tracker - Główny plik aplikacji
Uruchomienie: python run.py
"""

import os
from app import create_app
from flask_migrate import Migrate

# Tworzenie aplikacji Flask
app = create_app(os.getenv('FLASK_CONFIG', 'development'))

if __name__ == '__main__':
    # Uruchomienie aplikacji w trybie rozwoju
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=True if os.getenv('FLASK_ENV') == 'development' else False
    )
