def get_grid_number(r, c):
    return int(r/3) * 3 + int(c/3)

def create_empty_map():
    map = []
    for r in range(9):
        map.append([0] * 9)

    return map

def print_map(map):
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

            print(map[r][c], "", end="")
            col += 1

        print("|")
        row += 1
    print("-"*25)

def scanning(map, action_log):
    #Make a map check
    for n in range(1, 10):
        check_map = create_empty_map()
        #print("[Scanning] Now checking", n)

        for r in range(9):
            for c in range(9):
                #Have other number
                if(not map[r][c] == 0):
                    check_map[r][c] = 1

                #Same Number
                if(map[r][c] == n):
                    #Found same, put it into check map
                    #Fill row & col
                    for f in range(9):
                        check_map[r][f] = 1
                        check_map[f][c] = 1

                    #Fill grid
                    gr = int(get_grid_number(r, c) / 3) * 3
                    gc = int(get_grid_number(r, c) % 3) * 3
                    for cr in range(3):
                        for cc in range(3):
                            check_map[gr+cr][gc+cc] = 1
        
        #Check is there only 1 empty in grid
        '''
        Sample
        1 1 1
        1 1 1
        1 0 1
        '''
        '''
        0-2, 3-5, 6-8
        '''
        #g for grid top-left position
        #suppose to be 0, 3, 6
        for gr in range(0, 7, 3):
            for gc in range(0, 7, 3):
                last_empty_pos = { "x":-1, "y":-1 }
                empty_count = 0
                for cr in range(3):
                    for cc in range(3):
                        if(check_map[gr+cr][gc+cc] == 1):
                            empty_count += 1
                        else:
                            last_empty_pos['x'] = gc+cc
                            last_empty_pos['y'] = gr+cr
                if(empty_count == 8):
                    '''
                    print("[Scanning] Found one,",
                          "num:", n,
                          ", grid:", get_grid_number(gr, gc), 
                          ", r:", last_empty_pos['y'],
                          ", c:", last_empty_pos['x'])
                    '''
                    action_log.append({
                        "action": "scanning",
                        "number": n,
                        "grid": get_grid_number(gr, gc),
                        "row": last_empty_pos['y'],
                        "col": last_empty_pos['x']
                    })

                    #Fill
                    #print('[Scanning] Before:')
                    #print_map(map)
                    #print('[Scanning] After:')
                    map[last_empty_pos['y']][last_empty_pos['x']] = n
                    #print_map(map)
                    return True

    return False

def single_candidate(map, action_log):
    #Search square by square
    for r in range(9):
        for c in range(9):
            #Already have number
            if(not map[r][c] == 0):
                continue

            #Check number
            check_number = 0
            check_number_list = [False] * 9

            #Search col & row
            for p in range(9):
                if(not map[r][p] == 0):
                    if(not check_number_list[map[r][p] - 1]):
                        check_number += 1
                        check_number_list[map[r][p] - 1] = True

                if(not map[p][c] == 0):
                    if(not check_number_list[map[p][c] - 1]):
                        check_number += 1
                        check_number_list[map[p][c] - 1] = True

            #Search grid
            gr = int(get_grid_number(r, c) / 3) * 3
            gc = int(get_grid_number(r, c) % 3) * 3
            for cr in range(3):
                for cc in range(3):
                    #print(gr + cr, gc + cc)
                    if(not map[gr + cr][gc + cc] == 0):
                        if(not check_number_list[map[gr + cr][gc + cc] - 1]):
                            check_number += 1
                            check_number_list[map[gr + cr][gc + cc] - 1] = True

            #Check last
            if(check_number == 8):
                last_num = 1
                for p in check_number_list:
                    if(not p):
                       break
                    
                    last_num += 1

                map[r][c] = last_num

                '''
                print("[Single Candidate] Found",
                      ", number:", last_num,
                      ", grid:", get_grid_number(r, c),
                      ", r:", r,
                      ", c:", c)
                '''
                
                action_log.append({
                    "action": "single_candidate",
                    "number": last_num,
                    "row": r,
                    "col": c
                })
                return True

    return False

def eliminating_number(map, action_log):
    #Make a check map pin all number
    ori_check_map = create_empty_map()
    for r in range(9):
        for c in range(9):
            if(not map[r][c] == 0):
                ori_check_map[r][c] = 1
    
    print_map(ori_check_map)

    return False

#sudoku data[y][x]
#0 for empty
map = [
    [0, 0, 0, 1, 0, 4, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 9, 0, 0],
    [0, 9, 0, 7, 0, 3, 0, 6, 0],
    [8, 0, 7, 0, 0, 0, 1, 0, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 4, 0, 0, 0, 5, 0, 9],
    [0, 5, 0, 4, 0, 2, 0, 3, 0],
    [0, 0, 8, 0, 0, 0, 6, 0, 0],
    [0, 0, 0, 8, 0, 6, 0, 0, 0]
]
#action, number, row, col
action_log = []

print("Original:")
print_map(map)

#Start checking
eliminating_number(map, action_log)
'''
while True:
    if(scanning(map, action_log)): continue
    if(single_candidate(map, action_log)): continue

    break
'''

print('End, no skill can be applied')
for action in action_log:
    print(action['action'], ", number:", action['number'], ', row:', action['row'], ', col:', action['col'])

print('End')
print_map(map)