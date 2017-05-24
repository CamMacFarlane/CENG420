import random
import time
x_len = 3
y_len = 3
horzLine = "----"*x_len
debug = True
mainBoard = [[' ' for k in range(x_len)] for k in range(y_len)]


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
def move(player, curX, curY, newX, newY, state=mainBoard, quiet = False):
    ret  = False
    if(state[curY][curX] != player):
        if(debug):
            print("INVALID MOVE: not your piece")
    elif(state[newY][newX] != ' '):
        if(debug):
            print("INVALID MOVE: space is not free")
    else:
        swap = state[curY][curX]
        state[curY][curX] = state[newY][newX]
        state[newY][newX] = swap
        if not quiet: print("Player", player, "moves: (",curX, "," , curY , ")", "to", "(", newX, ",", newY, ")")
        ret = True
    return ret

def checkGoalState(player, state=mainBoard, quiet=False):
    #horizontal
    for k in range(y_len):
        if(state[k] == [player]*x_len):
            if not quiet: print("\nhorizontal line for ", player,"!")
            return True
    
    #vertical
    
    for i in range(x_len):
        col = ""
        for k in range(y_len):
            col += state[k][i]
            if(col == player*x_len):
                if not quiet: print("\nvertical line for ", player,"!")
                return True
    
    #diagonal
    if(state[0][0] == player):
        if(state[1][1] == player):
            if(state[2][2] == player):
                if not quiet: print("\nDiagonal line for ", player,"!")
                return True
    if(state[0][2] == player):
        if(state[1][1] == player):
            if(state[2][0] == player):
                if not quiet: print("\nDiagonal line for ", player,"!")
                return True

#populates board to beginning game state
def populateBoard(state=mainBoard):
    for i in range(x_len):
        state[0][i] = "X" 
        state[x_len - 1 ][i] = 'O'


def randomDance(state=mainBoard):
    populateBoard()
    printState(state)
    while(True):
        Attempt = 0
        time.sleep(0.1)
        
        while(move('O', random.randint(0,2), random.randint(0,2), random.randint(0,2),random.randint(0,2)) == False):
            Attempt = Attempt +1
            print("Attempt = ", Attempt , "\r", end="")
        
        printState(state)
        if(checkGoalState('O')):
            time.sleep(2)
        
        Attempt = 0
        time.sleep(0.1)
        
        while(move('X', random.randint(0,2), random.randint(0,2), random.randint(0,2),random.randint(0,2)) == False ):
            Attempt = Attempt +1
            print("Attempt = ", Attempt , "\r", end="")

        printState(state)
        if(checkGoalState('X')):
            time.sleep(2)

#randomDance()