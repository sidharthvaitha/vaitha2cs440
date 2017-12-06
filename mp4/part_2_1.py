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

PADDLE_HEIGHT = 0.2
MIN_X_VEL = 0.03
BOUNCE_REWARD = 1
MISS_REWARD = -1
MOVE_UP = 0.04
MOVE_DOWN = -0.04
STAY = 0

props = [PADDLE_HEIGHT]

class state():
    "Stores the continuous state"
    def __init__(self, ball_x, ball_y, velocity_x, velocity_y, paddle_y):
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.paddle_y = paddle_y




#init_state = (0.5, 0.5, 0.03, 0.01, 0.5 - PADDLE_HEIGHT / 2)



def BounceCheck(cur_state):
#    reward = 0
    if cur_state.ball_y < 0:
#        reward = 0
        cur_state.ball_y = -cur_state.ball_y
        cur_state.velocity_y = -cur_state.velocity_y
    if cur_state.ball_y > 1:
#        reward = 0
        cur_state.ball_y = 2 - cur_state.ball_y
        cur_state.velocity_y = -cur_state.velocity_y
    if cur_state.ball_x < 0:
#        reward = 0
        cur_state.ball_x = -cur_state.ball_x
        cur_state.velocity_x = -cur_state.velocity_x
#    if cur_state.ball_x > 1:
#        reward = 0
#        cur_state.ball_x = 2-cur_state.ball_x
#        cur_state.velocity_x = -cur_state.velocity_x
    if cur_state.ball_x > 1 and cur_state.ball_y > cur_state.paddle_y and cur_state.ball_y < cur_state.paddle_y + props[0]:
#        reward = 1
        print("Hit")
        cur_state.ball_x = 2-cur_state.ball_x
        cur_state.velocity_y = -cur_state.velocity_y + random.uniform(-0.03, 0.03)
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
#    else:
#        reward = -1
    return cur_state

def Reward(cur_state):
    reward = 0
    if cur_state.ball_x > 1:
        reward = -1
        if cur_state.ball_y > cur_state.paddle_y and cur_state.ball_y < cur_state.paddle_y + props[0]:
            reward = 1
    return reward


def Move(cur_state, action):
    cur_state.ball_x +=  cur_state.velocity_x
    cur_state.ball_y +=  cur_state.velocity_y
    if action == 1: #Move Up
        cur_state.paddle_y -= 0.04
    if action == 2: #Move Down
        cur_state.paddle_y += 0.04
    return cur_state

# Returns a tuple
def Discretize(cur_state):
    discrete_ball_x = int(numpy.floor(12*cur_state.ball_x))
    if discrete_ball_x >= 12:
        discrete_ball_x = 11
    discrete_ball_y = int(numpy.floor(12*cur_state.ball_y))
    if discrete_ball_y >= 12:
        discrete_ball_y = 11
    discrete_velocity_x = int(numpy.sign(cur_state.velocity_x))
    if abs(cur_state.velocity_y) > 0.015:
        discrete_velocity_y = int(numpy.sign(cur_state.velocity_y))
    else:
        discrete_velocity_y = 0
    discrete_paddle_y = int(numpy.floor(12*cur_state.paddle_y/(1-props[0])))
    if discrete_paddle_y >= 12:
        discrete_paddle_y = 11
    return (discrete_ball_x, discrete_ball_y, discrete_velocity_x, discrete_velocity_y, discrete_paddle_y)


#test = state(.98,0.75, 0, -0.3, 0)

#print(Reward(test))
#def q_fun()



#%%

cur_state = state(0.5, 0.5, 0.03, 0.01, 0.5 - props[0]/2)
rewards = 0
q = {}
count = {}
training_game = 0
test_game = 0
C = 50
gamma = 0.7
epsilon = 0.05
grid = 12
vel_x = [-1, 1]
vel_y = [-1, 0, 1]
bounce = 0
total_bounce = 0

for x in range(grid):
    for y in range(grid):
        for x_v in range(len(vel_x)):
            for y_v in range(len(vel_y)):
                for p_y in range(grid):
                    for act in range(3):
                        q[(x,y,vel_x[x_v],vel_y[y_v],p_y, act)] = 0.0



tick = 0
while (training_game <100000):
    
    cur_tuple = Discretize(cur_state)
    for act in range(3):
        if ((cur_tuple + (act, )) not in count):
            count[cur_tuple + (act, )] = 0

    best = []
    
    if random.uniform(0,1) < epsilon:
        action = random.choice([0, 1, 2])
    else:
        for act in range(3):
            best.append(q[cur_tuple + (act, )])
        action = numpy.argmax(best)
    count[cur_tuple + (action, )] += 1
    alpha = C/(C + count[cur_tuple + (act, )] )
    R = Reward(cur_state)
#    print([R, cur_state.ball_x, tick])
    next_state = copy.deepcopy(cur_state)
#    print(next_state.ball_y)
    next_state = Move(next_state, action)
#    print(next_state.ball_x)
    next_state = BounceCheck(next_state)
#    print(next_state.ball_x)
    next_tuple = Discretize(next_state)
    next_action = []
    for act in range(3):
        next_action.append(q[next_tuple + (act, )])
    next_q = max(next_action)
    q[cur_tuple + (act, )] += alpha * (R + (gamma * next_q) - q[cur_tuple + (act, )])

#    print("Before Move: ",cur_state.ball_x)
    Move(cur_state, action)
#    print("After Move: ",cur_state.ball_x)
    cur_state = BounceCheck(cur_state)
#    print("Bounce Check: ",cur_state.ball_x)
    if R == -1:
#        print("New Game")
        cur_state = state(0.5, 0.5, 0.03, 0.01, 0.5 - props[0]/2)
        training_game += 1
        bounce = 0
        bounce_ave = total_bounce/training_game
        if training_game % 1000 == 0:
            print("Bounce Average: ", bounce_ave)
    elif R == 1:
        bounce += 1
#        print([bounce,tick])
        total_bounce += 1
    tick += 1



#%%
all_total=[]
best_total = 0
total = 0
j = 0
while(j<1000):
    test_state = state(0.5, 0.5, 0.03, 0.01, 0.5 - props[0]/2)
    total = 0
    while (Reward(test_state) != -1):
        test_tuple = Discretize(test_state)
        maxlist = []
        for act in range(3):
            maxlist.append(q[test_tuple + (act, )])
        best_move = numpy.argmax(maxlist)
        Move(test_state, best_move)
        total += Reward(test_state)
#        print("Count is ", total)
        
#    total += teststate.count
    j += 1
    all_total.append(total+1)
    if total+1 > best_total:
        best_total = total+1
        
print("Best Run: ", best_total)
ave = sum(all_total)/len(all_total)
print("Average: ", ave)








#pygame.init()
#BLACK     = (0  ,0  ,0  )
#WHITE     = (255,255,255)
#FPSCLOCK = pygame.time.Clock()
#FPS =200
#cur_state = state(0.5, 0.5, 0.03, 0.01, 0.5 - PADDLE_HEIGHT / 2)
#DISPLAYSURF = pygame.display.set_mode((1000,1000)) 
#pygame.display.set_caption('Pong')
#DISPLAYSURF.fill((0,0,0))
#pygame.draw.rect(DISPLAYSURF, WHITE, ((500, 500),(5,5)))
#
#  
#for x in range(20000):
#
##    drawArena()
##    drawPaddle(paddle1)
##    drawPaddle(paddle2)
##    drawBall(ball)
#    cur_state = Move(cur_state)
#    [cur_state, reward] = BounceCheck(cur_state)
#    print(cur_state.ball_x)
#    ball = ((int(cur_state.ball_x*1000),int(cur_state.ball_y*1000)),(5,5))
##    ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
##    score = checkPointScored(paddle1, ball, score, ballDirX)
##    ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
##    paddle2 = artificialIntelligence (ball, ballDirX, paddle2)
#
##    displayScore(score)
#    DISPLAYSURF.fill((0,0,0))
#    pygame.draw.rect(DISPLAYSURF, WHITE, ball)
##    pygame.draw.rect(DISPLAYSURF, WHITE, ((500, 500),(5,5)))
#    pygame.display.update()
#    FPSCLOCK.tick(FPS)
##    pygame.time.delay(100)
#
#pygame.display.quit()
#pygame.quit()
#sys.exit()



#print(Discretize(test))

"""
Add one special state for all cases when the ball has passed your paddle (ball_x > 1). 
This special state needn't differentiate among any of the other variables listed above,
 i.e., as long as ball_x > 1, the game will always be in this state, regardless of 
 the ball's velocity or the paddle's location. This is the only state with a reward of -1.
"""


       
#[test_state, reward] = BounceCheck(test)
#print(test_state.ball_y)
#print(reward)