# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 12:47:43 2017

@author: Ben
"""

import copy
import random
import time

board = []
board_data = [0,0,0]
color_all = []
color_set = set()
color_list = []
color_path = []
const_board = [] #Contains sets of possible values for a given location
const_board_num = []

big_count = [0]
queue = []

def getFile(name):  
    r=0
    c=0
    board[:] = []
    color_path[:] = []
    temp_color = 0
    board.append([])
    board_data[0]=0 #??
    board_data[1]=0 #??
    board_data[2]=0
       
    file = open(name, 'r')
    
    while 1:
        char = file.read(1)
        if not char:
            break  
        if char != '\n':
            board[r].append(char)
            if char != '_':
#                source_sink_set.add([r,c])
                if char not in color_set:
                    color_set.add(char)
                    color_all.append(char)
                    temp_color +=1
                    color_list.append(char)
                    color_path.append([])
                    color_path[len(color_path)-1].append([r,c])
                else:
                    color_path[color_list.index(char)].append([r,c])
            c += 1
        else: 
            width = c
            c = 0
            r += 1
            board.append([])
    height = r+1
    file.close()
    board_data[0] = height
    board_data[1] = width
    board_data[2] = temp_color

    
    return


def printBoard():
    for r in range(board_data[0]):
        for c in range(board_data[1]):
            print(board[r][c], end='')
        print('') #Just for newline after each row
    return



#def checkRegion(board_temp):
#    for i in range(board_data[0]):
#        for j in range(board_data[1]):
#            if board_temp[i][j] == '_':
#                exploreRegion()
#    
#    
#    return


#def exploreRegion():
#    front =[]
#    front.append([row,col])
#    while(len(front) != 0):
#        #Up
#        if row - 1 >= 0:
#            if board_temp[row - 1][col] == '_':
#                front.append([row -1, col])
#                board_temp[row][col] = -1
##        else:
#            
#        #Left
#        if col - 1 >= 0 and board_temp[row][col - 1] == '_':
#            total += checkConstraining(board_temp, row, col-1)
#        #Right
#        if col + 1 < board_data[1] and board_temp[row][col + 1] == '_':
#            total += checkConstraining(board_temp, row, col+1)
#        #Down
#        if row + 1 < board_data[0] and board_temp[row + 1][col] == '_':
#            total += checkConstraining(board_temp, row+1, col)
#    return


def mostConstrainedVariable(board_temp):
    for i in range(board_data[0]):
        for j in range(board_data[1]):
            if board_temp[i][j] == '_':
                for c in range(len(color_list)):
                    val = color_list[c]
                    if consistencyCheck(board_temp, [i,j], val) == True:
                        const_board[i][j].append(val)
                        const_board_num[i][j] += 1

    return



def updateConstBoard(row,col, const_temp, const_num_temp):
#    for c in range(len(const_temp[row][col])):
#        val = const_temp[row][col][c]
#        if consistencyCheck(board, [row,col], val) == False:
    const_temp[row][col][:]=[]
    const_num_temp[row][col] = 0
#    print(const_num_temp)
    if row - 1 >= 0 and col + 1 < board_data[1] and board[row - 1][col + 1] == '_':
        temp = list(const_temp[row - 1][col + 1])
        for c in range(len(temp)):
            val = temp[c]
            if consistencyCheck(board, [row - 1,col + 1], val) == False:
                const_temp[row - 1][col + 1].remove(val)
                const_num_temp[row - 1][col + 1] -= 1
    if row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col - 1] == '_':
        temp = list(const_temp[row - 1][col - 1])
        for c in range(len(temp)):
            val = temp[c]
            if consistencyCheck(board, [row - 1,col - 1], val) == False:
                const_temp[row - 1][col - 1].remove(val)
                const_num_temp[row - 1][col - 1] -= 1        
    if row + 1 < board_data[0] and col + 1 < board_data[1] and board[row + 1][col + 1] == '_':
        temp = list(const_temp[row + 1][col + 1])
        for c in range(len(temp)):
            val = temp[c]
            if consistencyCheck(board, [row + 1,col + 1], val) == False:
                const_temp[row + 1][col + 1].remove(val)
                const_num_temp[row + 1][col + 1] -= 1        
    if row + 1 < board_data[0] and col - 1 >= 0 and board[row + 1][col - 1] == '_':
        temp = list(const_temp[row + 1][col - 1])
        for c in range(len(temp)):
            val = temp[c]
            if consistencyCheck(board, [row + 1,col - 1], val) == False:
                const_temp[row + 1][col - 1].remove(val)
                const_num_temp[row + 1][col - 1] -= 1   
    if row - 1 >= 0  and board[row - 1][col] == '_':
        temp = list(const_temp[row - 1][col])
        for c in range(len(temp)):       
            val = temp[c]
            if consistencyCheck(board, [row - 1,col], val) == False:
                const_temp[row - 1][col].remove(val)
                const_num_temp[row - 1][col] -= 1
    if col - 1 >= 0 and board[row][col - 1] == '_':
        temp = list(const_temp[row][col - 1])
        for c in range(len(temp)):
            val = temp[c]
            if consistencyCheck(board, [row,col - 1], val) == False:
                const_temp[row][col - 1].remove(val)
                const_num_temp[row][col - 1] -= 1        
    if row + 1 < board_data[0] and board[row + 1][col] == '_':
        temp = list(const_temp[row + 1][col])
        for c in range(len(temp)):
            val = temp[c]
            if consistencyCheck(board, [row + 1,col], val) == False:
                const_temp[row + 1][col].remove(val)
                const_num_temp[row + 1][col] -= 1        
    if col + 1 < board_data[1] and board[row][col + 1] == '_':
        temp = list(const_temp[row][col + 1])
        for c in range(len(temp)):
            val = temp[c]
            if consistencyCheck(board, [row,col + 1], val) == False:
                const_temp[row][col + 1].remove(val)
                const_num_temp[row][col + 1] -= 1  
    return
        
        
        
def checkConstraining(board_temp, row, col):
    total = 0
    for i in range(len(const_board[row][col])):
        val = const_board[row][col][i]
        if consistencyCheck(board_temp, [row,col], val) == True:
            total +=1
    
    
    return total


def checkConstraining2(board_temp, row, col):
    total = 0
    for i in range(len(const_board[row][col])):
        val = const_board[row][col][i]
        if consistencyCheck(board_temp, [row,col], val) == True:
            total +=1
    return total


    
def mostConstrainingVariable(board_temp,var_list):
    best_total = 1000
    best_i = -1
    total = 0
    for i in range(len(var_list)):
        
        row = var_list[i][0]
        col = var_list[i][1]
        if row - 1 >= 0 and col + 1 < board_data[1] and board_temp[row - 1][col + 1] == '_':
            total += checkConstraining(board_temp, row-1, col+1)
        #Upper Left
        if row - 1 >= 0 and col - 1 >= 0 and board_temp[row - 1][col - 1] == '_':
            total += checkConstraining(board_temp, row-1, col-1)
        #Lower Right
        if row + 1 < board_data[0] and col + 1 < board_data[1] and board_temp[row + 1][col + 1] == '_':
            total += checkConstraining(board_temp, row+1, col+1)
        #Lower Left
        if row + 1 < board_data[0] and col - 1 >= 0 and board_temp[row + 1][col - 1] == '_':
            total += checkConstraining(board_temp, row+1, col-1)
        #Up
        if row - 1 >= 0 and board_temp[row - 1][col] == '_':
            total += checkConstraining(board_temp, row-1, col)
        #Left
        if col - 1 >= 0 and board_temp[row][col - 1] == '_':
            total += checkConstraining(board_temp, row, col-1)
        #Right
        if col + 1 < board_data[1] and board_temp[row][col + 1] == '_':
            total += checkConstraining(board_temp, row, col+1)
        #Down
        if row + 1 < board_data[0] and board_temp[row + 1][col] == '_':
            total += checkConstraining(board_temp, row+1, col)
        if total < best_total:
            best_total = total
            best_i = i
        
        return var_list[best_i]



def leastConstrainingValue(const, row,col):
    best_total = 0
    best_i = -1
    total = 0
    for i in range(len(const[row][col])):
        val = const[row][col][i]
#        print(val)
        board_temp = copy.deepcopy(board)
        board_temp[row][col] = val
        if row - 1 >= 0 and col + 1 < board_data[1] and board[row - 1][col + 1] == '_':
            total += checkConstraining2(board_temp, row-1, col+1)
        #Upper Left
        if row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col - 1] == '_':
            total += checkConstraining2(board_temp, row-1, col-1)
        #Lower Right
        if row + 1 < board_data[0] and col + 1 < board_data[1] and board[row + 1][col + 1] == '_':
            total += checkConstraining2(board_temp, row+1, col+1)
        #Lower Left
        if row + 1 < board_data[0] and col - 1 >= 0 and board[row + 1][col - 1] == '_':
            total += checkConstraining2(board_temp, row+1, col-1)
        #Up
        if row - 1 >= 0 and board[row - 1][col] == '_':
            total += checkConstraining2(board_temp, row-1, col)
        #Left
        if col - 1 >= 0 and board[row][col - 1] == '_':
            total += checkConstraining2(board_temp, row, col-1)
        #Right
        if col + 1 < board_data[1] and board[row][col + 1] == '_':
            total += checkConstraining2(board_temp, row, col+1)
        #Down
        if row + 1 < board_data[0] and board[row + 1][col] == '_':
            total += checkConstraining2(board_temp, row+1, col)
#        print(total)
        if total > best_total:
            best_total = total
            best_i = i
    
    return const[row][col][best_i]



def isContiguous(board_temp, color_num): #board_temp is a copy of the board as it will be modified
    row_source = color_path[color_num][0][0]
    col_source = color_path[color_num][0][1]
    row_sink = color_path[color_num][1][0]
    col_sink = color_path[color_num][1][1]

    row = row_source
    col = col_source
    board_temp[row][col] = "."
    flag = True
    while(flag):
        if col + 1 < board_data[1] and board_temp[row][col + 1] == color_list[color_num]:
            board_temp[row][col + 1] = "."
            row_temp = row
            col_temp = col + 1
        elif col - 1 >= 0 and board_temp[row][col - 1] == color_list[color_num]:
            board_temp[row][col - 1] = "."
            row_temp = row
            col_temp = col - 1
        elif row + 1 < board_data[0] and board_temp[row + 1][col] == color_list[color_num]:
            board_temp[row + 1][col] = "."
            row_temp = row + 1
            col_temp = col
        elif row - 1 >= 0 and board_temp[row - 1][col] == color_list[color_num]:
            board_temp[row - 1][col] = "."
            row_temp = row - 1
            col_temp = col
        else:
            return False
        row = row_temp
        col = col_temp
        if row == row_sink and col == col_sink:
            flag = False

    return True

def isComplete():
    #Check that all spaces are used
    for r in range(board_data[0]):
        for c in range(board_data[1]):
            if board[r][c] == '_':
                return False
    #Check that each color is continuous
    temp_board = copy.deepcopy(board)
    for i in range(board_data[2]):
        if isContiguous(temp_board, i) == False:
            return False
    return True      




def checkSources(board_temp):
    for i in range(len(color_list)):
        val = color_list[i]
        short = color_path[i]
        row_source = short[0][0]
        col_source = short[0][1]
        row_sink = short[1][0]
        col_sink = short[1][1]
        source_count = 0
        if col_source + 1 < board_data[1] and board_temp[row_source][col_source + 1] == val:
            source_count += 1
        if col_source - 1 >= 0 and board_temp[row_source][col_source - 1] == val:
            source_count += 1
        if row_source + 1 < board_data[0] and board_temp[row_source + 1][col_source] == val:
            source_count += 1
        if row_source - 1 >= 0 and board_temp[row_source - 1][col_source] == val:
            source_count += 1
        if source_count > 1:
            return False 
        sink_count = 0
        if col_sink + 1 < board_data[1] and board_temp[row_sink][col_sink + 1] == val:
            sink_count += 1
        if col_sink - 1 >= 0 and board_temp[row_sink][col_sink - 1] == val:
            sink_count += 1
        if row_sink + 1 < board_data[0] and board_temp[row_sink + 1][col_sink] == val:
            sink_count += 1
        if row_sink - 1 >= 0 and board_temp[row_sink - 1][col_sink] == val:
            sink_count += 1
        if sink_count > 1:
            return False 
    return True

def checkZigZag(board_temp, var, val):
    #Check for 4 corners
    #Upper Right
    row = var[0]
    col = var[1]
    if row - 1 >= 0 and col + 1 < board_data[1]:
        if board_temp[row - 1][col] == val and board_temp[row][col + 1] == val and board_temp[row - 1][col + 1] == val:
            return False
    #Upper Left
    if row - 1 >= 0 and col - 1 >= 0:
        if board_temp[row - 1][col] == val and board_temp[row][col - 1] == val and board_temp[row - 1][col - 1] == val:
            return False
    #Lower Right
    if row + 1 < board_data[0] and col + 1 < board_data[1]:
        if board_temp[row + 1][col] == val and board_temp[row][col + 1] == val and board_temp[row + 1][col + 1] == val:
            return False
    #Lower Left
    if row + 1 < board_data[0] and col - 1 >= 0:
        if board_temp[row + 1][col] == val and board_temp[row][col - 1] == val and board_temp[row + 1][col - 1] == val:
            return False
    return True


def checkSpur(board_temp, var, val):
    #Check for spurs
    row = var[0]
    col = var[1]
    #Upper
    if row - 1 >= 0 and col - 1 >= 0 and col + 1 < board_data[1]:
        if board_temp[row - 1][col - 1] == val and board_temp[row - 1][col] == val and board_temp[row - 1][col + 1] == val:
            return False
    #Lower
    if row + 1 < board_data[0] and col - 1 >= 0 and col + 1 < board_data[1]:
        if board_temp[row + 1][col - 1] == val and board_temp[row + 1][col] == val and board_temp[row + 1][col + 1] == val:
            return False
    #Right
    if row - 1 >= 0 and row + 1 < board_data[0] and col + 1 < board_data[1]:
        if board_temp[row + 1][col + 1] == val and board_temp[row][col + 1] == val and board_temp[row - 1][col + 1] == val:
            return False
    #Left
    if row - 1 >= 0 and row + 1 < board_data[0] and col - 1 >= 0:
        if board_temp[row + 1][col - 1] == val and board_temp[row][col - 1] == val and board_temp[row - 1][col - 1] == val:
            return False
    return True
    
    



def checkAdj(board_temp, var, val):
    same_count = 0
    row = var[0]
    col = var[1]
#    print([row,col])
    if col + 1 < board_data[1] and board_temp[row][col + 1] == val:
        same_count += 1
    if col - 1 >= 0 and board_temp[row][col - 1] == val:
        same_count += 1
    if row + 1 < board_data[0] and board_temp[row + 1][col] == val:
        same_count += 1
    if row - 1 >= 0 and board_temp[row - 1][col] == val:
        same_count += 1
    if same_count > 2:
        return False

    free_count = 0
    if col + 1 < board_data[1] and board_temp[row][col + 1] == '_':
        free_count += 1
    if col - 1 >= 0 and board_temp[row][col - 1] == '_':
        free_count += 1
    if row + 1 < board_data[0] and board_temp[row + 1][col] == '_':
        free_count += 1
    if row - 1 >= 0 and board_temp[row - 1][col] == '_':
        free_count += 1
#    print(same_count)
#    print(free_count)
    
    inx = color_list.index(val)
    if var != color_path[inx][0] and var != color_path[inx][1]:
        if same_count == 0 and free_count < 2:
            return False
#    inx = color_list.index(val)
    if var != color_path[inx][0] and var != color_path[inx][1]:
        if same_count == 1 and free_count < 1:
            return False
    if var != color_path[inx][0] and var != color_path[inx][1]:
        if free_count == 0 and same_count !=2:
            return False
    return True

    

def isConsistent(board_temp, var, val):
    if consistencyCheck(board_temp, var, val) == False:
        return False
    temp = copy.deepcopy(board_temp)
    temp[var[0]][var[1]] = val
    if areaCheck(temp, var[0], var[1]) == False:
#        print("A")
        return False
    return True

   

def consistencyCheck(board_temp, var, val):
    
    if checkAdj(board_temp, var, val) == False:
#        print("Adj")
        return False    
    if checkZigZag(board_temp, var, val) == False:
#        print("zig")
        return False    
    if checkSpur(board_temp, var, val) == False:
#        print("spur")
        return False    
    if checkSources(board_temp) == False:
#        print("sources")
        return False
    else:
        return True


def selectVar(board_temp, const_num, dumb):
    if dumb == 1:
        
        total = 0
        for i in range(board_data[0]):
            total = total + board[i].count('_')
        if total == 0:
            return None
        rand_pick = random.randint(1, total)
    
        count = 0
        row = 0
        col =0
        for r in range(board_data[0]):
            for c in range(board_data[1]):
                if board[r][c] == '_':
                    count += 1
                    if count == rand_pick:
                        row = r
                        col = c
                        break
        return [row, col]
    
    elif dumb == 2 or dumb == 3:
        most = 1000
        old_most = 1000
        most_list = []
        for i in range(board_data[0]):
            for j in range(board_data[1]):
                if const_num[i][j] != 0 and const_num[i][j] <= most:
    #                print([i,j, most])
                    most = const_num[i][j]
                    if most != old_most:
                        old_most = most
                        most_list[:]=[]
                    most_list.append([i,j])
    #    print(most_list)
        var = mostConstrainingVariable(board_temp,most_list)
#    print(A)
        return var
    

def areaCheck(board, row, col):
#    print("Checking Area")
#    print([row,col])
    if row - 1 >= 0 and col + 1 < board_data[1] and board[row - 1][col + 1] != '_':
        val = board[row - 1][col + 1]
        if consistencyCheck(board, [row - 1,col + 1], val) == False:
#            print("B")
            return False
    if row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col - 1] != '_':
        val = board[row - 1][col - 1]
        if consistencyCheck(board, [row - 1,col - 1], val) == False:
#            print("C")
            return False      
    if row + 1 < board_data[0] and col + 1 < board_data[1] and board[row + 1][col + 1] != '_':
        val = board[row + 1][col + 1]
        if consistencyCheck(board, [row + 1,col + 1], val) == False:
#            print("D")
            return False 
    if row + 1 < board_data[0] and col - 1 >= 0 and board[row + 1][col - 1] != '_':
        val = board[row + 1][col - 1]
        if consistencyCheck(board, [row + 1,col - 1], val) == False:
#            print("E")
            return False      
    if row - 1 >= 0  and board[row - 1][col] != '_':
        val = board[row - 1][col]
        if consistencyCheck(board, [row - 1,col], val) == False:
#            print("F")
            return False    
    if col - 1 >= 0 and board[row][col - 1] != '_':
        val = board[row][col - 1]
        if consistencyCheck(board, [row, col - 1], val) == False:
#            print("G")
            return False          
    if row + 1 < board_data[0] and board[row + 1][col] != '_':
        val = board[row + 1][col]
        if consistencyCheck(board, [row + 1,col], val) == False:
#            print("H")
            return False            
    if col + 1 < board_data[1] and board[row][col + 1] != '_':
        val = board[row][col + 1]
        if consistencyCheck(board, [row, col + 1], val) == False:
#            print("I")
            return False    
        
    return True


def forwardChecking(const_num):
    for i in range(board_data[0]):
        for j in range(board_data[1]):
            if board[i][j] == '_' and const_num[i][j] == 0:
                return False  
    return True


def createQueue():
    for row in range(board_data[0]):
        for col in range(board_data[1]):
            if row - 1 >= 0 and col + 1 < board_data[1]:
                queue.append([[row - 1, col + 1], [row, col]])
            if row - 1 >= 0 and col - 1 >= 0 :
                queue.append([[row - 1, col - 1], [row, col]])     
            if row + 1 < board_data[0] and col + 1 < board_data[1]:
                queue.append([[row + 1, col + 1], [row, col]])
            if row + 1 < board_data[0] and col - 1 >= 0:
                queue.append([[row + 1, col - 1], [row, col]])      
            if row - 1 >= 0:
                queue.append([[row - 1, col], [row, col]])  
            if col - 1 >= 0:
                queue.append([[row, col - 1], [row, col]])         
            if row + 1 < board_data[0]:
                queue.append([[row + 1, col], [row, col]])            
            if col + 1 < board_data[1]:
                queue.append([[row, col + 1], [row, col]])
#    print(queue)
            
    return


def updateQueue(queue_temp,row, col):
  
    if row - 1 >= 0 and col + 1 < board_data[1]:
        if [[row, col], [row - 1, col + 1]] not in queue:
            queue_temp.append([[row, col], [row - 1, col + 1]])
    if row - 1 >= 0 and col - 1 >= 0 :
        if [[row, col], [row - 1, col - 1]] not in queue:
            queue_temp.append([[row, col], [row - 1, col - 1]])     
    if row + 1 < board_data[0] and col + 1 < board_data[1]:
        if [[row, col], [row + 1, col + 1]] not in queue:
            queue_temp.append([[row, col], [row + 1, col + 1]])
    if row + 1 < board_data[0] and col - 1 >= 0:
        if [[row, col], [row + 1, col - 1]] not in queue:
            queue_temp.append([[row, col], [row + 1, col - 1]])      
    if row - 1 >= 0:
        if [[row, col], [row - 1, col]] not in queue:
            queue_temp.append([[row, col], [row - 1, col]])  
    if col - 1 >= 0:
        if [[row, col], [row, col - 1]] not in queue:
            queue_temp.append([[row, col], [row, col - 1]])         
    if row + 1 < board_data[0]:
        if [[row, col], [row + 1, col]] not in queue:
            queue_temp.append([[row, col], [row + 1, col]])            
    if col + 1 < board_data[1]:
        if [[row, col], [row, col + 1]] not in queue:
            queue_temp.append([[row, col], [row, col + 1]]) 
    return


def arcCon(queue_temp, const, const_num, board_temp):
    while(len(queue_temp) != 0):
#        print(const_num)
        del_flag = False
        del_flag2 = False
        [curr_X, curr_Y] = queue_temp.pop(0)
        old_val = board_temp[curr_X[0]][curr_X[1]]
        if board_temp[curr_X[0]][curr_X[1]] == '_':
            val_list = list(const[curr_X[0]][curr_X[1]])
        else:
            val_list =[board_temp[curr_X[0]][curr_X[1]]]
        
        for i in range(len(val_list)):

            val = val_list[i]
            board_temp[curr_X[0]][curr_X[1]] = val
            if board_temp[curr_Y[0]][curr_Y[1]] == '_':
                size = const_num[curr_Y[0]][curr_Y[1]]
                for j in range(len(const[curr_Y[0]][curr_Y[1]])):
                    val2 = const[curr_Y[0]][curr_Y[1]][j]
#                    print(val2)
                    if consistencyCheck(board_temp, [curr_Y[0], curr_Y[1]], val2) == False:
                        size -= 1
                        if size == 0:
                            del_flag = True
            else:
                val2 = board_temp[curr_Y[0]][curr_Y[1]]
                if consistencyCheck(board_temp, [curr_Y[0], curr_Y[1]], val2) == False:
                    del_flag = True
            if del_flag == True:
#                print([curr_X[0], curr_X[1],curr_Y[0], curr_Y[1], val])
                const[curr_X[0]][curr_X[1]].remove(val)
                const_num[curr_X[0]][curr_X[1]] -= 1
                del_flag = False
                del_flag2 = True
                
        if del_flag2 == True:
            updateQueue(queue_temp, curr_X[0], curr_X[1])
            del_flag2 = False
        board_temp[curr_X[0]][curr_X[1]] = old_val
        
    return





def backTracking(board, const, const_num, dumb):
    big_count[0] += 1
#    printBoard()
#    print(const_num)
#    print("")
    #temp_board = copy.deepcopy(board)
    #Check for solution
    if isComplete():
        return board
    queue_temp = list(queue)
    board_temp = copy.deepcopy(board)
    if dumb == 3:
        arcCon(queue_temp, const, const_num, board_temp)
#    print("Check")
#    print(const_num)
    A = selectVar(board, const_num, dumb)
    if A == None:
#        print("Full Failure")
        return False
    
    [row, col] = [A[0],A[1]]
    curr_var = [row, col]
#    print("Placing: ",curr_var)
    
    while(len(const[row][col]) != 0):
        if dumb == 1:
            curr_value = random.choice(const[row][col])
        elif dumb == 2 or dumb == 3:
            curr_value = leastConstrainingValue(const,row,col)
#        print(const[row][col])
#        curr_value = leastConstrainingValue(const,row,col)
#        print(curr_value)
#        print("Value: ",curr_value)
        const[row][col].remove(curr_value)
        #print(const[row][col])
        #print(curr_value)
        #Check consistency
        if isConsistent(board, curr_var, curr_value):
            board[row][col] = curr_value
            const_temp = copy.deepcopy(const)
            const_num_temp = copy.deepcopy(const_num)
            updateConstBoard(row, col, const_temp, const_num_temp)
            #print(temp2)
            if forwardChecking(const_num_temp) == True:
                result = backTracking(board, const_temp, const_num_temp, dumb)
                if result != False:
                    return result
                else:
                   board[row][col] = '_'
    #               print([row, col])
            else:
                board[row][col] = '_'

    return False



def flowFree(filename, dumb):
    board[:] = []

    color_all[:] = []
    color_set.clear()
    color_list[:] = []
    color_path[:] = []
    const_board[:] = [] #Contains sets of possible values for a given location
    const_board_num[:] = []
    
    big_count[0] = 0
    queue[:] = []
    
    getFile(filename)
    for j in range(board_data[0]): #row
        const_board.append([])
        const_board_num.append([])
    for k in range(board_data[1]): #col
        for j in range(board_data[0]):
            const_board[j].append([])
            const_board_num[j].append([])
            
    for k in range(board_data[1]): #col
        for j in range(board_data[0]):
            const_board_num[j][k] = 0
    mostConstrainedVariable(board)
#    print(const_board_num)
#    selectVar(board)
    createQueue()
    
    temp = copy.deepcopy(const_board)      
    print(backTracking(board, temp, const_board_num, dumb))
    printBoard() 
    print(big_count[0])      

    return



#Dumb - 1
#Smart - 2
#Smarter - 3

#start_time = time.time()
#flowFree("input55.txt",3)
#print(time.time() - start_time)

start_time = time.time()
flowFree("input88.txt",3)
print(time.time() - start_time)


#getFile("input991.txt")
#printBoard()
#print(color_set)
#print(board_data[2])
