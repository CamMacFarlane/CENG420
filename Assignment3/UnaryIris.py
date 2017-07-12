from sklearn import datasets
import numpy
import random
import math

MAX_RADIUS = 2.0
REQ_MATCHES = 10
DEBUG = True
OPTIMIZE = False

random.seed()

iris = datasets.load_iris()

Setosa = iris.data[0:49, :]
Versicolor = iris.data[50:99, :]
Virginica = iris.data[100:149, :]

#SetosaTraining = numpy.array([[1.0,2.0,3.0,4.0]])
#TestData = numpy.array([[1.0, 1.0, 1.0, 1.0]])

def distance(a, b):  # function for computing euclidean distance (higher = less similar) between two arrays
	sum = 0
	for i in range(0,4):
		sum += math.pow((a[i]-b[i]), 2)
	return math.sqrt(sum)

def classify(Specimen, Reference, radius=MAX_RADIUS, matches=REQ_MATCHES):		# finds # of test samples within radius. returns true if > 5. 
	count = 0
	for i in range(0, len(Reference[:, 1])):
		similarity = distance(Specimen, Reference[i])
		if DEBUG: print(similarity)
		if similarity < radius:
			count += 1
	if count > matches:
		return True

# select 15 setosa specimens for training / validation

for i in range(0, 15):
	index = random.randrange(49-i)
	if i == 0: 
		SetosaTraining = numpy.array([Setosa[index, :]])
	else:
		SetosaTraining = numpy.concatenate((SetosaTraining, [Setosa[index, :]]))

#SetosaTraining = numpy.delete(SetosaTraining, 0, 0)

# Select 5 Setosa and 5 Versicolor for testing

for i in range(0,10):
	if i < 5: 
		genus = Setosa
	else:
		genus = Versicolor
	index = random.randrange(len(genus[:, 1]))
	if(i == 0):
		TestData = numpy.array([genus[index, :]])
	else:
		TestData = numpy.concatenate((TestData, [genus[index, :]]))
	genus = numpy.delete(genus, index, 0)

print("\nSetosa Training Data Set:\n", SetosaTraining)

print("\n\n\n\n Test Data: 5 Setosa Samples followed by 5 Versicolor Samples\n", TestData, "\n\n\n\n")

#This code used for testing and optimizing radius and # required

if OPTIMIZE:
	for rad in numpy.arange(0.0, 3.0, 0.1):
		for req in range(0, 15):
			correct = 0
			for test in range(0, 10):
					#print("classifying test sample %i...." % test)
					if classify(TestData[test, :], SetosaTraining, rad, req) == True:
						#print("Test %i Classified as Setosa\n" % test)
						if(test < 5): correct += 1
					else:
						#print("Test %i Classified as Negative\n" % test)
						if(test >= 5): correct += 1 
			print("tested with radius %f and requirement %i, correct = %i" % (rad, req, correct))


# Run classifier on Test data of mixed composition (5 setosa, 5 Versicolor)

if OPTIMIZE==False:
	correct = 0
	for test in range(0, 10):
						print("classifying test sample %i...." % test)
						if classify(TestData[test, :], SetosaTraining) == True:
							print("Test %i Classified as Setosa\n" % test)
							if(test < 5): 
								print("correct!")
								correct += 1
							else: print("false positive.")
						else:
							print("Test %i Classified as Negative\n" % test)
							if(test >= 5): 
								print("correct!")
								correct += 1
							else: print("false negative")
	print("\nTotal score = %i/10\n" % correct)
