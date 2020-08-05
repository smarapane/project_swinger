import requests
import os
from Backend.Records.playerBattingRecords import playerBattingRecords
from Backend.Records.playerBowlingRecords import playerBowlingRecords
from Backend.projections import Projections
from flask import Flask, request
from settings import BOT_ID

flask_app = Flask(__name__)
pbat = playerBattingRecords()
pbowl = playerBowlingRecords()
pbatters = pbat.getPlayers()
pbowlers = pbowl.getPlayers()
Proj = Projections()


def updateStats():
    Proj = Projections(pbat.clean(), pbowl.clean())


@flask_app.route("/", methods=["GET"])
def retDrBob():
    return "Dr. Bob is running!"


@flask_app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if data["name"] != "Dr. Bob" and "dr bob" in data["text"]:
        parseMessage(data["text"], data)

    return "ok", 200


def parseMessage(message, data):
    msg = "I didn't quite catch that. "
    if (
        "hi" in message.lower()
        or "hello" in message.lower()
        or "howdy" in message.lower()
    ):
        msg = f"What's up {data['name']}!"
    elif "bye" in message.lower():
        msg = f"See ya later {data['name']}!"
    elif "batting" in message.lower():
        for batter in pbatters:
            if batter.split[0].lower() in message.lower():
                retProj = Proj.predict_batting(batter)
                msg = f"{batter}'s projected performance for the next game is {retProj[0]} runs in {retProj[1]} balls."
                break
            else:
                msg = "I couldn't find that player. Ask me for a list of batters or how to use me to get projections."
    elif "bowling" in message.lower():
        for bowler in pbowlers:
            if bowler.split[0].lower() in message.lower():
                retProj = Proj.predict_bowling(bowler)
                msg = f"{bowler}'s projected performance for the next game is {retProj[0]} wickets, {retProj[1]} wides, at an economy of {retProj[2]} runs."
            else:
                msg = "I couldn't find that player. Ask me for a list of bowlers or how to use me to get projections."
    elif "batters" in message.lower():
        msg = "Batters: "
        for batter in pbatters:
            msg += f"{batter}, "
        msg = msg[:-2]
    elif "bowlers" in message.lower():
        msg = "Bowlers: "
        for bowler in pbowlers:
            msg += f"{bowler}, "
        msg = msg[:-2]
    elif "info" in message.lower():
        msg = "For bowling/batting projections, ask me for a players bowling/batting projection. (ex. 'Dr. Bob, what are Sidath's batting projections?\n"
        msg += "For a list of batters/bowlers, ask me for the bowlers/batters on the squad. (ex. 'Dr. Bob, who are the bowlers on the squad?\n"
        msg += "For these instructions again, simply ask for info about me."

    send_message(msg)


def send_message(message):
    url = "https://api.groupme.com/v3/bots/post"

    data = {"bot_id": BOT_ID, "text": message}

    response = requests.post(url, params=data)
    print(response)


if __name__ == "__main__":
    updateStats()
    flask_app.run()
