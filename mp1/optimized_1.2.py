from array import array
from collections import deque
import Queue as Q
import copy
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

inputfile = "tinySearch.txt"
fruitdict = {}
fruitdict2 = {}
f = open('internallog.txt', 'w')

def buildfruitdict(fruits):
	count = 0
	for i in range(len(fruits)):
		fruitdict[fruits[i]] = i
	for i in range(len(fruits)):
		fruitdict2[i] = fruits[i]
	#print fruitdict

def check_if_bitset(val, n):
	return val & (1<<n)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def ispow2(value):
	return value & (value - 1)

def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)

def set_bit(value, bit):
    return value | (1<<bit)

def set_all_bits(n):
	value = 0
	for i in range(n):
		value = set_bit(value, i)
	return value

def computeheurestic1(i, j, fruits):
	distances = []
	for item in fruits:
		distances.append(manhattan_distance(item, (i, j)))
	return max(distances)

def getMSTWeight(i, j, fruits):
	nodes = [(i, j)]
	for i in range(len(fruitdict)):
		if (check_if_bitset(fruits, i) != 0):
			nodes.append(fruitdict2[i])
	G = np.zeros((len(nodes), len(nodes)))
	for idx1, node1 in enumerate(nodes):
		for idx2, node2 in enumerate(nodes):
			if (idx2 > idx1):
				G[idx1][idx2] = abs(node1[0]-node2[0]) + abs(node1[1]-node2[1])
	G_sparse = csr_matrix(G)
	G_MST = minimum_spanning_tree(G_sparse)
	return sum(sum(G_MST.toarray().astype(int)))

def maxdistance(i, j, fruits):
	items = [(i, j)]
	for i in range(len(fruitdict)):
		if (check_if_bitset(fruits, i) != 0):
			items.append(fruitdict2[i])
	max_distance = 0
	for i in range(len(items)):
		for j in range(i, len(items)):
			itemi = items[i]
			itemj = items[j]
			dist = manhattan_distance(itemi, itemj)
			if (dist > max_distance):
				max_distance = dist
	return max_distance


def calculate_startchar(fruitsinit):
	n = len(fruitsinit)
	startMark = '0'
	for i in range(n):
		if(startMark == '9'):
			startMark = 'a'
		elif(startMark == 'z'):
			startMark = 'A'
		else:
			startMark = chr(ord(startMark) + 1)
	return chr(ord(startMark) + 1)


def countsollength(data, camefrom, resultstate, starti, startj, fruitsinit):
	count = 0
	duplicate = copy.deepcopy(data)
	startMark = calculate_startchar(fruitsinit)
	while True:
		prev = camefrom[resultstate]
		if (data[prev[1][0]][prev[1][1]] == '%'):
			print("Error\n")
		if ((prev[1][0], prev[1][1]) == (starti, startj)):
			break
		count = count + 1
		if (data[prev[1][0]][prev[1][1]] == '.'):
			if(startMark == 'a'):
				startMark = '9'
			elif(startMark == 'A'):
				startMark = 'z'
			else:
				startMark = chr(ord(startMark) - 1)
			strlist = list(duplicate[prev[1][0]])
			strlist[prev[1][1]] = startMark
			duplicate[prev[1][0]] = "".join(strlist)
		else:
			strlist = list(duplicate[prev[1][0]])
			strlist[prev[1][1]] = '.'
			duplicate[prev[1][0]] = "".join(strlist)
		resultstate = prev
	outputfile = 'sol_' + inputfile
	writefile = open(outputfile, 'w')
	for line in duplicate:
		writefile.write(line)
		writefile.write('\n')
	writefile.close()
	return count


def checklastfruitfound(parentfruit, curri, currj):
	for i in range(len(fruitdict)):
		if (check_if_bitset(parentfruit, i) != 0):
			if (fruitdict2[i] == (curri, currj)):
				return True
	return False


def astarsearch(data, starti, startj, numrows, numcols, fruitsinit):
	count = 0
	count2 = 0
	rowNum = [-1, 0, 0, 1]
	colNum = [0, -1, 1, 0]
	q = Q.PriorityQueue()
	complete_fruitbitmask = set_all_bits(len(fruitsinit))
	print (str('Complete FruitMask is ' + str(complete_fruitbitmask)))
	q.put(    ((0,(starti,startj), complete_fruitbitmask, 0)  ))
	camefrom = {}
	costsofar = {}
	camefrom[(complete_fruitbitmask, (starti, startj))] = (starti, startj)
	costsofar[(complete_fruitbitmask, (starti, startj))] = 0
	visited = {}
	frontier_details = {}
	frontier_details[(complete_fruitbitmask, (starti, startj))] = 0
	#visited[(complete_fruitbitmask, (starti, startj))] = True
	count_added = 0
	while (q.qsize() > 0):
		item = q.get()
		
		if (count % 100000 == 0):
			print('Hundred Thousand\n')
		curri = item[1][0]
		currj = item[1][1]
		parentfruits = item[2]
		g = item[3]


		if (item[3] > costsofar[(parentfruits, (curri, currj))]):
			#print 'skipped'
			continue

		if ((parentfruits, (curri, currj)) in visited):
			continue

		visited[(parentfruits, (curri, currj))] = True

		count = count + 1

		oldparentfruits = parentfruits
		#and parentfruits[0][0] == curri and parentfruits[0][1] == currj
		if (ispow2(parentfruits) == 0 and checklastfruitfound(parentfruits, curri, currj)):
				print("All fruits found\n")
				print (str('Number of nodes expanded is ' + str(count) + '\n'))
				#resitem = (frozenset(oldparentfruits), (curri, currj))
				resitem = (0, (curri, currj))
				camefrom[(0, (curri, currj))] = (oldparentfruits, (curri, currj))
				print(str(countsollength(data, camefrom, resitem, starti, startj, fruitsinit)) + '\n')
				break
		elif ((curri, currj) in fruitdict):
				bit_to_clear = fruitdict[(curri, currj)]
				parentfruits = clear_bit(parentfruits, bit_to_clear)

		for i in range(4):
			row = curri + rowNum[i]
			col = currj + colNum[i]
			if (row > numrows or  col>numcols or data[row][col]=='%'):
				continue
			newcost = costsofar[(oldparentfruits, (curri, currj))] + 1
			if ((parentfruits, (row, col)) in visited):
				continue
			if (((parentfruits, (row, col)) in costsofar) == False or newcost < costsofar[(parentfruits, (row, col))]):
				costsofar[(parentfruits, (row, col))] = newcost
				priority = newcost + getMSTWeight(row, col, parentfruits)
				q.put((priority, (row, col), parentfruits, newcost))
				camefrom[(parentfruits, (row, col))] = (oldparentfruits, (curri, currj))
	
def main():
	fruits = []
	file =  open(inputfile, 'r') 
	board = file.read()
	data = filter(None, board.splitlines())
	numcols = max(len(r) for r in data) 
	numrows = len(data)
	print numrows
	print numcols
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
	#buildfruitdict(fruits)
	# n = len(fruits)
	# val = 0
	# for i in range(n):
	buildfruitdict(fruits)
	astarsearch(data, starti, startj, numrows, numcols, fruits)
	f.close()


if __name__== "__main__":
  main()
