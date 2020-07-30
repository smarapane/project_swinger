from Records.playerBattingRecords import playerBattingRecords
from Records.playerBowlingRecords import playerBowlingRecords
from projections import Projections
import os
import pandas as pd


bat = playerBattingRecords()
bowl = playerBowlingRecords()
projection = Projections(bat, bowl)

while True:
    input("Hit anything to continue")
    os.system("cls")

    print("What would you like to do?")
    print("'btr' to view batting records")
    print("'blr' to view bowling records")
    print("'predbat' to view batting projections")
    print("'predbowl' to view bowling projections")
    print("'exit' to exit the program")

    view = input("I would like to: ")
    os.system("cls")

    if view == "save":
        pbat = pd.concat(bat.getPlayers())
        pbowl = pd.concat(bowl.getPlayers())
        pbat.to_csv(
            r"C:\Users\smara\OneDrive - University of Cincinnati\project_swinger\pbat.csv"
        )
        pbowl.to_csv(
            r"C:\Users\smara\OneDrive - University of Cincinnati\project_swinger\pbowl.csv"
        )

    if view == "btr":
        players = bat.getPlayers()
        view = input("Enter the player's full name or 'all' to view stats: ")
        if view == "all":
            for i in players.values():
                print(i)
        elif view in players:
            print(players[view])
        else:
            print("Name not found!")

    elif view == "blr":
        players = bowl.getPlayers()
        view = input("Enter the player's full name or 'all' to view stats: ")
        if view == "all":
            for i in players.values():
                print(i)
        elif view in players:
            print(players[view])
        else:
            print("Name not found!")

    elif view == "predbat":
        projs = projection.predict_batting()
        view = input("Enter the player's full name or 'all' to view stats: ")
        if view == "all":
            print(projs)
        elif view in projs.Name.values:
            print(projs.loc[projs["Name"] == view])
        else:
            print("Name not found!")

    elif view == "predbowl":
        projs = projection.predict_bowling()
        view = input("Enter the player's full name or 'all' to view stats: ")
        if view == "all":
            print(projs)
        elif view in projs.Name.values:
            print(projs.loc[projs["Name"] == view])
        else:
            print("Name not found!")

    elif view == "exit":
        print("Goodbye!")
        break
    else:
        print("Invalid input. Exitting!")
