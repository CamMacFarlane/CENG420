import sega1
import time
import random
x_len = sega1.x_len
y_len = sega1.y_len
gameBoard = sega1.gameBoard

"""
Blocking detection: horizontal, vertical, diagonal:
Determines if the piece in question is blocking a potential line. (2 out of 3 in a row). 
If it is blocking, it adds 5 to the heuristic score (subject to change), as this is a very important move. 
Functions work by iterating through the row/column/diagonal and looking for 1 'player' and n-1 'opponents'
"""

def blocking_col(player, state, x):     #determines if a piece is blocking opponent's horizontal victory
    if player=='X':
        opponent='O'
    else:
        opponent = 'X'
    count_player = 0
    count_opponent = 0
    for i in range(y_len):
        if state[i][x] == opponent:
            count_opponent += 1
        if state[i][x] == player:
            count_player += 1
    if((count_opponent == (y_len-1)) & (count_player == 1)):          # if the piece is blocking
        return 5
    else:
        return 0
         
def blocking_row(player, state, y):     # determines if player is blocking opponent's veritcal victory
    if player=='X':
        opponent='O'
    else:
        opponent = 'X'
    count_player = 0
    count_opponent = 0
    for i in range(x_len):
        if state[y][i] == opponent:
            count_opponent += 1
        if state[y][i] == player:
            count_player += 1
    if((count_opponent == (x_len-1)) & (count_player == 1)):          
        return 5
    else:
        return 0

def blocking_diag(player, state, x, y):     #assumes a square board
    if(x != y & ((x+y) != (x_len-1))):
        return 0
    if player=='X':
        opponent='O'
    else:
        opponent = 'X'
    #diagonal uppper right to lower left
    if(x==y):
        count_player = 0
        count_opponent = 0
        for i in range(x_len):
            if state[i][i] == opponent:
                count_opponent += 1
            if state[i][i] == player:
                count_player += 1
        if((count_opponent == (x_len-1)) & (count_player == 1)):          # if the piece is blocking a row
            return 5
        else:
            return 0
            
    # diagonal lower left to upper right     
    if((x+y) == (x_len-1)):
        count_player = 0
        count_opponent = 0
        for i in range(x_len):
            if state[y_len-i-1][i] == opponent:
                count_opponent += 1
            if state[y_len-i-1][i] == player:
                count_player += 1
        if((count_opponent == (x_len-1)) & (count_player == 1)):          # if the piece is blocking
            return 5
        else:
            return 0

            
"""
num_inrow / num_incol:
Counts the number of other pieces in the same row or column. 
Adds 2 to the heuristic score for each pair of pieces in the same row/column.
"""
            
def num_inrow(player, state, x, y):    # returns the number of other pieces in the same column
    if state[y][x] != player:
        print("error, player not in spot")
    else:
        count = 0
        for i in range(x_len):
            if state[y][i] == player:
                count += 1
        return count-1    
        
def num_incol(player, state, x, y):         # returns number of other pieces in the same column
    if state[y][x] != player:
        print("error, player not in spot")
        return 0
    else:
        count = 0
        for i in range(y_len):
            if state[i][x] == player:
                count += 1
        return count-1    
        
def num_diag(player, state, x, y):
    if((x != y) & ((x+y) != (x_len-1))):       # skip if the piece is not along a diagonal line
        return 0
    if player=='X':
        opponent='O'
    else:
        opponent = 'X'
    count = 0
    if(x==y):
        count -= 1
        for i in range(x_len):
            if state[i][i] == player:
                count += 1
    if((x+y) == (x_len-1)):
        count -= 1
        for i in range(x_len):
            if state[y_len-i-1][i] == player:
                count += 1
    return count

"""
Score:
Calls the different functions and totals the score.
Adds 1000 if the state is a goal state, to ensure the heuristic search algorithm favours this state.
"""
        
def score(state, player):
    score = 0
    for x in range(x_len):
        for y in range(y_len):
            if state[y][x] == player:
                score += ( num_inrow(player, state, x, y) + num_incol(player, state, x, y) + num_diag(player, state, x, y) + blocking_row(player, state, y) + blocking_col(player, state, x) + blocking_diag(player, state, x, y))
    if(sega1.checkGoalState(player) == True):
        score += 1000       
    return score
    
"""
Heuristic function. 
Calculates score(player) - score(opponent) as a final heuristic score. 
This encourages that the selection of the next state to benefit the player as much as possible, without setting up the opponent for a victory.
"""

def heuristic(state, player):
    if player=='X':
        opponent='O'
    else:
        opponent = 'X'
    return(score(state, player) - score(state, opponent))
 
    
# TEST CASES: continuosly prints game boards and their heuristic scores
"""

sega1.populateBoard()
sega1.printState(gameBoard)
while(True):
    Attempt = 0
    time.sleep(5)
    
    while(sega1.move('O', random.randint(0,2), random.randint(0,2), random.randint(0,2),random.randint(0,2)) == False):
        Attempt = Attempt +1
        print("Attempt = ", Attempt , "\r", end="")
    
    sega1.printState(gameBoard)
    print("\n\nX's score for board: %i\n" % score(gameBoard, 'X'))
    print("\n\nO's score for board: %i\n" % score(gameBoard, 'O'))
    print("\n\nX's net score for board: %i\n" % (heuristic(gameBoard, 'X')))
    if(sega1.checkGoalState('O')):
        time.sleep(10)
    
    Attempt = 0
    time.sleep(5)
    
    while(sega1.move('X', random.randint(0,2), random.randint(0,2), random.randint(0,2),random.randint(0,2)) == False ):
        Attempt = Attempt +1
        print("Attempt = ", Attempt , "\r", end="")

    sega1.printState(gameBoard)
    print("\n\nX's score for board: %i\n" % score(gameBoard, 'X'))
    print("\n\nO's score for board: %i\n" % score(gameBoard, 'O'))
    print("\n\nX's net score for board: %i\n" % (heuristic(gameBoard, 'X')))
    if(sega1.checkGoalState('X')):
        time.sleep(10)
"""