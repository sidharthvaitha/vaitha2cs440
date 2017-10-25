import copy
import random


WIDTH = 8
HEIGHT = 8

movesx = [-1, 0, 1]

gameOver = False


class State:
	def __init__(self):
		self.player1positions = {}
		self.player2positions = {}
		self.score = -1


def ismaxmoveValidForMax(item, player1positions):
	row = item[0]
	col = item[1]
	if (row >= 0 and col>=0 and row<HEIGHT and col<WIDTH):
		if ((row, col) in player1positions):
			return False
		return True
	return False

def ismaxmoveValidForMin(item, player2positions):
	row = item[0]
	col = item[1]
	if (row >= 0 and col>=0 and row<HEIGHT and col<WIDTH):
		if ((row, col) in player2positions):
			return False
		return True
	return False


def defensiveheuristic(curstate, isplayer1):
	num_remaining = 0
	if (isplayer1):
		num_remaining = len(curstate.player1positions) 
	else:
		num_remaining = len(curstate.player2positions)
	score =  2*(num_remaining) + random.random()
	return score

def defensiveheuristic2(curstate, isplayer1):
	num_remaining = 0
	if (isplayer1):
		num_remaining = len(curstate.player1positions) 
	else:
		num_remaining = len(curstate.player2positions)
	num_covered = 0
	hash_covered = [False] * WIDTH
	if (isplayer1):
		for item in curstate.player1positions.keys():
			row = item[0]
			col = item[1]
			hash_covered[col] = True
		for i in range(8):
			if (hash_covered[i] == True):
				num_covered = num_covered + 1

	if (isplayer1 == False):
		for item in curstate.player2positions.keys():
			row = item[0]
			col = item[1]
			hash_covered[col] = True
		for i in range(8):
			if (hash_covered[i] == True):
				num_covered = num_covered + 1
	score =  2 * (num_remaining) + 3 * num_covered + random.random()
	return score

def offensiveheuristic(curstate, isplayer1):
	num_remaining = 0
	if (isplayer1==False):
		num_remaining = len(curstate.player1positions) 
	else:
		num_remaining = len(curstate.player2positions)
	score =  2*(30 - num_remaining) + random.random()
	return score


########################################################################################################################################
########################################################################################################################################


def calulateScoreMaxHeuristic(curstate):
	 return defensiveheuristic2(curstate, True)
	# offensiveheuristic(curstate, isplayer1)


def getLevel3Player1MoveState(curstate):
	maxscore = -1
	maxstate = State()
	testbool = False
	for key in curstate.player1positions.iterkeys():
		row = key[0]
		col = key[1]
		for i in range(3):
			nextrow = row + 1
			nextcol = col + movesx[i]
			if (ismaxmoveValidForMax((nextrow, nextcol), curstate.player1positions.keys())):
				newstate = State()
				if (i == 1 and (nextrow, nextcol) in curstate.player2positions):
					continue
				if (nextrow == HEIGHT - 1 or len(curstate.player2positions) == 0):
					curscore = 1 * float("inf")
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = newstate
				elif ((nextrow, nextcol) in curstate.player2positions):
					newstate.player1positions = copy.deepcopy(curstate.player1positions)
					newstate.player2positions = copy.deepcopy(curstate.player2positions)
					del newstate.player2positions[(nextrow, nextcol)]
					del newstate.player1positions[(row, col)]
					newstate.player1positions[(nextrow, nextcol)] = True
					if (len(curstate.player2positions) == 0):
						curscore = float("inf")
						if (curscore > maxscore):
							maxscore = curscore
							maxstate = newstate
					else:
						curscore = calulateScoreMaxHeuristic(newstate)
						if (curscore > maxscore):
							maxscore = curscore
							maxstate = newstate
				else:
					newstate.player1positions = copy.deepcopy(curstate.player1positions)
					newstate.player2positions = copy.deepcopy(curstate.player2positions)
					del newstate.player1positions[(row, col)]
					newstate.player1positions[(nextrow, nextcol)] = True
					curscore = calulateScoreMaxHeuristic(newstate)
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = newstate
	# if (testbool == False):
	# 	print('testbool is false for max level 3')
	return maxscore

def getLevel2Player1MoveState(curstate):
	minscore = 1000000
	minstate = State()
	testbool = False
	for key in curstate.player2positions.iterkeys():
		row = key[0]
		col = key[1]
		for i in range(3):
			nextrow = row - 1
			nextcol = col + movesx[i]
			if (ismaxmoveValidForMin((nextrow, nextcol), curstate.player2positions.keys())):
				newstate = State()
				if (i == 1 and (nextrow, nextcol) in curstate.player1positions):
					continue
				if (nextrow == 0 or len(curstate.player1positions) == 0):
						curscore = -1 * float("inf")
						if (curscore < minscore):
							minscore = curscore
							minstate = newstate
				elif ((nextrow, nextcol) in curstate.player1positions):
					newstate.player1positions = copy.deepcopy(curstate.player1positions)
					newstate.player2positions = copy.deepcopy(curstate.player2positions)
					del newstate.player1positions[(nextrow, nextcol)]
					del newstate.player2positions[(row, col)]
					newstate.player2positions[(nextrow, nextcol)] = True
					if (len(curstate.player1positions) == 0):
						curscore = -1 * float("inf")
						if (curscore < minscore):
							minscore = curscore
							minstate = newstate
					else:
						curscore = getLevel3Player1MoveState(newstate)
						if (curscore < minscore):
							minscore = curscore
							minstate = newstate
				else:
					newstate.player1positions = copy.deepcopy(curstate.player1positions)
					newstate.player2positions = copy.deepcopy(curstate.player2positions)
					del newstate.player2positions[(row, col)]
					newstate.player2positions[(nextrow, nextcol)] = True
					curscore = getLevel3Player1MoveState(newstate)
					if (curscore == -1):
						continue
					if (curscore < minscore):
						minscore = curscore
						minstate = newstate
	# if (testbool == False):
	# 	print('testbool is false for max layer 2')
	return minscore

def getPlayer1MoveState(curstate):
	maxscore = -1
	maxstate = State()
	testbool = False
	for key in curstate.player1positions.iterkeys():
		row = key[0]
		col = key[1]
		for i in range(3):
			nextrow = row + 1
			nextcol = col + movesx[i]
			if (ismaxmoveValidForMax((nextrow, nextcol), curstate.player1positions.keys())):
				testbool = True
				newstate = State()
				newstate.player1positions = copy.deepcopy(curstate.player1positions)
				newstate.player2positions = copy.deepcopy(curstate.player2positions)
				if (i == 1 and (nextrow, nextcol) in curstate.player2positions):
					continue
				if (nextrow == HEIGHT - 1 or len(curstate.player2positions) == 0):
					gameOver = True
					print('Game over winner is Max')
					return State()
				elif ((nextrow, nextcol) in curstate.player2positions):
					print('Max captures min player')
					newstate.player1positions = copy.deepcopy(curstate.player1positions)
					newstate.player2positions = copy.deepcopy(curstate.player2positions)
					del newstate.player2positions[(nextrow, nextcol)]
					del newstate.player1positions[(row, col)]
					newstate.player1positions[(nextrow, nextcol)] = True
					if (len(curstate.player2positions) == 0):
						gameOver = True
						print('Game over winner is Max2')
						return State()
					curscore = getLevel2Player1MoveState(newstate)
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = newstate
				else:
					newstate.player1positions = copy.deepcopy(curstate.player1positions)
					newstate.player2positions = copy.deepcopy(curstate.player2positions)
					del newstate.player1positions[(row, col)]
					newstate.player1positions[(nextrow, nextcol)] = True
					curscore = getLevel2Player1MoveState(newstate)
					if (curscore == 1000000):
						continue
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = copy.deepcopy(newstate)
	if (testbool == False or maxscore == -1):
		print('testbool is false for max')
		maxstate = curstate
	return maxstate


########################################################################################################################################
########################################################################################################################################

def calulateScoreMinHeuristic(curstate):
	#defensiveheuristic(curstate, True)
	return offensiveheuristic(curstate, False)


def getLevel3Player2MoveState(curstate):
	maxscore = -1
	maxstate = State()
	testbool = False
	for key in curstate.player2positions.iterkeys():
		row = key[0]
		col = key[1]
		for i in range(3):
			nextrow = row - 1
			nextcol = col + movesx[i]
			if (ismaxmoveValidForMin((nextrow, nextcol), curstate.player2positions.keys())):
				newstate = State()
				if (i == 1 and (nextrow, nextcol) in curstate.player1positions):
					continue

				if (nextrow == 0 or len(curstate.player1positions) == 0):
					curscore = float("inf")
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = newstate

				elif ((nextrow, nextcol) in curstate.player1positions):
					newstate.player1positions = copy.deepcopy(curstate.player1positions)
					newstate.player2positions = copy.deepcopy(curstate.player2positions)
					del newstate.player1positions[(nextrow, nextcol)]
					del newstate.player2positions[(row, col)]
					newstate.player2positions[(nextrow, nextcol)] = True
					if (len(curstate.player1positions) == 0):
						curscore = float("inf")
						if (curscore > maxscore):
							maxscore = curscore
							maxstate = newstate
					else:
						curscore = calulateScoreMinHeuristic(newstate)
						if (curscore > maxscore):
							maxcore = curscore
							maxstate = newstate
				else:
					
					newstate.player1positions = copy.deepcopy(curstate.player1positions)
					newstate.player2positions = copy.deepcopy(curstate.player2positions)
					del newstate.player2positions[(row, col)]
					newstate.player2positions[(nextrow, nextcol)] = True
					curscore = calulateScoreMinHeuristic(newstate)
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = newstate
	# if (testbool == False):
	# 	print('testbool is false for min layer 3')
	return maxscore

def getLevel2Player2MoveState(curstate):
	minscore = 1000000
	minstate = State()
	testbool = False
	for key in curstate.player1positions.iterkeys():
		row = key[0]
		col = key[1]
		for i in range(3):
			nextrow = row + 1
			nextcol = col + movesx[i]
			if (ismaxmoveValidForMax((nextrow, nextcol), curstate.player1positions.keys())):
				newstate = State()
				if (i == 1 and (nextrow, nextcol) in curstate.player2positions):
					continue

				if (nextrow == HEIGHT - 1 or len(curstate.player2positions) == 0):
					curscore = -float("inf")
					if (curscore < minscore):
						minscore = curscore
						minstate = newstate

				elif ((nextrow, nextcol) in curstate.player2positions):
					newstate.player1positions = copy.deepcopy(curstate.player1positions)
					newstate.player2positions = copy.deepcopy(curstate.player2positions)
					del newstate.player2positions[(nextrow, nextcol)]
					del newstate.player1positions[(row, col)]
					newstate.player1positions[(nextrow, nextcol)] = True
					if (len(curstate.player2positions) == 0):
						curscore = -float("inf")
						if (curscore < minscore):
							minscore = curscore
							minstate = newstate
					else:
						curscore = getLevel3Player2MoveState(newstate)
						if (curscore < minscore):
							minscore = curscore
							minstate = newstate
				else:
					newstate.player1positions = copy.deepcopy(curstate.player1positions)
					newstate.player2positions = copy.deepcopy(curstate.player2positions)
					del newstate.player1positions[(row, col)]
					newstate.player1positions[(nextrow, nextcol)] = True
					curscore = getLevel3Player2MoveState(newstate)
					if (curscore == -1):
						continue
					if (curscore < minscore):
						minscore = curscore
						minstate = newstate
	# if (testbool == False):
	# 	print('testbool is false for min layer 2')
	return minscore

def getPlayer2MoveState(curstate):
	maxscore = -1
	maxstate = State()
	testbool = False
	for key in curstate.player2positions.iterkeys():
		row = key[0]
		col = key[1]
		for i in range(3):
			nextrow = row - 1
			nextcol = col + movesx[i]
			if (ismaxmoveValidForMin((nextrow, nextcol), curstate.player2positions.keys())):
				testbool = True
				newstate = State()
				newstate.player1positions = copy.deepcopy(curstate.player1positions)
				newstate.player2positions = copy.deepcopy(curstate.player2positions)
				if (i == 1 and (nextrow, nextcol) in curstate.player1positions):
					continue
				if (nextrow == 0 or len(curstate.player1positions) == 0):
					gameOver = True
					print('Game over winner is Min')
					print(curstate.player2positions)
					return State()
				elif ((nextrow, nextcol) in curstate.player1positions):
					print('Min captures max player')

					newstate.player1positions = copy.deepcopy(curstate.player1positions)
					newstate.player2positions = copy.deepcopy(curstate.player2positions)
					del newstate.player1positions[(nextrow, nextcol)]
					del newstate.player2positions[(row, col)]
					newstate.player2positions[(nextrow, nextcol)] = True
					if (len(curstate.player1positions) == 0):
						gameOver = True
						print('Game over winner is Min2')
						print(curstate.player2positions)
						return State()
					curscore = getLevel2Player2MoveState(newstate)
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = newstate
				else:
					newstate.player1positions = copy.deepcopy(curstate.player1positions)
					newstate.player2positions = copy.deepcopy(curstate.player2positions)
					del newstate.player2positions[(row, col)]
					newstate.player2positions[(nextrow, nextcol)] = True
					curscore = getLevel2Player2MoveState(newstate)
					if (curscore == 1000000):
						continue
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = copy.deepcopy(newstate)
	if (testbool == False or maxscore == -1):
		print('testbool is false for min')
		maxstate = curstate
	return maxstate

########################################################################################################################################
########################################################################################################################################


def printstate(curstate):
	w, h = 8, 8
	data = [['*' for x in range(w)] for y in range(h)] 

	print'****************************************'
	for item in curstate.player1positions.keys():
		r = item[0]
		c = item[1]
		data[r][c] = 'a'

	for item in curstate.player2positions.keys():
		r = item[0]
		c = item[1]
		data[r][c] = 'b'

	for row in data:
		print " ".join(row)
	print'****************************************'


def main():
	initState = State();
	for i in range(2):
		for j in range(HEIGHT):
			initState.player1positions[(i, j)] = True
	for i in range(WIDTH - 2, WIDTH):
		for j in range(HEIGHT):
			initState.player2positions[(i, j)] = True

	printstate(initState)
	player2movestate = copy.deepcopy(initState)
	player1movestate = copy.deepcopy(initState)
	counter = 0
	while (gameOver == False):
		counter = counter + 1
		print('MinMove')
		player1movestate = getPlayer2MoveState(copy.deepcopy(player2movestate))
		printstate(player1movestate)
		if (len(player1movestate.player1positions) == 0):
			print('reached break condition 1')
			print(player1movestate.player2positions)
			break
		print('MaxMove')
		player2movestate = getPlayer1MoveState(copy.deepcopy(player1movestate))
		printstate(player2movestate)
		if (len(player2movestate.player1positions) == 0):
			print('reached break condition 3')
			print(player2movestate.player2positions)
			break
		if (counter == 100):
			break
		print('counter ', counter, ' Max positions len ', len(player2movestate.player1positions), ' Min positions len ', len(player2movestate.player2positions))
		
if __name__ == "__main__":
    main()



