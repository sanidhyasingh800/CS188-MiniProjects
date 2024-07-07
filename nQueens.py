import numpy as np
import time 
class NQueens:
    def __init__(self, size):
        self.queens = np.arange(size) # 0th index queen on 0th column , etc, value represents the row of the queen
        for i in range(self.queens.shape[0]):
            self.queens[i] = -1
        self.size = size
        self.domain = {}
        for i in range(size):
            self.domain[i] = np.arange(size)
    
    def setVariable(self, queen, row):
        self.queens[queen] = row

    def convertQueensToBoard(self):
        self.board = np.zeros((self.size, self.size))
        queens = self.queens
        for i in range(queens.shape[0]):
            if queens[i] != -1:
                self.board[queens[i]][i] = 1

    
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
    
    def minconflicts(self):
        self.convertQueensToBoard()
        total = 0
        for row in self.board:
            if np.sum(row) > 1:
                total += np.sum(row)
        for col in self.board.T:
            if np.sum(col) > 1:
                total += np.sum(col)
        diag = self.board.shape[0]
        for i in range(-1*(diag+1), diag):
            if np.sum(self.board.diagonal(i)) > 1:
                total += np.sum(self.board.diagonal(i)) 
            flipped_board = np.fliplr(self.board)
        for i in range(-1*(diag+1), diag):
            if np.sum(flipped_board.diagonal(i)) > 1:
                total += np.sum(flipped_board.diagonal(i))
        return total
    
    def getQueenWithMostConflicts(self):
        ## returns the queen with the most row conflicts 
        self.convertQueensToBoard()
        maxQueen = -1
        conflicts = -1000
        for queen in range(self.size):
            row = self.queens[queen]
            if np.sum(self.board[row]) > conflicts:
                maxQueen = queen
                conflicts = np.sum(self.board[row])
        return maxQueen

    
    def getRandomAssignment(self):
        size = self.size
        for i in range(self.queens.shape[0]):
            self.queens[i] = np.random.randint(0, size)
    
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
        self.problem.queens, cspmet = self.backtrackWithForwardChecking() # self.localSearch(500)
        print(cspmet)
        print(self.problem.constraintMet())
    
    def allAssigned(self, queens):
        for queen in queens:
            if queen == -1:
                return False
        return True
    
    def localSearch(self, iterations):
        for i in range(10): # 10 random restarts 
            self.problem.getRandomAssignment()
            numVars = self.problem.size
            minimumConflict = self.problem.minconflicts()
            for i in range(iterations): # perform iterative local search
                if self.problem.constraintMet():
                    return self.problem.queens, self.problem.minconflicts()
                queen = np.random.randint(0, numVars) # get any random queen 
                # queen = self.problem.getQueenWithMostConflicts()
                # find the value for chosen queen that minizes conflict
                for row in self.problem.domain[queen]:
                    current_row = self.problem.queens[queen]
                    self.problem.setVariable(queen, row)
                    new_conflict = self.problem.minconflicts()
                    if new_conflict <= minimumConflict:
                        minimumConflict = new_conflict
                    else:
                        self.problem.setVariable(queen, current_row)

        return self.problem.queens, self.problem.minconflicts()


    
    def backtrack(self):
        # return if assignment is complete, no check for illegal assignments
        if self.allAssigned(self.problem.queens):
            return self.problem.queens, True
        
        # find next unassigned variable
        for i in range(self.problem.queens.shape[0]):
            if self.problem.queens[i] == -1:
                queen = i
                break
        
        # try out each value for the unassigned variable, call backtrack for each new assignment to simulate dfs behavior
        for row in self.problem.domain[queen]:
            self.problem.setVariable(queen, row)
            if self.problem.constraintMet():  # partial assignments are also checked against constraints (main idea behind backtracking)
                ## perform filtering here, if any
                self.problem.queens, cspmet = self.backtrack()  # dfs call
                if self.problem.constraintMet() and self.allAssigned(self.problem.queens): # checking for goal state 
                    return self.problem.queens, True
            else:
                self.problem.setVariable(queen, -1) # if all possibilities fail for this variable, we backtrack and reset 
    
        return self.problem.queens, False
    
    def backtrackWithForwardChecking(self):
        # return if assignment is complete, no check for illegal assignments
        if self.allAssigned(self.problem.queens):
            return self.problem.queens, True
        
        # find next unassigned variable
        for i in range(self.problem.queens.shape[0]):
            if self.problem.queens[i] == -1:
                queen = i
                break
        
        # try out each value for the unassigned variable, call backtrack for each new assignment to simulate dfs behavior
        original_domain = {key: np.copy(value) for key, value in self.problem.domain.items()}
        for row in self.problem.domain[queen]:
            self.problem.setVariable(queen, row)
            if self.problem.constraintMet():  # partial assignments are also checked against constraints (main idea behind backtracking)
                ## forward checking (deletion of domain based on same row (diagonals not checked))

                for key in self.problem.domain.keys():
                    if self.problem.queens[key] == -1:
                        domain = self.problem.domain[key]
                        domain = np.delete(domain, np.where(domain == row))
                        self.problem.domain[key] = domain
        
                self.problem.queens, cspmet = self.backtrackWithForwardChecking()  # dfs call
                if self.problem.constraintMet() and self.allAssigned(self.problem.queens): # checking for goal state 
                    return self.problem.queens, True
                # reset domain if no possible configuration given current_var = current_val
                self.problem.domain = {key: np.copy(value) for key, value in original_domain.items()}

            else:
                self.problem.setVariable(queen, -1) # if all possibilities fail for this variable, we backtrack and reset 

    
        return self.problem.queens, False
    
    def dfs(self):
        # return if assignment is complete, no check for illegal assignments
        if self.allAssigned(self.problem.queens):
            return self.problem.queens, True
        
        # find next unassigned variable
        for i in range(self.problem.queens.shape[0]):
            if self.problem.queens[i] == -1:
                queen = i
                break
        
        # try out each value for the unassigned variable, call dfs for each new assignment 
        for row in self.problem.getDomain():
            self.problem.setVariable(queen, row)
            # if self.problem.constraintMet(): #no constraint checking done at intermediate step! (this is the difference between backtrack and dfs)
            self.problem.queens, cspmet = self.dfs()  # dfs call
            ## perform filtering here, if any
            if self.problem.constraintMet() and self.allAssigned(self.problem.queens): # checking for goal state 
                return self.problem.queens, True
            else:
                self.problem.setVariable(queen, -1) # if all possibilities fail for this variable, we reset domain
    
        return self.problem.queens, False


nQueens = NQueens(20)
Solver = nQueensSolver(nQueens)
start_time = time.time()
Solver.solve()
end_time = time.time()

nQueens.convertQueensToBoard()
print(nQueens.board)
print(nQueens.queens)
print("Time taken:", end_time - start_time, "seconds")




