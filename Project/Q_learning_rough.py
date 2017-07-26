# SETUP:
# ///////////////////////////////////////////////////////////////////////////////////////////

import numpy as np
import requests
import json
import time
import random
import math

# SERVER CONFIG:
# ///////////////////////////////////////////////////////////////////////////////////////////

domain = "http://localhost:3000"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
bot_name = "Q_bot"

# Q-LEARNING AND STATE INFO:
# ///////////////////////////////////////////////////////////////////////////////////////////

memory = list()
# memory = { {  'state': [ [threat0, food0], [threat1, food1], ..., [threatN, foodN] ], 
#               'action': number in interval [0, N], 
#               'reward': reward value for new state, 
#               'new_state': [ [threat0, food0], [threat1, food1], ..., [threatN, foodN] ] },
#            ...,
#            {}
#          }

current_state = list()
previous_state = list()

# HYPERPARAMETERS:
# ///////////////////////////////////////////////////////////////////////////////////////////

N = 16                   # Number of sectors/possible actions at each state
MAX_THREAT_LEVEL = 10   # Specifies range [0, MAX_THREAT_LEVEL] for threat scaling
MAX_FOOD_LEVEL = 10     # Specifies range [0, MAX_FOOD_LEVEL]   for food scaling
REWARD_FOR_EATING = 10
DEATH_PENALTY = -500    # Value of reward for actions that lead to death
GAMMA = 0.9             # Q-learning discount rate
EPSILON = 1             # Q-learning exploration rate

previousLargestMass = 0
previousTotalMass = 0

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

def removePlayer(name, identifier):
  removePlayerData = {
    "name": name,
    "id": identifier
  }
  res = requests.post(domain + '/removePlayer', data=json.dumps(removePlayerData), headers=headers)
  print(res.text)

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
    movePlayer(identifier, x, y)

def createStaticBots(number):
    for i in range(0, number):
        name = "staticBot_" + str(i)
        createPlayer(name, name)

def removeStaticBots(number):
    for i in range(0, number):
        name = "staticBot_" + str(i)
        removePlayer(name, name)


# Q-LEARNING FUNCTIONS:

def threat(x, y, mass):
    return mass/np.sqrt(x**2 + y**2)

def distance_inverse(x, y):
    return 1.0/np.sqrt(x**2 + y**2)

#Get the mass of a player, extracts the largest mass cell as well as the total mass
def getMassOfPlayer(playerJSON):
    totalMass = 0
    largestMass = 0
    # print(playerJSON)
    cells = [playerJSON["cells"][k] for k in range(len(playerJSON["cells"]))]
    # print(cells)
    for k in cells:
        mass = k["mass"]
        if mass > largestMass:
            largestMass = mass
        totalMass += mass

    return int(largestMass), int(totalMass)

def playerToFood(playerJSON):
    new_food = dict()
    new_food['id'] = playerJSON['id']
    new_food['x'] = playerJSON['x']
    new_food['y'] = playerJSON['y']
    new_food['mass'] = getMassOfPlayer(playerJSON)

def getState(playerID):
    global N, MAX_FOOD_LEVEL, MAX_THREAT_LEVEL
    global previousLargestMass, previousTotalMass
    currentLargestMass = 0
    view = getBoardState(playerID)

    # extract enemy data
    enemies = [view["players"][k] for k in range(0, len(view["players"]))] 
    # extract food data
    food = [view["food"][k] for k in range(0, len(view["food"]))]
    
    # generate new information for each enemy
    for k in enemies:
        #need to figure out which player we are then convert the absolute coordinates to relative
        if(k["id"] == playerID):
            player_y = k["y"]
            player_x = k["x"]
            currentLargestMass, currentTotalMass = getMassOfPlayer(k)
            enemies.remove(k)

    listOfFood = list()
    #If an enemy is smaller than us consider it food
    for k in enemies:
        largestMassOfEnemyk, totalMassOfEnemyk = getMassOfPlayer(k)
        print("num enemies: ", len(enemies))
        if(largestMassOfEnemyk < 1.15*currentLargestMass):
            print("food not enemy", enemies.index(k))
            food.append(playerToFood(k))
            listOfFood.append(k)
    
    for i in listOfFood:
        enemies.remove(i)
        print("remaining enemies after removeal:", len(enemies))

    for k in enemies:
        # new features to be calculated
        if(len(k['cells']) > 0):
            f = dict() #{"angle":, "threat":}
            
            # determine new feature values
            f["angle"] = np.arctan2(k["y"], k["x"])
            f["threat"] = threat(k["x"], k["y"], k['cells'][0]['mass'])
            # add features to each enemy after calculation
            k.update(f)

    # calculate angle and distance of food for sector placement
    for k in food:
        f = dict()
        f["angle"] = np.arctan2(k["y"] - player_y, k["x"] - player_x)
        f["distance"] = distance_inverse(abs(k["x"] -player_x), abs(k["y"] - player_y))
        f["value"] = MAX_FOOD_LEVEL*np.floor(k["mass"]*f["distance"])
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
                sector["food"].append(k["value"])

    sectorEvaluations = [list() for k in range(0, N)]

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
        sectorEvaluations[k].append(rel_threat)

    # sector food calc
    total_food = 0 
    for k in food:
        total_food += k["value"]

    for k in range(0, N):
        rel_food = 0
        if(total_food != 0 ):
            sector_food = sum(sectors[k]["food"])
            rel_food = (sector_food/total_food)
            rel_food = rel_food * MAX_FOOD_LEVEL
            rel_food = np.ceil(rel_food)
        sectorEvaluations[k].append(rel_food)

    massDelta = currentTotalMass - previousTotalMass
    
    previousLargestMass = currentLargestMass
    previousTotalMass = currentTotalMass
    # return sectorEvaluations with threat and food scoring calculated
    return sectorEvaluations, massDelta

def reward(state, massDelta):
    # Calculate the reward for a state
    # state is a list of sectors with [[threat0, food0], [threat1, food1], ... ,[ threaN, foodN]]
    #   for sectors 0 -> N
    
    total_threat = 0
    for k in state:
        total_threat += k[0]
    if(total_threat > 0):
        print("THREAT!! :", total_threat)
    
    total_food = 0
    for k in state:
        total_food += k[1]

    return (total_food  - total_threat + REWARD_FOR_EATING*massDelta)

# MAIN
# ///////////////////////////////////////////////////////////////////////////////////////////

def main():
    pass

main()
