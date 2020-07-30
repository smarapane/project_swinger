import pandas as pd
from Records.playerBattingRecords import playerBattingRecords
from Records.playerBowlingRecords import playerBowlingRecords
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.exceptions import UndefinedMetricWarning
import warnings


class Projections:
    def __init__(self, batrec, bowlrec):
        bat = batrec
        bowl = bowlrec
        bat.clean()
        bowl.clean()
        self.player_batting_dfs = bat.getPlayers()
        self.player_bowling_dfs = bowl.getPlayers()

    def predict_batting(self):
        sc = StandardScaler()
        lin = RandomForestRegressor(max_features=None)
        Name = []
        Runs = []
        Balls = []
        RsquaredRuns = []
        RsquaredBalls = []
        for i in self.player_batting_dfs:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
                Name.append(i)
                self.player_batting_dfs[i] = self.player_batting_dfs[i].sort_values(
                    by=["Match Date"], ignore_index=True
                )

                x = (
                    self.player_batting_dfs[i][["Runs", "Balls", "Batting Order No."]]
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

                Runs.append(
                    round(
                        lin.predict(
                            self.player_batting_dfs[i][
                                ["Runs", "Balls", "Batting Order No."]
                            ].tail(1)
                        )[0]
                    )
                )
                RsquaredRuns.append(lin.score(x, y))

                y = (
                    self.player_batting_dfs[i]["Balls"]
                    .tail(len(self.player_batting_dfs[i].index) - 1)
                    .values.tolist()
                )
                lin.fit(x, y)

                Balls.append(
                    round(
                        lin.predict(
                            self.player_batting_dfs[i][
                                ["Runs", "Balls", "Batting Order No."]
                            ].tail(1)
                        )[0]
                    )
                )
                RsquaredBalls.append(lin.score(x, y))

        return pd.DataFrame(
            data={
                "Name": Name,
                "Projected Runs": Runs,
                "Confidence for Runs": RsquaredRuns,
                "Projected Balls": Balls,
                "Confidence for Balls": RsquaredBalls,
            }
        )

    def predict_bowling(self):
        sc = StandardScaler()
        lin = RandomForestRegressor(max_features=None)
        Name = []
        Wickets = []
        Economy = []
        Wides = []
        RsquaredWkt = []
        RsquaredEcon = []
        RsquaredWd = []
        for i in self.player_bowling_dfs:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
                Name.append(i)
                self.player_bowling_dfs[i] = self.player_bowling_dfs[i].sort_values(
                    by=["Match Date"], ignore_index=True
                )

                x = (
                    self.player_bowling_dfs[i][["Wkts", "Econ", "Wides"]]
                    .head(len(self.player_bowling_dfs[i].index) - 1)
                    .values.tolist()
                )

                y = (
                    self.player_bowling_dfs[i]["Wkts"]
                    .tail(len(self.player_bowling_dfs[i].index) - 1)
                    .values.tolist()
                )
                x = sc.fit_transform(x)
                lin.fit(x, y)

                Wickets.append(
                    round(
                        lin.predict(
                            self.player_bowling_dfs[i][["Wkts", "Econ", "Wides"]].tail(
                                1
                            )
                        )[0]
                    )
                )
                RsquaredWkt.append(lin.score(x, y))

                y = (
                    self.player_bowling_dfs[i]["Econ"]
                    .tail(len(self.player_bowling_dfs[i].index) - 1)
                    .values.tolist()
                )
                lin.fit(x, y)

                Economy.append(
                    lin.predict(
                        self.player_bowling_dfs[i][["Wkts", "Econ", "Wides"]].tail(1)
                    )[0]
                )
                RsquaredEcon.append(lin.score(x, y))

                y = (
                    self.player_bowling_dfs[i]["Wides"]
                    .tail(len(self.player_bowling_dfs[i].index) - 1)
                    .values.tolist()
                )
                lin.fit(x, y)

                Wides.append(
                    round(
                        lin.predict(
                            self.player_bowling_dfs[i][["Wkts", "Econ", "Wides"]].tail(
                                1
                            )
                        )[0]
                    )
                )
                RsquaredWd.append(lin.score(x, y))

        return pd.DataFrame(
            {
                "Name": Name,
                "Projected Wkts": Wickets,
                "Confidence for Wickets": RsquaredWkt,
                "Projected Econ": Economy,
                "Confidence for Economy": RsquaredEcon,
                "Projected Wides": Wides,
                "Confidence for Wides": RsquaredWd,
            }
        )
