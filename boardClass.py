from tkinter import *
import time

class BoardGUI(Frame):

    
    def __init__(self, boardLength, boardFile = None, master =None):
        # check the the board size is correct for Halma
        if boardLength not in [8, 10, 16]:
            quit()

        self.board = []     # this array holds what the actual GUI is modeled after
        self.boardIndex = 0 # makes variable to find board size accessible
        
        # if there is a file, fill self.board with the file's information
        if boardFile != None:
            # for all of the lines in the file add it to self.board
            for line in boardFile:
                self.board.append(line.strip().split(" "))
                self.boardIndex += 1

            boardFile.close() # close the file
            
            # check to make sure the inputted file has the same number of lines
            # that was original inputted for the length if not then quit
            if self.boardIndex != boardLength:
                quit()
                
        #set up a board without a board file
        else:
            self.boardIndex = boardLength
            
            # loop through and add sections to board
            for x in range(self.boardIndex):
                self.board.append([])
                for y in range(self.boardIndex):
                    self.board[x].append("e")
            # then add the players to the board
            self._addPlayers()
                    
        # For two players, gameState just changes between 0 and 1,
        # where 0 means player 1's turn and 1 means player 2's turn
        self.gameState = 0

        # this will hold dictionaries for a player's possible moves
        # dictionaries are refreshed after every turn
        self.possibleMoves = [0,0]
        self.possibleMoves[self.gameState] = self._generateMoves()

        # create the frame for the GUI and set it on a grid
        Frame.__init__(self,master)
        self.master.title("Play Halma")
        self.grid(row=0, column=0, sticky=N+S+E+W)

        #set up the first label, which will change as the users play
        self.lbl = Label(text = "Welcome to Halma! \nPlayer 1 please enter your move!")
        self.lbl.grid(row=0,columnspan = self.boardIndex+1, sticky=N+S+E+W)

        # a list to hold all of the alphabet characters, used for the board and reading user entries
        self.alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P",
                    "Q","R","S","T","U","V","W","X","Y","Z"]
        
        # set up the top and side labels for the board
        for x in range(self.boardIndex):
            # top horizontal alphabetical labels
            label = Label(text = self.alphabet[x])
            label.grid(row = 1,column = x+1, sticky = N+S+E+W)
            # 0th column vertical numerical labels
            label2 = Label(text = str(x))
            label2.grid(row = x+2,column = 0, sticky = N+S+E+W)
            

        # initialize the array to hold the buttons
        self.boardButtons = []

        # fill the button array and
        # set the button text equal to the self.board's text
        for x in range(self.boardIndex):
            self.boardButtons.append([])
            
            for y in range(self.boardIndex):
                # check if the space is "e"
                # and if it is not, set the button text to what is in self.board
                if self.board[x][y] != "e":
                    self.boardButtons[x].append(Button(text = self.board[x][y],
                                                    command = lambda x=x, y=y: self.press(x,y)))
                # if it is, set the text to five empty spaces, which keeps it the same size as the others  
                else:
                    self.boardButtons[x].append(Button(text = "     ",
                                                    command = lambda x=x, y=y: self.press(x,y)))
                
                # these buttons are not actually meant to be pressed on; so don't give the user the option
                self.boardButtons[x][y]["state"] = DISABLED

                if (x+y) % 2 == 0:
                    self.boardButtons[x][y]["bg"] = "white"
                else:
                    self.boardButtons[x][y]["bg"] = "black"
                
                # add the button to the board
                self.boardButtons[x][y].grid(row=x+2, column=y+1, sticky=N+S+E+W)

        # initailize the entry area and add it to the grid
        self.e = Entry()
        self.e.grid(row=self.boardIndex+2, columnspan = self.boardIndex-1,\
                      sticky=N+S+E+W)
        
        # initialize the submit button-- which will read from the entry area above onclick--
        # and add it to the grid
        self.submit = Button(text="Submit", command = self._submit)
        self.submit.grid(row= self.boardIndex+2, column = self.boardIndex-1,\
                         columnspan = 3, sticky=N+S+E+W)

        self.startTime = time.time()


    # private function to add players to boards
    # 8X8 and 9X9 boards get 10 players per side
    # 10X10-15X15 boards get 15 players per side
    # 16X16 and larger board get 21 players per side
    def _addPlayers(self):
        if self.boardIndex == 8:
            #add 10 players to each side
            for j in range(0,4):
                for i in range(4+j,8):
                    self.board[j][i] = "p2"
                    self.board[i][j] = "p1"
        elif self.boardIndex == 10:
            #add 15 players to each side
            for j in range(0,5):
                for i in range(5+j,10):
                    self.board[j][i] = "p2"
                    self.board[i][j] = "p1"
        else:
            # add 21 players to each side
            for j in range(0,6):
                for i in range(10+j,16):
                    self.board[j][i] = "p2"
                    self.board[i][j] = "p1"

                    
    # this is the command that reads from the entry field
    # it checks the input, and then presses those spots
    def _submit(self):
        submittedMove = self.e.get()    # get what is in the entry field
        moveSplit = submittedMove.split("->")   # split it on the arrow

        self.e.delete(0,END)            # deletes the string in the entry field

        # if the string split is smaller than one, submittedMove is invalid
        if len(moveSplit) < 2:
            # change the top label and leave the function
            self.lbl["text"] = "{:04.2f}: {} is invalid. \n Enter something like: a1->b0".format((time.time()-self.startTime)/60,submittedMove)
            return
        # the submittedMove might be valid; so check each part of it is after it is split
        else:
            coords = [] # holds coordinate tuples to call press on
            
            # check each move in moveSplit is valid
            for move in moveSplit:
                # it is valid if there are only two characters in the string,
                # if the first character is is within self.alphabet,
                # and if the second character is within 0 to self.boardIndex
                if len(move) not in [2,3] and move[0].upper() not in self.alphabet[:self.boardIndex] and int(''.join(move[1:])) not in range(self.boardIndex):
                    # change the label because the move is invalid and leave the function
                    self.lbl["text"] = "{:04.2f}: {} is invalid. \n Enter something like: a1->b0".format((time.time()-self.startTime)/60,submittedMove)
                    return
                else:
                    # the move is valid so add a tuple of the x and y coordinates to coords
                    coords.append((int(''.join(move[1:])), self.alphabet.index(move[0].upper())))

            # check that the first coordinate is a key for the possibleMoves for this player
            if coords[0] in self.possibleMoves[self.gameState]:
                # check that the second coordinat is a value for that key
                if coords[1] in self.possibleMoves[self.gameState][coords[0]]:
                    self._unHighlightButton()
                    # call the press function for the above coordinates because they are a possible move
                    for x_coord, y_coord in coords:
                        self.press(x_coord,y_coord)
                    
                    win, winner = self.check_win()
                    if win == True:
                        self._disableGUI(winner)
                        return
                    else:
                        # change gameState after moving the board piece
                        self.gameState = (self.gameState+1)%2
                        self.possibleMoves[self.gameState] = self._generateMoves()  # generateMoves for the player whose turn it now is
                        self.lbl["text"] = "{:04.2f}: Player {} moved from {}{} to {}{}.\nPlayer {}, enter a move.".format((time.time()-self.startTime)/60,\
                                                                                                                           -self.gameState+2,\
                                                                                                                           self.alphabet[coords[0][1]],coords[0][0],\
                                                                                                                           self.alphabet[coords[1][1]],coords[1][0],\
                                                                                                                           self.gameState+1)
                        return  # leave the function

            # valid but impossible move entered; so let the user know
            self.lbl["text"] = "{:04.2f}: {} is impossible.\nEnter a better move Player {}".format((time.time()-self.startTime)/60,submittedMove,self.gameState+1)

            
    # takes in an x and y coordinate
    def press(self,x,y):
        # changes self.board[x][y] to whatever it should be after being pressed
        # and self.lbl to show what has happened
        if self.board[x][y] == "e":
            if self.gameState == 0:
                self.board[x][y] = "p1"
                self.boardButtons[x][y]["text"] = self.board[x][y]
            else:
                self.board[x][y] = "p2"
                self.boardButtons[x][y]["text"] = self.board[x][y]
        else:
           self.board[x][y] = "e"
           self.boardButtons[x][y]["text"] = "     "

        # highlight the pressed button
        self.boardButtons[x][y]["bg"] = "yellow"
    

    # just updates the button color based off of self.board
    # to highlight moves that had been made
    def _unHighlightButton(self):
        for x in range(self.boardIndex):
            for y in range(self.boardIndex):
                if self.boardButtons[x][y]["bg"]=="yellow":
                    if (x+y) % 2 == 0:
                        self.boardButtons[x][y]["bg"] = "white"
                    else:
                        self.boardButtons[x][y]["bg"] = "black"


    # generates all possible moves for a player based on self.gamestate
    # returns a dictionary that holds as keys players to move and the value is the places they can move to
    def _generateMoves(self):
        moves = {}  #create the new dictionary
        # loop through the whole board and add every pawn's location as a key to the moves dictionary with its value as an empty list for possible moves
        for i in range(self.boardIndex):
            for j in range(self.boardIndex):
                if self.gameState == 0 and self.board[i][j] == "p1":
                    moves[(i,j)] = []
                elif self.gameState == 1 and self.board[i][j] == "p2":
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
                and self.board[possible_x_move][possible_y_move] == "e":
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
                and self.board[x_spotReached][y_spotReached] == "e":
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
                and self.board[possible_x_move][possible_y_move] != "e":
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
                            win = self.board[j][i] == "p1"
                            if win != True:
                                break
                        if win != True:
                            break
                elif self.boardIndex == 10:
                    #check all 15 players in top right
                    # break out of for loops when win is false
                    for j in range(0,5):
                        for i in range(5+j,10):
                            win = self.board[j][i] == "p1"
                            if win != True:
                                break
                        if win != True:
                            break
                else:
                    # check all 21 players in top right
                    # break out of for loops when win is false
                    for j in range(0,6):
                        for i in range(10+j,16):
                            win = self.board[j][i] == "p1"
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
                            win = self.board[i][j] == "p2"
                            if win != True:
                                break
                        if win != True:
                            break
                elif self.boardIndex == 10:
                    #check all 15 players in top right
                    # break out of for loops when win is false
                    for j in range(0,5):
                        for i in range(5+j,10):
                            win = self.board[i][j] == "p2"
                            if win != True:
                                break
                        if win != True:
                            break
                else:
                    # check all 21 players in top right
                    # break out of for loops when win is false
                    for j in range(0,6):
                        for i in range(10+j,16):
                            win = self.board[i][j] == "p2"
                            if win != True:
                                break
                        if win != True:
                            break
                break   # break out of while loop. win is still TRUE

        # Since only one player can win, the method ends when one of the players has won
        # if neither wins, return -> False, ""
        return win, winner           


    # make it so the game can no longer be played and let the users know who won
    def _disableGUI(self, winner):
        self.e["state"] = DISABLED
        self.submit["state"] = DISABLED
        self.lbl["text"] = "{:04.2f}: Player {} has won! \nWoohoo!!".format((time.time()-self.startTime)/60,self.gameState+1)
                    
file = open("halma16Board.txt",'r')    # open the file with the board in it          
bFrame = BoardGUI(16)        # initiailize the BoardGUI
bFrame.mainloop()   # frame method that updates BoardGUI
        
