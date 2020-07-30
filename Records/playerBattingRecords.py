import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime as dt
from helper import getMatchInfo


class playerBattingRecords:
    def __init__(self):
        data = open("cricclubs_data/cricclubs_data.json")
        self.cricclubs_data = json.load(data)
        self.player_dfs = dict()

        self.player_dfs["Sidath Marapane"] = pd.read_html(
            self.cricclubs_data["batting"]["sid_bat"]
        )
        self.player_dfs["Sidath Marapane"][1]["Name"] = "Sidath Marapane"
        self.player_dfs["Vardhan Avarsala"] = pd.read_html(
            self.cricclubs_data["batting"]["vardhu_bat"]
        )
        self.player_dfs["Vardhan Avarsala"][1]["Name"] = "Vardhan Avarsala"
        self.player_dfs["Teja Bollimunta"] = pd.read_html(
            self.cricclubs_data["batting"]["teja_bat"]
        )
        self.player_dfs["Teja Bollimunta"][1]["Name"] = "Teja Bollimunta"
        self.player_dfs["Joel Matthew"] = pd.read_html(
            self.cricclubs_data["batting"]["joel_bat"]
        )
        self.player_dfs["Joel Matthew"][1]["Name"] = "Joel Matthew"
        self.player_dfs["Kamil Sacha"] = pd.read_html(
            self.cricclubs_data["batting"]["kamil_bat"]
        )
        self.player_dfs["Kamil Sacha"][1]["Name"] = "Kamil Sacha"
        self.player_dfs["Trey Faglie"] = pd.read_html(
            self.cricclubs_data["batting"]["trey_bat"]
        )
        self.player_dfs["Trey Faglie"][1]["Name"] = "Trey Faglie"
        self.player_dfs["Sam Thomas"] = pd.read_html(
            self.cricclubs_data["batting"]["sam_bat"]
        )
        self.player_dfs["Sam Thomas"][1]["Name"] = "Sam Thomas"
        self.player_dfs["Zubin Parida"] = pd.read_html(
            self.cricclubs_data["batting"]["zubin_bat"]
        )
        self.player_dfs["Zubin Parida"][1]["Name"] = "Zubin Parida"
        self.player_dfs["Vibhav Kavoori"] = pd.read_html(
            self.cricclubs_data["batting"]["vibhav_bat"]
        )
        self.player_dfs["Vibhav Kavoori"][1]["Name"] = "Vibhav Kavoori"
        self.player_dfs["Ryan Jones"] = pd.read_html(
            self.cricclubs_data["batting"]["ryan_bat"]
        )
        self.player_dfs["Ryan Jones"][1]["Name"] = "Ryan Jones"
        self.player_dfs["Aaron Varghese"] = pd.read_html(
            self.cricclubs_data["batting"]["aaron_bat"]
        )
        self.player_dfs["Aaron Varghese"][1]["Name"] = "Aaron Varghese"

    def addOutnOrder(self):
        match_info, match_dates = getMatchInfo(self.cricclubs_data, "sid_bat", 4, 6)
        out_dict = {
            "c": "Caught",
            "b": "Bowled",
            "r": "Run Out",
            "n": "Not Out",
            "R": "Retired",
        }
        for j in range(0, len(match_info)):
            match_date = match_dates[j]
            scorecard = match_info[j]
            for i in range(0, 25, 3):
                name = scorecard.iat[i, 0].replace("*", "")
                if name == "Extras":
                    break
                if name == "Dillon Patel":
                    continue
                out = scorecard.at[i + 2, "B"]
                runs = float(scorecard.at[i, "B"])
                row_change = (
                    self.player_dfs[name]
                    .loc[
                        (self.player_dfs[name]["Match Date"] == match_date)
                        & (self.player_dfs[name]["Runs"] == runs)
                    ]
                    .index.values.astype(int)
                )
                if len(row_change) != 0:
                    row_change = row_change[0]
                    self.player_dfs[name].at[row_change, "Batting Order No."] = (
                        i / 3
                    ) + 1
                    self.player_dfs[name].at[row_change, "Wicket"] = out_dict[out[0]]
                    self.player_dfs[name].at[row_change, "Bowler"] = self.getWicket(out)

        self.player_dfs["Sam Thomas"].at[
            len(self.player_dfs["Sam Thomas"].index) - 1, "Batting Order No."
        ] = 5.0
        self.player_dfs["Sam Thomas"].at[
            len(self.player_dfs["Sam Thomas"].index) - 1, "Wicket"
        ] = "Not Out"

    def getWicket(self, out):
        if out[0] == "b":
            return out[2:]
        if out[0] == "c":
            index = out.find(" b ")
            return out[index + 2 :]
        else:
            return "Not Applicable"

    def clean(self):
        for i in self.player_dfs:
            self.player_dfs[i] = self.player_dfs[i][1][
                ["Name", "Match Date", "Runs", "Balls", "SR"]
            ]
            self.player_dfs[i] = self.player_dfs[i].drop(
                index=len(self.player_dfs[i].index) - 1
            )
            self.player_dfs[i] = self.player_dfs[i][self.player_dfs[i].Runs != "DNB"]
            self.player_dfs[i] = self.player_dfs[i][
                self.player_dfs[i].Balls != 0
            ]  # TODO: fix this
            self.player_dfs[i]["Runs"] = (
                self.player_dfs[i]["Runs"].replace("\*", "", regex=True).astype(float)
            )
            self.player_dfs[i]["Balls"] = self.player_dfs[i]["Balls"].astype(float)
            self.player_dfs[i]["Match Date"] = pd.Series(
                self.player_dfs[i]["Match Date"], dtype="string"
            )

        self.addOutnOrder()

    def getPlayers(self):
        return self.player_dfs

    def test(self):
        self.clean()
        for i in self.player_dfs.values():
            print(i)
