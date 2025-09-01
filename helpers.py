import json
import sys
import os

def UpdateJSON(path, newData, flag="message"):
    # Get Data
    oldData = None
    with open(path, "r") as file:
        oldData = json.load(file)

    # Update Using Flag
    if flag == "message":
        oldData["messages"].append(newData)
    else:
        print("No Vaild Flag Given!")

    with open(path, "w") as file:
        json.dump(oldData, file, indent=4)


def ReadJSON(path, flag="message"):
    if flag == "message":
        with open(path, "r") as file:
            data = json.load(file)
            return data
    else:
        print("No Vaild Flag Given!")