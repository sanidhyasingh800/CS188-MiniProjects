"""
uses minimax and adversial search to find the next best move for tic tac toe 


"""


import numpy as np
from tictactoe import tictactoe

class Solver:

    def __init__(self, game):
        self.game = game

    
    def get_all_boards(self, board, player):
        boards = [] # a list of np arrays (boards)
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i][j] == -1:
                    temp_board = board.copy()
                    temp_board[i][j] = player
                    boards.append(temp_board)
        # print(boards)
        return boards

    def get_next_move(self, board):
        """ 
        takes a board and returns a position with the next best move
        first we have to define a get all possible next boards method 
        """
        v, board = self.value(board, 1)
        return board
    
    def max_value(self,board):
        v = -100000
        next_boards = self.get_all_boards(board, 1)
        best_move = np.array([])
        for b in next_boards:
            cur_v, _ = self.value(b, 0)
            if (cur_v > v):
                v = cur_v
                best_move = b

        return v, best_move
    
    def min_value(self,board):
        v = 100000
        next_boards = self.get_all_boards(board, 0)
        best_move = np.array([])
        for b in next_boards:
            cur_v, _= self.value(b, 1)
            if (cur_v <= v):
                v = cur_v
                best_move = b

        return v, best_move

    def value(self, board, agent):
        game = self.game
        if game.isWin(board, 1):
            return 1, board # a win for the computer (maxer agent)
        if game.isWin(board, 0):
            return 0, board # a win for the user (minimizer agent)
        if game.isTie(board):
            return 0.5, board # a tie
        if agent == 1: # we have a maxer agent
            return self.max_value(board)
        return self.min_value(board)
        


game = tictactoe()
solve = Solver(game)
# solve.get_next_move(game.board)


while True:
    if game.isWin(game.board, 1):
        break
    if game.isWin(game.board, 0):
        break
    game.display_board()
    game.get_move_from_player()
    game.board = solve.get_next_move(game.board)

if game.isWin(game.board, 0):
    print("User wins")
else:
    print("Computer wins")

# game.display_board()