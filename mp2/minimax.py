import copy
import random


WIDTH = 8
HEIGHT = 8

movesx = [-1, 0, 1]

gameOver = False


class State:
	def __init__(self):
		self.maxpositions = {}
		self.minpositions = {}
		self.score = -1


def ismaxmoveValidForMax(item, maxpositions):
	row = item[0]
	col = item[1]
	if (row >= 0 and col>=0 and row<HEIGHT and col<WIDTH):
		if ((row, col) in maxpositions):
			return False
		return True
	return False

def ismaxmoveValidForMin(item, minpositions):
	row = item[0]
	col = item[1]
	if (row >= 0 and col>=0 and row<HEIGHT and col<WIDTH):
		if ((row, col) in minpositions):
			return False
		return True
	return False


def defensiveheuristic(curstate, ismaxplayer):
	num_remaining = 0
	if (ismaxplayer):
		num_remaining = len(curstate.maxpositions) 
	else:
		num_remaining = len(curstate.minpositions)
	score =  2*(num_remaining) + random.random()
	return score

def defensiveheuristic2(curstate, ismaxplayer):
	num_remaining = 0
	if (ismaxplayer):
		num_remaining = len(curstate.maxpositions) 
	else:
		num_remaining = len(curstate.minpositions)
	num_covered = 0
	hash_covered = [False] * WIDTH
	if (ismaxplayer):
		for item in curstate.maxpositions.keys():
			row = item[0]
			col = item[1]
			hash_covered[col] = True
		for i in range(8):
			if (hash_covered[i] == True):
				num_covered = num_covered + 1

	if (ismaxplayer == False):
		for item in curstate.minpositions.keys():
			row = item[0]
			col = item[1]
			hash_covered[col] = True
		for i in range(8):
			if (hash_covered[i] == True):
				num_covered = num_covered + 1
	score =  2 * (num_remaining) + 3 * num_covered + random.random()
	return score

def offensiveheuristic(curstate, ismaxplayer):
	num_remaining = 0
	if (ismaxplayer==False):
		num_remaining = len(curstate.maxpositions) 
	else:
		num_remaining = len(curstate.minpositions)
	score =  2*(30 - num_remaining) + random.random()
	return score


########################################################################################################################################
########################################################################################################################################


def calulateScoreMaxHeuristic(curstate):
	 return defensiveheuristic2(curstate, True)
	# offensiveheuristic(curstate, ismaxplayer)


def getLevel3MaxScore(curstate):
	maxscore = -1
	maxstate = State()
	testbool = False
	for key in curstate.maxpositions.iterkeys():
		row = key[0]
		col = key[1]
		for i in range(3):
			nextrow = row + 1
			nextcol = col + movesx[i]
			if (ismaxmoveValidForMax((nextrow, nextcol), curstate.maxpositions.keys())):
				newstate = State()
				if (i == 1 and (nextrow, nextcol) in curstate.minpositions):
					continue
				if (nextrow == HEIGHT - 1 or len(curstate.minpositions) == 0):
					curscore = 1 * float("inf")
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = newstate
				elif ((nextrow, nextcol) in curstate.minpositions):
					newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
					newstate.minpositions = copy.deepcopy(curstate.minpositions)
					del newstate.minpositions[(nextrow, nextcol)]
					del newstate.maxpositions[(row, col)]
					newstate.maxpositions[(nextrow, nextcol)] = True
					if (len(curstate.minpositions) == 0):
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
					newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
					newstate.minpositions = copy.deepcopy(curstate.minpositions)
					del newstate.maxpositions[(row, col)]
					newstate.maxpositions[(nextrow, nextcol)] = True
					curscore = calulateScoreMaxHeuristic(newstate)
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = newstate
	# if (testbool == False):
	# 	print('testbool is false for max level 3')
	return maxscore

def getMinMoveAfterMaxScore(curstate):
	minscore = 1000000
	minstate = State()
	testbool = False
	for key in curstate.minpositions.iterkeys():
		row = key[0]
		col = key[1]
		for i in range(3):
			nextrow = row - 1
			nextcol = col + movesx[i]
			if (ismaxmoveValidForMin((nextrow, nextcol), curstate.minpositions.keys())):
				newstate = State()
				if (i == 1 and (nextrow, nextcol) in curstate.maxpositions):
					continue
				if (nextrow == 0 or len(curstate.maxpositions) == 0):
						curscore = -1 * float("inf")
						if (curscore < minscore):
							minscore = curscore
							minstate = newstate
				elif ((nextrow, nextcol) in curstate.maxpositions):
					newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
					newstate.minpositions = copy.deepcopy(curstate.minpositions)
					del newstate.maxpositions[(nextrow, nextcol)]
					del newstate.minpositions[(row, col)]
					newstate.minpositions[(nextrow, nextcol)] = True
					if (len(curstate.maxpositions) == 0):
						curscore = -1 * float("inf")
						if (curscore < minscore):
							minscore = curscore
							minstate = newstate
					else:
						curscore = getLevel3MaxScore(newstate)
						if (curscore < minscore):
							minscore = curscore
							minstate = newstate
				else:
					newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
					newstate.minpositions = copy.deepcopy(curstate.minpositions)
					del newstate.minpositions[(row, col)]
					newstate.minpositions[(nextrow, nextcol)] = True
					curscore = getLevel3MaxScore(newstate)
					if (curscore == -1):
						continue
					if (curscore < minscore):
						minscore = curscore
						minstate = newstate
	# if (testbool == False):
	# 	print('testbool is false for max layer 2')
	return minscore

def getNextMaxMoveState(curstate):
	maxscore = -1
	maxstate = State()
	testbool = False
	for key in curstate.maxpositions.iterkeys():
		row = key[0]
		col = key[1]
		for i in range(3):
			nextrow = row + 1
			nextcol = col + movesx[i]
			if (ismaxmoveValidForMax((nextrow, nextcol), curstate.maxpositions.keys())):
				testbool = True
				newstate = State()
				newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
				newstate.minpositions = copy.deepcopy(curstate.minpositions)
				if (i == 1 and (nextrow, nextcol) in curstate.minpositions):
					continue
				if (nextrow == HEIGHT - 1 or len(curstate.minpositions) == 0):
					gameOver = True
					print('Game over winner is Max')
					return State()
				elif ((nextrow, nextcol) in curstate.minpositions):
					print('Max captures min player')
					newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
					newstate.minpositions = copy.deepcopy(curstate.minpositions)
					del newstate.minpositions[(nextrow, nextcol)]
					del newstate.maxpositions[(row, col)]
					newstate.maxpositions[(nextrow, nextcol)] = True
					if (len(curstate.minpositions) == 0):
						gameOver = True
						print('Game over winner is Max2')
						return State()
					curscore = getMinMoveAfterMaxScore(newstate)
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = newstate
				else:
					newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
					newstate.minpositions = copy.deepcopy(curstate.minpositions)
					del newstate.maxpositions[(row, col)]
					newstate.maxpositions[(nextrow, nextcol)] = True
					curscore = getMinMoveAfterMaxScore(newstate)
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


def getLevel3MinScore(curstate):
	maxscore = -1
	maxstate = State()
	testbool = False
	for key in curstate.minpositions.iterkeys():
		row = key[0]
		col = key[1]
		for i in range(3):
			nextrow = row - 1
			nextcol = col + movesx[i]
			if (ismaxmoveValidForMin((nextrow, nextcol), curstate.minpositions.keys())):
				newstate = State()
				if (i == 1 and (nextrow, nextcol) in curstate.maxpositions):
					continue

				if (nextrow == 0 or len(curstate.maxpositions) == 0):
					curscore = float("inf")
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = newstate

				elif ((nextrow, nextcol) in curstate.maxpositions):
					newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
					newstate.minpositions = copy.deepcopy(curstate.minpositions)
					del newstate.maxpositions[(nextrow, nextcol)]
					del newstate.minpositions[(row, col)]
					newstate.minpositions[(nextrow, nextcol)] = True
					if (len(curstate.maxpositions) == 0):
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
					
					newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
					newstate.minpositions = copy.deepcopy(curstate.minpositions)
					del newstate.minpositions[(row, col)]
					newstate.minpositions[(nextrow, nextcol)] = True
					curscore = calulateScoreMinHeuristic(newstate)
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = newstate
	# if (testbool == False):
	# 	print('testbool is false for min layer 3')
	return maxscore

def getMaxMoveAfterMinScore(curstate):
	minscore = 1000000
	minstate = State()
	testbool = False
	for key in curstate.maxpositions.iterkeys():
		row = key[0]
		col = key[1]
		for i in range(3):
			nextrow = row + 1
			nextcol = col + movesx[i]
			if (ismaxmoveValidForMax((nextrow, nextcol), curstate.maxpositions.keys())):
				newstate = State()
				if (i == 1 and (nextrow, nextcol) in curstate.minpositions):
					continue

				if (nextrow == HEIGHT - 1 or len(curstate.minpositions) == 0):
					curscore = -float("inf")
					if (curscore < minscore):
						minscore = curscore
						minstate = newstate

				elif ((nextrow, nextcol) in curstate.minpositions):
					newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
					newstate.minpositions = copy.deepcopy(curstate.minpositions)
					del newstate.minpositions[(nextrow, nextcol)]
					del newstate.maxpositions[(row, col)]
					newstate.maxpositions[(nextrow, nextcol)] = True
					if (len(curstate.minpositions) == 0):
						curscore = -float("inf")
						if (curscore < minscore):
							minscore = curscore
							minstate = newstate
					else:
						curscore = getLevel3MinScore(newstate)
						if (curscore < minscore):
							minscore = curscore
							minstate = newstate
				else:
					newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
					newstate.minpositions = copy.deepcopy(curstate.minpositions)
					del newstate.maxpositions[(row, col)]
					newstate.maxpositions[(nextrow, nextcol)] = True
					curscore = getLevel3MinScore(newstate)
					if (curscore == -1):
						continue
					if (curscore < minscore):
						minscore = curscore
						minstate = newstate
	# if (testbool == False):
	# 	print('testbool is false for min layer 2')
	return minscore

def getNextMinMoveState(curstate):
	maxscore = -1
	maxstate = State()
	testbool = False
	for key in curstate.minpositions.iterkeys():
		row = key[0]
		col = key[1]
		for i in range(3):
			nextrow = row - 1
			nextcol = col + movesx[i]
			if (ismaxmoveValidForMin((nextrow, nextcol), curstate.minpositions.keys())):
				testbool = True
				newstate = State()
				newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
				newstate.minpositions = copy.deepcopy(curstate.minpositions)
				if (i == 1 and (nextrow, nextcol) in curstate.maxpositions):
					continue
				if (nextrow == 0 or len(curstate.maxpositions) == 0):
					gameOver = True
					print('Game over winner is Min')
					print(curstate.minpositions)
					return State()
				elif ((nextrow, nextcol) in curstate.maxpositions):
					print('Min captures max player')

					newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
					newstate.minpositions = copy.deepcopy(curstate.minpositions)
					del newstate.maxpositions[(nextrow, nextcol)]
					del newstate.minpositions[(row, col)]
					newstate.minpositions[(nextrow, nextcol)] = True
					if (len(curstate.maxpositions) == 0):
						gameOver = True
						print('Game over winner is Min2')
						print(curstate.minpositions)
						return State()
					curscore = getMaxMoveAfterMinScore(newstate)
					if (curscore > maxscore):
						maxscore = curscore
						maxstate = newstate
				else:
					newstate.maxpositions = copy.deepcopy(curstate.maxpositions)
					newstate.minpositions = copy.deepcopy(curstate.minpositions)
					del newstate.minpositions[(row, col)]
					newstate.minpositions[(nextrow, nextcol)] = True
					curscore = getMaxMoveAfterMinScore(newstate)
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
	for item in curstate.maxpositions.keys():
		r = item[0]
		c = item[1]
		data[r][c] = 'a'

	for item in curstate.minpositions.keys():
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
			initState.maxpositions[(i, j)] = True
	for i in range(WIDTH - 2, WIDTH):
		for j in range(HEIGHT):
			initState.minpositions[(i, j)] = True

	printstate(initState)
	minmovestate = copy.deepcopy(initState)
	maxmovestate = copy.deepcopy(initState)
	counter = 0
	while (gameOver == False):
		counter = counter + 1
		print('MinMove')
		minmovestate = getNextMinMoveState(copy.deepcopy(maxmovestate))
		printstate(minmovestate)
		if (len(minmovestate.maxpositions) == 0):
			print('reached break condition 1')
			print(minmovestate.minpositions)
			break
		print('MaxMove')
		maxmovestate = getNextMaxMoveState(copy.deepcopy(minmovestate))
		printstate(maxmovestate)
		if (len(maxmovestate.maxpositions) == 0):
			print('reached break condition 3')
			print(maxmovestate.minpositions)
			break
		if (counter == 100):
			break
		print('counter ', counter, ' Max positions len ', len(maxmovestate.maxpositions), ' Min positions len ', len(maxmovestate.minpositions))
		
if __name__ == "__main__":
    main()



