"""
Use this when the AgarBots Script hits an error mid-way and fails to remove bots. 
"""

import requests
import random
import time

NUM_BOTS = 10

removePlayerURL = "https://agar-willy-branch.herokuapp.com/removePlayer"

def removeplayer(identifier):
	r = requests.post(removePlayerURL, headers={"content-type": "application/json"}, json={"id": identifier})
	print(r.status_code, r.reason)

ID = str(4732)

for i in range(0, NUM_BOTS):
	playerID = ID + str(i)
	removeplayer(playerID)

