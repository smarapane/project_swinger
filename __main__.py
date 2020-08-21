from Backend.Records.playerBattingRecords import playerBattingRecords
from Backend.Records.playerBowlingRecords import playerBowlingRecords
from Backend.projections import Projections
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64
import pandas as pd
from flask import Flask, render_template, request, jsonify
import sys
from functools import partial

app = Flask(
    __name__, template_folder="Frontend", static_url_path="/", static_folder="Frontend"
)

bat = playerBattingRecords()
bowl = playerBowlingRecords()
projection = Projections(bat.clean(), bowl.clean())
batters = bat.getPlayers()
bowlers = bowl.getPlayers()


@app.route("/get_player", methods=["GET"])
def get_stats():
    player = request.args.get("player")
    graphs = get_graphs(player)
    stats = projection.predict_batting(player)
    plural = get_plural("bat", stats)
    bat_stats = f"{player.split()[0]} is projected to bat {stats[0]} {plural[0]} in {stats[1]} {plural[1]}."
    bowl_stats = "He did not bowl this season."
    if player in bowlers.keys():
        stats = projection.predict_bowling(player)
        plural = get_plural("bowl", stats)
        bowl_stats = f"He is also projected to bowl {stats[0]} {plural[0]} and {stats[2]} {plural[1]} at an economy of {stats[1]} {plural[2]} an over."
    return jsonify({"bat_proj": bat_stats, "bowl_proj": bowl_stats, "graphs": graphs})


def get_plural(innings, stats):
    plural = []
    if innings == "bat":
        plural_runs = "runs" if stats[0] != 1 else "run"
        plural_balls = "balls" if stats[1] != 1 else "ball"
        plural.extend([plural_runs, plural_balls])
    else:
        plural_wickets = "wickets" if stats[0] != 1 else "wicket"
        plural_wides = "wides" if stats[1] != 1 else "wide"
        plural_runs = "runs" if stats[2] != 1 else "run"
        plural.extend([plural_wickets, plural_wides, plural_runs])
    return plural


def get_graphs(player):
    png_strings = []
    graph_funcs = [
        bat.plot_runs,
        bat.plot_runs_per_team,
        partial(bat.plot_per_batno, key="Runs"),
        partial(bat.plot_per_batno, key="SR"),
        bat.plot_wicket,
        bat.plot_bowler,
        bat.table,
    ]
    for func in graph_funcs:
        fig = func(player=player)
        output = BytesIO()
        FigureCanvas(fig).print_png(output)
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(output.getvalue()).decode("utf8")
        png_strings.append(pngImageB64String)
    if player in bowlers.keys():
        graph_funcs = [
            partial(bowl.plot_over_time, key="Wkts"),
            partial(bowl.plot_over_time, key="Econ"),
            partial(bowl.plot_over_time, key="Wides"),
            partial(bowl.plot_per_team, key="Wkts"),
            partial(bowl.plot_per_team, key="Runs"),
            bowl.table,
        ]
        for func in graph_funcs:
            fig = func(player=player)
            output = BytesIO()
            FigureCanvas(fig).print_png(output)
            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(output.getvalue()).decode("utf8")
            png_strings.append(pngImageB64String)
    return png_strings


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", players=bat.getPlayers())


if __name__ == "__main__":
    app.run()
    # bat.test()
    # bowl.test()
