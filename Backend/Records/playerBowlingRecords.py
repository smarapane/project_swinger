import pandas as pd
import json


class playerBowlingRecords:
    def __init__(self):
        data = open("Backend/cricclubs_data/cricclubs_data.json")
        self.cricclubs_data = json.load(data)
        self.player_dfs = dict()

        self.player_dfs["Sidath Marapane"] = pd.read_html(
            self.cricclubs_data["bowling"]["sid_bowl"]
        )
        self.player_dfs["Sidath Marapane"][1]["Name"] = "Sidath Marapane"
        self.player_dfs["Vardhan Avarsala"] = pd.read_html(
            self.cricclubs_data["bowling"]["vardhu_bowl"]
        )
        self.player_dfs["Vardhan Avarsala"][1]["Name"] = "Vardhan Avarsala"
        self.player_dfs["Teja Bollimunta"] = pd.read_html(
            self.cricclubs_data["bowling"]["teja_bowl"]
        )
        self.player_dfs["Teja Bollimunta"][1]["Name"] = "Teja Bollimunta"
        self.player_dfs["Sam Thomas"] = pd.read_html(
            self.cricclubs_data["bowling"]["sam_bowl"]
        )
        self.player_dfs["Sam Thomas"][1]["Name"] = "Sam Thomas"
        self.player_dfs["Aaron Varghese"] = pd.read_html(
            self.cricclubs_data["bowling"]["aaron_bowl"]
        )
        self.player_dfs["Aaron Varghese"][1]["Name"] = "Aaron Varghese"
        self.player_dfs["Vibhav Kavoori"] = pd.read_html(
            self.cricclubs_data["bowling"]["vibhav_bowl"]
        )
        self.player_dfs["Vibhav Kavoori"][1]["Name"] = "Vibhav Kavoori"

    def clean(self):
        for i in self.player_dfs:
            self.player_dfs[i] = self.player_dfs[i][1][
                [
                    "Name",
                    "Match Date",
                    "Against",
                    "Overs",
                    "Runs",
                    "Wkts",
                    "Econ",
                    "Wides",
                ]
            ]
            self.player_dfs[i] = self.player_dfs[i].drop(
                index=len(self.player_dfs[i].index) - 1
            )
            self.player_dfs[i]["Match Date"] = pd.to_datetime(
                self.player_dfs[i]["Match Date"]
            )
        return self.player_dfs

    def getPlayers(self):
        return self.player_dfs

    def test(self):
        self.clean()
        for i in self.player_dfs:
            print(self.player_dfs[i])
