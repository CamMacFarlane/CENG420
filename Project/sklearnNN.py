"""
sklearnNN:
Uses training data to train a Mult-level-perceptron classifier.
ideally: Feed in inputs and the classifier will recommend a good move. 

This doesn't seem to work right now. Will work on expanding radius and generating more test data. 
"""

import csv
from sklearn.neural_network import MLPClassifier
import numpy as np

N = 16										# Number of moves to be taken during the test. 
ALG = "Greedy"								# Use this to specify which algorithm is used for the test.
RADIUS = 1000

filename = "TrainingData_Radius" + str(RADIUS) + "_ALG_" + ALG + "_N_" + str(N) + ".csv"

with open(filename, newline='') as csvfile:
	row_count = sum(1 for row in csvfile)
csvfile.close()

testData = [[0 for x in range((2*N))] for y in range(row_count)]
testLabels = [0 for y in range(row_count)]

with open(filename, newline='') as csvfile:
     testreader = csv.reader(csvfile, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
     i = 0
     for row in testreader:
     	for j in range(0, 2*N):     		
	     	testData[i][j] = float(row[j].replace(' ', ''))
     	testLabels[i] = int(float(row[32].replace(' ', '')))
     	i += 1

testData = np.array(testData)
testLabels = np.array(testLabels)

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                     hidden_layer_sizes=(5, 2), random_state=1)

clf.fit(testData, testLabels)       

print("Neural net Constructed & online!")

MLPClassifier(activation='relu', alpha=1e-04, batch_size='auto',
       beta_1=0.9, beta_2=0.999, early_stopping=False,
       epsilon=1e-08, hidden_layer_sizes=(5, 2), learning_rate='constant',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,
       solver='sgd', tol=0.0001, validation_fraction=0.1, verbose=True,
       warm_start=False)


# Decision algorithm:
# Reformats state into a 32x1 array and feeds into classifier. 
# Does it work? Not really. 

def SamDecide(state):

	# must re-encode state into a list of 2N numbers

	print(state)
	stateArray = [0 for x in range(32)]
	i = 0
	for sector in state:
		for item in sector:
			stateArray[i] = float(item)
			i += 1
	stateArray = np.array(stateArray)
	# return prediction from NN
	return clf.predict(stateArray.reshape(1,-1))