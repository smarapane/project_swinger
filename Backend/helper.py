import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime as dt
import pandas as pd

# I thought I would have to use this method for bowling stats as well
# which did not end up happening


def getMatchInfo(data, innings, scorecard_loc1, scorecard_loc2):
    """
    Get the links from the personal websites and return match information
    """
    req = requests.get(data["batting"][innings])
    soup = BeautifulSoup(req.content, "lxml")
    parsed_table = soup.find_all("table")[1]
    match_info = []
    match_dates = []
    for tag in parsed_table.find_all("a"):
        if not tag.has_attr("class"):
            url = "https://cricclubs.com" + tag["href"]
            match_dates.append(
                dt.strftime(
                    dt.strptime(
                        pd.read_html(url)[8].iloc[1]["Match Details.1"], "%m/%d/%Y"
                    ),
                    "%m/%d/%Y",
                )
            )
            scorecard_num = (
                scorecard_loc1
                if "Sidath" in pd.read_html(url)[scorecard_loc1].columns[0]
                else scorecard_loc2
            )
            match_info.append(pd.read_html(url)[scorecard_num])

    return match_info, match_dates
