from tkinter import *
from Board import Board
from Agent_Board import Agent_Board
from Agent import Agent
import time


class BoardGUI(Frame):
    def __init__(self, boardLength, ai = 0, boardFile=None, master=None):
        # check the the board size is correct for Halma
        if boardLength not in [8, 10, 16]:
            quit()

        self.board = Board(boardLength, boardFile)  # this array holds what the actual GUI is modeled after
        self.boardIndex = self.board.getSize()  # makes variable to find board size accessible
        self.buttonText = ["    ", "p1", "p2"]

        # if there is a file, fill self.board with the file's information
        if boardFile != None:
            # check to make sure the inputted file has the same number of lines
            # that was original inputted for the length if not then quit
            if self.boardIndex != boardLength:
                quit()
        self.ai = ai
        self.agent = Agent()

        # create the frame for the GUI and set it on a grid
        Frame.__init__(self, master)
        self.master.title("Play Halma")
        self.grid(row=0, column=0, sticky=N + S + E + W)

        # set up the first label, which will change as the users play
        self.lbl = Label(text="Welcome to Halma! \nPlayer 1 please enter your move!")
        self.lbl.grid(row=0, columnspan=self.boardIndex + 1, sticky=N + S + E + W)

        # a list to hold all of the alphabet characters, used for the board and reading user entries
        self.alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
                         "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        # set up the top and side labels for the board
        for x in range(self.boardIndex):
            # top horizontal alphabetical labels
            label = Label(text=self.alphabet[x])
            label.grid(row=1, column=x + 1, sticky=N + S + E + W)
            # 0th column vertical numerical labels
            label2 = Label(text=str(x))
            label2.grid(row=x + 2, column=0, sticky=N + S + E + W)

        # initialize the array to hold the buttons
        self.boardButtons = []

        # fill the button array and
        # set the button text equal to the self.board's text
        for x in range(self.boardIndex):
            self.boardButtons.append([])

            for y in range(self.boardIndex):
                # check if the space is "e"
                # and if it is not, set the button text to what is in self.board
                self.boardButtons[x].append(Button(text=self.buttonText[self.board.getPosition(x, y)],
                                                   command=lambda x=x, y=y: self.press(x, y)))
                self.boardButtons[x][y]["state"] = DISABLED

                if (x + y) % 2 == 0:
                    self.boardButtons[x][y]["bg"] = "white"
                else:
                    self.boardButtons[x][y]["bg"] = "black"

                # add the button to the board
                self.boardButtons[x][y].grid(row=x + 2, column=y + 1, sticky=N + S + E + W)

        # initailize the entry area and add it to the grid
        self.e = Entry()
        self.e.grid(row=self.boardIndex + 2, columnspan=self.boardIndex - 1, \
                    sticky=N + S + E + W)

        # initialize the submit button-- which will read from the entry area above onclick--
        # and add it to the grid
        self.submit = Button(text="Submit", command=self._submit)
        self.submit.grid(row=self.boardIndex + 2, column=self.boardIndex - 1, \
                         columnspan=3, sticky=N + S + E + W)

        self.startTime = time.time()

    # this is the command that reads from the entry field
    # it checks the input, and then presses those spots
    def _submit(self):
        submittedMove = self.e.get()  # get what is in the entry field
        moveSplit = submittedMove.split("->")  # split it on the arrow

        self.e.delete(0, END)  # deletes the string in the entry field

        # if the string split is smaller than one, submittedMove is invalid
        if len(moveSplit) < 2:
            # change the top label and leave the function
            self.lbl["text"] = "{:04.2f}: {} is invalid. \n Enter something like: a1->b0".format(
                (time.time() - self.startTime) / 60, submittedMove)
            return
        # the submittedMove might be valid; so check each part of it is after it is split
        else:
            coords = []  # holds coordinate tuples to call press on

            # check each move in moveSplit is valid
            for move in moveSplit:
                # it is valid if there are only two characters in the string,
                # if the first character is is within self.alphabet,
                # and if the second character is within 0 to self.boardIndex
                if len(move) not in [2, 3] and move[0].upper() not in self.alphabet[:self.boardIndex] and int(
                        move[1:]) not in range(self.boardIndex):
                    # change the label because the move is invalid and leave the function
                    self.lbl["text"] = "{:04.2f}: {} is invalid. \n Enter something like: a1->b0".format(
                        (time.time() - self.startTime) / 60, submittedMove)
                    return
                else:
                    # the move is valid so add a tuple of the x and y coordinates to coords
                    coords.append((int(move[1:]), self.alphabet.index(move[0].upper())))

            # check that the first coordinate is a key for the possibleMoves for this player
            if coords[0] in self.board.getMoves(1):
                # check that the second coordinat is a value for that key
                if coords[1] in self.board.getMoves(1)[coords[0]]:
                    self._unHighlightButton()
                    # call the press function for the above coordinates because they are a possible move
                    for x_coord, y_coord in coords:
                        self.press(x_coord, y_coord)

                    win, winner = self.board.check_win()
                    if win == True:
                        self._disableGUI(winner)
                        return
                    else:
                        self.board.changeGameState()
                        self.lbl["text"] = "{:04.2f}: Player {} moved from {}{} to {}{}.\n\
                        Player {} is THINKING...".format((time.time() - self.startTime) / 60, \
                                                         -self.board.getGameState() + 2, \
                                                         self.alphabet[coords[0][1]], coords[0][0], \
                                                         self.alphabet[coords[1][1]], coords[1][0], \
                                                         self.board.getGameState() + 1)
                        if(self.ai != 0):
                            # Call the agent here
                            agent_board = Agent_Board(self.board.getBoard(), 0, 2)
                            start = time.time()
                            v, new_board = self.agent.minimax_decision(agent_board)
                            end = time.time()
                            t = end-start
                            print("Time: "+ str(t))
                            old_board = self.board.getBoard()
                            self.board.updateBoard(new_board)
                            self._unHighlightButton()
                            self._updateButtons()
                            self.highlight_move(old_board,new_board)
                            self.board.changeGameState()
                            self.lbl["text"] = "Agent moved! Player 1 it is your turn."
                        return  # leave the function

            # valid but impossible move entered; so let the user know
            self.lbl["text"] = "{:04.2f}: {} is impossible.\nEnter a better move Player {}".format \
                ((time.time() - self.startTime) / 60, submittedMove, self.board.getGameState() + 1)

    # takes in an x and y coordinate
    def press(self, x, y):
        # changes self.board[x][y] to whatever it should be after being pressed
        # and self.lbl to show what has happened
        if self.board.getPosition(x, y) == 0:
            if self.board.getGameState() == 0:
                self.board.setPosition(x, y, 1)
                self.boardButtons[x][y]["text"] = "p1"
            else:
                self.board.setPosition(x, y, 2)
                self.boardButtons[x][y]["text"] = "p2"
        else:
            self.board.setPosition(x, y, 0)
            self.boardButtons[x][y]["text"] = "     "

        # highlight the pressed button
        self.boardButtons[x][y]["bg"] = "yellow"

    def _updateButtons(self):
        for x in range(self.board.getSize()):
            for y in range(self.board.getSize()):
                text = self.board.getPosition(x, y)
                if text == 1:
                    self.boardButtons[x][y]["text"] = "p1"
                elif text == 2:
                    self.boardButtons[x][y]["text"] = "p2"
                else:
                    self.boardButtons[x][y]["text"] = "     "

    # just updates the button color based off of self.board
    # to highlight moves that had been made
    def _unHighlightButton(self):
        for x in range(self.boardIndex):
            for y in range(self.boardIndex):
                if self.boardButtons[x][y]["bg"] == "yellow":
                    if (x + y) % 2 == 0:
                        self.boardButtons[x][y]["bg"] = "white"
                    else:
                        self.boardButtons[x][y]["bg"] = "black"

    def highlight_move(self,board1,board2):
        oldx = -1
        oldy = -1
        newx = -1
        newy = -1
        for x in range(self.boardIndex):
            for y in range(self.boardIndex):
                if board1[x][y] != board2[x][y]:
                    self.boardButtons[x][y]["bg"] = "yellow"
                    """
                    if board2[x][y] == 2:
                        newx = self.alphabet[8-x]
                        newy = 8-y
                    elif board2[x][y] == 0:
                        oldx = self.alphabet[8-x]
                        oldy = 8-y
                    """
        #return oldx, oldy, newx, newy



    # make it so the game can no longer be played and let the users know who won
    def _disableGUI(self, winner):
        self.e["state"] = DISABLED
        self.submit["state"] = DISABLED
        self.lbl["text"] = "{:04.2f}: Player {} has won! \nWoohoo!!".format((time.time() - self.startTime) / 60,
                                                                            self.board.getGameState() + 1)


#file = open("halma16Board.txt",'r')    # open the file with the board in it
bFrame = BoardGUI(8)  # initiailize the BoardGUI
bFrame.mainloop()  # frame method that updates BoardGUI
