"""
Static-Bot Performance Test:
Spawns N static bots and one algorithm controlled player. 
Will move according to specified algorithm for specified number of turns.
Logs cell radius over time and writes to .csv in a new row after test execution.
"""

import Q_learning_rough as API
import random
import csv
import sklearnNN
import time

# PROPERTIES + GLOBAL VARIABLES ########

N = 16
MOVES = 400									# Number of moves to be taken during the test. 
ALG = "NNClassifier"								# Use this to specify which algorithm is used for the test.
PLAYER_ID = "hero"							# The ID and name of the algorithm-controlled player.
RADIUS = 1000
BOT_MASS = 1000
DELAY = 0.5

#######

def decide(state):
	if (ALG == "Greedy"):
		return API.evaluateState(state)
	if (ALG == "NNClassifier"):
		return sklearnNN.SamDecide(initialState)
	if (ALG == "Random"):
		return random.randint(0,(N-1))

# Change config and double-check:

print(API.getConfig())
API.setConfig(RADIUS, BOT_MASS)
print(API.getConfig())

# spawn bots

#API.createStaticBots(10)
API.createPlayer(PLAYER_ID, PLAYER_ID)

sizePlot = [0 for i in range(MOVES)]

i = 0
while (i < MOVES):

	start = time.time()

	initialState, initialMassDelta = API.getState(PLAYER_ID)
	# move player
	move = decide(initialState)
	print("using ", ALG, "algorithm, decided on move: ", str(move), ", moving now. i = ", str(i))
	API.move(PLAYER_ID, move, N)

	# get mass of player + log it:
	view = API.getBoardState(PLAYER_ID)
	size = view["players"][0]["cells"][0]["radius"]
	print("size = ", size)
	sizePlot[i] = size

	end = time.time()
	duration = (end-start)
	wait = max((DELAY - duration), 0)
	time.sleep(wait)

	print("duration of loop = ", duration)

	i += 1

# End Test. Purge Bots. 

API.removeStaticBots(10)
API.removePlayer(PLAYER_ID, PLAYER_ID)

# add mass over time to a comma-separated string

sizeString = ALG + ","
for item in sizePlot:
	sizeString += (str(item) + ",")

# add data to .csv for comparison to other runs / algorithms.

with open('TestResults.csv', 'a', newline="") as csvfile:
	    writer = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
	    writer.writerow(sizeString)

# Note:
# .csv file will have spaces between every character (?) 
# until I find a fix, just ctrl-f find and replace all spaces woth nothing in excel / notepad / whatever. 