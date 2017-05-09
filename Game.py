class Game():
	def __init__(self, aiPlayer, boardLength, boardFile=None):

		self.board = Board(boardLength,boardFile)
		# For two players, gameState just changes between 0 and 1,
        # where 0 means player 1's turn and 1 means player 2's turn
        self.gameState = 0

        # this will hold dictionaries for a player's possible moves
        # dictionaries are refreshed after every turn
        self.possibleMoves = [0,0]
        self.possibleMoves[self.gameState] = self._generateMoves()