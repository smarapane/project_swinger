import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime as dt


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

    def addOutnOrder(self):
        req = requests.get(self.cricclubs_data["batting"]["sid_bat"])
        soup = BeautifulSoup(req.content, "lxml")
        parsed_table = soup.find_all("table")[1]
        for tag in parsed_table.find_all("a"):
            if not tag.has_attr("class"):
                url = "https://cricclubs.com" + tag["href"]
                match_date = dt.strftime(
                    dt.strptime(
                        pd.read_html(url)[8].iloc[1]["Match Details.1"], "%m/%d/%Y"
                    ),
                    "%m/%d/%Y",
                )
                scorecard_num = 4 if "Sidath" in pd.read_html(url)[4].columns[0] else 6
                scorecard = pd.read_html(url)[scorecard_num]
                for i in range(0, 25, 3):
                    name = scorecard.iat[i, 0].replace("*", "")
                    if name == "Extras":
                        break
                    if name == "Dillon Patel":
                        continue
                    out = scorecard.at[i + 2, "B"]
                    runs = float(scorecard.at[i, "B"])
                    self.player_dfs[name]["Batting Order No."] = -1
                    # print(match_date)
                    # print(len(self.player_dfs[name][self.player_dfs[name]['Match Date'] == match_date]['Match Date']))
                    self.player_dfs[name].loc[
                        (self.player_dfs[name]["Match Date"] == match_date),
                        "Batting Order No.",
                    ] = (i / 3) + 1

    def clean(self):
        for i in self.player_dfs:
            self.player_dfs[i] = self.player_dfs[i][1][
                ["Name", "Match Date", "Runs", "Balls", "SR"]
            ]
            self.player_dfs[i] = self.player_dfs[i].drop(
                index=len(self.player_dfs[i].index) - 1
            )
            self.player_dfs[i] = self.player_dfs[i][self.player_dfs[i].Runs != "DNB"]
            self.player_dfs[i] = self.player_dfs[i][self.player_dfs[i].Balls != 0]
            self.player_dfs[i]["Runs"] = (
                self.player_dfs[i]["Runs"].replace("\*", "", regex=True).astype(float)
            )
            self.player_dfs[i]["Balls"] = self.player_dfs[i]["Balls"].astype(float)
            self.player_dfs[i]["Match Date"] = pd.Series(
                self.player_dfs[i]["Match Date"], dtype="string"
            )

        return self.player_dfs

    def test(self):
        self.clean()
        self.addOutnOrder()
        for i in self.player_dfs.values():
            print(i)
