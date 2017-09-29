from array import array

from collections import deque

import Queue as Q

import copy

import numpy as np

from scipy.sparse import csr_matrix

from scipy.sparse.csgraph import minimum_spanning_tree



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



def writemazetofileastar(data, endi, endj, starti, startj, parentQ):
	strlist = copy.copy(data)       # str list
	charlist = []
	for row in range(len(strlist)):
		charlist.append([])
		for col in range(len(strlist[row])):
			charlist[row].append( strlist[row][col] )       # to char list
	startMark = '1'                 # 1-9 a-z A-Z

	while not parentQ.empty():
		path = parentQ.get()
		i = path[0]
		j = path[1]
		if (i == -1 or j == -1):
			continue
		if (data[i][j] == 'P'):
			continue
		if(data[i][j] == '.'):
			if(charlist[i][j] != '.'):
				continue;	# bug
			charlist[i][j] = startMark
			if(startMark == '9'):
				startMark = 'a'
			elif(startMark == 'z'):
				startMark = 'A'
			else:
				startMark = chr(ord(startMark) + 1)
		else:
			charlist[i][j] = '.'

	writefile = open('solution.txt', 'w')
	for row in range(len(strlist)):
		writeline = ''
		for col in range(len(strlist[row])):
			writeline += charlist[row][col]
		writefile.write(writeline)
		writefile.write('\n')
	writefile.close()





def computeheurestic1(i, j, fruits):
	distances = []
	for item in fruits:
		distances.append(manhattan_distance(item, (i, j)))
	return max(distances)

def getMSTWeight(i, j, fruits):
	nodes = [(i, j)] + fruits
	G = np.zeros((len(nodes), len(nodes)))
	for idx1, node1 in enumerate(nodes):
		for idx2, node2 in enumerate(nodes):
			G[idx1][idx2] = abs(node1[0]-node2[0]) + abs(node1[1]-node2[1])
	G_sparse = csr_matrix(G)
	G_MST = minimum_spanning_tree(G_sparse)
	return sum(sum(G_MST.toarray().astype(int)))


def maxdistance(i, j, fruits):
	items = [(i, j)] + fruits
	max_distance = 0
	for i in range(len(items)):
		for j in range(i, len(items)):
			itemi = items[i]
			itemj = items[j]
			dist = manhattan_distance(itemi, itemj)
			if (dist > max_distance):
				max_distance = dist
	return max_distance

def countsollength(data, camefrom, resultstate, starti, startj):
	count = 0
	while True:
		prev = camefrom[resultstate]
		count = count + 1
		if (data[prev[1][0]][prev[1][1]] == '%'):
			print("Error")
		if ((prev[1][0], prev[1][1]) == (starti, startj)):
			break
		resultstate = prev
	return count



def astarsearch(data, starti, startj, numrows, numcols, fruitsinit):

	#h = computeh(data, starti, startj, numrows, numcols, endi, endj)

	count = 0
	count2 = 0
	rowNum = [-1, 0, 0, 1]
	colNum = [0, -1, 1, 0]
	q = Q.PriorityQueue()
	parent = Q.Queue()
	parent.put( (-1, -1) )
	q.put(    ((0,(starti,startj), frozenset(fruitsinit), parent)  ))
	camefrom = {}
	costsofar = {}
	camefrom[(frozenset(fruitsinit), (starti, startj))] = (frozenset(fruitsinit), (starti, startj))
	costsofar[(frozenset(fruitsinit), (starti, startj))] = 0
	visited = {}
	visited[(frozenset(fruitsinit), (starti, startj))] = True
	while (q.qsize() > 0):
		item = q.get()
		count = count + 1
		curri = item[1][0]
		currj = item[1][1]
		parentQ = Q.Queue()
		parentQ.queue = copy.deepcopy(item[3].queue)
		parentfruits = list(item[2])
		oldparentfruits = copy.deepcopy(parentfruits)
		if (len(parentfruits) == 1 and parentfruits[0][0] == curri and parentfruits[0][1] == currj ):
				print("All fruits found")
				resitem = (frozenset(oldparentfruits), (curri, currj))
				print("Path Length: " + str(len(parentQ.queue)))
				writemazetofileastar(data, curri, currj, starti, startj, parentQ)
				break

		elif ((curri, currj) in parentfruits):
				parentfruits.remove((curri, currj))

		for i in range(4):
			row = curri + rowNum[i]
			col = currj + colNum[i]
			if (row > numrows or  col>numcols or data[row][col]=='%'):
				continue
			newcost = costsofar[(frozenset(oldparentfruits), (curri, currj))] + 1
			if ((frozenset(parentfruits), (row, col)) in visited):
				continue
			if (((frozenset(parentfruits), (row, col)) in costsofar) == False or newcost < costsofar[(frozenset(parentfruits), (row, col))]):
				costsofar[(frozenset(parentfruits), (row, col))] = newcost
				priority = newcost + maxdistance(row, col, parentfruits)
				visited[(frozenset(parentfruits), (row, col))] = True
				myParentQ = Q.Queue()
				myParentQ.queue = copy.deepcopy(parentQ.queue)
				myParentQ.put( (curri, currj) )
				q.put((priority, (row, col), frozenset(parentfruits), myParentQ))
				camefrom[(frozenset(parentfruits), (row, col))] = (frozenset(oldparentfruits), (curri, currj))

def main():
	fruits = []
	file =  open('tinySearch.txt', 'r') 
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
	# print maxdistance(starti, startj, fruits)


if __name__== "__main__":
  main()