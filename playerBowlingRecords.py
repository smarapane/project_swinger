import pandas as pd
import json
import lxml
import html5lib


class playerBowlingRecords():

    def __init__(self):
        data = open("cricclubs_data.json")
        self.cricclubs_data = json.load(data)
        self.player_dfs = []

        self.sid_dfs = pd.read_html(self.cricclubs_data["bowling"]["sid_bowl"])
        self.sid_dfs[1]['Name'] = 'Sidath'
        self.vardhu_dfs = pd.read_html(self.cricclubs_data["bowling"]["vardhu_bowl"])
        self.vardhu_dfs[1]['Name'] = 'Vardhan'
        self.teja_dfs = pd.read_html(self.cricclubs_data["bowling"]["teja_bowl"])
        self.teja_dfs[1]['Name'] = 'Teja'
        self.sam_dfs = pd.read_html(self.cricclubs_data["bowling"]["sam_bowl"])
        self.sam_dfs[1]['Name'] = 'Sam'

        self.player_dfs.append(self.sid_dfs)
        self.player_dfs.append(self.vardhu_dfs)
        self.player_dfs.append(self.teja_dfs)
        self.player_dfs.append(self.sam_dfs)

    def clean(self):
        for i in range(len(self.player_dfs)):
            self.player_dfs[i] = self.player_dfs[i][1][['Name', 'Match Date', 'Overs', 'Runs', 'Wkts', 'Econ', 'Wides']]
            self.player_dfs[i] = self.player_dfs[i].drop(index=len(self.player_dfs[i].index)-1)
            self.player_dfs[i]['Match Date'] = pd.to_datetime(self.player_dfs[i]['Match Date'])

        return pd.concat(self.player_dfs, ignore_index=True)

    def test(self):
        print(self.clean())
