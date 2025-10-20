from sklearn.ensemble import RandomForestClassifier
from DTO.alcocholQuizRequest import alcocholQuizRequest

class getAlcocholQuizResponse:
    def __init__(self):
        self.model = self.train_model()

    def train_model(self):
        X = [
            [0, 0, 0, 0.5, 1.5, 0, 10, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 2.5, 5, 1, 30.5, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 4.5, 16, 1, 75.5, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 6.5, 20, 1, 300, 1, 1, 1, 1, 1, 1, 1]
        ]

        Y = ["a", "b", "c",  "d"]

        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=None,
            random_state=42
        )

        model.fit(X, Y)

        return model

    def predictAmswer(self, data: alcocholQuizRequest):
        predict = self.model.predict([[
            data.FeltNeedToLimitDrinking,
            data.OthersSuggestedYouDrinkTooMuch,
            data.GotAngryAtCriticism,
            data.DrinkingDaysPerWeek,
            data.WeeklyAlcoholAmount,
            data.EnjoysDrinking,
            data.WeeklyAlcoholSpending,
            data.FeltGuiltyAboutDrinking,
            data.DrinksInMorning,
            data.ThinksOftenAboutAlcohol,
            data.HardToStopAfterOneDrink,
            data.DrinksAloneOrSecretly,
            data.TriedToQuitButFailed,
            data.UsesAlcoholToCope
        ]])

        return str(predict[0])