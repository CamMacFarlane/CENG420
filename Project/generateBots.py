import AgarBots 
from state import state_function
import random
import time

BOTNAME = "CamBot"
DURATION = 100000
NUM_BOTS = 3
NUM_OBSTACLES = 5


ID = str(random.randrange(10000))
# AgarBots.createStaticObstacles(NUM_OBSTACLES)

for i in range(0, NUM_BOTS):
    playerID = ID + str(i)
    name = BOTNAME + playerID 
    AgarBots.makeplayer(name, playerID, 50)


def evaluateState(sectorArray):
    bestsector = random.randint(1,len(sectorArray) + 1)
    bestsectorEvaluation = -1000
    for sector in sectorArray:
        threat = sector[0]
        food = sector[1]
        evaluation = food - threat
        if evaluation > bestsectorEvaluation:
            bestsector = sectorArray.index(sector) + 1
            bestsectorEvaluation = evaluation
    return bestsector


# def testSecorMovement(playerID):
#     view = AgarBots.getView(playerID)
#     sectors = state_function.get_states(view, 8, 10, 10, playerID)
#     for i in range(len(sectors)):
#         print("Moving sector:", i+1)
#         AgarBots.move(playerID, i + 1, len(sectors) + 1)
#         time.sleep(3)

# playerID = ID + "0"
# testSecorMovement(playerID)

for j in range(1, DURATION):
    for i in range(0, NUM_BOTS):
        
        playerID = ID + str(i)
        if(AgarBots.isAlive(playerID)):
            view = AgarBots.getView(playerID)
            # print(view)
            sectors = state_function.get_states(view, 16, 10, 10, playerID)
            sector = evaluateState(sectors) 

            print(sectors)
            print("Chose:", sector, sectors[sector - 1])
            AgarBots.move(playerID, sector, len(sectors) + 1)
    time.sleep(random.random())

print(AgarBots.getNearbyObjects(ID + "0"))

for i in range(0, NUM_BOTS):
    playerID = ID + str(i)
    AgarBots.removeplayer(playerID)

