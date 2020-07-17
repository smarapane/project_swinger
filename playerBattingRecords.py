import pandas as pd
import json
import lxml
import html5lib


class playerBattingRecords():

    def __init__(self):
        data = open("cricclubs_data.json")
        self.cricclubs_data = json.load(data)
        self.player_dfs = []

        self.sid_dfs = pd.read_html(self.cricclubs_data["batting"]["sid_bat"])
        self.sid_dfs[1]['Name'] = 'Sidath'
        self.vardhu_dfs = pd.read_html(self.cricclubs_data["batting"]["vardhu_bat"])
        self.vardhu_dfs[1]['Name'] = 'Vardhan'
        self.teja_dfs = pd.read_html(self.cricclubs_data["batting"]["teja_bat"])
        self.teja_dfs[1]['Name'] = 'Teja'
        self.joel_dfs = pd.read_html(self.cricclubs_data["batting"]["joel_bat"])
        self.joel_dfs[1]['Name'] = 'Joel'
        self.kamil_dfs = pd.read_html(self.cricclubs_data["batting"]["kamil_bat"])
        self.kamil_dfs[1]['Name'] = 'Kamil'
        self.trey_dfs = pd.read_html(self.cricclubs_data["batting"]["trey_bat"])
        self.trey_dfs[1]['Name'] = 'Trey'
        self.sam_dfs = pd.read_html(self.cricclubs_data["batting"]["sam_bat"])
        self.sam_dfs[1]['Name'] = 'Sam'
        self.zubin_dfs = pd.read_html(self.cricclubs_data["batting"]["zubin_bat"])
        self.zubin_dfs[1]['Name'] = 'Zubin'

        self.player_dfs.append(self.sid_dfs)
        self.player_dfs.append(self.vardhu_dfs)
        self.player_dfs.append(self.teja_dfs)
        self.player_dfs.append(self.joel_dfs)
        self.player_dfs.append(self.kamil_dfs)
        self.player_dfs.append(self.trey_dfs)
        self.player_dfs.append(self.sam_dfs)
        self.player_dfs.append(self.zubin_dfs)

    def clean(self):
        for i in range(len(self.player_dfs)):
            self.player_dfs[i] = self.player_dfs[i][1][['Name', 'Match Date', 'Runs', 'Balls', 'SR']]
            self.player_dfs[i] = self.player_dfs[i].drop(index=len(self.player_dfs[i].index)-1)
            self.player_dfs[i] = self.player_dfs[i][self.player_dfs[i].Runs != "DNB"]
            self.player_dfs[i]['Runs'] = self.player_dfs[i]['Runs'].replace('\*', '', regex=True).astype(float)
            self.player_dfs[i]['Balls'] = self.player_dfs[i]['Balls'].astype(float)
            self.player_dfs[i]['Match Date'] = pd.to_datetime(self.player_dfs[i]['Match Date'])

        return pd.concat(self.player_dfs, ignore_index=True)

    def test(self):
        print(self.clean())
