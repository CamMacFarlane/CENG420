
# Get neccesary math functions
import random
from math import floor

# Define the size of the board
N = 4

# Termination condition
#   - # of non-intersecting queens == N
termination_condition = N
current_max_fit = -N

#  Each chromosome is a list of (x,y) pairs representing the positions of the queens in the board 
#   chromosome = [ |x0|, |x1|, ... , |xN| ]
#                  |y0|  |y1|        |yN|
chromosome = list()

# Fitness Function:
#   - number of non-intersecting queens on board
#       - refine with number of available spaces to place next queen?

# Population
#   - Want:
#       - Elitism -> preserve the already placed queens on the board

population = list() # a list of individuals
initial_population_size = N  # Is this a good value?

# Genetic algorithm parameters
mutation_resistance = 0.9
mutation_rate = 0.7
crossover_rate = 0.5

def create_chromosome():
    # want: list of [x,y] such that x is in [0, N-1] and y is in [0, N-1]
    #       generate chromosome such that each row has exactly one queen in it
    chromosome = [[z, random.randint(0, N-1)] for z in range(0,N)]
    return chromosome

# adapted from example code in course repo
def roulette_wheel():
    wheel = 0
    
    for individual in population:
        wheel += individual['fitness']
    
    selection_point = random.randint(0, wheel)

    angle = 0
    
    for individual in population:
        angle += individual['fitness']
        if angle >= selection_point:
            return individual

def fitness():

    for individual in population:
        # avoid recalculating fitness for all individuals
        if(individual['fitness'] < 0):
            # get chromosome value
            chromosome = individual['chromosome']
            
            # Since initialization function ensures no two queens have same row
            #   check only if same column or same diagonal

            # maximum fitness is a perfect score of N non-intersecting queens
            individual['fitness'] = N

            # for each queen on the board
            for k in range(0, N):
                # queen to check for intersections
                queen_i = chromosome[k]
                
                # check for column intersections with queens below current queen_i
                for x in range(k+1,N):
                    
                    queen_j = chromosome[x]
                    # check if same column in columns below queen_i
                    if(queen_i[1] == queen_j[1]):
                        # if queen_i intersects another queen, reduce fitness score by 1
                        #print queen_i, " same column as", queen_j  # DEBUG
                        individual['fitness'] -= 1

                # check if same diagonal for queens below queen_i
                # check positive, [x+1, y+1], diagonal
                queen_j = list(queen_i)
                while((queen_j[0] < N) and (queen_j[1] < N)):
                    queen_j[0] += 1
                    queen_j[1] += 1
                    if queen_j in chromosome:
                        # intersection
                        individual['fitness'] -= 1

                # check negative, [x+1, y-1], diagonal
                queen_j = list(queen_i)
                while((queen_j[0] < N) and (queen_j[1] > 0)):
                    queen_j[0] += 1
                    queen_j[1] -= 1
                    if queen_j in chromosome:
                        # intersection
                        individual['fitness'] -= 1

def initialize_population():
    count = 0

    while count < initial_population_size:
        chromosome = create_chromosome()

        individual = dict()
        individual['chromosome'] = list(chromosome)

        individual['fitness'] = -1
        population.append(individual)
        count += 1

def crossover(parent_a, parent_b):
    # choose such that we never swap parent chromosomes or allow mutation to handle that case?
    # change replacement rate to grow population?

    # determine swap point in chromosomes
    swap_point = random.randint(0, N-1)

    # Generate first offspring
    offspring_1 = dict()
    offspring_1['chromosome'] = parent_a['chromosome'][:swap_point] + parent_b['chromosome'][swap_point:]
    offspring_1['fitness'] = -1

    # Generate second offspring
    offspring_2 = dict()
    offspring_2['chromosome'] = parent_b['chromosome'][:swap_point] + parent_a['chromosome'][swap_point:]
    offspring_2['fitness'] = -1

    return offspring_1, offspring_2

def mutation(individual):
    # apply a random mutation to the chromosome
    #   NOTE: must still preserve the one queen per row condition
    #   THEREFORE: mutation simply changes the column entry for a queen in a random row

    # get chromosome to be modified
    chromosome = individual['chromosome']
    
    # Randomly select row (gene) to mutate
    row = random.randint(0, N-1)

    # Apply mutation
    chromosome[row][1] = random.randint(0, N-1)
    
    # Save result back to individual, ensure new fitness value is calculated
    individual['chromosome'] = chromosome
    individual['fitness'] = -1

    return individual

# testing

def display_individual(individual):
    for x in range(0,N):

        queen_x = individual['chromosome'][x][0]
        queen_y = individual['chromosome'][x][1]

        for y in range(0,N):
            if(queen_x == x and queen_y == y):
                print "Q",
            else:
                print "_",
        print ""

initialize_population()

for k in population:
    print k

fitness()

for k in population:
    print k

fitness()

for k in population:
    display_individual(k)
    print ""

# Genetic algorithm to solve N-Queens problem

initialize_population()
fitness()

while current_max_fit < termination_condition:

    new_offsprings = floor(len(population) * crossover_rate / 2)

    new_generation = list()

    while new_offsprings > 0:
        parent_one = roulette_wheel()
        parent_two = roulette_wheel()

        offspring_one, offspring_two = crossover(parent_one, parent_two)

        offspring_one = mutation(offspring_one)
        offspring_two = mutation(offspring_two)

        new_generation.append(offspring_one)
        new_generation.append(offspring_two)

        new_offsprings -= 1

    population = sorted(population, key=lambda k: k['fitness'])
    del population[0:len(new_generation)]

    population = new_generation + population
    
    fitness()

    max_fit_individual = max(population, key=lambda k: k['fitness'])
    current_max_fit = max_fit_individual['fitness']


for k in population:
    print k

display_individual(max_fit_individual)
