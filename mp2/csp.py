import copy
import random
import sys
board = []
colors = set()
listcolors = []
num_colors = 0
WIDTH = 5
HEIGHT = 5
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
			if (c != '_' and c!='\r'):
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
	#colors.remove('\r')
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
	return True


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
	if (checkAdjConstraint(temp, pos, value) == False):
		return False
	if (checkSpurs(temp, pos, value) == False):
		return False
	if (checkZigZags(temp, pos, value) == False):
		return False
	if (checkSourcesInflux(temp) == False):
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
	if (checkconsistency(temp, pos, value) == False):
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
		temp[row][col] = value

		rowNum = [-1, 0, 0, 1, -1, -1, 1, 1]
		colNum = [0, -1, 1, 0, 1, -1, 1, -1]
		for j in range(8):
			newrow = row + rowNum[j]
			newcol = col + colNum[j]
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
		for j in range(8):
			newrow = row + rowNum[j]
			newcol = col + colNum[j]
			if (isValid(newrow, newcol) and temp[newrow][newcol] == '_'):
				cur = cur + checkconstraints(temp, (newrow, newcol))
		if (cur < curmax):
			curmax = cur
			bestindex = i
		return varlist[bestindex]


def getnextvar(temp, num_colors_remaining):
	curmax = 100000
	temp1 = 10000
	varlist = []
	for i in range(HEIGHT):
		for j in range(WIDTH):
			if (num_colors_remaining[i][j] != 0 and num_colors_remaining[i][j] <= curmax):
				temp1 = num_colors_remaining[i][j]
				if (temp1 != curmax):
					curmax = temp1
					varlist[:] = []
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
			newrow = currow + rowNum[i]
			newcol = curcol + colNum[i]
			if (isValid(newrow, newcol) and temp[newrow][newcol] == value):
				temp[newrow][newcol] = '*'
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
	for i in range(len(listcolors)):
		if (isContinuous(temp, i) == False):
			return False
	return True


def updateRemainingColors(pos, temp_colors, temp_num):
	row = pos[0]
	col = pos[1]
	temp_colors[row][col][:] = []
	temp_num[row][col] = 0

	rowNum = [-1, 0, 0, 1, -1, -1, 1, 1]
	colNum = [0, -1, 1, 0, 1, -1, 1, -1]
	for i in range(8):
		newrow = row + rowNum[i]
		newcol = col + colNum[i]
		if (isValid(newrow, newcol)):
			temp2 = list(temp_colors[newrow][newcol])
			for j in range(len(temp2)):
				value = temp2[j]
				if (checkconsistency(board, (newrow, newcol), value) == False):
					temp_colors[newrow][newcol].remove(value)
					temp_num[newrow][newcol] -= 1
	return

def initializecolorlist(temp):
	for i in range(HEIGHT):
		for j in range(WIDTH):
			if (temp[i][j] == '_'):
				for value in listcolors:
					if (checkconsistency(temp, (i, j), value)):
						remaining_colors[i][j].append(value)
						num_remaining[i][j] += 1


def backtrack(board, remcolor, remnum):
	if (isComplete()):
		return board
	temp = copy.deepcopy(board)
	var = getnextvar(board, remnum)
	if (var == None):
		print('full failiure')
		return False
	row = var[0]
	col = var[1]
	while (len(remcolor[row][col]) != 0):
		value = getLeastConstrainingValue(remcolor, (row, col))
		remcolor[row][col].remove(value)
		if (checkStrongConsistency(board, (row, col), value)):
			board[row][col] = value
			tempremcolor = copy.deepcopy(remcolor)
			tempremnum = copy.deepcopy(remnum)
			updateRemainingColors((row, col), tempremcolor, tempremnum)
			if (forwardChecking(tempremnum)):
				result = backtrack(board, tempremcolor, tempremnum)
				if (result):
					return result
				else:
					board[row][col] = '_'
			else:
				board[row][col] = '_'
	return False



def main():
	initialize()
	printboard()
	WIDTH = len(board)
	HEIGHT = len(board[0])
	initializecolorlist(board)
	print(backtrack(board, remaining_colors, num_remaining))
	printboard()


if __name__ == "__main__":
    main()
