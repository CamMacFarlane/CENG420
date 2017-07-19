# SETUP:
# ///////////////////////////////////////////////////////////////////////////////////////////
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Global variables for tuning/adjustment:
# ///////////////////////////////////////////////////////////////////////////////////////////

# Number of sectors
N = 8

# Discretization level specifiers
MAX_THREAT_LEVEL   = 10    # Number of discrete threat levels to consider
MAX_FOOD_LEVEL     = 10    # Number of discrete food levels to consider

# Function Defs:
# ///////////////////////////////////////////////////////////////////////////////////////////

def threat(x, y, mass):
    # calculate the threat value for an enemy given their mass and location
    #   threat = mass/distance
    # function can be changed/improved later if needed
    return mass/np.sqrt(x**2 + y**2)

def distance(x, y):
    pass

# Test Data:
# ///////////////////////////////////////////////////////////////////////////////////////////
# example game state array
#   "view" is a formatted array of all visible enemies and food items within a radius
#view = {"players": [{"x": 100, "y": 80, "mass": 25}, 
#                    {"x": -80, "y": 100, "mass": 50}], 
#        "food": [   {"x": 25, "y": 24},
#                    {"x": -35, "y": -70},
#                    {"x": 50, "y": 65},
#                    {"x": -75, "y": -80}] }

# random game state generation





# MAIN:
# ///////////////////////////////////////////////////////////////////////////////////////////

# information from game state array
# ///////////////////////////////////////////////////////////////////////////////////////////

# extract enemy data
enemies = [view["players"][k] for k in range(0, len(view["players"]))] 

# generate new information for each enemy
for k in enemies:
    # new features to be calculated
    f = dict() #{"angle":, "threat":}
    
    # determine new feature values
    f["angle"] = np.arctan2(k["y"], k["x"])
    f["threat"] = threat(k["x"], k["y"], k["mass"])     #could simply pass ref to dictionary?
    
    # add features to each enemy after calculation
    k.update(f)

# extract food data
food = [view["food"][k] for k in range(0, len(view["food"]))]

# calculate angle of food for sector placement
for k in food:
    f = dict()
    f["angle"] = np.arctan2(k["y"], k["x"])
    k.update(f)

# group enemies/food by sector
# ///////////////////////////////////////////////////////////////////////////////////////////

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
        # if the enemy angle is within the edges of a sector
        if (angle > sector["edge1"] and angle < sector["edge2"]):
            # add that enemy's threat score to the list of threats in that sector
            sector["food"].append(angle)

# define discrete states for Q-learning based on sector threats/food
# ///////////////////////////////////////////////////////////////////////////////////////////

states = [list() for k in range(0, N)]

# sector threat calc
# sum all visible threat values
total_threat = 0;

for k in enemies:
    total_threat += k["threat"]

# for each sector
for k in range(0, N):
    # add threat values for all enemies in that sector
    sector_threat = sum(sectors[k]["threats"])
    
    # divide by total threat to get realtive threat in that sector
    #   use np.ceil() to get an discrete value, overestimate the threat to err on the side of caution
    #   multiply by MAX_THREAT_LEVEL to scale threat into discrete range
    rel_threat = np.ceil((sector_threat/total_threat)*MAX_THREAT_LEVEL)
    
    # add discrete threat value to state matrix
    states[k].append(rel_threat)

# sector food calc
# all food has the same value
total_food = len(food)

for k in range(0, N):
    sector_food = float(len(sectors[k]["food"]))
    
    rel_food = np.floor((sector_food/total_food)*MAX_FOOD_LEVEL)

    states[k].append(rel_food)


# TESTING:
# ///////////////////////////////////////////////////////////////////////////////////////////
def DEBUG():
    print "Enemies:"
    for k in enemies:
        print k
    print ""

    print "Food:"
    for k in food:
        print k    
    print ""

    print "Sector Edges:"
    print sector_edges
    print ""

    print "Sector contents:"
    for k in range(0, N):
        print k, sectors[k]
    print ""

    print "Total Threat:"
    print total_threat
    print ""

    print "Sector Threats:"
    for sector in sectors:
        print sector["threats"]
    print ""

    print "States:"
    for k in states:
        print k

# plotting food and enemies for verification

# pull data from worldview

food_angles = []
food_radii = []

enemy_angles = []
enemy_radii = []

ax = plt.subplot(111, projection='polar')
ax.set_ylim(0, 120)

plt.show()

DEBUG()

# NOTES:
# ///////////////////////////////////////////////////////////////////////////////////////////
#   # Use ceiling() for conservative threat calculation (round towards higher threat)
#   sector_threat = ceiling((sum(threats_in_sector)/sum(visible_threats))*MAX_THREAT_STATES)
#   
#   # Use floor() for conservative food calculation (round towards less food)
#   sector_food = floor((sum(food_in_sector)/sum(visible_food))*MAX_FOOD_STATES)
#   
#
#   # Modelling based on n-armed bandit problem at: 

#
#   # sector data structures
#   #   can create using numpy.linspace(-np.pi, np.pi, N)
    #   needs [-pi, pi] range to match arctan2() output
#   sector_edges = [theta_0, theta_1, ..., theta_n]
#   
#   # simple sector data structure (expand to include future state values in v0.2) where,
    #   edge_2 > edge_1
    #   sector_threat is the result of the above threat calculation
    #   sector_food is the result of the above food calculation
    #
#   sector = [sector_threat, sector_food]
#   
#   # Movement direction for a given state is
#   move_angle = sector_edges[edge_2] - sector_edges[edge_1]
#
#
#   # state matrix
#   states = [sector_0, sector_1, ..., sector_N]
# 
