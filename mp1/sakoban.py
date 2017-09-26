from array import array
from collections import deque
import Queue as Q


def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)


def computeh(data, starti, startj, numrows, numcols, endi, endj):
	h = [[False for i in range(numcols)] for j in range(numrows)]
	for i in range(numrows):
		for j in range(numcols):
			h[i][j] = manhattan_distance((i, j), (endi, endj))
	return h

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


def computeheurestic1(i, j, fruits):
	distances = []
	for item in fruits:
		distances.append(manhattan_distance(item, (i, j)))
	return max(distances)

def isComplete(destinations, boxes):
	for item in destinations:
		if (item not in boxes):
			return False
	return True

def computeheuristic(destinations, boxes):
	sum = 0
	for box in boxes:
		distances = []
		for item in distances:
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
	hashmap[(tuple(fruits), (starti, startj))] = True
	while (q.qsize() > 0 and len(fruits)>0):
		item = q.get()
		curri = item[1][0]
		currj = item[1][1]
		if (isComplete(boxes, destinations)):
			print('Complete')
		for i in range(4):
			row = curri + rowNum[i]
			col = currj + colNum[i]
			newcost = costsofar[(curri, currj)] + 1
			if (row > numrows or  col>numcols or data[row][col]=='%'):
				continue
			if (((row, col) in costsofar) == False or newcost < costsofar[(row, col)]):
				costsofar[(row, col)] = newcost
				
				priority = newcost + computeheurestic(destinations, boxes)
				hashmap[(tuple(fruits), (row, col))] = True
				if 
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
	astarsearch(data, starti, startj, numrows, numcols, fruits)


if __name__== "__main__":
  main()