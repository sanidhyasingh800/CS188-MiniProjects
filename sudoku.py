import numpy as np





class SudokuBoard:
    def __init__(self,board):
        self.board = board
    
    def setVariable(self, number, row, col):
        self.board[row][col] = number
    
    def constraintMet(self):
        for row in self.board:
            row = row[row !=0]
            if np.unique(row).shape[0] != row.shape[0]:
                return False
        for col in self.board.T:
            col = col[col != 0]
            if np.unique(col).shape[0] != col.shape[0]:
                return False
        for rowgroup in range(3):
            for colgroup in range(3):
                subgroup = np.array([[0,0,0], [0,0,0], [0,0,0]])
                for i in range(3):
                    for j in range(3):
                        subgroup[i][j] = self.board[i + 3*rowgroup][j + 3 *colgroup]
                subgroup = subgroup.flatten()
                subgroup = subgroup[subgroup !=0]
                if np.unique(subgroup).shape[0] != subgroup.shape[0]:
                    return False
        return True
    def getVariables(self):
        variables = []
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] == 0:
                    variables.append((i,j))
        return variables
    
    def getDomain(self):
        return [1,2,3,4,5,6,7,8,9]
    
    def setBoard(self, variables):
        for variable in variables:
            self.board[variable[0][0]][variable[0][1]] = variable[1]

    

class CSPSolver:

    def __init__(self, variables, domain, problem):
        self.variablesAndDomains = [(variable, 0, domain) for variable in variables]
        self.problem = problem
    
    def solve(self):
        self.variablesAndDomains = self.dfs(self.variablesAndDomains)
    
    def allAssigned(self, assignment):
        for variable in assignment:
            if variable[1] == 0:
                return False
        return True
    
    def changeAssignment(self, assignment, next_variable):
        for i in range(len(assignment)):
            if next_variable[0][0] == assignment[i][0][0]  and next_variable[0][1] == assignment[i][0][1]:
                assignment[i] = next_variable
                return assignment
        return assignment


    def dfs(self, assignment):
        if self.allAssigned(assignment):
            return assignment, True
        for variable in assignment:
            if variable[1] == 0:
                next_variable = variable
                break
        for value in next_variable[2]:
            self.problem.setVariable(value, next_variable[0][0], next_variable[0][1])

            if self.problem.constraintMet():
                next_variable = (next_variable[0], value, next_variable[2])
                assignment = self.changeAssignment(assignment, next_variable)
                resultingAssignment, cspmet = self.dfs(assignment)
                if self.problem.constraintMet() and self.allAssigned(assignment):
                    return resultingAssignment, True
                assignment = self.changeAssignment(assignment, (next_variable[0], 0, next_variable[2]))
                self.problem.setVariable(0, next_variable[0][0], next_variable[0][1])
    
            else:
                self.problem.setVariable(0, next_variable[0][0], next_variable[0][1])
    
        return assignment, False

sudoku = SudokuBoard(np.array([[4,0,0,3,0,0,0,0,0], 
                               [5,0,0,0,9,2,8,0,6], 
                               [8,9,0,0,0,0,1,0,7], 
                               [0,0,6,0,0,3,0,0,5], 
                               [0,8,0,7,0,0,0,0,9],
                               [0,7,0,6,4,0,3,0,0],
                               [6,0,4,0,0,7,0,0,0], 
                               [0,0,0,0,0,0,0,5,0], 
                               [0,0,3,0,1,6,0,2,8]]))

Solver = CSPSolver(sudoku.getVariables(), sudoku.getDomain(), sudoku)

Solver.solve()
print(sudoku.board)

            

            



    
