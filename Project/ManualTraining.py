"""
Manual ot Training:
Spawns N static bots and one algorithm controlled player. 
Moves Randomly and logs 'successful' moves in .csv
Use this data for training NN classifier. 
"""
import Q_learning_rough as API
import random
import csv
import time
import math

# PROPERTIES + GLOBAL VARIABLES ########

N = 16
MOVES = 1000									# Number of moves to be taken during the test. 
ALG = "Greedy"								# Use this to specify which algorithm is used for the test.
BOT_ID = "staticBot_0"							# The ID and name of the algorithm-controlled player.
CUTOFF = -100									# What is considered to be a 'good' move.  	
DELAY = 0.1
PLAYER_NAME = "sam_irl"
NUM_BOTS = 10
csvFile = "sam_HumanData.csv"

API.createStaticBots(NUM_BOTS)

# First we have to find the ID of the human player (randomly assigned)
# This is a hassle but usually pretty quick.

def findID(playerName):
	FOUND_ID = False
	while(not FOUND_ID):
		for i in range(NUM_BOTS):
			data = API.getBoardState("staticBot_" + str(i))
			for item in data["players"]:
				if item["name"] == PLAYER_NAME:
					PLAYER_ID = item["id"]
					print("\n\nfound player ID!\n")
					print(PLAYER_ID)
					FOUND_ID = True
		time.sleep(0.5)
	return PLAYER_ID


def formatSectorsForLearning(sectorArray):
    threatArray = []
    foodArray = []
    for sector in sectorArray:
        threatArray += [sector[0]]
        foodArray += [sector[1]]
    return [threatArray, foodArray]


def writeToCSV(learningInformation):
    with open(csvFile, "a", newline='') as output:
        writer = csv.writer(output)
        writer.writerow(learningInformation)  


PLAYER_ID = findID(PLAYER_NAME)

data = API.getBoardState(PLAYER_ID)
for item in data["players"]:
	if item["id"] == PLAYER_ID:
		former_x = item["x"]
		former_y = item["y"]

while(True):

	data = API.getBoardState(PLAYER_ID)

	for item in data["players"]:
		if item["id"] == PLAYER_ID:
			current_x = item["x"]
			current_y = item["y"]

	diff_x = current_x - former_x
	diff_y = current_y - former_y


	if (diff_x == 0 and diff_y == 0):
		angle = 1000000					# this move can be ignored
	elif diff_x == 0:
		angle = diff_y / math.fabs(diff_y) * ( math.pi / 2 )
	else:
		angle = math.atan((diff_y/diff_x))

	# re-format angles from 0 to 2*pi

	if(diff_x < 0 and diff_y > 0):	angle = -angle
	if(diff_x > 0 and diff_y > 0): angle = math.pi - angle
	if(diff_x > 0 and diff_y < 0): angle = math.pi - angle
	if(diff_x < 0 and diff_y < 0): angle = 2*math.pi - angle

	action = math.floor(angle / ((2*math.pi)/N))	

	former_x = current_x	
	former_y = current_y

	if (angle < 100):
		sectors, massDelta = API.getState(PLAYER_ID)
		threatAndFoodArrays = formatSectorsForLearning(sectors)
		observation = threatAndFoodArrays[0] + threatAndFoodArrays[1]
		learningInformation = observation + [action]
		writeToCSV(learningInformation)

	time.sleep(DELAY)


