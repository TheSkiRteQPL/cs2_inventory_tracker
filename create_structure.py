#!/usr/bin/env python3
"""
Skrypt do tworzenia struktury aplikacji Flask CS2 Inventory Tracker
Autor: Assistant
Data: 2025-09-27
"""

import os
import sys

def create_file(filepath, content=""):
    """Tworzy plik z zawartością"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Utworzono: {filepath}")

def create_folder(folderpath):
    """Tworzy folder"""
    os.makedirs(folderpath, exist_ok=True)
    print(f"📁 Utworzono: {folderpath}")

def main():
    print("🚀 CS2 Inventory Tracker - Generator struktury aplikacji")
    print("=" * 60)

    base_dir = "cs2_inventory_tracker"

    # Główny folder aplikacji
    folders = [
        f"{base_dir}",
        f"{base_dir}/app",
        f"{base_dir}/app/models",
        f"{base_dir}/app/routes", 
        f"{base_dir}/app/services",
        f"{base_dir}/app/utils",
        f"{base_dir}/app/static/css",
        f"{base_dir}/app/static/js",
        f"{base_dir}/app/static/img/placeholders",
        f"{base_dir}/app/templates/auth",
        f"{base_dir}/app/templates/dashboard",
        f"{base_dir}/app/templates/settings",
        f"{base_dir}/app/templates/components",
        f"{base_dir}/config",
        f"{base_dir}/migrations"
    ]

    # Tworzenie folderów
    for folder in folders:
        create_folder(folder)

    # Pliki główne
    files = [
        f"{base_dir}/run.py",
        f"{base_dir}/requirements.txt",
        f"{base_dir}/.env.example",
        f"{base_dir}/README.md",
        f"{base_dir}/app/__init__.py",
        f"{base_dir}/config/__init__.py",
        f"{base_dir}/config/development.py",
        f"{base_dir}/config/production.py"
    ]

    # Modele
    model_files = [
        f"{base_dir}/app/models/__init__.py",
        f"{base_dir}/app/models/user.py",
        f"{base_dir}/app/models/steam_profile.py", 
        f"{base_dir}/app/models/inventory.py",
        f"{base_dir}/app/models/price_alert.py"
    ]

    # Routing
    route_files = [
        f"{base_dir}/app/routes/__init__.py",
        f"{base_dir}/app/routes/auth.py",
        f"{base_dir}/app/routes/dashboard.py",
        f"{base_dir}/app/routes/profile.py",
        f"{base_dir}/app/routes/api.py",
        f"{base_dir}/app/routes/settings.py"
    ]

    # Serwisy
    service_files = [
        f"{base_dir}/app/services/__init__.py",
        f"{base_dir}/app/services/steam_api.py",
        f"{base_dir}/app/services/price_tracker.py",
        f"{base_dir}/app/services/notification.py"
    ]

    # Utilities
    util_files = [
        f"{base_dir}/app/utils/__init__.py",
        f"{base_dir}/app/utils/validators.py",
        f"{base_dir}/app/utils/helpers.py"
    ]

    # Statyczne pliki
    static_files = [
        f"{base_dir}/app/static/css/style.css",
        f"{base_dir}/app/static/js/main.js",
        f"{base_dir}/app/static/js/dashboard.js",
        f"{base_dir}/app/static/js/charts.js"
    ]

    # Template'y
    template_files = [
        f"{base_dir}/app/templates/base.html",
        f"{base_dir}/app/templates/auth/login.html",
        f"{base_dir}/app/templates/auth/register.html",
        f"{base_dir}/app/templates/dashboard/index.html",
        f"{base_dir}/app/templates/dashboard/inventory.html", 
        f"{base_dir}/app/templates/dashboard/analytics.html",
        f"{base_dir}/app/templates/settings/profile.html",
        f"{base_dir}/app/templates/settings/steam_profiles.html",
        f"{base_dir}/app/templates/settings/alerts.html",
        f"{base_dir}/app/templates/components/navbar.html",
        f"{base_dir}/app/templates/components/sidebar.html",
        f"{base_dir}/app/templates/components/item_card.html"
    ]

    all_files = files + model_files + route_files + service_files + util_files + static_files + template_files

    # Tworzenie wszystkich plików
    for file_path in all_files:
        create_file(file_path)

    print("=" * 60)
    print("✅ Struktura aplikacji została utworzona pomyślnie!")
    print(f"📂 Główny folder: {base_dir}")
    print("\n🎯 Następne kroki:")
    print("1. cd cs2_inventory_tracker")
    print("2. python -m venv venv") 
    print("3. source venv/bin/activate  # Linux/Mac")
    print("   # lub venv\\Scripts\\activate  # Windows")
    print("4. pip install -r requirements.txt")
    print("5. python run.py")

if __name__ == "__main__":
    main()
