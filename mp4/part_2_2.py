# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 16:02:31 2017

@author: Ben
"""

import time
import random
import numpy
#import pygame
#import sys
import copy
from datetime import datetime
import pickle

PADDLE_HEIGHT = 0.2
MIN_X_VEL = 0.03
BOUNCE_REWARD = 1
MISS_REWARD = -1
MOVE_UP = -0.04
MOVE_DOWN = 0.04
STAY = 0

props = [PADDLE_HEIGHT]

tot=[0]

status_flag = [0]

class state():
    "Stores the continuous state"
    def __init__(self, ball_x, ball_y, velocity_x, velocity_y, paddle_y, paddle_y_2):
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.paddle_y = paddle_y
        self.paddle_y_2 = paddle_y_2



def Update(cur_state, action, action2):
    cur_state.ball_x +=  cur_state.velocity_x
    cur_state.ball_y +=  cur_state.velocity_y
    status_flag[0] = 0
    if action == 1: #Move Up
        cur_state.paddle_y -= 0.04
        if cur_state.paddle_y < 0:
            cur_state.paddle_y = 0
    if action == 2: #Move Down
        cur_state.paddle_y += 0.04
        if cur_state.paddle_y > 1 - props[0]:
            cur_state.paddle_y = 1 - props[0]
    if action2 == 1: #Move Up
        cur_state.paddle_y_2 -= 0.02
        if cur_state.paddle_y_2 < 0:
            cur_state.paddle_y_2 = 0
    if action2 == 2: #Move Down
        cur_state.paddle_y_2 += 0.02
        if cur_state.paddle_y_2 > 1 - props[0]:
            cur_state.paddle_y_2 = 1 - props[0]
    if cur_state.ball_y < 0:
        status_flag[0] = 0
        cur_state.ball_y = -cur_state.ball_y
        cur_state.velocity_y = -cur_state.velocity_y
    if cur_state.ball_y > 1:
        status_flag[0] = 0
        cur_state.ball_y = 2 - cur_state.ball_y
        cur_state.velocity_y = -cur_state.velocity_y
#    if cur_state.ball_x < 0:
#        status_flag[0] = 0
#        cur_state.ball_x = -cur_state.ball_x
#        cur_state.velocity_x = -cur_state.velocity_x
    if cur_state.ball_x < 0:
        status_flag[0] = -2
        if cur_state.ball_y > cur_state.paddle_y_2 and cur_state.ball_y < cur_state.paddle_y_2 + props[0]:
            tot[0]+=1
#                print("Hit")
            status_flag[0] = 2
            cur_state.ball_x = -cur_state.ball_x
            cur_state.velocity_y = cur_state.velocity_y + random.uniform(-0.03, 0.03)
            orig_x = numpy.sign(cur_state.velocity_x) # Need when x velocity goes to zero
            cur_state.velocity_x = -cur_state.velocity_x + random.uniform(-0.015, 0.015)
            if abs(cur_state.velocity_y) > 1:
                cur_state.velocity_y = numpy.sign(cur_state.velocity_y)  
            if abs(cur_state.velocity_x) > 1:
                cur_state.velocity_x = 0.9*numpy.sign(cur_state.velocity_x)  
            if abs(cur_state.velocity_x) <= 0.03:
                cur_state.velocity_x = numpy.sign(cur_state.velocity_x)*0.03  
            if cur_state.velocity_x == 0:
                cur_state.velocity_x = -orig_x*0.03 #negative to switch the direction
    if cur_state.ball_x > 1:
            status_flag[0] = -1
            if cur_state.ball_y > cur_state.paddle_y and cur_state.ball_y < cur_state.paddle_y + props[0]:
                tot[0]+=1
#                print("Hit")
                status_flag[0] = 1
                cur_state.ball_x = 2-cur_state.ball_x
                cur_state.velocity_y = cur_state.velocity_y + random.uniform(-0.03, 0.03)
                orig_x = numpy.sign(cur_state.velocity_x) # Need when x velocity goes to zero
                cur_state.velocity_x = -cur_state.velocity_x + random.uniform(-0.015, 0.015)
                if abs(cur_state.velocity_y) > 1:
                    cur_state.velocity_y = numpy.sign(cur_state.velocity_y)  
                if abs(cur_state.velocity_x) > 1:
                    cur_state.velocity_x = 0.9*numpy.sign(cur_state.velocity_x)  
                if abs(cur_state.velocity_x) <= 0.03:
                    cur_state.velocity_x = numpy.sign(cur_state.velocity_x)*0.03  
                if cur_state.velocity_x == 0:
                    cur_state.velocity_x = -orig_x*0.03 #negative to switch the direction
    return cur_state
    


# Returns a tuple
def Discretize(cur_state):
    discrete_ball_x = int(numpy.floor(12*cur_state.ball_x))
    if discrete_ball_x >= 12:
        discrete_ball_x = 11
    if discrete_ball_x < 0:
        discrete_ball_x = 0
    discrete_ball_y = int(numpy.floor(12*cur_state.ball_y))
    if discrete_ball_y >= 12:
        discrete_ball_y = 11
    if discrete_ball_y < 0:
        discrete_ball_y = 0
    discrete_velocity_x = int(numpy.sign(cur_state.velocity_x))
    if abs(cur_state.velocity_y) > 0.015:
        discrete_velocity_y = int(numpy.sign(cur_state.velocity_y))
    else:
        discrete_velocity_y = 0
    discrete_paddle_y = int(numpy.floor(12*cur_state.paddle_y/(1-props[0])))
    if discrete_paddle_y >= 12:
        discrete_paddle_y = 11
    if discrete_paddle_y < 0:
        discrete_paddle_y = 0

    return (discrete_ball_x, discrete_ball_y, discrete_velocity_x, discrete_velocity_y, discrete_paddle_y)

def d_P_2(cur_state):
    discrete_paddle_y_2 = int(numpy.floor(12*cur_state.paddle_y_2/(1-props[0])))
    if discrete_paddle_y_2 >= 12:
        discrete_paddle_y_2 = 11
    if discrete_paddle_y_2 < 0:
        discrete_paddle_y_2 = 0
    return discrete_paddle_y_2

#
#test = state(1.01,0.1, 0, -0.3, 0)
#
#print(Reward(test))
#def q_fun()

def print_game(cur_state):
    grid_size = 12
    ans = []
    print('***************************************')
    for i in range(grid_size):
        temp = []
        for j in range(grid_size):
            temp.append(' ')
        ans.append(temp)
    ball_coordsx = Discretize(cur_state)[0]
    ball_coordsy = Discretize(cur_state)[1]
    paddle_coordsy = Discretize(cur_state)[4]
    paddle_coordsy_2 = d_P_2(cur_state)   
    ball_coords = [ball_coordsy, ball_coordsx]
    paddle_coords = [paddle_coordsy, 11]
    paddle_coords_2 = [paddle_coordsy_2, 0]
    ans[int(paddle_coords[0]*(9/11))][paddle_coords[1]] = '|'
    ans[int((paddle_coords[0])*(9/11)+1)][paddle_coords[1]] = '|'
    ans[int((paddle_coords[0])*(9/11)+2)][paddle_coords[1]] = '|'
    ans[int(paddle_coords_2[0]*(9/11))][paddle_coords_2[1]] = '|'
    ans[int((paddle_coords_2[0])*(9/11)+1)][paddle_coords_2[1]] = '|'
    ans[int((paddle_coords_2[0])*(9/11)+2)][paddle_coords_2[1]] = '|'
    ans[ball_coords[0]][ball_coords[1]] = 'b'
    for line in ans:
        print (' '.join(str(v) for v in line))
    print('***************************************')
    
def dup(from_obj, to_obj):    
    to_obj.ball_x = from_obj.ball_x
    to_obj.ball_y = from_obj.ball_y
    to_obj.velocity_x = from_obj.velocity_x
    to_obj.velocity_y = from_obj.velocity_y
    to_obj.paddle_y = from_obj.paddle_y
    to_obj.paddle_y_2 = from_obj.paddle_y_2
#%%

print(str(datetime.now()))

current_state = state(0.5, 0.5, 0.03, 0.01, 0.5 - props[0]/2, 0.5 - props[0]/2)
next_state = state(0.5, 0.5, 0.03, 0.01, 0.5 - props[0]/2, 0.5 - props[0]/2)
cur_tuple = Discretize(current_state)
rewards = 0
q = {}
count = {}
training_game = 0
test_game = 0
C = 75
gamma = 0.7
epsilon = 0.05
grid = 12
vel_x = [-1, 1]
vel_y = [-1, 0, 1]
bounce = 0
total_bounce = 0

P_1_win = 0
P_2_win = 0


for x in range(grid):
    for y in range(grid):
        for x_v in range(len(vel_x)):
            for y_v in range(len(vel_y)):
                for p_y in range(grid):
                    for act in range(3):
                        q[(x,y,vel_x[x_v],vel_y[y_v],p_y, act)] = 0.0


# R=0
# tick = 0
# while (training_game <100000):
    
    
    
#     if (current_state.paddle_y_2 + 0.1) - current_state.ball_y > 0.08:
#         action_2 = 1 #Move Up
#     elif (current_state.paddle_y_2 + 0.1) - current_state.ball_y < -0.08:
#         action_2 = 2 #Move down
#     else:
#         action_2 = 0 #stay
    
#     cur_tuple = Discretize(current_state)
    
#     for act in range(3):
#         if ((cur_tuple + (act, )) not in count):
#             count[cur_tuple + (act, )] = 0

#     best = []
    
#     if random.uniform(0,1) < epsilon:
#         action = random.choice([0, 1, 2])
#     else:
#         for act in range(3):
#             best.append(q[cur_tuple + (act, )])
#         if (best[0] == 0 and best[1] == 0 and best[2] == 0):
#             action = random.choice([0, 1, 2])
#         else:
# #            action = random.choice(numpy.argwhere(best == numpy.amax(best)))
#             action = numpy.argmax(best)
            
# #    print(action)
#     count[cur_tuple + (action, )] += 1
#     alpha = C/(C + count[cur_tuple + (action, )] )
#     next_state = Update(next_state, action, action_2)
# #    print_game(next_state)
# #    time.sleep(0.1)
#     next_tuple = Discretize(next_state)
    
    
#     if status_flag[0] == -1: #Game lost
#         R = -1
#         next_q = -1
# #        print("Miss")
#     if status_flag[0] == 0:
#         R = 0
#         next_action = []
#         for act in range(3):
#             next_action.append(q[next_tuple + (act, )])
#         next_q = max(next_action)
#     if status_flag[0] == 1: #player 1 wins
#         R = 1
#         for act in range(3):
#             next_action.append(q[next_tuple + (act, )])
#         next_q = max(next_action)
#     if status_flag[0] == -2: #Player 2 loss
#         R = 1
#         next_q = 1
#     if status_flag[0] == 2:  #Player 2 hit
#         R = 0
#         next_action = []
#         for act in range(3):
#             next_action.append(q[next_tuple + (act, )])




#     q[cur_tuple + (action, )] += alpha * (R + (gamma * next_q) - q[cur_tuple + (action, )])
#     dup(next_state, current_state)
    
# #    current_state = next_state
# #    print(current_state.ball_x)
#     if status_flag[0] == -1:
# #        print("New Game")
#         current_state = state(0.5, 0.5, 0.03, 0.01, 0.5 - props[0]/2, 0.5 - props[0]/2)
#         next_state = state(0.5, 0.5, 0.03, 0.01, 0.5 - props[0]/2, 0.5 - props[0]/2)
#         training_game += 1
#         P_2_win += 1
#         if training_game == 30000:
#             epsilon = 0
#         bounce = 0
#         if training_game % 1000 == 0:
#             print(training_game)
#             print("Player 1: ", P_1_win)
#             print("Player 2: ", P_2_win)
#     if status_flag[0] == -2:
#         current_state = state(0.5, 0.5, 0.03, 0.01, 0.5 - props[0]/2, 0.5 - props[0]/2)
#         next_state = state(0.5, 0.5, 0.03, 0.01, 0.5 - props[0]/2, 0.5 - props[0]/2)
#         training_game += 1
#         P_1_win += 1
# #        total_P_1_wins += 1
#         if training_game == 30000:
#             epsilon = 0
#         bounce = 0
#         if training_game % 1000 == 0:
#             print(training_game)
#             print("Player 1: ", P_1_win)
#             print("Player 2: ", P_2_win)
# #    if status_flag[0] == 2:
# #        bounce += 1
# #        total_bounce += 1   


#     tick += 1



#%%
# q = pickle.load( open( "save.p", "rb" ) )
# print("Length of q is ", len(q))
# all_total=[]
# best_total = 0
# total = 0
# j = 0
# P_1_win = 0
# P_2_win = 0

# while(j<1000):
#     test_state = state(0.5, 0.5, 0.03, 0.01, 0.5 - props[0]/2, 0.5 - props[0]/2)
#     total = 0
#     over = False
#     while (over != True):
#         if (test_state.paddle_y_2 + 0.1) - test_state.ball_y > 0.08:
#             action_2 = 1 #Move Up
#         elif (test_state.paddle_y_2 + 0.1) - test_state.ball_y < -0.08:
#             action_2 = 2 #Move down
#         else:
#             action_2 = 0 #stay
#         test_tuple = Discretize(test_state)
#         maxlist = []
#         for act in range(3):
#             maxlist.append(q[test_tuple + (act, )])
#         best_move = numpy.argmax(maxlist)
#         test_state = Update(test_state, best_move, action_2)
#         if status_flag[0] == -2:
#             P_1_win += 1
#             over = True
#         if status_flag[0] == -1:
#             P_2_win += 1
#             over = True
            
# #        reward = status_flag[0]
# #        total += reward
        
# #        print("Count is ", total)
# #        print_game(test_state)  
# #        time.sleep(0.1)
# #    total += teststate.count
#     j += 1
#     all_total.append([P_1_win,P_1_win])
# #    if total+1 > best_total:
# #        best_total = total+1
        
# #print("Best Run: ", best_total)
# #ave = sum(all_total)/len(all_total)
# print("Player 1: ", P_1_win)
# print("Player 2: ", P_2_win)
# print("Win Rate: ", P_1_win/1000)
#print("Var: ", numpy.var(all_total))


q = pickle.load( open( "save.p", "rb" ) )
print("Length of q is ", len(q))
# print(q)
results = []

total = 0
games_lost = 0
p1 = 0
p2 = 0

while(games_lost < 1000):
    test = state(0.5, 0.5, 0.03, 0.01, 0.5 - props[0]/2, 0.5 - props[0]/2)
    total = 0
    done = False
    while (done != True):
        if (test.paddle_y_2 + 0.1) - test.ball_y > 0.08:
            a2 = 1 #Move Up
        elif (test.paddle_y_2 + 0.1) - test.ball_y < -0.08:
            a2 = 2 #Move down
        else:
            a2 = 0 #stay
        testtuple = Discretize(test)
        alist = []
        for i in range(3):
            alist.append(q[testtuple + (i,)])
        move = numpy.argmax(alist)
        test = Update(test, move, a2)
        if (status_flag[0] == -2):
            p1 += 1
            done = True
        if (status_flag[0] == -1):
            p2 += 1
            done = True
    games_lost += 1
    results.append([p1, p2])

print("Player 1: ", p1)
print("Player 2: ", p2)
print("Win Rate: ", p1/1000)
print(results)

