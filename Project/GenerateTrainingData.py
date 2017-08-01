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
MOVES = 200									# Number of moves to be taken during the test. 
ALG = "Greedy"								# Use this to specify which algorithm is used for the test.
PLAYER_ID = "hero"							# The ID and name of the algorithm-controlled player.
CUTOFF = 5									# What is considered to be a 'good' move.  	
RADIUS = 1000
BOT_MASS = 1000

filename = "TrainingData_Radius" + str(RADIUS) + "_ALG_" + ALG + "_N_" + str(N) + ".csv"

#######

def decide(state):
	if (ALG == "Greedy"):
		return API.evaluateState(state)
	if (ALG == "Random"):
		return random.randint(0,(N-1))

# Change config and double-check:

print(API.getConfig())
API.setConfig(RADIUS, BOT_MASS)
print(API.getConfig())

API.createStaticBots(10)
API.createPlayer(PLAYER_ID, PLAYER_ID)

sizePlot = [0 for i in range(MOVES+2)]


# Generating Training Data:
# Moves randomly and logs 'good' moves to a .csv for training the NN. 
# moves are deemed to be good / succesful if they result in increasing score. (Subject to change)

i = 0
while (i < MOVES):

	# Get initial state
	start1 = time.time()
	initialState, initialMassDelta = API.getState(PLAYER_ID)			# 1st API Call
	end = time.time()
	print("API request time #1 ", str(end-start1))
	intialScore = API.reward(initialState, initialMassDelta)

	# move player
	move = decide(initialState)			
	start = time.time()							# 2nd API call
	API.move(PLAYER_ID, move, N)
	end = time.time()
	print("API request time #2 ", str(end-start))
	# assess previous move
	start = time.time()
	newState, newMassDelta = API.getState(PLAYER_ID)
	end = time.time()				# 3rd API call
	print("API request time #3 ", str(end-start))
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
		with open(filename, 'a', newline='') as csvfile:
			    writer = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
			    writer.writerow(stateString)
		    
	end = time.time()
	duration = (end-start1)
	print("total loop duration: ", duration)
	i += 1
