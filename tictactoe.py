"""
We will design this in 3 stages
- the tictactoe UI that lets 2 people play tictactoe and defines the isTerminal Function
- then we will expand this class to return and keep track of stages, utilties, etc.
- then we implement the solver class 
- time: 60 minutes 
"""
import numpy as np
import random
class tictactoe:

    def __init__(self):
        self.board = np.array([[-1,-1,-1], [-1,-1,-1], [-1, -1, -1]])
        self.O = 0 # User 
        self.X = 1 # Computer 
    

    def isWin(self, board, player):
        winning_position = np.array([player, player, player])
        for row in board:
            if (winning_position == row).all():
                return True
        for column in board.T:
            if (winning_position == column).all():
                return True
        if board[0][0] == board[1][1] == board[2][2] == player:
            return True
        if board[0][2] == board[1][1] == board[2][0] == player:
            return True
        return False
    
    def isTie(self, board):
        for rows in board:
            if (rows == -1).any():
                return False
        if not self.isWin(board, 1) and not self.isWin(board, 0):
            return True
            
    
    def display_board(self):
        print(self.board)

    def get_move_from_player(self):
        user_input = input("Please enter move position as x,y: ")
        x,y = user_input.split(",")
        x = int(x)
        y = int(y)
        self.board[x][y] = 0
    
    def perform_move(self):
        x = random.randint(0,2)
        y = random.randint(0,2)
        while self.board[x][y] != -1:
            x = random.randint(0,2)
            y = random.randint(0,2)
        self.board[x][y] = 1


        





    
