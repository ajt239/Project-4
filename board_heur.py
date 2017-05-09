from copy import deepcopy
from time import time
import statistics
import math
def evaluate(board):
    """
    Heuristic function to evaluate a state
    :param state: 
    :return: 
    """

    # value = 0                                                           # initialize state's value
    # distances = []                                                      # array of each pawn's distance to goal

    # # Find the overall distance to the goal = average of all the pieces distances to goal
    # # ------------------------------------------------------------------------------------------------------------------
    # for y in range(rows):
    #     for x in range(columns):
    #         if state[y][x] == 1:                                        # Find each Agent pawn on the board
    #                                                                     # TODO: distance function
    #             distance = get_distance(x,y)                            # Get the distance of that pawn to the goal
    #             distance = math.floor((1 - distance/8) * 100)           # Percentage completed
    #             distances.append(distance)                              # add the distance to the array
    # # ------------------------------------------------------------------------------------------------------------------

    # # avg_dist = statistics.harmonic_mean(distances)?
    # # avg_dist = statistics.median(distances)
    # # avg_dist = statistics.mode(distances)
    # avg_dist = statistics.mean(distances)

    # value += avg_dist

    value = 0
    if rows == 8:
        goodPawns = pawns_in_goal(board)
        badPawns = pawns_in_base(board)
        mildPawns = 10-(goodPawns+badPawns)
        value = (goodPawns + mildPawns/2 - badPawns)/10
    elif rows == 10:
        goodPawns = pawns_in_goal(board)
        badPawns = pawns_in_base(board)
        mildPawns = 15-(goodPawns+badPawns)
        value = (goodPawns + mildPawns/2 - badPawns)/15
    else:
        goodPawns = pawns_in_goal(board)
        badPawns = pawns_in_base(board)
        mildPawns = 21-(goodPawns+badPawns)
        value = (goodPawns + mildPawns/2 - badPawns)/21
    display_board(board)
    print(value)

    return value


def get_distance(x,y):
    # TODO: Edit this so it gets the distance left to the deepest position of the win area that is not filled by '1'
    # TODO: Does this need to be under-estimated? => distance defined by how many jumps it would take to get there
    """
    Get the fraction/ratio of distance the pawn has left to the goal
    The goal is defined as the middle position of the winning area: (6,1) 
    :param x: 
    :param y: 
    :return: 
    """
    goal_x = 6
    goal_y = 1

    x_distance = abs(goal_x - x)
    y_distance = abs(goal_y - y)

    # for now, pythagorean theorem
    distance = math.floor(math.sqrt(pow(x_distance, 2) + pow(y_distance,2)))

    return distance

def pawns_in_goal(board):
    pawns = 0
    if rows == 8:
        #add 10 players to each side
        for x in range(0,4):
            for y in range(4+x,8):
                if board[x][y] == 1:
                    pawns += 1
    elif rows == 10:
        #add 15 players to each side
        for x in range(0,5):
            for y in range(5+x,10):
                if board[x][y] == 1:
                    pawns += 1
    else:
        # add 21 players to each side
        for x in range(0,6):
            for y in range(10+x,16):
                if board[x][y] == 1:
                    pawns += 1
    return pawns



def pawns_in_base(board):
    weight = 0
    if rows == 8:
        #add 10 players to each side
        for x in range(0,4):
            for y in range(4+x,8):
                if board[y][x] == 1:
                    weight += 1
    elif rows == 10:
        #add 15 players to each side
        for x in range(0,5):
            for y in range(5+x,10):
                if board[y][x] == 1:
                    weight -= 1
    else:
        # add 21 players to each side
        for x in range(0,6):
            for y in range(10+x,16):
                if board[y][x] == 1:
                    weight -= 1
    return weight

def display_board(board):
    for row in board:
        for column in row:
            print(column, end=' ')
        print()

#              0  1  2  3  4  5  6  7
init_board = [[0, 0, 0, 0, 2, 2, 2, 2],  # 0
              [0, 0, 0, 0, 0, 2, 0, 2],  # 1
              [0, 0, 0, 0, 0, 1, 2, 2],  # 2
              [0, 0, 0, 0, 0, 0, 0, 2],  # 3
              [1, 0, 0, 1, 0, 0, 0, 0],  # 4
              [0, 1, 0, 0, 0, 0, 0, 0],  # 5
              [1, 1, 0, 0, 0, 0, 0, 0],  # 6
              [1, 1, 1, 0, 0, 0, 0, 0]]  # 7

#              0  1  2  3  4  5  6  7
bigJump_board = [[0, 0, 0, 0, 2, 2, 2, 2],  # 0
              [0, 0, 0, 0, 0, 2, 1, 2],  # 1
              [0, 0, 0, 0, 0, 1, 2, 2],  # 2
              [0, 0, 0, 0, 0, 0, 0, 2],  # 3
              [1, 0, 0, 1, 0, 0, 0, 0],  # 4
              [0, 1, 0, 0, 0, 0, 0, 0],  # 5
              [1, 1, 0, 0, 0, 0, 0, 0],  # 6
              [0, 1, 1, 0, 0, 0, 0, 0]]  # 7

#              0  1  2  3  4  5  6  7
noJump_board = [[0, 0, 0, 0, 2, 2, 2, 2],  # 0
              [0, 0, 0, 0, 0, 2, 0, 2],  # 1
              [0, 0, 0, 1, 0, 1, 2, 2],  # 2
              [1, 0, 0, 0, 0, 0, 0, 2],  # 3
              [0, 0, 0, 1, 0, 0, 0, 0],  # 4
              [0, 1, 0, 0, 0, 0, 0, 0],  # 5
              [1, 1, 0, 0, 0, 0, 0, 0],  # 6
              [1, 1, 1, 0, 0, 0, 0, 0]]  # 7

#              0  1  2  3  4  5  6  7
nextJump_board = [[0, 0, 0, 0, 2, 1, 2, 2],  # 0
              [0, 0, 0, 0, 0, 2, 0, 2],  # 1
              [0, 0, 0, 0, 0, 1, 2, 2],  # 2
              [0, 0, 0, 0, 0, 0, 0, 2],  # 3
              [1, 0, 0, 1, 0, 0, 0, 0],  # 4
              [0, 1, 0, 0, 0, 0, 0, 0],  # 5
              [1, 1, 0, 0, 0, 0, 0, 0],  # 6
              [0, 1, 1, 0, 0, 0, 0, 0]]  # 7


rows = 8
columns = 8

evaluate(init_board)
evaluate(bigJump_board)
evaluate(noJump_board)
evaluate(nextJump_board)
