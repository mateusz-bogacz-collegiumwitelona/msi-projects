## Uruchomienie aplikacji

1. Przejdź do katalogu `backend`.

2. Wykonaj poniższe polecenia:

```shell
# Utworzenie wirtualnego środowiska Python
python -m venv .venv

# Aktywacja wirtualnego środowiska
.\.venv\Scripts\Activate.ps1 #windows
source ./.venv/bin/activate   #linux

# Instalacja wymaganych pakietów
pip install -r requirements.txt

# Uruchomienie aplikacji
python main.py

```

3. Dokumentacja API (Swagger) jest dostępna pod adresem: `http://127.0.0.1:8000/docs`
