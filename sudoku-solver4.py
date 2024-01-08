import time
import itertools
from pprint import pprint
from constraint import *
import random

'''
unit: box, row, col, grid
Index: start from 0
Box: 0 1 2
     3 4 5
     6 7 8
sudoku[y][x]
'''

'''------Solver-----'''
'''Helper functions'''
def create_empty_sudoku():
    sudoku = []
    for r in range(9):
        sudoku.append([0] * 9)

    return sudoku

def print_sudoku(sudoku):
    row = 0
    col = 0
    for r in range(9):
        row %= 3
        if(row == 0):
            print("-"*25)

        for c in range(9):
            col %= 3
            if(col == 0):
                print("| ", end="")

            print(sudoku[r][c], "", end="")
            col += 1

        print("|")
        row += 1
    print("-"*25)

def getBoxXYFromBoxNum(box):    
    x = box % 3 * 3
    y = int(box / 3) * 3
    return [x, y]

def getBoxNumFromXY(x, y):
    return int(y / 3) * 3 + int(x / 3)

def getBoxXYFromXY(x, y):
    return getBoxXYFromBoxNum(getBoxNumFromXY(x, y))

def getBoxRemainingNumber(box):
    box = getBoxXYFromBoxNum(box)
    checking = [item for item in range(1, 10)]

    for r in range(box[1], box[1] + 3):
        for c in range(box[0], box[0] + 3):
            if(modified_sudoku[r][c] != 0):
                checking.remove(modified_sudoku[r][c])

def countElement(list, element):
    count = 0
    for i in range(len(list)):
        if(list[i] == element):
            count += 1
    
    return count

#This function will loop number by number
#Check filled sudoku is there one remaining grid
#0 for empty, 1 for filled
def last_remaining_cell():
    for n in range(1, 10):
        #A empty sudoku for storing filled grid
        checking = create_empty_sudoku()

        #Start filling
        for r in range(9):
            for c in range(9):
                val = modified_sudoku[r][c]
                if(val == n):
                    #Fill box
                    box = getBoxXYFromXY(c, r)
                    for gr in range(3):
                        for gc in range(3):
                            checking[box[1] + gr][box[0] + gc] = 1
                    
                    #Fill row
                    for rr in range(9):
                        checking[rr][c] = 1

                    #Fill col
                    for cc in range(9):
                        checking[r][cc] = 1
                elif(val != 0):
                    checking[r][c] = 1

        #Check remaining one grid
        #Box
        for b in range(9):
            count = 0
            box = getBoxXYFromBoxNum(b)
            last_empty_grid = [-1, -1]
            #Find 0 amount
            for r in range(box[1], box[1] + 3):
                for c in range(box[0], box[0] + 3):
                    if(checking[r][c] == 0):
                        count += 1
                        last_empty_grid[0] = c
                        last_empty_grid[1] = r

            #If amount == 1, then fill it
            if(count == 1):
                modified_sudoku[last_empty_grid[1]][last_empty_grid[0]] = n
                action_log.append([
                    "last_remaining_cell_box",
                    last_empty_grid[0],
                    last_empty_grid[1],
                    n
                ])
                getNotes()
                return True
        
        #Row
        for r in range(9):
            count = 0
            last_empty_grid = [-1, -1]
            #Find 0 amount
            for c in range(9):
                if(checking[r][c] == 0):
                    count += 1
                    last_empty_grid[0] = c
                    last_empty_grid[1] = r

            #If amount == 1, then fill it
            if(count == 1):
                modified_sudoku[last_empty_grid[1]][last_empty_grid[0]] = n
                action_log.append([
                    "last_remaining_cell_row",
                    last_empty_grid[0],
                    last_empty_grid[1],
                    n
                ])
                getNotes()
                return True
        
        #Col
        for c in range(9):
            count = 0
            last_empty_grid = [-1, -1]
            #Find 0 amount
            for r in range(9):
                if(checking[r][c] == 0):
                    count += 1
                    last_empty_grid[0] = c
                    last_empty_grid[1] = r

            #If amount == 1, then fill it
            if(count == 1):
                modified_sudoku[last_empty_grid[1]][last_empty_grid[0]] = n
                action_log.append([
                    "last_remaining_cell_row",
                    last_empty_grid[0],
                    last_empty_grid[1],
                    n
                ])
                getNotes()
                return True
    
    return False

#0 for possible, 1 for filled
def getNote(x, y):
    if(modified_sudoku[y][x] != 0):
        return []

    #Index - 1
    possible = [0] * 9

    #Loop Box
    box = getBoxXYFromXY(x, y)
    for gr in range(box[1], box[1] + 3):
        for gc in range(box[0], box[0] + 3):
            val = modified_sudoku[gr][gc]
            if(val != 0):
                possible[val - 1] = 1
                
    #Loop Row
    for gr in range(9):
        val = modified_sudoku[gr][x]
        if(val != 0):
            possible[val - 1] = 1

    #Loop Col
    for gc in range(9):
        val = modified_sudoku[y][gc]
        if(val != 0):
            possible[val - 1] = 1

    return possible

def create_empty_sudoku_note():
    sudoku_note.clear()
    for r in range(9):
        sudoku_note.append([] * 9)
        for c in range(9):
            sudoku_note[r].append([] * 9)

    return sudoku_note

def getNotes():
    create_empty_sudoku_note()

    #Loop through grid and get all notes
    for r in range(9):
        for c in range(9):
            sudoku_note[r][c] = getNote(c, r)

def getNoteNumbers(sets):
    numbers = []
    for i in range(len(sets)):
        if(sets[i] == 0):
            numbers.append(i+1)
    return numbers

def print_notes():
    for r in range(9):
        for c in range(9):
            numbers = getNoteNumbers(sudoku_note[r][c])
            print("X:", c, ", Y:", r, ":", numbers)

def getDistinctNumberNotes(notes):
    found = []
    for i in range(len(notes)):
        for k in range(len(notes[i])):
            if(not notes[i][k] in found):
                found.append(notes[i][k])
    return found

#Note2 is subset of note1
def isSubset(note1, note2):
    for i in range(len(note2)):
        if(not note2[i] in note1):
            return False
    return True

def obvious():
    #Loop through grid and get all notes
    for r in range(9):
        for c in range(9):
            #obvious singles
            if(countElement(sudoku_note[r][c], 0) == 1):
                modified_sudoku[r][c] = sudoku_note[r][c].index(0) + 1
                action_log.append([
                    "obvious_singles",
                    c,
                    r,
                    sudoku_note[r][c].index(0) + 1
                ])
                getNotes()  #Reset notes
                return True

    #Pairs
    '''
    obvious pairs: check empty & remove other have same numbers
    '''
    for r in range(9):
        for c in range(9):
            #First, find a note with only length is 2
            if(countElement(sudoku_note[r][c], 0) == 2):
                removed = False
                same_notes_grid = [
                    [c, r]
                ]
                pairs_number = getNoteNumbers(sudoku_note[r][c])
                removed_location = []
                
                #Then find another more pair is same notes, with same unit
                #If so, then remove other same number from same unit notes
                #Row
                for rr in range(9):
                    if(countElement(sudoku_note[rr][c], 0) == 2 
                       and sudoku_note[r][c] == sudoku_note[rr][c] 
                       and rr != r):
                        print("found row match")
                        print(c, rr, sudoku_note[rr][c])
                        print(c, r, sudoku_note[r][c])
                        same_notes_grid.append([c, rr])
                        
                        #Is them the same box?
                        if(getBoxNumFromXY(c, r) == getBoxNumFromXY(c, rr)):
                            box = getBoxXYFromXY(c, r)
                            for gr in range(box[1], box[1] + 3):
                                for gc in range(box[0], box[0] + 3):
                                    #Check it's not r and rr
                                    if(gc == c and (gr == r or gr == rr)):
                                        continue
                                    #Also not filled blank
                                    if(modified_sudoku[gr][gc] != 0):
                                        continue
                                        
                                    #Remove if they noted
                                    for i in range(len(pairs_number)):
                                        if(sudoku_note[gr][gc][pairs_number[i] - 1] == 0):
                                            removed = True
                                            removed_location.append([gc, gr])
                                        sudoku_note[gr][gc][pairs_number[i] - 1] = 1
                            if(removed):
                                action_log.append([
                                    "obvious_pairs_box",
                                    same_notes_grid,
                                    pairs_number,
                                    removed_location
                                ])
                                return True

                        #Clear Row
                        for rrr in range(9):
                            if(rrr == rr or rrr == r):
                                continue
                            if(modified_sudoku[rrr][c] != 0):
                                continue

                            for i in range(len(pairs_number)):
                                if(sudoku_note[rrr][c][pairs_number[i] - 1] == 0):
                                    removed = True
                                    removed_location.append([c, rrr])
                                sudoku_note[rrr][c][pairs_number[i] - 1] = 1
                        if(removed):
                            action_log.append([
                                "obvious_pairs_row",
                                same_notes_grid,
                                pairs_number,
                                removed_location
                            ])
                            return True

                #Col
                for cc in range(9):
                    if(countElement(sudoku_note[r][cc], 0) == 2
                       and sudoku_note[r][c] == sudoku_note[r][cc]
                       and cc != c):
                        print("found col match")
                        print(c, r, sudoku_note[r][c])
                        print(cc, r, sudoku_note[r][cc])
                        same_notes_grid.append([cc, r])

                        #Is them the same box?
                        if(getBoxNumFromXY(c, r) == getBoxNumFromXY(cc, r)):
                            box = getBoxXYFromXY(c, r)
                            for gr in range(box[1], box[1] + 3):
                                for gc in range(box[0], box[0] + 3):
                                    #Check it's not r and rr
                                    if(gr == r and (gc == c or gc == cc)):
                                        continue
                                    #Also not filled blank
                                    if(modified_sudoku[gr][gc] != 0):
                                        continue
                                        
                                    #Remove if they noted
                                    for i in range(len(pairs_number)):
                                        if(sudoku_note[gr][gc][pairs_number[i] - 1] == 0):
                                            removed = True
                                            removed_location.append([gc, gr])
                                        sudoku_note[gr][gc][pairs_number[i] - 1] = 1
                            if(removed):
                                action_log.append([
                                    "obvious_pairs_box",
                                    same_notes_grid,
                                    pairs_number,
                                    removed_location
                                ])
                                return True

                        #Clear Col
                        for ccc in range(9):
                            if(ccc == cc or ccc == c):
                                continue
                            if(modified_sudoku[r][ccc] != 0):
                                continue

                            for i in range(len(pairs_number)):
                                if(sudoku_note[r][ccc][pairs_number[i] - 1] == 0):
                                    removed = True
                                    removed_location.append([ccc, r])
                                sudoku_note[r][ccc][pairs_number[i] - 1] = 1
                        if(removed):
                            action_log.append([
                                "obvious_pairs_col",
                                same_notes_grid,
                                pairs_number,
                                removed_location
                            ])
                            return True

                #Box
                for b in range(9):
                    box = getBoxXYFromBoxNum(b)
    
    #Triples
    '''
    condition: have two same combination in same row/col/grid
        obvious triples:
        condition:
        (123) (123) (123) - {3/3/3} (in terms of candidates per cell)
        (123) (123) (12) - {3/3/2} (or some combination thereof)å
        (123) (12) (23) - {3/2/2}
        (12) (23) (13) - {2/2/2}
    '''
    for b in range(9):
        removed_location = []
        box = getBoxXYFromBoxNum(b)
        box_notes = []
        for gr in range(box[1], box[1] + 3):
            for gc in range(box[0], box[0] + 3):
                box_notes.append(getNoteNumbers(sudoku_note[gr][gc]))
        box_notes_combination = [list(p) for p in itertools.combinations(box_notes, 3)]
        for i in range(len(box_notes_combination)):
            #Check all notes have at least length 2
            check = False
            for k in range(3):
                if(len(box_notes_combination[i][k]) < 2 or len(box_notes_combination[i][k]) > 3):
                    check = True
            if(check):
                continue

            distinct_notes = getDistinctNumberNotes(box_notes_combination[i])
            if(len(distinct_notes) == 3):
                print("Found Triples", box_notes_combination[i], distinct_notes)

                #Remove same number from box
                for gr in range(box[1], box[1] + 3):
                    for gc in range(box[0], box[0] + 3):
                        #Loop distinct notes
                        if(modified_sudoku[gr][gc] != 0):
                            continue

                        if(not isSubset(distinct_notes, sudoku_note[gr][gc])):
                            #Remove number!
                            removed = False

                            for n in range(3):
                                if(sudoku_note[gr][gc][distinct_notes[n] - 1] == 0):
                                    removed = True
                                    removed_location.append([gc, gr])
                                sudoku_note[gr][gc][distinct_notes[n] - 1] = 1
                            
                            if(removed):
                                action_log.append([
                                    "obvious_triples_box",
                                    same_notes_grid,
                                    [
                                        b
                                        ,box_notes_combination[i]
                                    ],
                                    removed_location
                                ])
                                return True

    return False

'''-----CSP Solver-----'''
def csp_solve(hints):
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

'''------Validator-----'''
def isSudokuValid(sudoku):
    #Check unit by unit
    valid = [x for x in range(1, 10)]
    
    #Row
    for r in range(9):
        tmp = sorted(sudoku[r])
        if(tmp != valid):
            return False
    
    #Col
    for c in range(9):
        tmp = []
        for r in range(9):
            tmp.append(sudoku[r][c])
        tmp = sorted(tmp)

        if(tmp != valid):
            return False
    
    #Box
    for b in range(9):
        box = getBoxXYFromBoxNum(b)
        tmp = []
        for gr in range(box[1], box[1] + 3):
            for gc in range(box[0], box[0] + 3):
                tmp.append(sudoku[gr][gc])
        tmp = sorted(tmp)

        if(tmp != valid):
            return False

    return True

'''------Main Program-----'''
#Skill, x, y, number
action_log = []
'''
original_sudoku = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
'''
original_sudoku = [
    [0, 0, 0, 8, 2, 0, 6, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 8, 0, 7, 0, 0, 0, 0, 2],
    [0, 0, 6, 4, 0, 0, 0, 0, 0],
    [8, 4, 0, 0, 0, 3, 9, 0, 0],
    [0, 0, 5, 0, 0, 0, 0, 0, 8],
    [0, 0, 4, 0, 0, 0, 0, 0, 0],
    [2, 7, 0, 3, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 9, 0, 1, 0]
]
modified_sudoku = original_sudoku.copy()
sudoku_note = []
    
print("[csp time]")
hints = []
for i in range(9):
    for k in range(9):
        hints.append(original_sudoku[i][k])
csp_answers = csp_solve(hints)
print(pretty(csp_answers[0]))
print(len(csp_answers))

def debug():
    print_sudoku(modified_sudoku)
    pprint(action_log)
    print_notes()
    print()

getNotes()
while(True):
    if(last_remaining_cell()):
        continue
    
    '''
    print("Before")
    pprint(action_log)
    print_notes()
    print()
    '''
    if(obvious()):
        continue

    break

print('End')
if(isSudokuValid(modified_sudoku)):
    print_sudoku(modified_sudoku)
    print("NICEEEEEEEEE!!!!!!!!!!")
else:
    print("FUCKKKKKKKKKK")
    debug()