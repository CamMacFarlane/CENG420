import random
import time
x_len = 3
y_len = 3
horzLine = "----"*x_len
debug = False
gameBoard = [[' ' for k in range(x_len)] for k in range(y_len)]


#prints the state passed
def printState(state):
    print("Y\X 0   1   2")
    print(" ",horzLine)
    for k in range(x_len):
        print(k ,"| ", end = "")
        for i in range(y_len):
            print(state[k][i], "| ", end = "")
        print()
        print(" ",horzLine)

#returns True if the move was valid
def move(player, curX, curY, newX, newY):
    ret  = False
    if(gameBoard[curY][curX] != player):
        if(debug):
            print("INVALID MOVE: not your piece")
    elif(gameBoard[newY][newX] != ' '):
        if(debug):
            print("INVALID MOVE: space is not free")
    else:
        swap = gameBoard[curY][curX]
        gameBoard[curY][curX] = gameBoard[newY][newX]
        gameBoard[newY][newX] = swap
        print("Player", player, "moves: (",curX, "," , curY , ")", "to", "(", newX, ",", newY, ")")
        ret = True
    return ret

def checkGoalState(player):
    #horizontal
    for k in range(y_len):
        if(gameBoard[k] == [player]*x_len):
            print("horizontal line for ", player,"!")
            return True
    
    #vertical
    
    for i in range(x_len):
        col = ""
        for k in range(y_len):
            col += gameBoard[k][i]
            if(col == player*x_len):
                print("vertical line for ", player,"!")
                return True
    
    #diagonal
    if(gameBoard[0][0] == player):
        if(gameBoard[1][1] == player):
            if(gameBoard[2][2] == player):
                print("Diagonal line for ", player,"!")
                return True
    if(gameBoard[0][2] == player):
        if(gameBoard[1][1] == player):
            if(gameBoard[2][0] == player):
                print("Diagonal line for ", player,"!")
                return True

#populates board to beginning game state
def populateBoard():
    for i in range(x_len):
        gameBoard[0][i] = "X" 
        gameBoard[x_len - 1 ][i] = 'O'


def randomDance():
    populateBoard()
    printState(gameBoard)
    while(True):
        Attempt = 0
        time.sleep(0.1)
        
        while(move('O', random.randint(0,2), random.randint(0,2), random.randint(0,2),random.randint(0,2)) == False):
            Attempt = Attempt +1
            print("Attempt = ", Attempt , "\r", end="")
        
        printState(gameBoard)
        if(checkGoalState('O')):
            time.sleep(2)
        
        Attempt = 0
        time.sleep(0.1)
        
        while(move('X', random.randint(0,2), random.randint(0,2), random.randint(0,2),random.randint(0,2)) == False ):
            Attempt = Attempt +1
            print("Attempt = ", Attempt , "\r", end="")

        printState(gameBoard)
        if(checkGoalState('X')):
            time.sleep(2)

randomDance()