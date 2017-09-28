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

def getMSTWeight(i, j, fruits):
	nodes = [(i, j)] + fruits
	G = np.zeros((len(nodes), len(nodes)))
	for idx1, node1 in enumerate(nodes):
		for idx2, node2 in enumerate(nodes):
			G[idx1][idx2] = abs(node1[0]-node2[0]) + abs(node1[1]-node2[1])
	G_sparse = csr_matrix(G)
	G_MST = minimum_spanning_tree(G_sparse)
	return sum(sum(G_MST.toarray().astype(int)))



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
	q.put(    ((0,(starti,startj), frozenset(fruitsinit))  ))
	camefrom = {}
	costsofar = {}
	camefrom[(frozenset(fruitsinit), (starti, startj))] = (starti, startj)
	costsofar[(frozenset(fruitsinit), (starti, startj))] = 0
	visited = {}
	visited[(frozenset(fruitsinit), (starti, startj))] = True
	while (q.qsize() > 0):
		item = q.get()
		count = count + 1
		if (count % 10000 == 0):
			print('Ten Thousand')
		curri = item[1][0]
		currj = item[1][1]
		parentfruits = list(item[2])
		if (len(parentfruits) == 0 ):
			print ('Length of parent fruits is: ', count)
		if (len(parentfruits) == 1 and parentfruits[0][0] == curri and parentfruits[0][1] == currj ):
				print("All fruits found")
				break
		for i in range(4):
			row = curri + rowNum[i]
			col = currj + colNum[i]
			if (row > numrows or  col>numcols or data[row][col]=='%'):
				continue
			childfruits = copy.deepcopy(parentfruits)

			if ((row, col) in childfruits and len(childfruits) == 1):
				print('All fruits found (childfruits)')
				resitem = (frozenset(parentfruits), (curri, currj))
				print(countsollength(data, camefrom, resitem, starti, startj))
				childfruits.remove((row, col))
				print  (count)

				return

			elif ((row, col) in childfruits):
				childfruits.remove((row, col))

			newcost = costsofar[(frozenset(parentfruits), (curri, currj))] + 1

			if ((frozenset(childfruits), (row, col)) in visited):
				continue

			if (((frozenset(childfruits), (row, col)) in costsofar) == False or newcost < costsofar[(frozenset(childfruits), (row, col))]):
				costsofar[(frozenset(childfruits), (row, col))] = newcost
				priority = newcost + getMSTWeight(row, col, childfruits)
				visited[(frozenset(childfruits), (row, col))] = True
				q.put((priority, (row, col), frozenset(childfruits)))
				camefrom[(frozenset(childfruits), (row, col))] = (frozenset(parentfruits), (curri, currj))


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


if __name__== "__main__":
  main()