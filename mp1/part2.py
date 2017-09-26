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

def astarsearch(data, starti, startj, numrows, numcols, fruits):
	#h = computeh(data, starti, startj, numrows, numcols, endi, endj)
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
		if (data[curri][currj] == '.'):
			print('found1: ')
			print(curri, " ", currj)
			strlist = list(data[curri])
			strlist[currj] = 'b'
			data[curri] = "".join(strlist)
			fruits.remove((curri, currj))
			writemazetofileastar(data, curri, currj, starti, startj, camefrom)
			if (len(fruits) == 0):
				print("All fruits found")
				break
		for i in range(4):
			row = curri + rowNum[i]
			col = currj + colNum[i]
			newcost = costsofar[(curri, currj)] + 1
			if (row > numrows or  col>numcols or data[row][col]=='%'):
				continue
			if ((tuple(fruits), (row, col)) in hashmap):
				continue
			if (((row, col) in costsofar) == False or newcost < costsofar[(row, col)]):
				costsofar[(row, col)] = newcost
				priority = newcost + computeheurestic1(row, col, fruits)
				hashmap[(tuple(fruits), (row, col))] = True
				q.put((priority, (row, col)))
				camefrom[(row, col)] = (curri, currj)

def main():
	fruits = []
	file =  open('mediumSearch.txt', 'r') 
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

	# while (len(fruits) > 0):
	# 	minitem = findnearestneighbour(fruitstarti, fruitstartj, fruits)
	# 	fruits.remove(minitem)
	# 	print(minitem)
	# 	astarsearch(data, fruitstarti, fruitstartj, numrows, numcols, minitem[0], minitem[1])
	# 	fruitstarti = minitem[0]
	# 	fruitstartj = minitem[1]




 #  def findnearestneighbour(starti, startj, pointlist):
	# minvalue = 10000000000000000000000
	# minitem = (pointlist[0][0], pointlist[0][1])
	# for item in pointlist:
	# 	hvalue = manhattan_distance((starti, startj), item)
	# 	if (hvalue < minvalue):
	# 		minvalue = hvalue
	# 		minitem = item
	# return minitem