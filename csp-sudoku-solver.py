import constraint
import random

ROWS = 'abcdefghi'
COLS = '123456789'
DIGITS = range(1, 10)

VARS = [row + col for row in ROWS for col in COLS]
ROWGROUPS = [[row + col for col in COLS] for row in ROWS]
COLGROUPS = [[row + col for row in ROWS] for col in COLS]

SQUAREGROUPS = [
    [ROWS[3 * rowgroup + k] + COLS[3 * colgroup + j]
     for j in range(3) for k in range(3)]
    for colgroup in range(3) for rowgroup in range(3)
]

def solve(hints):
    problem = Problem()

    for var, hint in zip(VARS, hints):
        problem.addVariables([var], [hint] if hint in DIGITS else DIGITS)

    for vargroups in [ROWGROUPS, COLGROUPS, SQUAREGROUPS]:
        for vargroup in vargroups:
            problem.addConstraint(AllDifferentConstraint(), vargroup)

    return problem.getSolutions()

def pretty(var_to_value):
    board = ''
    for rownum, row in enumerate('abcdefghi'):
        for colnum, col in enumerate('123456789'):
            board += str(var_to_value[row+col]) + ' '
            if colnum % 3 == 2:
                board += ' '

        board += '\n'
        if rownum % 3 == 2:
            board += '\n'

    return board

#New Functions
def getCol(s, c):
    return s[c:len(s):9]
def getRow(s, r):
    return s[r*9:(r+1)*9]
def getBox(s, c, r):
    tmp = []
    for t in range(3):
        for x in range(3):
            tmp.append(s[r * 27 + x + (c * 3) + t * 9])
    return tmp
def checkValid(row):
    row.sort()
    for i in range(1, 10):
        if row[i-1] != i:
            return False

    return True
def generatePuzzle():
    puzzle = [
        5, 3, 4, 6, 7, 8, 9, 1, 2,
        6, 7, 2, 1, 9, 5, 3, 4, 8,
        1, 9, 8, 3, 4, 2, 5, 6, 7,
        8, 5, 9, 7, 6, 1, 4, 2, 3,
        4, 2, 6, 8, 5, 3, 7, 9, 1,
        7, 1, 3, 9, 2, 4, 8, 5, 6,
        9, 6, 1, 5, 3, 7, 2, 8, 4,
        2, 8, 7, 4, 1, 9, 6, 3, 5,
        3, 4, 5, 2, 8, 6, 1, 7, 9
    ]

    while True:
        flag = False
        #Shuffle puzzle
        for t in range(100):
            i1 = random.randint(0, 8)
            i2 = random.randint(0, 8)

            if i1 == i2:
                continue

            #0 1
            #9 10
            for i in range(9):
                puzzle[i * 9 + i1], puzzle[i * 9 + i2] = puzzle[i * 9 + i2], puzzle[i * 9 + i1]
        
        #Checking
        for r in range(3):
            for c in range(3):
                if not checkValid(getBox(puzzle, c, r)):
                    flag = True
        for r in range(3):
            if not checkValid(getRow(puzzle, r)):
                    flag = True
        for c in range(3):
            if not checkValid(getCol(puzzle, c)):
                    flag = True
        if flag:
            continue  

        break

    return puzzle
    
def hidePuzzle(p):
    tmp = list(p[:])
    for t in range(10):
        i1 = random.randint(0, 80)

        tmp[i1] = 0

    return tmp

original = generatePuzzle()
hints = hidePuzzle(original)
print(hints)

#Solving
print("length: " + str(len(solve(hints))))