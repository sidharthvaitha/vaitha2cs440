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
global_count = [0, 0]


class state:
    def __init__(self, ballx, bally, velocityx, velocityy, paddlepos, paddle2pos):
    	self.bx = ballx
    	self.by = bally
    	self.vx = velocityx
    	self.vy = velocityy
    	self.py = paddlepos
    	self.p2y = paddle2pos

def updatestate(s1, a, a2):
	s1.bx += s1.vx
	s1.by += s1.vy
	cur_status[0] = 0

	if (a == 2):
		# print("Move down")
		s1.py += .04
		if (s1.py > 1 - PADDLE_HEIGHT[0]):
			s1.py = 1 - PADDLE_HEIGHT[0]
	if (a == 1):
		# print("Move up")
		s1.py -= .04
		if (s1.py < 0):
			s1.py = 0


	if (a2 == 2):
		s1.p2y += .02
		if (s1.p2y > 1 - PADDLE_HEIGHT[0]):
			s1.p2y = 1 - PADDLE_HEIGHT[0]
	if (a2 == 1):
		s1.p2y -= .02
		if (s1.p2y < 0):
			s1.p2y = 0


	if (s1.by < 0):
		s1.by = -s1.by
		s1.vy = - s1.vy

	if (s1.by > 1):
		s1.by = 2 - s1.by
		s1.vy = - s1.vy


	if (s1.bx < 0):
		cur_status[0] = -2

		if (s1.by > s1.p2y and s1.by < s1.p2y + PADDLE_HEIGHT[0]):
			cur_status[0] = 2
			tot[0] += 1
			s1.bx = -s1.bx
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
		else:
			global_count[0] += 1



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
		else:
			global_count[1] += 1

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
	copy.p2y = cur.p2y

def discrete_p2(cur):
	disp2 = int(numpy.floor(12*cur.p2y/(1-PADDLE_HEIGHT[0])))
	if disp2 >= 12:
		disp2 = 11
	if disp2 < 0:
		disp2 = 0
	return disp2


def print_game(cur_state):
    grid_size = 12
    ans = []
    print('***************************************')
    for i in range(grid_size):
        temp = []
        for j in range(grid_size):
            temp.append(' ')
        ans.append(temp)
    ball_coordsx = convert_discrete(cur_state)[0]
    ball_coordsy = convert_discrete(cur_state)[1]
    paddle_coordsy = convert_discrete(cur_state)[4]
    paddle_coordsy_2 = discrete_p2(cur_state)   
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


print("Starting TIME: ", str(datetime.now()))

q = pickle.load( open( "save.p", "rb" ) )
print("Length of q is ", len(q))
# print(q)
results = []

total = 0
games_lost = 0
p1 = 0
p2 = 0

while(games_lost < 1000):
	test = state(0.5, 0.5, 0.03, 0.01, 0.5 - PADDLE_HEIGHT[0]/2, 0.5 - PADDLE_HEIGHT[0]/2)
	total = 0
	done = False
	while (done != True):
		if (test.p2y + 0.1) - test.by > 0.08:
			a21 = 1 #Move Up
		elif (test.p2y + 0.1) - test.by < -0.08:
			a21 = 2 #Move down
		else:
			a21 = 0 #stay
		testtuple = convert_discrete(test)
		alist = []
		for i in range(3):
			alist.append(q[testtuple + (i,)])
		move = numpy.argmax(alist)
		test = updatestate(test, move, a21)
		if (cur_status[0] == -2):
			p1 += 1
			done = True
			# print("Player 2 lost")
			# print(convert_discrete(test))
		if (cur_status[0] == -1):
			p2 += 1
			done = True
			# print("Player 1 lost")
			# print(cur_status[0])
			# print(convert_discrete(test))
		# print(cur_status[0])
		# print_game(test)  
		# time.sleep(0.3)
	games_lost += 1
	results.append([p1, p2])

print("Player 1: ", p1)
print("Player 2: ", p2)
print("Win Rate: ", p1/1000)
# print(results)

