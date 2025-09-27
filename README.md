# CS2 Inventory Tracker

Aplikacja Flask do śledzenia i analizy wartości inwentarza Counter-Strike 2.

## 🚀 Funkcje

- **System użytkowników** - Rejestracja, logowanie, bezpieczne szyfrowanie haseł
- **Zarządzanie profilami Steam** - Dodawanie wielu profili Steam (URL, ID64, Trade Link)
- **Dashboard analityczny** - Przegląd wartości inwentarza z wykresami
- **Śledzenie cen** - Historia cen przedmiotów z różnych okresów
- **Alerty cenowe** - Powiadomienia o osiągnięciu docelowych cen
- **Responsywny design** - Bootstrap 5.3 z dark theme

## 📋 Wymagania

- Python 3.8+
- Flask 3.0+
- Steam API Key
- Redis (opcjonalnie, dla cache i Celery)

## 🛠️ Instalacja

1. **Klonowanie/rozpakowanie projektu:**
```bash
# Jeśli używasz Git
git clone <repository-url>
cd cs2_inventory_tracker

# Lub uruchom skrypt generujący strukturę
python create_structure.py
```

2. **Utworzenie środowiska wirtualnego:**
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instalacja zależności:**
```bash
pip install -r requirements.txt
```

4. **Konfiguracja:**
```bash
# Skopiuj przykładową konfigurację
cp .env.example .env

# Edytuj .env i uzupełnij:
# - SECRET_KEY (wygeneruj bezpieczny klucz)
# - STEAM_API_KEY (pobierz z https://steamcommunity.com/dev/apikey)
# - DATABASE_URL (domyślnie SQLite)
# - Pozostałe ustawienia według potrzeb
```

5. **Inicjalizacja bazy danych:**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Uruchomienie aplikacji:**
```bash
python run.py
```

Aplikacja będzie dostępna pod adresem: http://localhost:5000

## 🗄️ Struktura projektu

```
cs2_inventory_tracker/
├── app/
│   ├── __init__.py              # Factory aplikacji Flask
│   ├── models/                  # Modele bazy danych
│   │   ├── user.py             # Model użytkownika
│   │   ├── steam_profile.py    # Model profilu Steam
│   │   ├── inventory.py        # Model inwentarza
│   │   └── price_alert.py      # Model alertów
│   ├── routes/                  # Routing aplikacji
│   │   ├── auth.py             # Autentykacja
│   │   ├── dashboard.py        # Dashboard główny
│   │   ├── profile.py          # Profile Steam
│   │   ├── settings.py         # Ustawienia
│   │   └── api.py              # API endpoints
│   ├── services/                # Serwisy biznesowe
│   │   ├── steam_api.py        # Integracja Steam API
│   │   ├── price_tracker.py    # Śledzenie cen
│   │   └── notification.py     # Powiadomienia
│   ├── utils/                   # Narzędzia pomocnicze
│   ├── templates/               # Szablony HTML
│   └── static/                  # Pliki statyczne
├── config/                      # Konfiguracja
├── migrations/                  # Migracje bazy danych
├── requirements.txt             # Zależności Python
├── run.py                      # Punkt wejścia aplikacji
└── .env.example                # Przykładowa konfiguracja
```

## 🔧 APIs i Integracje

### Steam Web API
- Pobieranie danych inwentarza
- Informacje o graczach
- Szczegóły przedmiotów

### Price APIs
- Steam Community Market
- CSGOSKINS.GG
- Pricempire
- Inne źródła danych cenowych

## 🛡️ Bezpieczeństwo

- **Szyfrowanie haseł** - Flask-Bcrypt z salt
- **CSRF Protection** - Flask-WTF
- **Session Security** - Bezpieczne ciasteczka
- **Input validation** - WTForms z walidacją
- **SQL Injection Protection** - SQLAlchemy ORM

## 📈 Funkcjonalności

### Dashboard
- Sumaryczna wartość inwentarza
- Wykresy trendów cenowych (7/30 dni)
- Lista przedmiotów z analizą
- Przegląd zysków/strat

### Zarządzanie Profilami Steam
- Dodawanie profili przez URL/ID/Trade Link
- Przełączanie między profilami
- Automatyczna synchronizacja inwentarzy
- Walidacja Steam ID

### Alerty Cenowe
- Ustawianie progów cenowych
- Powiadomienia email/push
- Powtarzające się alerty
- Historia powiadomień

### Analiza Danych
- Historia cen przedmiotów
- Trendy rynkowe
- Analiza ROI
- Porównania czasowe

## 🚀 Deployment

### Development
```bash
export FLASK_ENV=development
python run.py
```

### Production
```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### Docker (opcjonalnie)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
```

## 📝 TODO / Przyszłe funkcje

- [ ] Powiadomienia push (WebSockets)
- [ ] Eksport danych do CSV/Excel
- [ ] Analiza sentiment rynku
- [ ] Integracja z platformami handlowymi
- [ ] Mobile App (React Native)
- [ ] Portfolio sharing
- [ ] Advanced analytics (ML predictions)

## 🤝 Contributing

1. Fork projektu
2. Utwórz branch dla nowej funkcji (`git checkout -b feature/AmazingFeature`)
3. Commit zmian (`git commit -m 'Add some AmazingFeature'`)
4. Push do branch (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

## 📄 Licencja

Ten projekt jest licencjonowany na licencji MIT - zobacz plik [LICENSE](LICENSE) po szczegóły.

## ⚠️ Disclaimer

Ta aplikacja jest stworzona wyłącznie do celów edukacyjnych i informacyjnych. Autorzy nie ponoszą odpowiedzialności za jakiekolwiek straty finansowe wynikające z korzystania z aplikacji.

## 📞 Kontakt

- GitHub: [Twój GitHub]
- Email: [Twój Email]

---

**CS2 Inventory Tracker** - Śledź, analizuj, optymalizuj! 🎯
