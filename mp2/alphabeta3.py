import copy
import random
import sys
import time


WIDTH = 8
HEIGHT = 8

numExpandedPlayer1 = [0]
numExpandedPlayer2 = [0]
player1Time = 0
player2Time = 0
counter = 0

# WIDTH = 5
# HEIGHT = 10

movesx = [-1, 0, 1]

gameOver = False


class State:
	def __init__(self):
		self.player1positions = {}
		self.player2positions = {}
		self.score = -1
		self.numPlayer1row = 0
		self.numPlayer2row = 0


def ismoveValidforPlayer1(item, player1positions):
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


def offensiveheuristic2(curstate, isplayer1):
	num_remaining = 0
	num_opponent_remaining = 0
	if (isplayer1==False):
		num_opponent_remaining = len(curstate.player1positions)
		num_remaining = len(curstate.player2positions)
	else:
		num_opponent_remaining = len(curstate.player2positions)
		num_remaining = len(curstate.player1positions)

	num_covered = 0
	hash_covered = [False] * WIDTH
	min_distance = 0 
	numInOpponentRow = 0
	if (isplayer1 == False):
		for item in curstate.player1positions.keys():
			row = item[0]
			col = item[1]
			hash_covered[col] = True
		for i in range(8):
			if (hash_covered[i] == True):
				num_covered = num_covered + 1

		min_distance = 16
		for item in curstate.player2positions.keys():
			row = item[0]
			col = item[1]
			distance = row
			if (distance != 0):
				min_distance = min(distance, min_distance)
			else:
				numInOpponentRow += 1

		# for item in curstate.player2positions.keys():
		# 	row = item[0]
		# 	col = item[1]


	if (isplayer1):
		for item in curstate.player2positions.keys():
			row = item[0]
			col = item[1]
			hash_covered[col] = True
		for i in range(8):
			if (hash_covered[i] == True):
				num_covered = num_covered + 1

		for item in curstate.player1positions.keys():
			row = item[0]
			col = item[1]
			distance = abs(HEIGHT - 1 - row)
			if (distance != 0):
				min_distance = min(distance, min_distance)
			else:
				numInOpponentRow += 1

	score =  2 * (30 - min_distance) + (2 * num_remaining) + (20 * numInOpponentRow) + random.random()
	return score

def offensiveheuristic(curstate, isplayer1):
	num_remaining = 0
	if (isplayer1==False):
		num_remaining = len(curstate.player1positions) 
	else:
		num_remaining = len(curstate.player2positions)
	score =  2*(30 - num_remaining) + random.random()
	return score



def calulateScorePlayer1Heuristic(curstate):
	 return offensiveheuristic2(curstate, True)

def calulateScorePlayer2Heuristic(curstate):
	 return -1 * defensiveheuristic2(curstate, False)


def alphabeta(curstate, isPlayer1, alpha, beta, curdepth, maxdepth, Player1Heuristic):
	

	if (curdepth == maxdepth):
		if(Player1Heuristic):
			return calulateScorePlayer1Heuristic(curstate), copy.deepcopy(curstate)
		else:
			return calulateScorePlayer2Heuristic(curstate), copy.deepcopy(curstate)

	if (Player1Heuristic):
		numExpandedPlayer1[0] += 1
	elif (Player1Heuristic == False):
		numExpandedPlayer2[0] += 1


	isbreak = False
	if (isPlayer1):
		bestVal = -1 * float("inf")
		bestState = copy.deepcopy(curstate)
		testbool = False
		if (len(curstate.player2positions) == 0):
			print ('Zero length for player1')
			print(curdepth)
		for key in curstate.player1positions.iterkeys():
			row = key[0]
			col = key[1]
			for i in range(3):
				nextrow = row + 1
				nextcol = col + movesx[i]
				if (ismoveValidforPlayer1((nextrow, nextcol), curstate.player1positions.keys())):
					testbool = True
					newstate = State()
					newstate.player1positions = copy.deepcopy(curstate.player1positions)
					newstate.player2positions = copy.deepcopy(curstate.player2positions)
					newstate.numPlayer1row = curstate.numPlayer1row
					newstate.numPlayer2row = curstate.numPlayer2row
					if (i == 1 and (nextrow, nextcol) in curstate.player2positions):
						continue
					if ((nextrow == HEIGHT - 1 and curstate.numPlayer2row >= 2) or len(curstate.player2positions) == 0):
						if (curdepth == 0):
							print('Game over winner is Player1')
							print('Number of nodes expanded by Player1 is ', numExpandedPlayer1[0])
							print('Number of nodes expanded by Player2 is ', numExpandedPlayer2[0])
							print('Total time for moves for player 1 is ', player1Time)
							print('Total time for moves for player 2 is ', player2Time)
							sys.exit()
						else:
							curscore = float("inf")
							newstate.numPlayer2row += 1
							if (curscore > bestVal):
								bestVal = curscore
								bestState = copy.deepcopy(newstate)
								alpha = max(alpha, bestVal)
								if beta <= alpha:
									isbreak = True
									break

					elif ((nextrow, nextcol) in curstate.player2positions):
						#print('Player1 captures Player 2 player')
						newstate.player1positions = copy.deepcopy(curstate.player1positions)
						newstate.player2positions = copy.deepcopy(curstate.player2positions)
						del newstate.player2positions[(nextrow, nextcol)]
						del newstate.player1positions[(row, col)]
						newstate.player1positions[(nextrow, nextcol)] = True

						if (nextrow == HEIGHT - 1):
							newstate.numPlayer2row += 1
						if (len(curstate.player2positions) == 0):
							if (curdepth == 0):
								print('Game over winner is Player1')
								print('Number of nodes expanded by Player1 is ', numExpandedPlayer1[0])
								print('Number of nodes expanded by Player2 is ', numExpandedPlayer2[0])
								print('Total time for moves for player 1 is ', player1Time)
								print('Total time for moves for player 2 is ', player2Time)
								sys.exit()
							else:
								curscore = float("inf")
								if (curscore > bestVal):
									bestVal = curscore
									bestState = copy.deepcopy(newstate)
									alpha = max(alpha, bestVal)
									if beta <= alpha:
										isbreak = True
										break
						else:
							curscore, stateresult = alphabeta(newstate, False, alpha, beta, curdepth + 1, maxdepth, Player1Heuristic)
							if (curscore > bestVal):
									frompos = (row, col)
									topos = (nextrow, nextcol)
									bestVal = curscore
									bestState = copy.deepcopy(newstate)
									alpha = max(alpha, bestVal)
									if beta <= alpha:
										isbreak = True
										break
					else:
						newstate.player1positions = copy.deepcopy(curstate.player1positions)
						newstate.player2positions = copy.deepcopy(curstate.player2positions)
						del newstate.player1positions[(row, col)]
						newstate.player1positions[(nextrow, nextcol)] = True
						if (nextrow == HEIGHT - 1):
							newstate.numPlayer2row += 1
						curscore, stateresult = alphabeta(newstate, False, alpha, beta, curdepth + 1, maxdepth, Player1Heuristic)
						if (curscore > bestVal):
							frompos = (row, col)
							topos = (nextrow, nextcol)
							bestVal = curscore
							bestState = copy.deepcopy(newstate)
							alpha = max(alpha, bestVal)
							if beta <= alpha:
								isbreak = True
								break
			if (isbreak):
				isbreak = False
				break
		return bestVal, bestState

	else:
		bestVal = float("inf")
		bestState = copy.deepcopy(curstate)
		testbool = False
		if (len(curstate.player2positions) == 0):
			print ('Zero length for player2')
			print(curdepth)
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
					newstate.numPlayer1row = curstate.numPlayer1row
					newstate.numPlayer2row = curstate.numPlayer2row
					if (i == 1 and (nextrow, nextcol) in curstate.player1positions):
						continue
					if ((nextrow == 0 and curstate.numPlayer1row >= 2) or len(curstate.player1positions) == 0):
						if (curdepth == 0):
							print('Game over winner is Player2')
							print('Number of nodes expanded by Player1 is ', numExpandedPlayer1[0])
							print('Number of nodes expanded by Player2 is ', numExpandedPlayer2[0])
							print('Total time for moves for player 1 is ', player1Time)
							print('Total time for moves for player 2 is ', player2Time)
							sys.exit()
						else:
							curscore = -1 * float("inf")
							if (curscore < bestVal):
								bestVal = curscore
								bestState = copy.deepcopy(newstate)
								beta = min(beta, bestVal)
								if beta <= alpha:
									isbreak = True
									break
					elif ((nextrow, nextcol) in curstate.player1positions):
						#print('Min captures max player')
						newstate.player1positions = copy.deepcopy(curstate.player1positions)
						newstate.player2positions = copy.deepcopy(curstate.player2positions)
						del newstate.player1positions[(nextrow, nextcol)]
						del newstate.player2positions[(row, col)]
						newstate.player2positions[(nextrow, nextcol)] = True
						if (nextrow == 0):
							newstate.numPlayer1row += 1
						if (len(curstate.player1positions) == 0):
							if (curdepth == 0):
								print('Game over winner is Player2')
								print('Number of nodes expanded by Player1 is ', numExpandedPlayer1[0])
								print('Number of nodes expanded by Player2 is ', numExpandedPlayer2[0])
								print('Total time for moves for player 1 is ', player1Time)
								print('Total time for moves for player 2 is ', player2Time)
								sys.exit()
							else:
								curscore = -1 * float("inf")
								if (curscore < bestVal):
									bestVal = curscore
									bestState = copy.deepcopy(newstate)
									beta = min(beta, bestVal)
									if beta <= alpha:
										isbreak = True
										break
						else:
							curscore, stateresult = alphabeta(newstate, True, alpha, beta, curdepth + 1, maxdepth, Player1Heuristic)
							if (curscore < bestVal):
								frompos = (row, col)
								topos = (nextrow, nextcol)
								bestVal = curscore
								bestState = copy.deepcopy(newstate)
								beta = min(beta, bestVal)
								if beta <= alpha:
									isbreak = True
									break
					else:
						newstate.player1positions = copy.deepcopy(curstate.player1positions)
						newstate.player2positions = copy.deepcopy(curstate.player2positions)
						del newstate.player2positions[(row, col)]
						newstate.player2positions[(nextrow, nextcol)] = True
						if (nextrow == 0):
							newstate.numPlayer1row += 1
						curscore, stateresult = alphabeta(newstate, True, alpha, beta, curdepth + 1, maxdepth, Player1Heuristic)
						if (curscore < bestVal):
							frompos = (row, col)
							topos = (nextrow, nextcol)
							bestVal = curscore
							bestState = copy.deepcopy(newstate)
							beta = min(beta, bestVal)
							if beta <= alpha:
								isbreak = True
								break
			if (isbreak):
				isbreak = False
				break
		return bestVal, bestState



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


def diff1(oldarray, newarray):
	dict = {}
	for item in oldarray:
		dict[item] = True
	count = 0
	for item in newarray:
		if (item not in dict):
			count = count + 1
	if (count > 1):
		return False
	return True


def main():
	initState = State()
	for i in range(2):
		for j in range(WIDTH):
			initState.player1positions[(i, j)] = True
	for i in range(HEIGHT - 2, HEIGHT):
		for j in range(WIDTH):
			initState.player2positions[(i, j)] = True

	printstate(initState)
	player2movestate = copy.deepcopy(initState)
	player1movestate = copy.deepcopy(initState)

	# testscore, teststate = alphabeta(initState, True, -1 * float("inf"), float("inf"), 0, 3, True)
	# printstate(teststate)

	while (gameOver == False):
		global counter
		global player2Time
		global player1Time
		counter += 1
		start_time = time.time()
		score, player1movestate = alphabeta(player2movestate, True, -1 * float("inf"), float("inf"), 0, 3, True)
		player1Time += (time.time() - start_time)
		printstate(player1movestate)
		if (len(player1movestate.player1positions) == 0):
			print('reached break condition 1')
			break
		start_time = time.time()
		score, player2movestate = alphabeta(player1movestate, False, -1 * float("inf"), float("inf"), 0, 3, False)
		player2Time += (time.time() - start_time)
		printstate(player2movestate)
		if (len(player2movestate.player1positions) == 0):
			print('reached break condition 3')
			break
		if (counter == 100):
			break
		print('counter ', counter, ' Player1 positions len ', len(player2movestate.player1positions), ' Player2 positions len ', len(player2movestate.player2positions), ' Num in Player 1 row ', player2movestate.numPlayer1row, ' Num in Player 2 row ', player2movestate.numPlayer2row)


if __name__ == "__main__":
    main()
