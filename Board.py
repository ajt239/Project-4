
class Board():

    def __init__(self, boardLength, boardFile=None):
        self.board = []     # this array holds what the actual GUI is modeled after
        self.boardIndex = 0 # makes variable to find board size accessible
        
        # if there is a file, fill self.board with the file's information
        if boardFile != None:
            # for all of the lines in the file add it to self.board
            for line in boardFile:
                self.board.append(int(line.strip().split(" ")))
                self.boardIndex += 1

            boardFile.close() # close the file
        #set up a board without a board file
        else:
            self.boardIndex = boardLength
            
            # loop through and add sections to board
            for x in range(self.boardIndex):
                self.board.append([])
                for y in range(self.boardIndex):
                    self.board[x].append(0)
            # then add the players to the board
            self._addPlayers()

        # For two players, gameState just changes between 0 and 1,
        # where 0 means player 1's turn and 1 means player 2's turn
        self.gameState = 0

        # this will hold dictionaries for a player's possible moves
        # dictionaries are refreshed after every turn
        self.possibleMoves = [0,0]
        self.possibleMoves[self.gameState] = self._generateMoves()

    def getSize(self):
        return self.boardIndex

    def getGameState(self):
        return self.gameState

    def getPosition(self,x,y):
        return self.board[x][y]

    def setPosition(self,x,y,stringToSetTo):
        self.board[x][y] = stringToSetTo

    def getMoves(self,state = -1):
        if state == -1:
            return self.possibleMoves
        else:
            return self.possibleMoves[self.gameState]

    def updateBoard(self, board):
        self.board = board

    def getBoard(self):
        return self.board

    def changeGameState(self):
        # change gameState after moving the board piece
        self.gameState = (self.gameState+1)%2
        self.possibleMoves[self.gameState] = self._generateMoves()  # generateMoves for the player whose turn it now is

    # private function to add players to boards
    # 8X8 and 9X9 boards get 10 players per side
    # 10X10-15X15 boards get 15 players per side
    # 16X16 and larger board get 21 players per side
    def _addPlayers(self):
        if self.boardIndex == 8:
            #add 10 players to each side
            for j in range(0,4):
                for i in range(4+j,8):
                    self.board[j][i] = 2
                    self.board[i][j] = 1
        elif self.boardIndex == 10:
            #add 15 players to each side
            for j in range(0,5):
                for i in range(5+j,10):
                    self.board[j][i] = 2
                    self.board[i][j] = 1
        else:
            # add 21 players to each side
            for j in range(0,6):
                for i in range(10+j,16):
                    self.board[j][i] = 2
                    self.board[i][j] = 1


    # generates all possible moves for a player based on self.gamestate
    # returns a dictionary that holds as keys players to move and the value is the places they can move to
    def _generateMoves(self):
        moves = {}  #create the new dictionary
        # loop through the whole board and add every pawn's location as a key to the moves dictionary with its value as an empty list for possible moves
        for i in range(self.boardIndex):
            for j in range(self.boardIndex):
                if self.gameState == 0 and self.board[i][j] == 1:
                    moves[(i,j)] = []
                elif self.gameState == 1 and self.board[i][j] == 2:
                    moves[(i,j)] = []
        # for all the pawns added above, add to their lists of possible moves all of the moves they can make by moving once or by jumping
        for key in moves:
            self._addSingleMoves(key,moves[key])
            self._addJumpMoves(key, moves[key],self._possibleJumpSpots(key))
        return moves    #looks like {(x,y):[(move1x,move1y),(move2x,move2y)],(x1,y1):[...]}-- the key is the location and the value is a list of possible places to move to


    # looks at all 8 spaces around any pawn contained in the board and adds them to the the list of possible moves if they are empty (or do not contain any pawns)
    def _addSingleMoves(self, key, path):
        # loop through all eight squares around the pawn
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                possible_x_move = key[0]+i
                possible_y_move = key[1]+j
                # check that the new  x,y spot is not the same as the key, is on the board, and is empty
                if (possible_x_move,possible_y_move) != key \
                and possible_x_move in range(self.boardIndex) and possible_y_move in range(self.boardIndex) \
                and self.board[possible_x_move][possible_y_move] == 0:
                    path.append((possible_x_move,possible_y_move))  # if so, it is possible to move there

       
    # sort of recursive, looks for places to jump to and calls on possibleJumpSpots to get lists of places to jump to            
    def _addJumpMoves(self, key, path, possibleJumps):
        # checks if there are any pawns to jump over in possibleJumps
        if len(possibleJumps) == 0:
            return
        else:
            # loop through all jumps
            while len(possibleJumps)>0:
                jump = possibleJumps[0]
                # calculate the next x,y coordinate after making a jump
                x_spotReached = (key[0]-jump[0])*-1+jump[0]
                y_spotReached = (key[1]-jump[1])*-1+jump[1]
                # check that the coordinate has not already been reached, that it is not the key arg,
                # that it is within the board boundaries, and that it is not already occupied
                if (x_spotReached, y_spotReached) not in path and (x_spotReached, y_spotReached) != key\
                and x_spotReached in range(self.boardIndex) and y_spotReached in range(self.boardIndex) \
                and self.board[x_spotReached][y_spotReached] == 0:
                    path.append((x_spotReached,y_spotReached))      # add the spot to the path
                    self._addJumpMoves((x_spotReached,y_spotReached),path,self._possibleJumpSpots((x_spotReached,y_spotReached)))   # check if there are any jumps you can make from there

                possibleJumps.pop(0)    # remove this jump from the list of possibleJumps


    # returns a list of all neighbors to arg key that are occupied by a pawn
    def _possibleJumpSpots(self, key):
        jumps = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                possible_x_move = key[0]+i
                possible_y_move = key[1]+j
                if (possible_x_move,possible_y_move) != key \
                and possible_x_move in range(self.boardIndex) and possible_y_move in range(self.boardIndex) \
                and self.board[possible_x_move][possible_y_move] != 0:
                    jumps.append((possible_x_move,possible_y_move))
        return jumps


    def check_win(self):
        # Method for checking if there is a winner
        # method call:
        #   win, player = self.check_win()
        # 
        # Return variable can be used like this:
        #   if win:
        #       print("Player " + player " won!")
        #   else:
        #       print("No win")

        # initally, there is no win and no winner
        win = True
        winner = ""

        while win == True:
            if self.gameState == 0:
                winner = "p1"
                #check for p1 in top right
                #change win to False if anything in top right is not "p1"
                if self.boardIndex == 8:
                    #check all 10 players in top right
                    # break out of for loops when win is false
                    for j in range(0,4):
                        for i in range(4+j,8):
                            win = self.board[j][i] == 1
                            if win != True:
                                break
                        if win != True:
                            break
                elif self.boardIndex == 10:
                    #check all 15 players in top right
                    # break out of for loops when win is false
                    for j in range(0,5):
                        for i in range(5+j,10):
                            win = self.board[j][i] == 1
                            if win != True:
                                break
                        if win != True:
                            break
                else:
                    # check all 21 players in top right
                    # break out of for loops when win is false
                    for j in range(0,6):
                        for i in range(10+j,16):
                            win = self.board[j][i] == 1
                            if win != True:
                                break
                        if win != True:
                            break
                break   # break out while loop. win is still TRUE
            else:
                winner = "p2"
                #check for p2 in bottom left
                #change win to False if anything in bottom left is not "p2"
                if self.boardIndex == 8:
                    #check all 10 players in bottom left
                    # break out of for loops when win is false
                    for j in range(0,4):
                        for i in range(4+j,8):
                            win = self.board[i][j] == 2
                            if win != True:
                                break
                        if win != True:
                            break
                elif self.boardIndex == 10:
                    #check all 15 players in top right
                    # break out of for loops when win is false
                    for j in range(0,5):
                        for i in range(5+j,10):
                            win = self.board[i][j] == 2
                            if win != True:
                                break
                        if win != True:
                            break
                else:
                    # check all 21 players in top right
                    # break out of for loops when win is false
                    for j in range(0,6):
                        for i in range(10+j,16):
                            win = self.board[i][j] == 2
                            if win != True:
                                break
                        if win != True:
                            break
                break   # break out of while loop. win is still TRUE

        # Since only one player can win, the method ends when one of the players has won
        # if neither wins, return -> False, ""
        return win, winner 