from Backend.Records.playerBattingRecords import playerBattingRecords
from Backend.Records.playerBowlingRecords import playerBowlingRecords
from Backend.projections import Projections
import pandas as pd
from flask import Flask, render_template, request
import sys

app = Flask(
    __name__, template_folder="Frontend", static_url_path="/", static_folder="Frontend"
)

bat = playerBattingRecords()
bowl = playerBowlingRecords()
# projection = Projections(bat.clean(), bowl.clean())


@app.route("/", methods=["POST", "GET"])
def dropdown():
    if request.method == "POST":
        print(request.form["player_selection"])
        return "ok", 200
    return render_template("index.html", players=bat.getPlayers())


if __name__ == "__main__":
    # app.run()
    pbat = playerBattingRecords()
    pbowl = playerBowlingRecords()
    pbatters = pd.concat(pbat.clean())
    pbowlers = pd.concat(pbowl.clean())
    pbatters.to_csv("pbat.csv")
    pbowlers.to_csv("pbowl.csv")
