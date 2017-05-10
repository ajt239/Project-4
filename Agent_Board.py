from copy import deepcopy


class Agent_Board:

    def __init__(self, board, depth, player):
        self.board = board
        self.depth = depth
        self.columns = len(self.board[0])
        self.rows = len(board)
        self.board_tiles = self.get_board_tiles()
        self.player = player
        self.pawn_positions = self.get_pawn_positions()
        self.jump_path = set()

        #self.scores = {(0,7): 100, (0,6): 100, (0,5): 100, (0,4): 100, (1,7): 100, (1,6): 100, (1,5): 100, ()}

    def get_pawn_positions(self):
        """
        
        :return: 
        """
        pawns = set()
        for row in range(self.rows):
            for column in range(self.columns):
                if self.board[row][column] == self.player:
                    pawns.add((column,row))
        return pawns

    def move_generator(self):
        moves = []

        for pawn in self.pawn_positions:
            x, y = pawn
            self.jump_path.clear()
            self.jump_path.add((x,y))
            moves += self.gen_jump_moves(x, y, self.board)

        for pawn in self.pawn_positions:
            x, y = pawn
            moves += self.gen_single_moves(x, y)

        return moves

    def gen_jump_moves(self, x, y, board):
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
        :param board: 
        :return: A list of boards created by each move
        """
        moves = []
        consider = self.gen_next_positions(x, y)

        for position in consider:
            i, j = position

            if board[j][i] in [1, 2]:

                new_x, new_y = self.jump(x,y,i,j)
                z = {(new_x, new_y)} & self.board_tiles

                if len(z) != 0 and len(z & self.jump_path) == 0 and board[new_y][new_x] == 0:
                    new_board = deepcopy(board)
                    new_board[y][x] = 0
                    new_board[new_y][new_x] = self.player

                    moves.append(new_board)
                    self.jump_path.add((new_x, new_y))

                    moves += self.gen_jump_moves(new_x, new_y, new_board)

        return moves

    def gen_single_moves(self, x, y):
        """
        
        :param x: 
        :param y: 
        :return: 
        """
        moves = []

        consider = self.gen_next_positions(x,y)
        for position in consider:
            column, row = position

            if self.board[row][column] == 0:

                new_board = deepcopy(self.board)
                new_board[y][x] = 0
                new_board[row][column] = self.player

                moves.append(new_board)

        return moves

    def gen_next_positions(self, x, y):
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
        next_set &= self.board_tiles
        return next_set

    def jump(self, x, y, i, j):
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

    def get_board_tiles(self):
        """
        
        :return: 
        """
        board_set = set([])
        for x in range(self.rows):
            for y in range(self.columns):
                board_set.add((x, y))
        return board_set

    def display_board(self):
        for row in self.board:
            for column in row:
                print(column, end=' ')
            print()
        print()

    def cutoff_test(self):

        if self.depth == 4 or self.terminal_test():
            return True
        else:
            return False

    def terminal_test(self):
        """
        8x8 board
        :param state: 
        :param depth: 
        :return: 
        """

        win = False

        if self.board[3][7] == 1 and \
            self.board[2][6] == self.board[2][7] == 1 and \
            self.board[1][5] == self.board[1][6] == self.board[1][7] == 1 and \
            self.board[0][4] == self.board[0][5] == self.board[0][6] == self.board[0][7] == 1:
            win = True
            return win

        if self.board[4][0] == 2 and \
            self.board[5][0] == self.board[5][1] == 2 and \
            self.board[6][0] == self.board[6][1] == self.board[6][2] == 2 and \
            self.board[7][0] == self.board[7][1] == self.board[7][2] == self.board[7][3] == 2:
            win = True
            return win

        return win

    def utility(self):
        value = 0
        goodPawns = self.pawns_in_goal()
        badPawns = self.pawns_in_base()
        mildPawns = self.pawns_in_middle()

        if self.rows == 8:
            # mildPawns = 10-(goodPawns+badPawns)
            value = (goodPawns + mildPawns - badPawns) / 10
        elif self.rows == 10:
            # mildPawns = 15-(goodPawns+badPawns)
            value = (goodPawns + mildPawns - badPawns) / 15
        else:
            # mildPawns = 21-(goodPawns+badPawns)
            value = (goodPawns + mildPawns - badPawns) / 21

        return value

    def pawns_in_goal(self):
        pawnsInGoal = 0
        if self.player == 1:
            for pawn in self.pawn_positions:
                x = pawn[1]
                y = pawn[0]
                if self.rows == 8:
                    # add 10 players to each side
                    if x in range(0, 4):
                        if y in range(4 + x, 8):
                            pawnsInGoal += 1
                elif self.rows == 10:
                    # add 15 players to each side
                    if x in range(0, 5):
                        if y in range(5 + x, 10):
                            pawnsInGoal += 1
                else:
                    # add 21 players to each side
                    for x in range(0, 6):
                        for y in range(10 + x, 16):
                            pawnsInGoal += 1
        else:
            for pawn in self.pawn_positions:
                x = pawn[0]
                y = pawn[1]
                if self.rows == 8:
                    # add 10 players to each side
                    if x in range(0, 4):
                        if y in range(4 + x, 8):
                            pawnsInGoal += 1
                elif self.rows == 10:
                    # add 15 players to each side
                    if x in range(0, 5):
                        if y in range(5 + x, 10):
                            pawnsInGoal += 1
                else:
                    # add 21 players to each side
                    for x in range(0, 6):
                        for y in range(10 + x, 16):
                            pawnsInGoal += 1
        return pawnsInGoal

    def pawns_in_base(self):
        weight = 0
        if self.player == 1:
            for pawn in self.pawn_positions:
                x = pawn[0]
                y = pawn[1]
                if self.rows == 8:
                    # check 10 players to each side
                    if x in range(0, 4):
                        if y in range(4 + x, 8):
                            weight += 1
                elif self.rows == 10:
                    # check 15 players to each side
                    if x in range(0, 5):
                        if y in range(5 + x, 10):
                            weight += 1
                else:
                    # check 21 players to each side
                    if x in range(0, 6):
                        if y in range(10 + x, 16):
                            weight += 1
        else:
            for pawn in self.pawn_positions:
                x = pawn[1]
                y = pawn[0]
                if self.rows == 8:
                    # check 10 players to each side
                    if x in range(0, 4):
                        if y in range(4 + x, 8):
                            weight += 1
                elif self.rows == 10:
                    # check 15 players to each side
                    if x in range(0, 5):
                        if y in range(5 + x, 10):
                            weight += 1
                else:
                    # check 21 players to each side
                    if x in range(0, 6):
                        if y in range(10 + x, 16):
                            weight += 1

        return weight

    def pawns_in_middle(self):
        # Made for 8 by 8 only and checks only for player 1
        value = 0

        # for x in range(3,rows-3):
        #     if board[x][x-3] == 1:
        #         value += 1/8
        #     else board[x-3][x] == 1:
        #         value +=7/8

        if self.player == 1:
            for pawn in self.pawn_positions:
                x = pawn[1]
                y = pawn[0]
                if pawn == (1, 4) or pawn == (6, 3):
                    value += 2 / 4

                elif pawn == (4, 1) or pawn == (3, 6):
                    value += 3 / 4

                elif x in range(2):
                    if y in range(2):
                        value += 1 / 20
                    elif y in range(4):
                        value += 1 / 4

                elif x in range(2, self.rows - 2):
                    if y in range(2) and x < 4:
                        value += 1 / 4
                    elif y in range(2, self.columns - 2):
                        if y >= x:
                            value += 3 / 4
                        else:
                            value += 2 / 4
                    else:
                        value += 1 / 4

                elif x in range(self.rows - 2, self.rows):
                    if y in range(self.rows - 2, self.rows):
                        value += 1 / 20
                    elif y in range(4, 6):
                        value += 1 / 4
        else:
            for pawn in self.pawn_positions:
                x = pawn[1]
                y = pawn[0]
                if pawn == (1, 4) or pawn == (6, 3):
                    value += 3 / 4

                elif pawn == (4, 1) or pawn == (3, 6):
                    value += 2 / 4

                elif x in range(2):
                    if y in range(2):
                        value += 1 / 20
                    elif y in range(4):
                        value += 1 / 4

                elif x in range(2, self.rows - 2):
                    if y in range(2) and x < 4:
                        value += 1 / 4
                    elif y in range(2, self.columns - 2):
                        if y >= x:
                            value += 2 / 4
                        else:
                            value += 3 / 4
                    else:
                        value += 1 / 4

                elif x in range(self.rows - 2, self.rows):
                    if y in range(self.rows - 2, self.rows):
                        value += 1 / 20
                    elif y in range(4, 6):
                        value += 1 / 4

        return value