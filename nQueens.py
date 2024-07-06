import numpy as np

class NQueens:
    def __init__(self, size):
        self.queens = np.arange(size) # 0th index queen on 0th column , etc, value represents the row of the queen
        for i in range(self.queens.shape[0]):
            self.queens[i] = -1
        self.size = size
    
    def setVariable(self, queen, row):
        self.queens[queen] = row

    def convertQueensToBoard(self):
        self.board = np.zeros((self.size, self.size))
        queens = self.queens
        for i in range(queens.shape[0]):
            if queens[i] != -1:
                self.board[i][queens[i]] = 1

    
    def constraintMet(self):
        self.convertQueensToBoard()
        for row in self.board:
            if np.sum(row) > 1:
                return False
        for col in self.board.T:
            if np.sum(col) > 1:
                return False
        diag = self.board.shape[0]
        for i in range(-1*(diag+1), diag):
            if np.sum(self.board.diagonal(i)) > 1:
                return False
            flipped_board = np.fliplr(self.board)
        for i in range(-1*(diag+1), diag):
            if np.sum(flipped_board.diagonal(i)) > 1:
                return False
        return True
    
    def getVariables(self):
        return self.queens

    
    def getDomain(self):
        domain = []
        for i in range(self.size):
            domain.append(i)
        return domain
    
    def setVariable(self, queen, row):
        self.queens[queen] = row


class nQueensSolver:

    def __init__(self,problem):
        self.problem = problem
    
    def solve(self):
        self.problem.queens, cspmet = self.dfs(self.problem.queens)
        print(cspmet)
    
    def allAssigned(self, queens):
        for queen in queens:
            if queen == -1:
                return False
        return True
    
    def changeAssignment(self, assignment, next_variable):
        for i in range(len(assignment)):
            if next_variable[0][0] == assignment[i][0][0]  and next_variable[0][1] == assignment[i][0][1]:
                assignment[i] = next_variable
                return assignment
        return assignment


    def dfs(self, queens):
        if self.allAssigned(queens):
            return queens, True
        for i in range(queens.shape[0]):
            if queens[i] == -1:
                queen = i
                break
        for row in self.problem.getDomain():
            self.problem.setVariable(queen, row)
            if self.problem.constraintMet():
                resultingQueens, cspmet = self.dfs(queens)
                if self.problem.constraintMet() and self.allAssigned(resultingQueens):
                    return resultingQueens, True
                queens[queen] = -1
                self.problem.setVariable(queen, -1)
            else:
                self.problem.setVariable(queen, -1)
    
        return queens, False


nQueens = NQueens(16)
Solver = nQueensSolver(nQueens)
Solver.solve()
nQueens.convertQueensToBoard()
print(nQueens.board)
print(nQueens.queens)