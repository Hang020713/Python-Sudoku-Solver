import time
import itertools
from pprint import pprint

'''
unit: box, row, col, grid
Index: start from 0
Box: 0 1 2
     3 4 5
     6 7 8
sudoku[y][x]

last remaining cell: check number

last free cell: check empty
last possible number: check empty
obvious singles: check empty
obvious pairs: check empty & remove other have same numbers
    condition: have two same combination in same row/col/grid
obvious triples:
    condition:
    (123) (123) (123) - {3/3/3} (in terms of candidates per cell)
    (123) (123) (12) - {3/3/2} (or some combination thereof)
    (123) (12) (23) - {3/2/2}
    (12) (23) (13) - {2/2/2}
hidden quads: ---
hidden singles: check empty, check for one and only one
pointing paris: check empty, remove same numbers on grid
'''

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
            #Pairs
            if(countElement(sudoku_note[r][c], 0) == 2):
                same_notes = 0
                same_notes_grid = [
                    [c, r]
                ]
                pairs_number = getNoteNumbers(sudoku_note[r][c])

                #Check have other grid, row, col notes have same numbers
                #Box
                box = getBoxXYFromXY(c, r)
                for gr in range(box[1], box[1] + 3):
                    for gc in range(box[0], box[0] + 3):
                        if(sudoku_note[r][c] == sudoku_note[gr][gc] and gr != r and gc != c):
                            same_notes += 1
                            same_notes_grid.append([gc, gr])

                #Row
                for gr in range(9):
                    if(sudoku_note[r][c] == sudoku_note[gr][c] and gr != r):
                        same_notes += 1
                        same_notes_grid.append([c, gr])
                
                #Col
                for gc in range(9):
                    if(sudoku_note[r][c] == sudoku_note[r][gc] and gc != c):
                        same_notes += 1
                        same_notes_grid.append([gc, r])

                #If yes, then remove same unit other notes
                if(same_notes != 0):
                    #Remove
                    removed = False
                    #Box
                    for gr in range(box[1], box[1] + 3):
                        for gc in range(box[0], box[0] + 3):
                            if(countElement(sudoku_note[gr][gc], 0) > 2):
                                for i in range(2):
                                    if(sudoku_note[gr][gc][pairs_number[i] - 1] == 0):
                                        removed = True
                                    sudoku_note[gr][gc][pairs_number[i] - 1] = 1

                    #Row
                    for gr in range(9):
                        if(countElement(sudoku_note[gr][c], 0) > 2):
                            for i in range(2):
                                if(sudoku_note[gr][c][pairs_number[i] - 1] == 0):
                                        removed = True
                                sudoku_note[gr][c][pairs_number[i] - 1] = 1

                    #Col
                    for gc in range(9):
                        if(countElement(sudoku_note[r][gc], 0) > 2):
                            for i in range(2):
                                if(sudoku_note[r][gc][pairs_number[i] - 1] == 0):
                                        removed = True
                                sudoku_note[r][gc][pairs_number[i] - 1] = 1

                    if(removed):
                        #Add records
                        action_log.append([
                            "obvious_pairs",
                            same_notes_grid,
                            pairs_number
                        ])

                        return True
                
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
    #Loop over unit
    #Get all box notes
    #Loop all combination
    #Get distinct set, check if length = 3
    #Box
    for b in range(9):
        box = getBoxXYFromBoxNum(b)
        box_notes = []
        for gr in range(box[1], box[1] + 3):
            for gc in range(box[0], box[0] + 3):
                box_notes.append(sudoku_note[gr][gc])
        box_notes_combination = [list(p) for p in itertools.combinations(box_notes, 3)]
        for i in range(len(box_notes_combination)):
            distinct_notes = getDistinctNumberNotes(box_notes_combination[i])
            if(len(distinct_notes) == 3):
                print(box_notes_combination[i])
                return True

    return False

#Main Program
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
    [0, 0, 2, 0, 8, 5, 0, 0, 4],
    [0, 0, 0, 0, 3, 0, 0, 6, 0],
    [0, 0, 4, 2, 1, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 5, 2],
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [9, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 6, 0, 0, 0],
    [2, 5, 0, 4, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 6, 0, 0]
]
modified_sudoku = original_sudoku
sudoku_note = []

'''
getNotes()
obvious()
print_sudoku(modified_sudoku)
print(action_log) 
'''

def debug():
    print_sudoku(modified_sudoku)
    pprint(action_log)
    print_notes()
    print()

'''
getNotes()
obvious()
debug()
'''

getNotes()
print_notes()
print()
while(True):
    if(last_remaining_cell()): 
        pprint(action_log)
        #time.sleep(6)
        continue

    if(obvious()):
        pprint(action_log)
        #time.sleep(6)
        continue

    break
print('End')
debug()