import copy
import random
import sys
board = []
colors = set()
listcolors = []
num_colors = 0
WIDTH = 0
HEIGHT = 0
filename = "input55.txt"
remaining_colors = []
num_remaining = []
colorPoints = []

def initialize():
	nr = 0
	nc = 0
	file = open(filename, 'r')
	board[:] = []
	board.append([])

	while(True):
		c = file.read(1)
		if (not c):
			break
		if (c != '\n'):
			board[nr].append(c)
			if (c != '_'):
				if (c not in colors):
					colors.add(c)
					listcolors.append(c)
					colorPoints.append([])
					colorPoints[len(colorPoints) - 1].append((nr, nc))
				else:
					
					colorPoints[listcolors.index(c)].append((nr, nc))
			nc = nc + 1
		else:
			WIDTH = nc
			nc = 0
			nr = nr + 1
			board.append([])
	HEIGHT = nr
	file.close()
	colors.remove('\r')
	num_colors = len(colors)
	for item in board:
		if (len(item) == 6):
			del item[-1]
	WIDTH = len(board)
	HEIGHT = len(board[0])

	for i in range(HEIGHT):
		remaining_colors.append([])
		num_remaining.append([])

	for i in range(HEIGHT):
		for j in range(WIDTH):
			remaining_colors[j].append([])
			num_remaining[j].append([])

	for i in range(HEIGHT):
		for j in range(WIDTH):
			num_remaining[i][j] = 0
	return





def printboard():
	for item in board:
		print ''.join(item)

# def findMostConstrainedVariable():
# 	temp = copy.deepcopy(board)
# 	for i in range(HEIGHT):
# 		for j in range(WIDTH):
# 			if (temp[i][j] == '_'):
# 				for item in colors:
# 					if (consistencycheck(temp, (i, j), val)):


def isValid(row, col):
	if (row < 0 or row > HEIGHT - 1):
		return False
	if (col <0 or col > WIDTH - 1):
		return False
	return True


def checkAdjConstraint(temp, pos, value):
	row = pos[0]
	col = pos[1]
	rowNum = [-1, 0, 0, 1]
	colNum = [0, -1, 1, 0]
	numsame = 0
	numfree = 0
	for i in range(4):
		newrow = row + rowNum[i]
		newcol = col + colNum[i]
		if (isValid(newrow, newcol)):
			if (temp[newrow][newcol] == value):
				numsame = numsame + 1
			if (temp[newrow][newcol] == '_'):
				numfree = numfree + 1
	if (numsame > 2):
		return False
	index = listcolors.index(value)
	if (pos != colorPoints[index][0] and  pos != colorPoints[index][1]):
		if (numsame == 0 and numfree < 2):
			return False
		if (numsame == 1 and numfree < 1):
			return False
		if (numfree==0 and numsame!=2):
			return False
	return True



def checkSpurs(temp, pos, value):
	row = pos[0]
	col = pos[1]
	if (isValid(row, col) == False):
		return False
	if (isValid(row - 1, col -1) and isValid(row, col + 1)):
		if (temp[row - 1][col - 1] == value and temp[row - 1][col] == value and temp[row - 1][col + 1] == value):
			return False
	if (isValid(row + 1, col - 1) and isValid(row + 1, col + 1)):
		if (temp[row + 1][col - 1] == value and temp[row + 1][col] == value and temp[row + 1][col + 1] == value):
			return False
	if (isValid(row + 1, col + 1) and isValid(row - 1, col + 1)):
		if (temp[row + 1][col + 1] == value and temp[row][col + 1] == value and temp[row - 1][col + 1] == value):
			return False
	if (isValid(row + 1, col - 1) and isValid(row - 1, col - 1)):
		if (temp[row + 1][col - 1] == value and temp[row][col - 1] == value and temp[row - 1][col - 1] == value):
			return False
	return False


def checkZigZags(temp, pos, value):
	row = pos[0]
	col = pos[1]
	if (isValid(row, col) == False):
		return False
	rowNum = [-1, -1, 1, 1]
	colNum = [1, -1, 1, -1]
	if (isValid(row - 1, col) and isValid(row, col + 1)):
		if temp[row - 1][col] == value and temp[row][col + 1] == value and temp[row - 1][col + 1] == value:
		    return False

	if (isValid(row - 1, col) and isValid(row, col - 1)):
		if temp[row - 1][col] == value and temp[row][col - 1] == value and temp[row - 1][col - 1] == value:
		    return False

	if (isValid(row + 1, col) and isValid(row, col + 1)):
		if temp[row + 1][col] == value and temp[row][col + 1] == value and temp[row + 1][col + 1] == value:
		    return False

	if (isValid(row + 1, col) and isValid(row, col - 1)):
		if temp[row + 1][col] == value and temp[row][col - 1] == value and temp[row + 1][col - 1] == value:
			return False

	return True


def checkSourcesInflux(temp):
	for i in range(len(listcolors)):
		value = listcolors[i]
		pos = colorPoints[i]
		sourcerow = pos[0][0]
		sourcecol = pos[0][1]
		destrow = pos[1][0]
		destcol = pos[1][1]
		rowNum = [-1, 0, 0, 1]
		colNum = [0, -1, 1, 0]
		sourceinflux = 0
		destinflux = 0
		for i in range(4):
			newrow = sourcerow + rowNum[i]
			newcol = sourcecol + colNum[i]
			if (isValid(newrow, newcol)):
				if (temp[newrow][newcol] == value):
					sourceinflux = sourceinflux + 1

			newrow = destrow + rowNum[i]
			newcol = destcol + colNum[i]
			if (isValid(newrow, newcol)):
				if (temp[newrow][newcol] == value):
					destinflux = destinflux + 1

			if (sourceinflux > 1 or destinflux > 1):
				return False
	return True

def checkconsistency(temp, pos, value):
	if (checkAdjConstraint == False or checkSpurs == False or checkZigZags == False or checkSourcesInflux == False):
		return False
	return True


def checkconstraints(temp, pos):
	num = 0
	row = pos[0]
	col = pos[1]
	for i in range(len(remaining_colors[row][col])):
		value = remaining_colors[row][col][i]
		if (checkconsistency(temp, pos, value)):
			num = num + 1
	return num


def checkarea(temp, pos):
	row = pos[0]
	col = pos[1]
	rowNum = [-1, 0, 0, 1, -1, -1, 1, 1]
	colNum = [0, -1, 1, 0, 1, -1, 1, -1]
	for i in range(8):
		newrow = row + rowNum[i]
		newcol = col + colNum[i]
		if (isValid(newrow, newcol) and temp[newrow][newcol] != '_'):
			value = temp[newrow][newcol]
			if (checkconsistency(temp, (newrow, newcol), value) == False):
				return False
	return True

def checkStrongConsistency(temp, pos, value):
	if (checkconsistency(temp, pos, value)):
		return False
	temp2 = copy.deepcopy(temp)
	temp2[pos[0]][pos[1]] = value
	if (checkarea(temp2, pos) == False):
		return False
	return True


def getLeastConstrainingValue(temp_remaining_colors, pos):
	curmin = -1
	bestindex = -1
	cur = 0
	row = pos[0]
	col = pos[1]
	for i in range(len(temp_remaining_colors[row][col])):
		value = temp_remaining_colors[row][col][i]
		temp = copy.deepcopy(board)
		temp[row][col] = val

		rowNum = [-1, 0, 0, 1, -1, -1, 1, 1]
		colNum = [0, -1, 1, 0, 1, -1, 1, -1]
		for i in range(8):
			newrow = row + rowNum[i]
			newcol = col + colNum[i]
			if (isValid(newrow, newcol) and temp[newrow][newcol] == '_'):
				cur = cur + checkconstraints(temp, (newrow, newcol))

		if (cur > curmin):
			curmin = cur
			bestindex = i

	return temp_remaining_colors[row][col][bestindex]


def getMostConstrainingVariable(temp, varlist):
	curmax = 1000
	bestindex = -1
	cur = 0
	for i in range(len(varlist)):
		row = varlist[i][0]
		col = varlist[i][1]

		rowNum = [-1, 0, 0, 1, -1, -1, 1, 1]
		colNum = [0, -1, 1, 0, 1, -1, 1, -1]
		for i in range(8):
			newrow = row + rowNum[i]
			newcol = col + colNum[i]
			if (isValid(newrow, newcol) and temp[newrow][newcol] == '_'):
				cur = cur + checkconstraints(temp, (newrow, newcol))

		if (cur < curmax):
			curmax = cur
			bestindex = i
	return varlist[bestindex]


def getnextvar(temp, num_colors_remaining):
	curmax = 100000
	temp = 10000
	varlist = []
	for i in range(HEIGHT):
		for j in range(WIDTH):
			if (num_colors_remaining[i][j] != 0 and num_colors_remaining <= curmax):
				temp = num_colors_remaining[i][j]
				if (temp != curmax):
					curmax = temp
				varlist.append((i, j))
	return getMostConstrainingVariable(temp, varlist)


def forwardChecking(num_colors_remaining):
	for i in range(HEIGHT):
		for j in range(WIDTH):
			if (board[i][j] == '_' and num_colors_remaining[i][j] == 0):
				return False
	return True



def isContinuous(temp, colorindex):
	value = listcolors[colorindex]
	pos = colorPoints[colorindex]
	sourcerow = pos[0][0]
	sourcecol = pos[0][1]
	destrow = pos[1][0]
	destcol = pos[1][1]
	currow = sourcerow
	curcol = sourcecol
	temp[currow][curcol] = '*'
	while(1):
		rowNum = [-1, 0, 0, 1]
		colNum = [0, -1, 1, 0]
		flag = False
		for i in range(4):
			newrow = currow + newrow[i]
			newcol = curcol + newcol[i]
			if (isValid(newrow, newcol) and temp[newrow][newcol] == value):
				temp[newrow][newcol] == '*'
				flag = True
				currow = newrow
				curcol = newcol
				break
		if (flag == False):
			return False
		if (currow == destrow and curcol == destcol):
			break
	return True

def isComplete():
	for i in range(HEIGHT):
		for j in range(WIDTH):
			if (board[i][j] == '_'):
				return False
	temp = copy.deepcopy(board)
	for i in len(listcolors):
		if (isContinuous(temp, i) == False):
			return False
	return True


def main():
	initialize()
	printboard()


if __name__ == "__main__":
    main()
