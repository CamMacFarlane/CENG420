import requests
import json
import time
# domain = "http://0.0.0.0:3000"
domain = "https://agar-willy-branch.herokuapp.com"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def createPlayer(name, id):
  removePlayerData = {
    "name": name,
    "id": id
  }
  requests.post(domain + '/removePlayer', data=json.dumps(removePlayerData), headers=headers)
  createPlayerData = {
    "name": name,
    "id": id
  }
  res = requests.post(domain + '/createPlayer', data=json.dumps(createPlayerData), headers=headers)
  print(res.text)

def movePlayer(x, y):
  url = domain + '/move'
  moveData = {
    "id": "hungry_bot",
    "x": x,
    "y": y
  }
  requests.post(url, data=json.dumps(moveData), headers=headers)

def getBoardState():
  url = domain + '/getNearbyObjects'
  data = {
    "id": "hungry_bot"
  }
  res = requests.post(url, data=json.dumps(data), headers=headers)
  return json.loads(res.text)

def findFood():
  while(1):
    board = getBoardState()
    targetX = float(board["food"][0]["x"]) - float(board["players"][0]["x"])
    targetY = float(board["food"][0]["y"]) - float(board["players"][0]["y"])
    movePlayer(targetX, targetY)
    time.sleep(5)
def main():
  for i in range(20):
    createPlayer("hungry_bot" + str(i), "hungry_bot" + str(i))
# findFood()

main()