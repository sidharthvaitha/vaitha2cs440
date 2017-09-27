from array import array
from collections import deque
import Queue as Q


def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)

def writemazetofileastar(data, endi, endj, starti, startj, camefrom):
	curr = (endi, endj)
	duplicate = data
	while True:
		prev = camefrom[(curr[0], curr[1])]
		if (data[prev[0]][prev[1]] == '%'):
			print("Error")
		if (prev == (starti, startj)):
			break;
		strlist = list(duplicate[prev[0]])
		strlist[prev[1]] = 'a'
		duplicate[prev[0]] = "".join(strlist)
		curr = (prev[0], prev[1])
	numrows = len(data)
	writefile = open('output2.txt', 'w')
	for line in duplicate:
		writefile.write(line)
		writefile.write('\n')
	writefile.close()


def isComplete(destinations, boxes):
	for item in destinations:
		if (item not in boxes):
			return False
	return True

def computeheuristic(destinations, boxes):
	sum = 0
	for box in boxes:
		distances = []
		for item in destinations:
			distances.append(manhattan_distance(box, item))
		sum = sum + min(distances)
	return sum

def astarsearch(data, starti, startj, numrows, numcols, boxes, destinations):
	rowNum = [-1, 0, 0, 1]
	colNum = [0, -1, 1, 0]
	q = Q.PriorityQueue()
	q.put(((0,(starti,startj))  ))
	camefrom = {}
	costsofar = {}
	camefrom[(starti, startj)] = (starti, startj)
	costsofar[(starti, startj)] = 0
	hashmap = {}
	while (q.qsize() > 0):
		item = q.get()
		curri = item[1][0]
		currj = item[1][1]
		if (isComplete(boxes, destinations)):
			print('Complete')
		for i in range(4):
			row = curri + rowNum[i]
			col = currj + colNum[i]
			if (row > numrows or  col>numcols or data[row][col]=='%'):
				continue
			if ((row, col) in boxes):
				boxnextrow = row + rowNum[i]
				boxnextcol = col + colNum[i]
				if (boxnextrow > numrows or  boxnextcol>numcols or data[boxnextrow][boxnextcol]=='%' or (boxnextrow, boxnextcol) in boxes):
					continue
			newcost = costsofar[(curri, currj)] + 1
			if (((row, col) in costsofar) == False or newcost < costsofar[(row, col)]):
				costsofar[(row, col)] = newcost
				if ((row, col) in boxes):
					boxes.remove((row, col))
					boxes.append((row + rowNum[i], col + colNum[i]))
				priority = newcost + computeheuristic(destinations, boxes)
				q.put((priority, (row, col)))
				camefrom[(row, col)] = (curri, currj)

def main():
	boxes = []
	destinations = []
	file =  open('sakoban1.txt', 'r') 
	board = file.read()
	data = filter(None, board.splitlines())
	numcols = max(len(r) for r in data)
	numrows = len(data)
	for r in data:
		r = list(r)
	for i in range(numrows):
		for j in range(numcols):
			if (data[i][j] == 'P'):
				starti = i
				startj = j
			if (data[i][j] == 'b'):
				boxes.append((i, j))
			if (data[i][j] == '.'):
				destinations.append((i, j))
			if (data[i][j] == 'B'):
				boxes.append((i, j))
				destinations.append((i, j))
	astarsearch(data, starti, startj, numrows, numcols, boxes, destinations)


if __name__== "__main__":
  main()