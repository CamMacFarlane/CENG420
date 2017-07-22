import AgarBots 
from state import state_function
import random
import time

BOTNAME = "CamBot"
DURATION = 100000
NUM_BOTS = 1
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



for j in range(1, DURATION):
    for i in range(0, NUM_BOTS):
        playerID = ID + str(i)

        view = AgarBots.getView(playerID)
        # print(view)
        sectors = state_function.get_states(view, 10, 10, 10, playerID)
        sector = evaluateState(sectors) 

        print(sectors)
        print("Chose:", sector, sectors[sector - 1])
        AgarBots.move(playerID,len(sectors) + 1,sector)
        time.sleep(random.random())

print(AgarBots.getNearbyObjects(ID + "0"))

for i in range(0, NUM_BOTS):
    playerID = ID + str(i)
    AgarBots.removeplayer(playerID)
