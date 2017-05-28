import sega1
import time
import random
x_len = sega1.x_len
y_len = sega1.y_len
gameBoard = sega1.mainBoard
debug = False

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
    if player=='X':
        opponent='O'
    else:
        opponent = 'X'
    #diagonal uppper left to lower right
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
    if(sega1.checkGoalState(player, state, quiet=True) == True):
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
 
    
#PERMUTATIONS AND MOVE EVALUATION

def buildPermutations(player, state):  # returns a list of the possible next states
    spaces = []
    filled = []
    boards = []
    if player=='X':
        opponent='O'
    else:
        opponent = 'X'
    for x in range(x_len):              # generates lists of coordinates for empty spaces and player-occupied spaces
        for y in range(y_len):
            if state[y][x] == ' ':
                spaces.append([x,y])
            elif state[y][x] == player:
                filled.append([x,y])
                
    for piece in range(len(filled)):      # builds every possible next-state and stores boards in an array
        for space in range(len(spaces)):
            tmp_board = [x[:] for x in state]
            sega1.move(player, filled[piece][0], filled[piece][1], spaces[space][0], spaces[space][1], state=tmp_board, quiet=True)
            boards.append(tmp_board)
    return boards

def analyzePermutations(player, states, board):                 # takes the heuristic score of each optional state and moves to the highest scoring
    scores = [' ' for k in range(len(states))]
    for state in range(len(states)):
        scores[state] = heuristic(states[state], player)
    selected_state = scores.index(max(scores))
    print("\nMy turn!\n")
    if(debug):
        for i in range(len(states)):
            if(debug): 
                sega1.printState(states[i])
                print("\n score: ", scores[i], "\n")
    return states[selected_state]                               # returns new gameboard
    
# start game
# loops and alternates human and computer moves until there is a winner. 

sega1.populateBoard()
print("\nStarting Game! 3x3 Sega!\n")
sega1.printState(gameBoard)
firstmove = True
while(not sega1.checkGoalState('X', state=gameBoard, quiet=True) and not sega1.checkGoalState('O', state=gameBoard, quiet=True) or firstmove): 
    firstmove = False
    # take and perform user's move
    moves = input("\nenter to and from coordinates for X, 4 numbers, separated by spaces: \n\n")
    move = moves.split()
    sega1.move('X', int(move[0]), int(move[1]), int(move[2]), int(move[3]), gameBoard)
    sega1.printState(gameBoard)
    if(sega1.checkGoalState('X', state=gameBoard)):
        print("\n\nX wins!\n")
        break
    #computer's turn
    boards = buildPermutations('O', gameBoard)
    new_board = analyzePermutations('O', boards, gameBoard)
    gameBoard = [x[:] for x in new_board]
    sega1.printState(gameBoard)
    if(sega1.checkGoalState('O', state=gameBoard)): 
        print("\n\nO wins!\n")
        break
    







