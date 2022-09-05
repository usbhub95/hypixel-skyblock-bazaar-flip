# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 15:21:12 2022

@author: usbhu
"""

from requests import get
from json import dump
import csv
from os import startfile
from operator import itemgetter

# get user's money
cash = int(input("money to spend?"))/7

# get data from api
bazaarJson = get("https://api.hypixel.net/skyblock/bazaar").json()
itemsJson = get("https://api.hypixel.net/resources/skyblock/items").json()

# ergonomics
bazaar = bazaarJson["products"]
items = itemsJson["items"]
bazaarProcessed = []
fieldNames = ["Name", "Sell Price", "Hourly Instasells", "NPC Price", "NPC Margin", "Profit Ratio", "Score", "Amount to Buy"]

# grab wanted items and data
for i in items:
    if (i["id"] in bazaar.keys()) and (i.get("npc_sell_price", False)):
        try:
            npcMargin = i["npc_sell_price"]-(bazaar[i["id"]]["sell_summary"][0]["pricePerUnit"]+0.1)
        except IndexError:
            npcMargin = 0
            
        if (npcMargin > 0) and (bazaar[i["id"]]["quick_status"]["sellMovingWeek"]/168 >= 33600) and (bazaar["ENDER_PEARL"]["sell_summary"][0]["pricePerUnit"] < bazaar[i["id"]]["sell_summary"][0]["pricePerUnit"]):
            index = len(bazaarProcessed)
            bazaarProcessed.insert(index, {"Name":i["name"]})
            
            try:
                bazaarProcessed[index]["Sell Price"] = bazaar[i["id"]]["sell_summary"][0]["pricePerUnit"]
            except IndexError:
                bazaarProcessed[index]["Sell Price"] = 1
            
            bazaarProcessed[index]["Hourly Instasells"] = bazaar[i["id"]]["quick_status"]["sellMovingWeek"]/168
            bazaarProcessed[index]["NPC Price"] = i["npc_sell_price"]
            bazaarProcessed[index]["NPC Margin"] = npcMargin
            bazaarProcessed[index]["Profit Ratio"] = npcMargin/bazaarProcessed[index]["NPC Price"]
            bazaarProcessed[index]["Score"] = bazaarProcessed[index]["Profit Ratio"]*npcMargin
            bazaarProcessed[index]["Amount to Buy"] = cash//bazaarProcessed[index]["Sell Price"]

bazaarProcessed.sort(key=itemgetter("Score"), reverse=True)

# save the data!
with open("bazaarData.json", "w") as file:
    dump(bazaarJson, file)

with open("itemsData.json", "w") as file:
    dump(itemsJson, file)

with open("bazaarProcessed.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames = fieldNames)
    writer.writeheader()
    writer.writerows(bazaarProcessed)
    
# open the calculated file
startfile("bazaarProcessed.csv")