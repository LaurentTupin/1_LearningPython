import time

def minOut(L):   
    LL = list(range(1, len(L) + 2))    
    s_set = set(LL).difference(set(L))
    return min(s_set)

#tm_start = time.time()
## ============================================
#l = range(1,10000000)
#print(minOut(l))
#tm_end = time.time()
#print('-----------------------------------------------------------')
#print('Time of the request: ', int(tm_end - tm_start), 'secondes')



def solution1(N, S):
    int_return = 0
    l_bcde = ['b','c','d','e']
    l_fghj = ['f','g','h','j']
    l_defg = ['d','e', 'f','g']
    
    L_seat = S.split(' ')
    
    for i_row in range(1, N + 1):
        try:
            L_seatInRow = [x[1].lower() for x in L_seat if x[0] == str(i_row)]
            s_bcde = set(l_bcde).intersection(set(L_seatInRow))
            s_fghj = set(l_fghj).intersection(set(L_seatInRow))
            s_defg = set(l_defg).intersection(set(L_seatInRow))
            
            if len(s_bcde) == 0:
                if len(s_fghj) == 0:
                    int_return += 2
                else:
                    int_return += 1
            elif len(s_fghj) == 0:
                int_return += 1
            elif len(s_defg) == 0:
                int_return += 1
            else: pass
        #????????????????????????
        except:
            int_return += 2
        
    return int_return
        

#N = 3
#S = ""
#print(solution(N, S))



def solution2(A):
    # write your code in Python 3.6
    l_Delta = [x - y for (x, y) in zip(A[1:], A[:-1])]
    l_SameDirection = [x * y for (x, y) in zip(l_Delta[1:], l_Delta[:-1])]
    nbPositif = len([x for x in l_SameDirection if x >=0])
    l_SameDirection_Twice  = [x for (x, y) in zip(l_SameDirection[1::2], l_SameDirection[:-1:2]) if x>=0 and y>=0]
    nbPositif_Twice = len(l_SameDirection_Twice)
#    print(A)
#    print(l)
#    print(ll)
#    print(lll)
    return nbPositif - nbPositif_Twice
    

#A = [5, 4, 3, 2, 6]
##A = [1, 2, 3, 4, 5, 6, 7,8]
#print(solution2(A))








def f_getNextCell(d_board, Pos, l_exclude):
    l_position = []
    l_NextPos = [(Pos[0] - 1, Pos[1]), (Pos[0] + 1, Pos[1]), (Pos[0], Pos[1] - 1), (Pos[0], Pos[1] + 1)]
    
    for PosExcluse in l_exclude:
        if PosExcluse in l_NextPos: 
            l_NextPos.remove(PosExcluse)
    
    for cell in l_NextPos:
        if cell in d_board.keys():
            l_position.append(cell)
    
    return l_position
    

def solution3(Board):    
    i_MaxRow = len(Board) 
    i_MaxCol = len(Board[0])     
    l_position = [(a,b) for a in range (0, i_MaxRow) for b in range (0, i_MaxCol)]
    d_board = dict()
    l_value = []
    i_valueMax = 0
    
    # Fill Dictionary
    for Pos in l_position:
        d_board[Pos] = Board[Pos[0]][Pos[1]]
        
    # Find Path
    for Pos in l_position:
        i_value = d_board[Pos]
        if i_value < i_valueMax:
            continue
        else: i_valueMax = i_value
        l_position2 = f_getNextCell(d_board, Pos, [])
        l_exclude = []
        l_exclude.append(Pos)
        
        for Pos2 in l_position2:
            i_value2 = d_board[Pos2]
            l_position3 = f_getNextCell(d_board, Pos2, l_exclude)
            l_exclude2 = []
            l_exclude2.append(Pos2)
            
            for Pos3 in l_position3:  
                i_value3 = d_board[Pos3]
                l_position4 = f_getNextCell(d_board, Pos3, l_exclude2)
                
                for Pos4 in l_position4:
                    i_value4 = d_board[Pos4]
                    str_Value = str(i_value) + str(i_value2)+ str(i_value3)+str(i_value4)
                    l_value.append(str_Value)
    return max(l_value)
        
        
        
        
    

board =  [[1, 4, 7], [9, 5, 8], [4, 8, 2], [1, 2, 3]]
print(solution3(board))











