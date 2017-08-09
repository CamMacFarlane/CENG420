import requests
import json
import time
# domain = "http://0.0.0.0:3000"
domain = "http://localhost:3000"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def createPlayer():
  removePlayerData = {
    "name": "hungary_bot",
    "id": "deus_ex_machina_bot"
  }
  requests.post(domain + '/removePlayer', data=json.dumps(removePlayerData), headers=headers)
  createPlayerData = {
    "name": "hungary_bot",
    "id": "deus_ex_machina_bot"
  }
  res = requests.post(domain + '/createPlayer', data=json.dumps(createPlayerData), headers=headers)
  # print(res.text)
  time.sleep(0.2)

def movePlayer(x, y):
  url = domain + '/move'
  moveData = {
    "id": "deus_ex_machina_bot",
    "x": x, 
    "y": y
  }
  requests.post(url, data=json.dumps(moveData), headers=headers)

def getBoardState():
  url = domain + '/getNearbyObjects'
  data = {
    "id": "deus_ex_machina_bot"
  }
  res = requests.post(url, data=json.dumps(data), headers=headers)
  return json.loads(res.text)

def isAlive(identifier):
    url = domain + '/getNearbyObjects'

    r = requests.post(url, headers={"content-type": "application/json"}, json={"id": identifier})
    try:
        data = r.json()
        return True
    except ValueError:
        return False

def findFood():
  if(isAlive("deus_ex_machina_bot")):
    board = getBoardState()
    targetX = float(board["food"][0]["x"]) - float(board["players"][0]["x"])
    targetY = float(board["food"][0]["y"]) - float(board["players"][0]["y"])
    movePlayer(targetX, targetY)
  else:
    createPlayer()

def removePlayer():
  removePlayerData = {
    "name": "hungary_bot",
    "id": "deus_ex_machina_bot"
  }
  res = requests.post(domain + '/removePlayer', data=json.dumps(removePlayerData), headers=headers)

def play():
  createPlayer()
  findFood()


# main()