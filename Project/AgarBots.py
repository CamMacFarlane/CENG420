"""
Functions which simplify API calls etc. 
makes a number of Bots, moves them around randomly for a while, gets the state of one and removes all. 
"""

import requests
import math
DEBUG = True

makePlayerURL = "https://agar-willy-branch.herokuapp.com/createPlayer"
movePlayerURL = "https://agar-willy-branch.herokuapp.com/move"
removePlayerURL = "https://agar-willy-branch.herokuapp.com/removePlayer"
getNearbyObjectsURL = "https://agar-willy-branch.herokuapp.com/getNearbyObjects"
createStaticObstaclesURL = "https://agar-willy-branch.herokuapp.com/createStaticObstacles"
getPlayerInfoURL = "https://agar-willy-branch.herokuapp.com/getPlayerInfo"

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

def move(identifier, N, maxN):
	direction = 0 + (N * 2 * math.pi / maxN) + (math.pi / maxN)
	x = 200 * math.cos(direction)
	y = 200 * math.sin(direction)
	moveplayer(identifier, x, y)

def isAlive(identifier):
	r = requests.post(getPlayerInfoURL, headers={"content-type": "application/json"}, json={"id": identifier})
	if DEBUG: print(r.status_code, r.reason)
	try:
		data = r.json()
		return True
	except ValueError:
		return False

