# Dokumentacja

## Uruchomienie aplikacji

1. Przejdź do katalogu `backend`.

2. Wykonaj poniższe polecenia:

```shell
# Utworzenie wirtualnego środowiska Python
python -m venv .venv

# Aktywacja wirtualnego środowiska w Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Instalacja wymaganych pakietów
pip install -r requirements.txt

# Uruchomienie aplikacji
python main.py

```

3. Aplikacja będzie dostępna pod adresem: `http://127.0.0.1:8000/`
4. Dokumentacja API (Swagger) jest dostępna pod adresem: `http://127.0.0.1:8000/docs`