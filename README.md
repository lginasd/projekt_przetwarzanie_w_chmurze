# Projekt

REST API dla prostego sklepu internetowego stworzony za pomocą FastAPI.

## Funkcjonalności

- rejestracja i usunięcie użytkowników
- logowanie JWT
- role użytkowników (admin/user)
- CRUD dla wszystkich encji
- składanie zamówień
- walidacja danych
- autoryzacja endpointówtAPI.

# Konfiguracja

## .env

W pliku `.env` należy umieścić dane konfiguracyjne.

Przykład znajduje się w `.env.example`.

```env
SECRET_KEY=super_secret_key
```

- `SECRET_KEY` -- klucz JWT

# Uruchomienie

## Środowisko wirtualne

### Stworzenie

```bash
python -m venv .venv
```

### Aktywacja

Linux/macOS
```
source .venv/bin/activate
```

Windows
```
.venv\Scripts\activate
```

## Instalacja zależności

```bash
pip install -r requirements.txt
```

## Uruchomienie aplikacji

```bash
uvicorn app.main:app --reload
```

## Dokumentacja

### Swagger

Swagger UI jest automatycznie zachostowany na endpointcie `/docs`.

```
http://127.0.0.1:8000/docs
```

### openapi.json

Openapi jest dostępny na endpointcie `/openapi.json`.

```
http://127.0.0.1:8000/openapi.json
```

# Testy

Testy automatyczne są uruchomione za pmocą `pytest`.

```bash
pytest
```
