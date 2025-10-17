from fastapi import FastAPI
from Services.getAlcoholQuizResponse import getAlcocholQuizResponse
from DTO.alcocholQuizRequest import alcocholQuizRequest
import uvicorn

app = FastAPI(
    title="My Alcohol Quiz API",
    description="API do przewidywania wyników quizu alkoholowego",
    version="1.0.0"
)

predict = getAlcocholQuizResponse()

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
def getAlcocholQuiz(data: alcocholQuizRequest):
    """
    Endpoint POST do przewidywania wyniku quizu alkoholowego.
    Zwraca przewidywaną kategorię odpowiedzi na podstawie danych wejściowych.
    """
    response = predict.predictAmswer(data)
    return {"answear": response}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
