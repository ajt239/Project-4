from copy import deepcopy


class Board:

    def __init__(self, board, depth, player):
        self.board = board
        self.depth = depth
        self.x_dimension = len(self.board[0])
        self.y_dimension = len(board)
        self.board_tiles = self.get_board_tiles()
        self.player = player
        self.pawn_positions = self.get_pawn_positions()
        self.jump_path = set()

    def get_pawn_positions(self):
        """
        
        :return: 
        """
        pawns = set()
        for row in range(self.y_dimension):
            for column in range(self.x_dimension):
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
        for x in range(self.y_dimension):
            for y in range(self.x_dimension):
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
        # mildPawns = pawns_in_middle(board)
        if self.y_dimension == 8:
            mildPawns = 10 - (goodPawns + badPawns)
            value = (goodPawns + mildPawns / 2 - badPawns) / 10
        elif self.y_dimension == 10:
            mildPawns = 15 - (goodPawns + badPawns)
            value = (goodPawns + mildPawns / 2 - badPawns) / 15
        else:
            mildPawns = 21 - (goodPawns + badPawns)
            value = (goodPawns + mildPawns / 2 - badPawns) / 21

        return value

    def pawns_in_goal(self):
        pawns = 0
        if self.y_dimension == 8:
            # add 10 players to each side
            for x in range(0, 4):
                for y in range(4 + x, 8):
                    if self.board[x][y] == 1:
                        pawns += 1

        else:
            # add 21 players to each side
            for x in range(0, 6):
                for y in range(10 + x, 16):
                    if self.board[x][y] == 1:
                        pawns += 1
        return pawns

    def pawns_in_base(self):
        weight = 0
        if self.y_dimension == 8:
            # add 10 players to each side
            for x in range(0, 4):
                for y in range(4 + x, 8):
                    if self.board[y][x] == 1:
                        weight += 1
        elif self.y_dimension == 10:
            # add 15 players to each side
            for x in range(0, 5):
                for y in range(5 + x, 10):
                    if self.board[y][x] == 1:
                        weight -= 1
        else:
            # add 21 players to each side
            for x in range(0, 6):
                for y in range(10 + x, 16):
                    if self.board[y][x] == 1:
                        weight -= 1
        return weight

    def pawns_in_middle(self):
        value = 0
        for x in range(2, self.y_dimension - 2):
            for y in range(2, self.y_dimension - 2):
                pass