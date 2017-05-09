from Agent_Board import Agent_Board
import math

infinity = math.inf

class Agent:

    def __init__(self):
        self.player_1 = 1
        self.player_2 = 2

    def minimax_decision(self, state):
        depth = 0
        v = -infinity
        best_move = None
        moves = state.move_generator()

        for move in moves:
            board = Agent_Board(move, depth+1, self.player_1)

            val = self.min_value(board, depth+1, -infinity, infinity)

            if val > v:
                v = val
                best_move = board

        return v, best_move

    def max_value(self, state, depth, alpha, beta):
        """
        
        :param state: 
        :param alpha: 
        :param beta: 
        :return: 
        """
        if state.cutoff_test():
            return state.utility()

        v = -infinity
        moves = state.move_generator()

        for move in moves:
            board = Agent_Board(move, depth+1, self.player_2)
            v = max(v, self.min_value(board, depth+1, alpha, beta))

            if v >= beta:
                return v
            alpha = max(alpha,v)

        return v

    def min_value(self, state, depth, alpha, beta):
        """
        
        :param state: 
        :param depth: 
        :param alpha: 
        :param beta: 
        :return: 
        """
        if state.cutoff_test():
            return state.utility()

        v = infinity

        moves = state.move_generator()

        for move in moves:
            board = Agent_Board(move, depth+1, self.player_1)
            v = min(v, self.max_value(board, depth+1, alpha, beta))

            if v <=alpha:
                return v
            beta = min(beta,v)

        return v