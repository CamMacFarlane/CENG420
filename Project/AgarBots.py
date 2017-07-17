"""
Functions which simplify API calls etc. 
makes a number of Bots, moves them around randomly for a while, gets the state of one and removes all. 
"""

import requests

makePlayerURL = "https://agar-willy-branch.herokuapp.com/createPlayer"
movePlayerURL = "https://agar-willy-branch.herokuapp.com/move"
removePlayerURL = "https://agar-willy-branch.herokuapp.com/removePlayer"
getNearbyObjectsURL = "https://agar-willy-branch.herokuapp.com/getNearbyObjects"

# makePlayer: creates a player with the specified name, ID and mass.

def makeplayer(name, identifier, mass):
	r = requests.post(makePlayerURL, headers={'content-type':'application/json'}, json={"id": identifier, "name": name, "mass": mass})
	print(r)
	print("\nMaking new bot! Name: ", name)
	
# movePlayer: moves specified player in specified direction

def moveplayer(identifier, x, y):
	r = requests.post(movePlayerURL, headers={"content-type": "application/json"}, json={"id": identifier, "x": x, "y": y})
	print(r.status_code, r.reason)
	print("moving ", identifier, " to ", x, " , ", y)

# removePlayer: removes player specified by ID

def removeplayer(identifier):
	r = requests.post(removePlayerURL, headers={"content-type": "application/json"}, json={"id": identifier})
	print(r.status_code, r.reason)

# getNearbyObjects: Calls the GetNearbyObjects API and returns a formatted list which functions with the Threat-measuring function

def getNearbyObjects(identifier):
	r = requests.post(getNearbyObjectsURL, headers={"content-type": "application/json"}, json={"id": identifier})
	print(r.status_code, r.reason)
	data = r.json()
	nearby = {'players': [], 'food': []}
	for entry in data['players']:
		player = {"x" : 0, "y" : 0, "mass" : 0}
		player['x'] = entry['x']
		player['y'] = entry['y']
		player['mass'] = entry['cells'][0]['mass']
		nearby['players'].append(player)
	return nearby

