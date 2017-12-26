import numpy
import math
import random
import copy
import time
import pickle
from datetime import datetime

PADDLE_HEIGHT = [.2]
MIN_X_VEL = .03
HIT_REWARD = 1
MISS_REWARD = -1
MOVE_PADDLE = .04
tot = [0]
cur_status = [0]


class state:
    def __init__(self, ballx, bally, velocityx, velocityy, paddlepos):
    	self.bx = ballx
    	self.by = bally
    	self.vx = velocityx
    	self.vy = velocityy
    	self.py = paddlepos

def updatestate(s1, a):
	s1.bx += s1.vx
	s1.by += s1.vy
	cur_status[0] = 0

	if (a == 2):
		s1.py += .04
		if (s1.py > 1 - PADDLE_HEIGHT[0]):
			s1.py = 1 - PADDLE_HEIGHT[0]
	if (a == 1):
		s1.py -= .04
		if (s1.py < 0):
			s1.py = 0


	if (s1.by < 0):
		s1.by = -s1.by
		s1.vy = - s1.vy

	if (s1.by > 1):
		s1.by = 2 - s1.by
		s1.vy = - s1.vy

	if (s1.bx < 0):
		s1.bx = -s1.bx
		s1.vx = -s1.vx

	if (s1.bx > 1):
		cur_status[0] = -1
		if (s1.by > s1.py and s1.by < s1.py + PADDLE_HEIGHT[0]):
			cur_status[0] = 1
			tot[0] += 1
			s1.bx = 2 - s1.bx
			s1.vy = s1.vy + random.uniform(-.03, .03)
			ox = numpy.sign(s1.vx)
			s1.vx = -s1.vx + random.uniform(-.015, .015)
			if (abs(s1.vy) > 1):
				s1.vy = numpy.sign(s1.vy)
			if (abs(s1.vx) > 1):
				s1.vx = .9 * numpy.sign(s1.vx)
			if (abs(s1.vx) <= .03):
				s1.vx = numpy.sign(s1.vx) * .03
			if (s1.vx == 0):
				s1.vx = -ox *.03
	return s1
	
def convert_discrete(s1):
	dbx = int(numpy.floor(12 * s1.bx))
	if (dbx >= 12):
		dbx = 11
	if (dbx < 0):
		dbx = 0
	dby = int(numpy.floor(12 * s1.by))
	if (dby >= 12):
		dby = 11
	if (dby < 0):
		dby = 0
	dvx = int(numpy.sign(s1.vx))
	if (abs(s1.vy) > .015):
		dvy = int(numpy.sign(s1.vy))
	else:
		dvy = 0
	dpy = int(numpy.floor(12 * s1.py/(1 - PADDLE_HEIGHT[0])))
	if (dpy >= 12):
		dpy = 11
	if (dpy < 0):
		dpy = 0
	return (dbx, dby, dvx, dvy, dpy)

def duplicate_state(cur, copy):
	copy.bx = cur.bx
	copy.by = cur.by
	copy.vx = cur.vx
	copy.vy = cur.vy
	copy.py = cur.py

print("Starting TIME: ", str(datetime.now()))

s = state(.5,.5,.03,.01, .5 - PADDLE_HEIGHT[0]/2)
sprime = state(.5,.5,.03,.01, .5 - PADDLE_HEIGHT[0]/2)
stuple = convert_discrete(s)
q = {}
count = {}
games_lost = 0
c = 75
eps = .05
gamma = .7
gridlen = 12
velx = [-1,1]
vely = [-1,0, 1]
num = 0
total = 0


for x in range(gridlen):
    for y in range(gridlen):
        for vx in range(len(velx)):
            for vy in range(len(vely)):
                for ploc in range(gridlen):
                    for ac in range(3):
                        q[(x,y,velx[vx],vely[vy],ploc, ac)] = 0.0


t = 0
while (games_lost < 50000):
	stuple = convert_discrete(s)

	for a in range(3):
		if (stuple + (a,) not in count):
			count[stuple + (a,)] = 0

	alist = []
	besta = -1

	if (random.uniform(0, 1) < eps):
		besta = random.choice([0, 1, 2])
	else:
		for a in range(3):
			alist.append(q[stuple + (a,)])
		if (alist[0] == 0 and alist[1] == 0 and alist[2]==0):
			besta = random.choice([0, 1, 2])
		else:
			besta = numpy.argmax(alist)

	count[stuple + (besta,)] += 1
	alpha = c/(c + count[stuple + (besta,)])
	sprime = updatestate(sprime, besta)
	sprimetuple = convert_discrete(sprime)

	if (cur_status[0] == -1):
		nextq = -1
	if (cur_status[0] == 0 or cur_status[0] == 1):
		nexta = []
		for a in range(3):
			nexta.append(q[sprimetuple + (a,)])
		nextq = max(nexta)

	q[stuple + (besta,)] += alpha * (cur_status[0] + (gamma * nextq) - q[stuple + (besta,)])

	duplicate_state(sprime, s)

	if (cur_status[0] == -1):
		s = state(.5,.5,.03,.01, .5 - PADDLE_HEIGHT[0]/2)
		sprime = state(.5,.5,.03,.01, .5 - PADDLE_HEIGHT[0]/2)
		games_lost += 1
		num = 0
		if (games_lost == 30000):
			eps = 0

		curavg = tot[0]/games_lost
		if (games_lost % 1000 == 0):
			print(games_lost, "Average: ", curavg)
	elif (cur_status[0] == 1):
		num +=1 
		total += 1
	t += 1


pickle.dump( q, open( "save.p", "wb" ) )


results = []
best = 0
total = 0
games_lost = 0
while (games_lost < 1000):
	test = state(.5,.5,.03,.01, .5 - PADDLE_HEIGHT[0]/2)
	total = 0
	reward = 0
	while (reward != -1):
		testtuple = convert_discrete(test)
		alist = []
		for i in range(3):
			alist.append(q[testtuple + (i,)])
		move = numpy.argmax(alist)
		test = updatestate(test, move)
		reward = cur_status[0]
		total += cur_status[0]
	games_lost += 1
	results.append(total + 1)
	if (total + 1 > best):
		best = total + 1

print("Best Run: ", best)
testave = sum(results)/len(results)
print("Average: ", testave)
print(results)









