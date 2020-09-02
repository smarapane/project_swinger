import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class playerBowlingRecords:
    def __init__(self):
        """
        Get player data from json file which contains the personal stats site
        """
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
        """
        Clean the dataframes
        """
        for i in self.player_dfs:
            self.player_dfs[i] = self.player_dfs[i][1][
                [
                    "Name",
                    "Match Date",
                    "Against",
                    "Winner",
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
            self.player_dfs[i]["Match Date"] = pd.to_datetime(
                self.player_dfs[i]["Match Date"]
            )
        return self.player_dfs

    def getPlayers(self):
        """
        Return player dataframes
        """
        return self.player_dfs

    def plot_over_time(self, player, key):
        """
        Plot given key (Wkts, Econ, Wides) over time in line plot
        """
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        full_name = {"Wkts": "Wickets", "Econ": "Economy", "Wides": "Wides"}
        axis.set_title(f"{player}'s {full_name[key]} Over Time")
        axis.set_xlabel("Match Date")
        axis.set_ylabel(full_name[key])
        average_val = self.player_dfs[player].copy()
        average_val["Match Date"] = pd.to_datetime(average_val["Match Date"])
        average_val["Match Date"] = average_val["Match Date"].dt.strftime("%m/%d")
        average_val = average_val.groupby("Match Date").mean()
        average_val = average_val.sort_values(by="Match Date", ascending=True)
        axis.plot(average_val.index, average_val[key])
        return fig

    def plot_per_team(self, player, key):
        """
        Plot given key (Wkts, Runs) in pie chart
        """
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        full_name = {"Wkts": "Wickets", "Runs": "Runs"}
        teams = self.player_dfs[player]["Against"].unique().tolist()
        vals = [0 for i in range(len(teams))]
        total_vals = 0

        for index, row in self.player_dfs[player].iterrows():
            vals[teams.index(row["Against"])] += row[key]
            total_vals += row[key]

        wedges, texts, autotexts = axis.pie(
            vals, labels=teams, autopct="", textprops=dict(color="w")
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
            a.set_text(
                f"{round((vals[i]/total_vals) * 100)}%\n({vals[i]} {key.lower()})"
            )

        plt.setp(autotexts, size=8, weight="bold")
        axis.set_title(f"{full_name[key]} Per Team")
        return fig

    def table(self, player):
        """
        Create table of player bowling stats
        """
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        player_table = self.player_dfs[player].copy()
        player_table = player_table.drop(["Name"], axis=1)
        player_table["Match Date"] = pd.to_datetime(player_table["Match Date"]).dt.date
        the_table = axis.table(
            cellText=player_table.to_numpy().tolist(),
            colLabels=player_table.columns,
            loc="center",
        )
        the_table.auto_set_column_width(range(10))
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(10)
        the_table.scale(1, 1.5)
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        axis.axis("off")
        return fig
