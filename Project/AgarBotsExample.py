import AgarBots
import random
import time

BOTNAME = "SamBot"
DURATION = 3
NUM_BOTS = 10

ID = str(random.randrange(10000))

for i in range(0, NUM_BOTS):
	playerID = ID + str(i)
	name = BOTNAME + playerID 
	AgarBots.makeplayer(name, playerID, 50)

for j in range(1, DURATION):
	for i in range(0, NUM_BOTS):
		playerID = ID + str(i)
		x = random.randint(-200, 200)
		y = random.randint(-200, 200)
		AgarBots.moveplayer(playerID, x, y)
		time.sleep(0.5)

print(AgarBots.getNearbyObjects(ID + "0"))

for i in range(0, NUM_BOTS):
	playerID = ID + str(i)
	AgarBots.removeplayer(playerID)
