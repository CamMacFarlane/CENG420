"""
Functions which simplify API calls etc. 
makes a number of Bots, moves them around randomly for a while, gets the state of one and removes all. 
"""

import requests
import math
DEBUG = True

url = "http://localhost:3000/"


makePlayerURL = url + "createPlayer"
movePlayerURL = url + "move"
removePlayerURL = url + "removePlayer"
getNearbyObjectsURL = url + "getNearbyObjects"
createStaticObstaclesURL = url + "createStaticObstacles"
getPlayerInfoURL = url + "getPlayerInfo"

# makePlayer: creates a player with the specified name, ID and mass.

def makeplayer(name, identifier, mass):
	r = requests.post(makePlayerURL, headers={'content-type':'application/json'}, json={"id": identifier, "name": name, "mass": mass})
	if DEBUG: print(r)
	if DEBUG: print("\nMaking new bot! Name: ", name)
	
# movePlayer: moves specified player in specified direction

def moveplayer(identifier, x, y):
	r = requests.post(movePlayerURL, headers={"content-type": "application/json"}, json={"id": identifier, "x": x, "y": y})
	if DEBUG: print(r.status_code, r.reason)
	if DEBUG: print("moving ", identifier, " to ", x, " , ", y)

# removePlayer: removes player specified by ID

def removeplayer(identifier):
	r = requests.post(removePlayerURL, headers={"content-type": "application/json"}, json={"id": identifier})
	if DEBUG: print(r.status_code, r.reason)

def createStaticObstacles(number):
	r = requests.post(createStaticObstaclesURL, headers={"content-type": "application/json"}, json={"numberOfBots": number})
	if DEBUG: print(r.status_code, r.reason)

# getNearbyObjects: Calls the GetNearbyObjects API and returns a formatted list which functions with the Threat-measuring function

def getNearbyObjects(identifier):
	r = requests.post(getNearbyObjectsURL, headers={"content-type": "application/json"}, json={"id": identifier})
	if DEBUG: print(r.status_code, r.reason)
	data = r.json()
	nearby = {'players': [], 'food': []}
	for entry in data['players']:
		player = {"x" : 0, "y" : 0, "mass" : 0}
		player['x'] = entry['x']
		player['y'] = entry['y']
		player['mass'] = entry['cells'][0]['mass']
		nearby['players'].append(player)
	return nearby

# move: instructs specified player to move in direction specified by sector # and total # of sectors. 

def move(identifier, N, maxN=8):
	direction = 0 + ((maxN -1)/maxN)*(-math.pi) + N*(2*math.pi/maxN)
	x = 200 * math.cos(direction)
	y = 200 * math.sin(direction)
	moveplayer(identifier, x, y)

# isAlive: returns True if the player specified is currently alive. To be used in while(isAlive) context

def isAlive(identifier):
	r = requests.post(getPlayerInfoURL, headers={"content-type": "application/json"}, json={"id": identifier})
	if DEBUG: print(r.status_code, r.reason)
	try:
		data = r.json()
		if DEBUG: print(data)
		return True
	except ValueError:
		return False

def getView(identifier):
	if DEBUG: print(getNearbyObjectsURL)
	r = requests.post(getNearbyObjectsURL, headers={"content-type": "application/json"}, json={"id": identifier})
	if DEBUG: print(r.status_code, r.reason)
	data = r.json()
	return data

# startGame: needed for learning.py. 
# creates N static bots and a single 'player' bot. Returns the ID of the player. 
