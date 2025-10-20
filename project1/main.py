from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
from Services.getAlcoholQuizResponse import getAlcocholQuizResponse
from DTO.alcocholQuizRequest import alcocholQuizRequest
import uvicorn, os

app = FastAPI(
    title="My Alcohol Quiz API",
    description="API do przewidywania wyników quizu alkoholowego",
    version="1.0.0"
)

predict = getAlcocholQuizResponse()

# Ścieżka do bieżącego folderu (backend)
BASE_DIR = os.path.dirname(__file__)

# 🔹 Serwowanie strony głównej (index.html)
@app.get("/", response_class=HTMLResponse)
def home():
    file_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(file_path):
        return "<h2>Brak pliku index.html w katalogu backend</h2>"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# 🔹 Serwowanie arkusza stylów (style.css)
@app.get("/style.css")
def css():
    file_path = os.path.join(BASE_DIR, "style.css")
    if not os.path.exists(file_path):
        return Response("/* Brak pliku style.css */", media_type="text/css")
    with open(file_path, "r", encoding="utf-8") as f:
        return Response(f.read(), media_type="text/css")

@app.post(
    "/",
    summary="Przewidywanie wyniku quizu alkoholowego",
    description=(
        "Ten endpoint przyjmuje dane z quizu alkoholowego w formacie JSON i zwraca przewidywaną odpowiedź.\n\n"
        "**Parametry wejściowe:**\n"
        "- FeltNeedToLimitDrinking: bool – Czy kiedykolwiek czułeś(aś) potrzebę ograniczenia picia?\n"
        "- OthersSuggestedYouDrinkTooMuch: bool – Czy bliscy sugerowali Ci, że pijesz za dużo?\n"
        "- GotAngryAtCriticism: bool – Czy ludzie krytykowali Twoje picie i Cię to zdenerwowało?\n"
        "- DrinkingDaysPerWeek: float – Ile dni pijesz w tygodniu?\n"
        "- WeeklyAlcoholAmount: float – Ilość alkoholu tygodniowo (per piwo)\n"
        "- EnjoysDrinking: bool – Czy lubisz picie?\n"
        "- WeeklyAlcoholSpending: float – Ile wydajesz na alkohol tygodniowo?\n"
        "- FeltGuiltyAboutDrinking: bool – Czy kiedykolwiek czułeś(aś) się winny(a) z powodu picia?\n"
        "- DrinksInMorning: bool – Czy piłeś rano?\n"
        "- ThinksOftenAboutAlcohol: bool – Czy często myślisz o alkoholu?\n"
        "- HardToStopAfterOneDrink: bool – Czy trudno przestać po jednym lub dwóch drinkach?\n"
        "- DrinksAloneOrSecretly: bool – Czy pijesz samemu lub w ukryciu?\n"
        "- TriedToQuitButFailed: bool – Próby ograniczenia picia zakończone niepowodzeniem\n"
        "- UsesAlcoholToCope: bool – Czy picie służy radzeniu sobie ze stresem lub nudą?"
    ),
    response_description="Przewidywana odpowiedź na quiz"
)
		
		
# 🔹 Endpoint POST — przetwarzanie quizu
@app.post("/")
def getAlcocholQuiz(data: alcocholQuizRequest):
    response = predict.predictAmswer(data)
    return {"answear": response}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
