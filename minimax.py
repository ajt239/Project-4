from copy import deepcopy
from time import time
import statistics
import math

test_board = [[0, 2, 2],
              [1, 0, 2],
              [1, 1, 0]]

#              0  1  2  3  4  5  6  7
init_board = [[0, 0, 0, 0, 2, 0, 2, 2],  # 0
              [0, 0, 0, 0, 0, 2, 0, 2],  # 1
              [0, 0, 0, 0, 0, 1, 0, 2],  # 2
              [0, 0, 0, 0, 0, 0, 0, 0],  # 3
              [1, 0, 0, 1, 0, 0, 0, 0],  # 4
              [0, 1, 0, 0, 0, 0, 0, 0],  # 5
              [1, 1, 0, 0, 0, 0, 0, 0],  # 6
              [1, 1, 1, 0, 0, 0, 0, 0]]  # 7

movesMade = []

infinity = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
negativeInfinity = -999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
alpha = 0
beta = 0

def get_board_set(board):
    board_set = set([])
    for i in range(len(board)):
        for j in range(len(board[0])):
            board_set.add((i,j))
    return board_set


board_tiles = get_board_set(init_board)
columns = len(init_board[0])
rows = len(init_board)
player_1 = 1
player_2 = 2


# MINI-MAX =============================================================================================================
def minimax_decision(state):
    """
    
    :param state: The current state of the game (the board, a 2D array)
    :return: returns the board/move that is the optimal decision
    """
    depth = 0                                           #
    v = -99                                             #
    best_move = []                                      #
    moves = move_generator(state, player_1)             #

    #
    for move in moves:
        val = min_value(move, depth + 1,negativeInfinity,infinity)

        if val > v:
            v = val
            best_move = move


    movesMade.append(best_move)
    return v, best_move


def max_value(state, depth, alpha, beta):
    """
    
    :param state: The given state of the game (a board, 2D array)
    :return: return the board/move that is the optimal decision
    """

    # Terminal Test this state
    # ------------------------------------------------------------------------------------------------------------------
    # win, winner = terminal_test(state, depth)
    # if win:                                             # if it is a terminal state
    #    return utility(winner)                          # stop searching, find the utility of the state (win or loss)
    # ------------------------------------------------------------------------------------------------------------------


    # Cuttoff-Test this state
    # ------------------------------------------------------------------------------------------------------------------
    cutoff = cuttoff_test(state, depth)

    if cutoff:
        return evaluate(state)
    # ------------------------------------------------------------------------------------------------------------------

    v = negativeInfinity                                             # set a min
    moves = move_generator(state, player_1)             # Generate all moves for player 1 (Agent)

    # DEBUG ============================================================================================================
    # print("\nMAX - depth=" + str(depth) + "\n")
    # for move in moves:
    #    display_board(move)
    #    print()
    # ==================================================================================================================

    # Get the optimal move for player 1
    # ------------------------------------------------------------------------------------------------------------------
    for move in moves:
        v = max(v, min_value(move, depth+1, alpha, beta))

        if v >= beta:
            return v

        alpha = max(alpha,v)
    # ------------------------------------------------------------------------------------------------------------------

    return v


def min_value(state, depth, alpha, beta):
    """
    
    :param state: 
    :return: 
    """
    # Terminal Test this state
    # ------------------------------------------------------------------------------------------------------------------
    # win, winner = terminal_test(state, depth)
    #
    # if win:                                             # if it is a terminal state
    #    return utility(winner)                          # stop searching, find the utility of the state (win or loss)
    # ------------------------------------------------------------------------------------------------------------------

    # Cuttoff-Test this state
    # ------------------------------------------------------------------------------------------------------------------
    cutoff = cuttoff_test(state, depth)

    if cutoff:
        return evaluate(state)
    # ------------------------------------------------------------------------------------------------------------------

    v = infinity                                              # set a  max
    moves = move_generator(state, player_2)             # generate all moves for player 2 (opponent)

    # DEBUG ============================================================================================================
    # print("\nMIN - depth=" + str(depth) + "\n")
    # for move in moves:
    #    display_board(move)
    #    print()
    # ==================================================================================================================

    # Get the optimal move for player 2
    # ------------------------------------------------------------------------------------------------------------------
    for move in moves:
        v = min(v, max_value(move, depth+1, alpha, beta))

        if v<= alpha:
            return v

        beta = min(beta,v)
    # ------------------------------------------------------------------------------------------------------------------

    return v

"""
def terminal_test(state, depth):
    
    3x3 terminal test
    Determines if this state is a terminal state - a win/loss
    :param state: 
    :return: 
    
    if depth == 8:
        return True, 0
    win = False
    winner = 0
    if  state[1][0] == 2 and \
        state[2][0] == state[2][1] == 2:
        win = True
        winner = 2
        return win, winner
    if  state[1][2] == 1 and \
        state[0][1] == state[0][2] == 1:
        win = True
        winner = 1
        return win, winner
    return win, winner
    """

"""
def terminal_test(state):
    
    4x4 terminal test
    Determines if this state is a terminal state - a win/loss
    :param state: 
    :return: 
    
    win = False
    winner = 0
    if  state[2][0] == 2 and \
        state[3][0] == state[3][1] == 2:
        win = True
        winner = 2
        return win, winner
    if  state[1][3] == 1 and \
        state[0][2] == [0][3] == 1:
        win = True
        winner = 1
        return win, winner
    return win, winner
"""


def terminal_test(state):
    """
    8x8 board
    :param state: 
    :param depth: 
    :return: 
    """

    win = False
    winner = 0
    if state[3][7] == 1 and \
        state[2][6] == state[2][7] == 1 and \
        state[1][5] == state[1][6] == state[1][7] == 1 and \
        state[0][4] == state[0][5] == state[0][6] == state[0][7] == 1:

        win = True
        winner = 1
        return [win, winner]

    if state[4][0] == 2 and \
        state[5][0] == state[5][1] == 2 and \
        state[6][0] == state[6][1] == state[6][2] == 2 and \
        state[7][0] == state[7][1] == state[7][2] == state[7][3] == 2:

        win = True
        winner = 2
        return [win, winner]

    return [win, winner]


def utility(state):
    """
    Not a heuristic!
    Determine if the terminal state is a win or loss for player 1, the agent
    win = 1
    lose = 0
    :param state: 
    :return: 
    """
    if state == 1:
        return 1
    elif state == 2:
        return 0
    else:
        return -1


def cuttoff_test(state, depth):
    """
    
    :param state: 
    :param depth: 
    :return: 
    """
    if depth == 4 or terminal_test(state)[0]:
        return True
    else:
        return False


def evaluate(board):
    """
    Heuristic function to evaluate a state from a previous one
    :param state: 
    :return: 
    """

    value = negativeInfinity                                                          # initialize state's value
    # distances = []                                                      # array of each pawn's distance to goal

    # # Find the overall distance to the goal = average of all the pieces distances to goal
    # # ------------------------------------------------------------------------------------------------------------------
    # for y in range(rows):
    #     for x in range(columns):
    #         if state[y][x] == 1:                                        # Find each Agent pawn on the board
    #                                                                     # TODO: distance function
    #             distance = get_distance(find_move(previous_state,state))                            # Get the distance of that pawn to the goal
    #             distance = math.floor((1 - distance/8) * 100)           # Percentage completed
    #             distances.append(distance)                              # add the distance to the array
    # # ------------------------------------------------------------------------------------------------------------------

    # # avg_dist = statistics.harmonic_mean(distances)?
    # # avg_dist = statistics.median(distances)
    # # avg_dist = statistics.mode(distances)
    # avg_dist = statistics.mean(distances)
    if board not in movesMade:
        pawns = get_pawns_set(board)
        goodPawns = pawns_in_goal(pawns)
        badPawns = pawns_in_base(pawns)
        mildPawns = pawns_in_middle(board)
        if rows == 8:
            #mildPawns = 10-(goodPawns+badPawns)
            value = (goodPawns + mildPawns - badPawns)/10
        elif rows == 10:
            #mildPawns = 15-(goodPawns+badPawns)
            value = (goodPawns + mildPawns - badPawns)/15
        else:
            #mildPawns = 21-(goodPawns+badPawns)
            value = (goodPawns + mildPawns - badPawns)/21

    return value


def get_distance(x, y):
    # TODO: Edit this so it gets the distance left to the deepest position of the win area that is not filled by '1'
    # TODO: Does this need to be under-estimated? => distance defined by how many jumps it would take to get there
    """
    Get the fraction/ratio of distance the pawn has left to the goal
    The goal is defined as the middle position of the winning area: (6,1) 
    :param x: 
    :param y: 
    :return: 
    """
    #goal_x, goal_y = get_deepest_pos(board)

    x_distance = abs(goal_x - x)
    y_distance = abs(goal_y - y)

    # for now, pythagorean theorem
    distance = math.floor(math.sqrt(pow(x_distance, 2) + pow(y_distance,2)))

    return distance

def pawns_in_goal(pawns):
    pawnsInGoal = 0
    for pawn in pawns:
        x = pawn[0]
        y = pawn[1]
        if rows == 8:
            #add 10 players to each side
            if x in range(0,4):
                if y in range(4+x,8):
                    pawnsInGoal += 1
        elif rows == 10:
            #add 15 players to each side
            if x in range(0,5):
                if y in range(5+x,10):
                    pawnsInGoal += 1
        else:
            # add 21 players to each side
            for x in range(0,6):
                for y in range(10+x,16):
                    pawnsInGoal += 1
    return pawnsInGoal



def pawns_in_base(pawns):
    weight = 0
    for pawn in pawns:
        x = pawn[1]
        y = pawn[0]
        if rows == 8:
            #check 10 players to each side
            if x in range(0,4):
                if y in range(4+x,8):
                    weight += 1
        elif rows == 10:
            #check 15 players to each side
            if x in range(0,5):
                if y in range(5+x,10):
                    weight += 1
        else:
            # check 21 players to each side
            if x in range(0,6):
                if y in range(10+x,16):
                    weight += 1
        
    return weight

def pawns_in_middle(pawns):
    # Made for 8 by 8 only and checks only for player 1
    value = 0

    # for x in range(3,rows-3):
    #     if board[x][x-3] == 1:
    #         value += 1/8
    #     else board[x-3][x] == 1:
    #         value +=7/8


    for pawn in pawns:
        x = pawn[0]
        y = pawn[1]
        if pawn == (1,4) or pawn == (6,3):
            value += 2/4

        elif pawn == (4,1) or pawn == (3,6):
            value += 3/4

        elif x in range(2):
            if y in range(2):
                value += 1/20
            elif y in range(4):
                value += 1/4

        elif x in range(2,rows-2):
            if y in range(2) and x<4:
                value += 1/4
            elif y in range(2,columns-2):
                if y >= x:
                    value += 3/4
                else:
                    value += 2/4
            else:
                value += 1/4

        elif x in range(rows-2,rows):
            if y in range(rows-2,rows):
                value += 1/20
            elif y in range(4,6):
                value +=1/4


    return value


            



# END MINI-MAX ==========================================================================================================


# MOVE GENERATOR =======================================================================================================
def move_generator(board, player):
    """
    Generate all moves for one player
    :param board: The current board being worked with
    :param player: The current player
    :return: A list of all boards generated by each legal move
    """
    moves = []

    for y in range(rows):
        for x in range(columns):
            if board[y][x] == player:  # position holds a player 1 pawn
                # generate all moves for that pawn and add them to the list of moves
                moves += gen_pawn_moves(x, y, board, player)

    return moves


def gen_pawn_moves(x, y, board, player):
    """
    Generate all moves for one pawn
    :param x: The column position of the pawn
    :param y: The row position of the pawn
    :param board: The current board being worked with
    :param player: The current player
    :return: A list of boards created by each move
    """
    moves = []
    #MOVE ORDERING
    # find all the jump-moves a pawn could take and add them to the list of moves
    moves += gen_jump_moves(x, y, player, board)
    # find all the single-moves a pawn could take and add them to the list of moves
    moves += gen_single_moves(x, y, board, player)
    return moves


def gen_single_moves(x, y, board, player):
    """
    Generate all single-position moves a pawn could take
    :param x: The column position of the pawn
    :param y: The row position of the pawn
    :param board: The current board being worked with
    :param player: The current player
    :return: A list of boards created by each single-move
    """
    moves = []
    # The positions to consider:
    consider = gen_next_positions(x, y)
    for position in consider:
        column, row = position
        # if there is no pawn in that position, the current pawn can move there
        if board[row][column] == 0:
            # the new board this move would create
            new_board = deepcopy(board)
            new_board[y][x] = 0
            new_board[row][column] = player
            # add the new board to the list of moves
            moves.append(new_board)
    return moves


def gen_jump_moves(x, y, player, board, path=set()):
    """
    Generate all jump-moves a pawn could take, without making duplicate moves - where the pawn can make the same move,
    but by jumping a different path.
    Because jump moves can be chained, it must find those as well, using RECURSION to keep jumping until there are no 
    more positions to jump to.
    The algorithm works by looking at one pawn, and checking all the positions around it to see if there is a pawn to
    jump. Then it makes the jump, creating the new_board and saving it to the list of moves, and also records this move
    in the path set. This path set is created on the first run of this method, so each pawn has it's own path set. 
    The current move is checked against the path set, blocking the pawn from going to that position again, as it would
    be a waste of time.
    :param x: The column position of the pawn
    :param y: The row position of the pawn
    :param player: The current player
    :param board: A board object (2D Array) that represents the current move/board the pawn is making
    :param path: A set of coordinates of places that the pawn has already discovered
    :return: A list of boards created by each move
    """
    # DEBUG ============================================================================================================
    # print("Running jump moves algorithm...\n")
    # ==================================================================================================================

    moves = []  # a list of moves to be returned

    # The positions to consider:
    consider = gen_next_positions(x, y)

    # Look at each position
    for position in consider:
        i, j = position

        # If there is a pawn in that position, we can possibly jump it
        if board[j][i] in [1, 2]:
            # check if there is space open to jump, and if the jump takes the pawn off the board
            new_x, new_y = jump(x, y, i, j)  # get the coordinates of where the pawn will land
            z = prune({(new_x, new_y)})  # prune the coordinates away if it is outside the board

            # If there is a place to land (inside the board, not on the path, and on an empty space)
            if len(z) != 0 and len(z & path) == 0 and board[new_y][new_x] == 0:
                # DEBUG ================================================================================================
                # print("Jumping pawn (" + str(x) + "," + str(y) + ") to space (" + str(new_x) + "," + str(new_y) + ")\n")
                # print("Current Board")
                # display_board(board)
                # print()
                # ======================================================================================================

                # Make the new board this move would create
                # ------------------------------------------------------------------------------------------------------
                new_board = deepcopy(board)  # copy the previous board
                new_board[y][x] = 0  # remove the pawn from its old position
                new_board[new_y][new_x] = player  # place it in its new position
                # ------------------------------------------------------------------------------------------------------

                # DEBUG ================================================================================================
                # print("New board created by move:")
                # display_board(new_board)
                # print()
                # ======================================================================================================

                # ------------------------------------------------------------------------------------------------------
                moves.append(new_board)  # add the new board to the list of moves
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                path.add((new_x, new_y))  # add the previous position to the path
                # ------------------------------------------------------------------------------------------------------

                # DEBUG ================================================================================================
                # print("Path:")
                # print(path)
                # print()
                # ======================================================================================================

                # Look for another jump!
                moves += gen_jump_moves(new_x, new_y, player, new_board, path)

    return moves


def jump(x, y, i, j):
    """
    Calculates the new position of a jumping pawn
    Assumes all given coordinates are correct
    :param x: column coordinate of the pawn's current position
    :param y: row coordinate of the pawn's current position
    :param i: column coordinate of the pawn it is jumping
    :param j: row coordinate of the pawn it is jumping
    :return: new coordinate position of the pawn after it jumps
    """
    c = x - i
    k = y - j
    new_x = x - 2 * c
    new_y = y - 2 * k
    return new_x, new_y


def gen_next_positions(x, y):
    """
    Generates a set of (x,y) positions that a pawn must consider when moving
    :param x: The column position of the pawn
    :param y: The row position of the pawn
    :return: A set of positions surrounding the pawn
    """
    next_set = {(x - 1, y - 1),
                (x - 1, y),
                (x - 1, y + 1),
                (x, y - 1),
                (x, y + 1),
                (x + 1, y - 1),
                (x + 1, y),
                (x + 1, y + 1)}
    #
    #   [x-1, y-1]   [x-1,   y]   [x-1, y+1]
    #   [x,   y-1]     (x,y)      [x,   y+1]
    #   [x+1, y-1]   [x+1,   y]   [x+1, y+1]
    #
    # TODO: prune the positions that are out of range
    next_set = prune(next_set)
    return next_set


def prune(tiles):
    """
    Prunes away tiles that are out of the board from a set of tiles
    :param tiles: set of tiles (x,y) positions of the board
    :return: A pruned set of tiles that doesn't include out of range tiles
    """
    tiles &= board_tiles

    return tiles
# END MOVE GENERATOR ===================================================================================================

def get_pawns_set(board):
    board_set = set([])
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 1:
                board_set.add((i,j))
    return board_set


def display_board(board):
    for row in board:
        for column in row:
            print(column, end=' ')
        print()


def __main__():
    print("STARTING BOARD")
    display_board(init_board)
    print("-------------------\n\n")
    best_move = init_board
    for i in range(7):
        start = time()
        v, best_move = minimax_decision(best_move)
        print("-------------------\nBOARD {}".format(i))
        print("Heuristic value: ",v)
        display_board(best_move)
        end = time()
        t = end-start
        print("Time taken: ", t)
        print("-------------------\n\n")


if __name__ == '__main__':
    __main__()