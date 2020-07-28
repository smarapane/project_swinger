import pandas as pd
from Records.playerBattingRecords import playerBattingRecords
from Records.playerBowlingRecords import playerBowlingRecords
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler


class Projections:
    def __init__(self):
        bat = playerBattingRecords()
        bowl = playerBowlingRecords()
        self.player_batting_dfs = bat.clean()
        self.player_bowling_dfs = bowl.clean()

    def predict_batting(self):
        sc = StandardScaler()
        lin = RandomForestRegressor(max_features=None)
        for i in self.player_batting_dfs:
            self.player_batting_dfs[i] = self.player_batting_dfs[i].sort_values(
                by=["Match Date"], ignore_index=True
            )

            x = (
                self.player_batting_dfs[i][["Runs", "Balls"]]
                .head(len(self.player_batting_dfs[i].index) - 1)
                .values.tolist()
            )
            y = (
                self.player_batting_dfs[i]["Runs"]
                .tail(len(self.player_batting_dfs[i].index) - 1)
                .values.tolist()
            )

            x = sc.fit_transform(x)
            lin.fit(x, y)
            print(
                f"{self.player_batting_dfs[i].iloc[0]['Name']}\nPredicted Runs: {lin.predict(self.player_batting_dfs[i][['Runs', 'Balls']].tail(1))}"
            )

            y = (
                self.player_batting_dfs[i]["Balls"]
                .tail(len(self.player_batting_dfs[i].index) - 1)
                .values.tolist()
            )
            lin.fit(x, y)
            print(
                f"Predicted Balls: {lin.predict(self.player_batting_dfs[i][['Runs', 'Balls']].tail(1))}"
            )
