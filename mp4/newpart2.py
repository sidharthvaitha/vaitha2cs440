import numpy
import math
import random
import copy
import time

class state:
    def __init__(self):
        self.ballx = .5
        self.bally = .5
        self.discrete_ballx = int(12 * self.ballx)
        self.discrete_bally = int(12 * self.bally)
        self.paddlex = 1
        self.paddleheight = .2
        self.paddley = .5 - (self.paddleheight)/2
        self.discretepaddley = math.floor(12 * self.paddley/(1- self.paddleheight))
        self.velocityx = .03
        self.velocityy = .01
        self.discretevelocityx = 1
        self.discrete_velocityy = 0
        self.count = 0
        self.curstatus = 0

    def updateball(self):
        self.ballx += self.velocityx
        self.bally += self.velocityy
        self.curstatus = 0
#        print(self.ballx)
      

        if (self.bally < 0):
#            print("hit y = 0")
            self.bally = - self.bally
            self.velocityy = - self.velocityy

        elif (self.bally > 1):
#            print("hit y = 1")
            self.bally = 2 - self.bally
            self.velocityy = - self.velocityy

        if (self.ballx < 0):
#            print("hit x < 0")
            self.ballx - -self.ballx
            self.velocityx = - self.velocityx

        if (self.ballx >= 1 and self.bally > self.paddley and self.bally <(self.paddley + self.paddleheight)):
#            print("hit paddle")
            self.ballx = 2 * self.paddlex - self.ballx
            orig_x = self.velocityx
            self.velocityx = -self.velocityx + random.uniform(-0.015,0.015)
            self.velocityy = self.velocityy +  random.uniform(-0.03,0.03)
            self.count += 1
            self.curstatus = 1

            if abs(self.velocityy) > 1:
                self.velocityy = numpy.sign(self.velocityy) * .03
            if abs(self.velocityx) > 1:
                self.velocityx = numpy.sign(self.velocityx) * .03 
            if abs(self.velocityx) <= 0.03:
                cur_state.velocityx = numpy.sign(cur_state.velocityx)*0.03 
            if cur_state.velocityx == 0:
                cur_state.velocityx = -orig_x*0.03

        if (self.ballx > 1):
#            print("miss paddle")
            self.ballx = .5
            self.bally = .5
            self.velocityx = .03
            self.velocityy = .01
            self.curstatus = -1
            self.count = 0
            self.paddley = .5 - (self.paddleheight)/2
    
   

    def moveup(self):
        # print("paddle up")
        if (self.paddley < .05):
            self.paddley = 0
        else:
            self.paddley -= .04

    def movedown(self):
        # print("paddle down")
        if (self.paddley > .8):
            self.paddley = .8
        else:
            self.paddley += .04


    def movepaddle(self, action):
        if (action == 1):
            self.moveup()
        elif (action == 2):
            self.movedown()

    def convertdiscrete(self):
        self.discretepaddley = math.floor(12 * self.paddley/(1- self.paddleheight))
        if (self.paddley == (1- self.paddleheight)):
            self.discretepaddley = 11

        if(self.velocityx < 0):
            self.discretevelocityx = -1
        else:
            self.discretevelocityx = 1

        if (abs(self.velocityy) < .015):
            self.discrete_velocityy = 0
        elif (self.velocityy < -.015):
            self.discrete_velocityy = -1
        elif (self.velocityy > .015):
            self.discrete_velocityy = 1

        self.discrete_ballx = int(12 * self.ballx)
        self.discrete_bally = int(12 * self.bally)
        if (self.discrete_ballx >= 12):
            self.discrete_ballx = 11
        if (self.discrete_bally >= 12):
            self.discrete_bally = 11
        if (self.discretepaddley >= 12):
            self.discretepaddley = 11
        if (self.discrete_ballx < 0):
            self.discrete_ballx = 0
        if (self.discrete_bally < 0):
            self.discrete_bally = 0
        if (self.discretepaddley < 0):
            self.discretepaddley = 0

    def update_state(self, action = 0):
        self.updateball()
        self.movepaddle(action)
        self.convertdiscrete()

    def get_hashtuple(self):
        return (self.discrete_ballx, self.discrete_bally, self.discretevelocityx, self.discrete_velocityy, self.discretepaddley)

    def getstatus(self):
        return self.curstatus


def print_game(temp2):
    grid_size = 12
    ans = []
    print('***************************************')
#    print("Paddle Position ", cur_state.get_hashtuple()[4])
#    print(runcount)
    for i in range(grid_size):
        temp = []
        for j in range(grid_size):
            temp.append(' ')
        ans.append(temp)
    ball_coordsx = temp2.get_hashtuple()[0]
    ball_coordsy = temp2.get_hashtuple()[1]
    paddle_coordsy = temp2.get_hashtuple()[4]
    ball_coords = [ball_coordsy, ball_coordsx]
    paddle_coords = [paddle_coordsy, 11]
    ans[int(paddle_coords[0]*(9/11))][paddle_coords[1]] = '|'
    ans[int((paddle_coords[0])*(9/11)+1)][paddle_coords[1]] = '|'
    ans[int((paddle_coords[0])*(9/11)+2)][paddle_coords[1]] = '|'
    ans[ball_coords[0]][ball_coords[1]] = 'b'
#    print('***************************************')
    for line in ans:
        print (' '.join(str(v) for v in line))
    print('***************************************')


cur_state = state()
rewards = 0
q = {}
count = {}
games_lost = 0
C = 50
gamma = 0.7

gridlen = 12
velx = [-1,1]
vely = [-1,0, 1]


for x in range(gridlen):
    for y in range(gridlen):
        for vx in range(len(velx)):
            for vy in range(len(vely)):
                for ploc in range(gridlen):
                    for ac in range(3):
                        q[(x,y,velx[vx],vely[vy],ploc, ac)] = 0.0



def findQdiff(curtuple, j):
    maxlist = []
    for i in range(3):
        nextstate = copy.deepcopy(cur_state)
        nextstate.update_state(i)
        nexthash = nextstate.get_hashtuple()
        diff = q[nexthash + (i, )] 
        maxlist.append(diff)
    return max(maxlist)


def evaluate(curtuple, i):
    curactiontuple = curtuple + (i, )
#    if (count[curactiontuple] < 3):
#        return 2
#    else:
    return q[curactiontuple]

epsilon = 0.1
runcount = 0
while (games_lost < 100000):
    runcount += 1
    if (runcount % 1000000 == 0):
#        epsilon *= 0.999
        print ("games_lost", games_lost)
    curtuple = cur_state.get_hashtuple()
    for i in range(3):
        curactiontuple = curtuple + (i, )
#        print(curactiontuple)
        if (curactiontuple not in count):
            count[curactiontuple] = 0

    gains = []
    for i in range(3):
        gains.append(evaluate(curtuple, i))
        
    bestaction = numpy.argmax(gains)
    if gains[0] == 0 and gains[1] == 0 and gains[2] == 0 :
        bestaction = random.choice([0,1,2])
    else:
        rand_test = random.uniform(0,1)
        if rand_test < epsilon:
            bestaction = random.choice([0,1,2])
            
    
#    bestaction = numpy.argmax(gains)
    curactiontuple = curtuple + (bestaction, )
    alpha = C/(C + count[curactiontuple])
    # print(curactiontuple)
    cur_state.update_state(bestaction)
    q[curactiontuple] += alpha * (cur_state.getstatus() + (gamma * findQdiff(curtuple, bestaction)) -  q[curtuple + (bestaction,)])
#    print(q[curactiontuple])
    count[curactiontuple] += 1
#    cur_state.update_state(bestaction)
#    print(runcount)
#    print_game()
#    time.sleep(.1)
    if (cur_state.getstatus() == -1):
        # print("games lost")
        games_lost += 1
    if (cur_state.getstatus() == -1):
        rewards -= 1
    if (cur_state.getstatus() == 1):
        rewards += 1
#    print("paddle ",cur_state.discretepaddley)
#    print("Ball ",cur_state.discrete_bally)
print("Len of count is ", len(count))
print("Len of Q is ", len(q))
#%%
all_total=[]
best_total = 0
total = 0
j = 0
while(j<1000):
    teststate = state()
    total = 0
    while (teststate.getstatus() != -1):
        testtuple = teststate.get_hashtuple()
        maxlist = []
        for i in range(3):
            maxlist.append(q[testtuple + (i, )])
#        print(maxlist)
        bestmove = numpy.argmax(maxlist)
        teststate.update_state(bestmove)
        total += teststate.getstatus()
#        print("Count is ", total)
#        print_game(teststate)
#        time.sleep(.1)
#    total += teststate.count
    j += 1
    all_total.append(total+1)
    if total+1 > best_total:
        best_total = total+1
        
print("Best Run: ", best_total)
ave = sum(all_total)/len(all_total)
print("Average: ", ave)
print ("Variance is ", numpy.var(results))
