# SETUP:
# ///////////////////////////////////////////////////////////////////////////////////////////

import numpy as np
import requests
import json
import time

# CONFIG:
# ///////////////////////////////////////////////////////////////////////////////////////////

domain = "https://agar-willy-branch.herokuapp.com"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
bot_name = "Q_bot"

# Q-LEARNING STRUCTURES:
# ///////////////////////////////////////////////////////////////////////////////////////////

memory = list()
current_state = list()

# HYPERPARAMETERS:
# ///////////////////////////////////////////////////////////////////////////////////////////

N = 8                   # Number of sectors/possible actions at each state
MAX_THREAT_LEVEL = 10   # Specifies range [0, MAX_THREAT_LEVEL] for threat scaling
MAX_FOOD_LEVEL = 10     # Specifies range [0, MAX_FOOD_LEVEL]   for food scaling
DEATH_PENALTY = -500    # Value of reward for actions that lead to death
GAMMA = 0.9             # Q-learning discount rate
EPSILON = 1             # Q-learning exploration rate

# FUNCTIONS:
# ///////////////////////////////////////////////////////////////////////////////////////////

# SERVER FUNCTIONS:

def createPlayer(name, identifier):
  removePlayerData = {
    "name": name,
    "id": identifier
  }
  requests.post(domain + '/removePlayer', data=json.dumps(removePlayerData), headers=headers)
  createPlayerData = {
    "name": name,
    "id": identifier
  }
  res = requests.post(domain + '/createPlayer', data=json.dumps(createPlayerData), headers=headers)
  print(res.text)

def movePlayer(identifier, x, y):
  url = domain + '/move'
  moveData = {
    "id": identifier,
    "x": x, 
    "y": y
  }
  requests.post(url, data=json.dumps(moveData), headers=headers)

def getBoardState(identifier):
  url = domain + '/getNearbyObjects'
  data = {
    "id": identifier
  }
  res = requests.post(url, data=json.dumps(data), headers=headers)
  return json.loads(res.text)

def removePlayer(identifier):
  removePlayerData = {
    "name": bot_name,
    "id": identifier
  }
  requests.post(domain + '/removePlayer', data=json.dumps(removePlayerData), headers=headers)

def getNearbyObjects(identifier):
	r = requests.post(getNearbyObjectsURL, headers=headers, json={"id": identifier})
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

# Q-LEARNING FUNCTIONS:

def threat(x, y, mass):
    return mass/np.sqrt(x**2 + y**2)

def distance_inverse(x, y):
    return 1.0/np.sqrt(x**2 + y**2)

def getState(view, N, MAX_THREAT_LEVEL, MAX_FOOD_LEVEL, playerID):
    # extract enemy data
    enemies = [view["players"][k] for k in range(0, len(view["players"]))] 
    
    # generate new information for each enemy
    for k in enemies:
        #need to figure out which player we are then convert the absolute coordinates to relative
        if(k["id"] == playerID):
            player_y = k["y"]
            player_x = k["x"]
            enemies.remove(k)
    
    for k in enemies:
        # new features to be calculated
        if(len(k['cells']) > 0):
            f = dict() #{"angle":, "threat":}
            
            # determine new feature values
            f["angle"] = np.arctan2(k["y"], k["x"])
            f["threat"] = threat(k["x"], k["y"], k['cells'][0]['mass'])
            # add features to each enemy after calculation
            k.update(f)

    # extract food data
    food = [view["food"][k] for k in range(0, len(view["food"]))]
    # calculate angle and distance of food for sector placement
    for k in food:
        f = dict()
        f["angle"] = np.arctan2(k["y"] - player_y, k["x"] - player_x)
        f["distance"] = distance_inverse(abs(k["x"] -player_x), abs(k["y"] - player_y))
        k.update(f)

    # group enemies/food by sector
    # create list to hold information for each sector
    sectors = list()

    # generate sector edges, 
    #   since -pi and pi are count as different edges, need to add 1 to N to get correct angles
    sector_edges = np.linspace(-np.pi, np.pi, N+1)

    # define edges for each sector
    for k in range(0, N):
        f = {"edge1": 0, "edge2": 0, "threats": [], "food": []}

        f["edge1"] = sector_edges[k] 
        f["edge2"] = sector_edges[k+1]
        sectors.append(f)
        
    # define threats in each sector
    for k in enemies:
        if(len(k['cells']) > 0):

            # get enemy angle
            angle = k["angle"]
            # check which sector the enemy is in
            for sector in sectors:
                # if the enemy angle is within the edges of a sector
                if (angle > sector["edge1"] and angle < sector["edge2"]):
                    # add that enemy's threat score to the list of threats in that sector
                    sector["threats"].append(k["threat"])

    # define food in each sector
    for k in food:
        angle = k["angle"]
        # check which sector the enemy is in
        for sector in sectors:
            # if the food angle is within the edges of a sector
            if (angle > sector["edge1"] and angle < sector["edge2"]):
                # add that food score to the list of food in that sector
                sector["food"].append(k["distance"])

    states = [list() for k in range(0, N)]

    # sector threat calc
    # sum all visible threat values
    total_threat = 0;

    for k in enemies:
        try:
            total_threat += k["threat"]
        except:
            print(enemies)
    # for each sector
    
    for k in range(0, N):
        # add threat values for all enemies in that sector
        sector_threat = sum(sectors[k]["threats"])
        
        # divide by total threat to get realtive threat in that sector
        #   use np.ceil() to get an discrete value, overestimate the threat to err on the side of caution
        #   multiply by MAX_THREAT_LEVEL to scale threat into discrete range
        if(total_threat != 0):
            rel_threat = np.ceil((sector_threat/total_threat)*MAX_THREAT_LEVEL)
        else:
            rel_threat = 0
        # add discrete threat value to state list
        states[k].append(rel_threat*10)

    # sector food calc
    total_food = 0 
    for k in food:
        total_food += k["distance"]

    for k in range(0, N):
        rel_food = 0
        if(total_food != 0 ):
            sector_food = sum(sectors[k]["food"])
            rel_food = (sector_food/total_food)
            rel_food = rel_food * MAX_FOOD_LEVEL
            rel_food = np.ceil(rel_food*10)
        states[k].append(rel_food)

    # return states with threat and food scoring calculated
    return states

def reward(state):
    # Calculate the reward for a state
    # state is a list of sectors with [[threat0, food0], [threat1, food1], ... ,[ threaN, foodN]]
    #   for sectors 0 -> N
    
    total_threat = 0
    for k in state:
        total_threat += k[0]

    total_food = 0
    for k in state:
        total_food += k[1]

    return (N*MAX_THREAT_LEVEL - total_threat + total_food)

# MAIN
# ///////////////////////////////////////////////////////////////////////////////////////////

def main():
    pass

main()
