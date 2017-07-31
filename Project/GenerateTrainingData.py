"""
Static-Bot Performance Test:
Spawns N static bots and one algorithm controlled player. 
Moves Randomly and logs 'successful' moves in .csv
Use this data for training NN classifier. 
"""
import Q_learning_rough as API
import random
import csv
import time

# PROPERTIES + GLOBAL VARIABLES ########

N = 16
MOVES = 100									# Number of moves to be taken during the test. 
ALG = "Random"								# Use this to specify which algorithm is used for the test.
PLAYER_ID = "hero"							# The ID and name of the algorithm-controlled player.
CUTOFF = 5									# What is considered to be a 'good' move.  	

#######

def decide(state):
	if (ALG == "Greedy"):
		return API.evaluateState(state)
	if (ALG == "Random"):
		return random.randint(0,(N-1))

API.createStaticBots(10)
API.createPlayer(PLAYER_ID, PLAYER_ID)

sizePlot = [0 for i in range(MOVES+2)]


# Generating Training Data:
# Moves randomly and logs 'good' moves to a .csv for training the NN. 
# moves are deemed to be good / succesful if they result in increasing score. (Subject to change)


i = 0
while (i < MOVES):

	# Get initial state

	initialState, initialMassDelta = API.getState(PLAYER_ID)
	intialScore = API.reward(initialState, initialMassDelta)

	# move player

	move = decide(initialState)
	API.move(PLAYER_ID, move, N)

	# assess previous move

	newState, newMassDelta = API.getState(PLAYER_ID)
	newScore = API.reward(newState, newMassDelta)
	scoreChange = newScore - intialScore
	print("Score Change: ", scoreChange)

	# Write move information to CSV in format: State, move, ScoreChange

	if (scoreChange > CUTOFF):
		print("adding to csv")
		stateString = ""
		for sector in initialState:
			for item in sector:
				stateString += (str(item) + ",")
		stateString += (str(move) + ", " + str(scoreChange))
		with open('trainingData.csv', 'a', newline='') as csvfile:
			    writer = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
			    writer.writerow(stateString)
		    
	i += 1
