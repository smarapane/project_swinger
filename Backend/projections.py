from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.exceptions import UndefinedMetricWarning
import warnings


class Projections:
    def __init__(self, batters, bowlers):
        self.player_batting_dfs = batters
        self.player_bowling_dfs = bowlers
        self.bat_stats = {}
        self.bowl_stats = {}

    def predict_batting(self):
        """
        Get projected runs and balls for next match.
        Put runs, balls, and batting order no. into model
        """
        sc = StandardScaler()
        lin = RandomForestRegressor(max_features=None)
        for player in self.player_batting_dfs:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
                self.player_batting_dfs[player] = self.player_batting_dfs[
                    player
                ].sort_values(by=["Match Date"], ignore_index=True)

                x = (
                    self.player_batting_dfs[player][
                        ["Runs", "Balls", "Batting Order No."]
                    ]
                    .head(len(self.player_batting_dfs[player].index) - 1)
                    .values.tolist()
                )
                y = (
                    self.player_batting_dfs[player]["Runs"]
                    .tail(len(self.player_batting_dfs[player].index) - 1)
                    .values.tolist()
                )

                x = sc.fit_transform(x)
                lin.fit(x, y)

                Runs = round(
                    lin.predict(
                        self.player_batting_dfs[player][
                            ["Runs", "Balls", "Batting Order No."]
                        ].tail(1)
                    )[0]
                )
                RsquaredRuns = lin.score(x, y)

                y = (
                    self.player_batting_dfs[player]["Balls"]
                    .tail(len(self.player_batting_dfs[player].index) - 1)
                    .values.tolist()
                )
                lin.fit(x, y)

                Balls = round(
                    lin.predict(
                        self.player_batting_dfs[player][
                            ["Runs", "Balls", "Batting Order No."]
                        ].tail(1)
                    )[0]
                )
                RsquaredBalls = lin.score(x, y)

            self.bat_stats[player] = [Runs, Balls, RsquaredRuns, RsquaredBalls]

    def predict_bowling(self):
        """
        Get projected wickets, economy, and wides for next match.
        Put wickets, economy, and wides into model
        """
        sc = StandardScaler()
        lin = RandomForestRegressor(max_features=None)
        for player in self.player_bowling_dfs:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
                self.player_bowling_dfs[player] = self.player_bowling_dfs[
                    player
                ].sort_values(by=["Match Date"], ignore_index=True)

                x = (
                    self.player_bowling_dfs[player][["Wkts", "Econ", "Wides"]]
                    .head(len(self.player_bowling_dfs[player].index) - 1)
                    .values.tolist()
                )

                y = (
                    self.player_bowling_dfs[player]["Wkts"]
                    .tail(len(self.player_bowling_dfs[player].index) - 1)
                    .values.tolist()
                )
                x = sc.fit_transform(x)
                lin.fit(x, y)

                Wickets = round(
                    lin.predict(
                        self.player_bowling_dfs[player][["Wkts", "Econ", "Wides"]].tail(
                            1
                        )
                    )[0]
                )
                RsquaredWkt = lin.score(x, y)

                y = (
                    self.player_bowling_dfs[player]["Econ"]
                    .tail(len(self.player_bowling_dfs[player].index) - 1)
                    .values.tolist()
                )
                lin.fit(x, y)

                Economy = round(
                    lin.predict(
                        self.player_bowling_dfs[player][["Wkts", "Econ", "Wides"]].tail(
                            1
                        )
                    )[0],
                    2,
                )
                RsquaredEcon = lin.score(x, y)

                y = (
                    self.player_bowling_dfs[player]["Wides"]
                    .tail(len(self.player_bowling_dfs[player].index) - 1)
                    .values.tolist()
                )
                lin.fit(x, y)

                Wides = round(
                    lin.predict(
                        self.player_bowling_dfs[player][["Wkts", "Econ", "Wides"]].tail(
                            1
                        )
                    )[0]
                )
                RsquaredWd = lin.score(x, y)

            self.bowl_stats[player] = [
                Wickets,
                Economy,
                Wides,
                RsquaredWkt,
                RsquaredEcon,
                RsquaredWd,
            ]

    def get_batter(self, player):
        """
        Return projections for given player
        """
        return self.bat_stats[player]

    def get_bowler(self, player):
        """
        Return projections for given player
        """
        return self.bowl_stats[player]
