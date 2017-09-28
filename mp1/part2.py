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

def astarsearch(data, starti, startj, numrows, numcols, fruitsinit):
	#h = computeh(data, starti, startj, numrows, numcols, endi, endj)
	count = 0
	rowNum = [-1, 0, 0, 1]
	colNum = [0, -1, 1, 0]
	q = Q.PriorityQueue()
	q.put(    ((0,(starti,startj), fruitsinit)  ))
	camefrom = {}
	costsofar = {}
	camefrom[(tuple(fruitsinit), (starti, startj))] = (starti, startj)
	costsofar[(tuple(fruitsinit), (starti, startj))] = 0
	visited = {}
	visited[(tuple(fruitsinit), (starti, startj))] = True
	while (q.qsize() > 0):
		item = q.get()
		count = count + 1
		curri = item[1][0]
		currj = item[1][1]
		fruits = item[2]
		if (data[curri][currj] == '.'):
			print('found1: ')
			print(curri, " ", currj)
			strlist = list(data[curri])
			strlist[currj] = 'b'
			data[curri] = "".join(strlist)
			fruits.remove((curri, currj))
			#writemazetofileastar(data, curri, currj, starti, startj, camefrom)
			if (len(fruits) == 0):
				print("All fruits found")
				break
		for i in range(4):
			row = curri + rowNum[i]
			col = currj + colNum[i]
			if (row > numrows or  col>numcols or data[row][col]=='%'):
				continue
			if ((tuple(fruits), (row, col)) in visited):
				continue
			#newcost = costsofar[(curri, currj)] + 1
			newcost = costsofar[(tuple(fruits), (curri, currj))] + 1
			#if (((row, col) in costsofar) == False or newcost < costsofar[(row, col)]):
			if (((tuple(fruits), (row, col)) in costsofar) == False or newcost < costsofar[(tuple(fruits), (row, col))]):
				#costsofar[(row, col)] = newcost
				costsofar[(tuple(fruits), (row, col))] = newcost
				priority = newcost + computeheurestic1(row, col, fruits)
				visited[(tuple(fruits), (row, col))] = True
				q.put((priority, (row, col), fruits))
				camefrom[(tuple(fruits), (row, col))] = (curri, currj)

def main():
	fruits = []
	file =  open('smallSearch.txt', 'r') 
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
			if (data[i][j] == '.'):
				fruits.append((i, j))
	
	fruitstarti = starti
	fruitstartj = startj
	astarsearch(data, starti, startj, numrows, numcols, fruits)


if __name__== "__main__":
  main()