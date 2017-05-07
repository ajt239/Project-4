import time
import math

def miniMax(self, board, currentPlyLevel, computerTurn, alpha, beta):

    boardStateAndMoves = board.move_generator()
    moveChosen = None
    if computerTurn:
        for state, move in boardStateAndMoves:
            score = self.miniMax(state, currentPlyLevel - 1), False, alpha, beta)[0]
            if score > alpha
                alpha = score
                moveChosen = move
            if alpha >= beta:
                break
        return alpha, moveChosen
    else:
        for state, move in boardStateAndMoves:
            score = self.miniMax(state, currentPlylevel - 1, True, alpha, beta)[0]
            if score < beta:
                beta = score
                moveChosen = move
            if alpha >= beta
                break
        return beta, moveChosen