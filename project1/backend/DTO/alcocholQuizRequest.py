from pydantic import BaseModel

class alcocholQuizRequest(BaseModel):
    # 1–3: samoocena i reakcje otoczenia
    FeltNeedToLimitDrinking: bool              # 1. Czy kiedykolwiek czułeś(aś) potrzebę ograniczenia picia?
    OthersSuggestedYouDrinkTooMuch: bool       # 2. Czy bliscy sugerowali Ci, że pijesz za dużo?
    GotAngryAtCriticism: bool                  # 3. Czy ludzie krytykowali Twoje picie i Cię to zdenerwowało?

    # 4–5: częstotliwość i ilość
    DrinkingDaysPerWeek: float                 # 4. Ile dni pijesz w tygodniu?
    WeeklyAlcoholAmount: float                 # 5. Jaką ilość alkoholu pijesz w tygodniu (per piwo)?

    # 6: stosunek emocjonalny
    EnjoysDrinking: bool                       # 6. Czy lubisz to?

    # 7: ekonomiczny aspekt
    WeeklyAlcoholSpending: float                # 7. Ile wydajesz na to tygodniowo?

    # 8–14: skutki i zachowania związane z piciem
    FeltGuiltyAboutDrinking: bool              # 8. Czy kiedykolwiek czułeś(aś) się winny(a) z powodu picia?
    DrinksInMorning: bool                      # 9. Czy kiedykolwiek piłeś(aś) alkohol rano?
    ThinksOftenAboutAlcohol: bool              # 10. Czy często myślisz o alkoholu?
    HardToStopAfterOneDrink: bool              # 11. Czy trudno Ci przestać po jednym lub dwóch drinkach?
    DrinksAloneOrSecretly: bool                # 12. Czy zdarza Ci się pić samemu lub w ukryciu?
    TriedToQuitButFailed: bool                 # 13. Czy próbowałeś(aś) przestać lub ograniczyć picie, ale Ci się nie udało?
    UsesAlcoholToCope: bool                    # 14. Czy picie stało się dla Ciebie sposobem na stres, nudę lub emocje?

