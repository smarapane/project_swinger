import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from Backend.helper import getMatchInfo
import sys


class playerBattingRecords:
    def __init__(self):
        data = open("Backend/cricclubs_data/cricclubs_data.json")
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
            "S": "Stumped",
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
        self.player_dfs["Sam Thomas"].at[
            len(self.player_dfs["Sam Thomas"].index) - 1, "Bowler"
        ] = "Not Applicable"

    def getWicket(self, out):
        if out[0] == "b":
            return out[2:]
        if out[0] == "c" or out[0] == "s":
            index = out.find(" b ")
            return out[index + 3 :]
        else:
            return "Not Applicable"

    def clean(self):
        for i in self.player_dfs:
            self.player_dfs[i] = self.player_dfs[i][1][
                ["Name", "Match Date", "Against", "Winner", "Runs", "Balls", "SR"]
            ]
            self.player_dfs[i] = self.player_dfs[i].drop(
                index=len(self.player_dfs[i].index) - 1
            )
            self.player_dfs[i].rename(columns={"Winner": "Win"}, inplace=True)
            self.player_dfs[i].loc[
                (self.player_dfs[i]["Win"] == "Sidath's Big Bad Boofas"), "Win"
            ] = "W"
            self.player_dfs[i].loc[
                (
                    (self.player_dfs[i]["Win"] != "Sidath's Big Bad Boofas")
                    & (self.player_dfs[i]["Win"] != "W")
                ),
                "Win",
            ] = "L"
            self.player_dfs[i] = self.player_dfs[i][self.player_dfs[i].Runs != "DNB"]
            self.player_dfs[i] = self.player_dfs[i][self.player_dfs[i].Balls != 0]
            self.player_dfs[i]["Runs"] = (
                self.player_dfs[i]["Runs"].replace("\*", "", regex=True).astype(float)
            )
            self.player_dfs[i]["Balls"] = self.player_dfs[i]["Balls"].astype(float)
            self.player_dfs[i]["Match Date"] = pd.Series(
                self.player_dfs[i]["Match Date"], dtype="string"
            )

        self.addOutnOrder()
        return self.player_dfs

    def getPlayers(self):
        return self.player_dfs

    def plot_runs(self, player):
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.set_title(f"{player}'s Runs Over Time")
        axis.set_xlabel("Match Date")
        axis.set_ylabel("Runs")
        runs_dfs = self.player_dfs[player].copy()
        runs_dfs["Match Date"] = pd.to_datetime(runs_dfs["Match Date"])
        runs_dfs["Match Date"] = runs_dfs["Match Date"].dt.strftime("%m/%d")
        runs_dfs = runs_dfs.sort_values(by="Match Date", ascending=True)
        axis.plot(runs_dfs["Match Date"], runs_dfs["Runs"])
        return fig

    def plot_runs_per_team(self, player):
        fig = Figure(tight_layout=True)
        axis = fig.add_subplot(1, 1, 1)
        teams = self.player_dfs[player]["Against"].unique().tolist()
        runs = [0 for i in range(len(teams))]
        total_runs = 0

        for index, row in self.player_dfs[player].iterrows():
            runs[teams.index(row["Against"])] += row["Runs"]
            total_runs += row["Runs"]

        wedges, texts, autotexts = axis.pie(
            runs, labels=teams, autopct="", textprops=dict(color="w")
        )
        axis.legend(
            wedges,
            teams,
            title="Teams",
            loc="upper right",
            bbox_to_anchor=(1, 1),
            bbox_transform=plt.gcf().transFigure,
        )

        for i, a in enumerate(autotexts):
            a.set_text(f"{round((runs[i]/total_runs) * 100)}%\n({runs[i]} runs)")

        plt.setp(autotexts, size=13, weight="bold")
        axis.set_title("Runs Per Team")
        return fig

    def plot_per_batno(self, player, key):
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.scatter(
            self.player_dfs[player]["Batting Order No."], self.player_dfs[player][key]
        )
        axis.set_title(f"{player}'s {key} at Each Batting Order Position'")
        axis.set_xlabel("Batting Order Number")
        axis.set_ylabel(key)
        return fig

    def plot_wicket(self, player):
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        wickets = self.player_dfs[player]["Wicket"].unique().tolist()
        count = [0 for i in range(len(wickets))]
        for index, row in self.player_dfs[player].iterrows():
            count[wickets.index(row["Wicket"])] += 1
        axis.bar(wickets, count)
        axis.set_title("Count of Wicket")
        axis.set_xlabel("Wicket")
        axis.set_ylabel("Count")
        return fig

    def plot_bowler(self, player):
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        only_bowlers = self.player_dfs[player].loc[
            self.player_dfs[player]["Bowler"] != "Not Applicable"
        ]
        bowler = only_bowlers["Bowler"].unique().tolist()
        count = [0 for i in range(len(bowler))]
        for index, row in only_bowlers.iterrows():
            count[bowler.index(row["Bowler"])] += 1
        axis.bar(bowler, count)
        axis.set_title("Bowlers Who Took Wickets")
        axis.set_xlabel("Bowler")
        axis.set_ylabel("Count")
        return fig

    def table(self, player):
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        player_table = self.player_dfs[player].copy()
        player_table = player_table.drop(["Name"], axis=1)
        the_table = axis.table(
            cellText=player_table.to_numpy().tolist(),
            colLabels=player_table.columns,
            loc="center",
        )
        the_table.auto_set_column_width(range(10))
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(8.1)
        ax = fig.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        axis.axis("off")
        fig.subplots_adjust(right=0.867)
        return fig

    def test(self):
        self.table("Sidath Marapane")
