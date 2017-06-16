
# Get neccesary math functions
import random
from math import floor

# Define the size of the board
N = 4

# Termination condition
#   - # of non-intersecting queens == N
termination_condition = N

# Chromosome: a list of queen positions
#   - init elements to (-1, -1)?
chromosome = list()

#  Each chromosome is a list of (x,y) pairs representing the positions of the queens in the board 
#   chromosome = [ |x0|, |x1|, ... , |xN| ]
#                  |y0|  |y1|        |yN|

# Fitness Function:
#   - number of non-intersecting queens on board
#   - number of available spaces to place next queen

# Population
#   - Want:
#       - Elitism -> preserve the already placed queens on the board
#

population = list() # a list of individuals
initial_population_size = N  # Is this a good value?

# Genetic algorithm parameters
mutation_resistance = 0.9
mutation_rate = 0.7
crossover_rate = 0.5

def create_chromosome():

    # want: list of [x,y] such that x is in [0, N-1] and y is in [0, N-1]
    #       generate chromosome such that each row has exactly one queen in it
    chromosome = [[z, random.randint(0, N)] for z in range(0,N)]
    return chromosome

def fitness():

    for individual in population:
        # get chromosome value
        chromosome = individual['chromosome']
        
        # Since initialization function ensures no two queens have same row
        #   check only columns and diagonals

        # cases to check for
        #   - Same column: Qi.y == Qj.y
        #   - Same diagonal: (Qi.x == Qj.y && Qi.y == Qj.x)
        
        # maximum fitness is a perfect score of N non-intersecting queens
        individual['fitness'] = N

        # for each queen on the board
        for k in range(0, N):
            queen_i = chromosome[k]
            
            # check for intersections with queens below current queen_i
            for x in range(k+1,N):
                
                queen_j = chromosome[x]
                # check if same column in columns below queen_i
                if(queen_i[1] == queen_j[1]):
                    # if queen_i intersects another queen, reduce fitness score by 1
                    print queen_i, " same column as", queen_j  # DEBUG
                    individual['fitness'] -= 1

                # check if same diagonal for queens below queen_i
                if(queen_i[0] == queen_j[1] and queen_i[1] == queen_j[0]):
                    # if queen_i intersects another queen, reduce fitness score by 1
                    print queen_i, " same diagonal as ", queen_j   # DEBUG
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

    # for each row, randomly choose a column to put the queen in

def crossover():
    pass

def mutation():
    pass

# testing
initialize_population()

for k in population:
    print k

fitness()

for k in population:
    print k
