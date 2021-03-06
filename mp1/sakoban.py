from array import array
from collections import deque
import Queue as Q
import copy

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


def countsollength(data, camefrom, resultstate, starti, startj, fruitsinit):
	count = 0
	while True:
		prev = camefrom[resultstate]
		if (data[prev[1][0]][prev[1][1]] == '%'):
			print("Error\n")
		if ((prev[1][0], prev[1][1]) == (starti, startj)):
			break
		count = count + 1
		resultstate = prev
	return count

def isComplete(destinations, boxes):
	for item in destinations:
		if (item not in boxes):
			return False
	print (destinations)
	print (boxes)
	return True

def computeheuristic(destinations, boxes):
	sum = 0
	for box in boxes:
		distances = []
		for item in destinations:
			distances.append(manhattan_distance(box, item))
		sum = sum + min(distances)
	return sum

def cornerhelper(data, boxes, direction):
	#or (direction[0], direction[1]) in boxes
	if (data[direction[0]][direction[1]] == '%' ):
		return True
	return False


def iscorner(curri, currj, data, boxes):
	rowNum = [-1, 0, 0, 1]
	colNum = [0, -1, 1, 0]
	count= 0
	up = (curri - 1, currj)
	down = (curri + 1, currj)
	left = (curri, currj - 1)
	right= (curri, currj + 1)
	if (cornerhelper(data, boxes, up)  and cornerhelper(data, boxes, left)):
		return True
	elif (cornerhelper(data, boxes, up)  and cornerhelper(data, boxes, right)):
		return True
	elif (cornerhelper(data, boxes, down)  and cornerhelper(data, boxes, right)):
		return True
	elif (cornerhelper(data, boxes, down)  and cornerhelper(data, boxes, left)):
		return True
	else:
		return False


def astarsearch(data, starti, startj, numrows, numcols, boxesinit, destinations):
	count = 0
	count2 = 0
	rowNum = [-1, 0, 0, 1]
	colNum = [0, -1, 1, 0]
	q = Q.PriorityQueue()
	q.put(    ((0,(starti,startj), frozenset(boxesinit))  ))
	camefrom = {}
	costsofar = {}
	camefrom[(frozenset(boxesinit), (starti, startj))] = (starti, startj)
	costsofar[(frozenset(boxesinit), (starti, startj))] = 0
	visited = {}
	visited[(frozenset(boxesinit), (starti, startj))] = True
	count = 0
	while (q.qsize() > 0):
		item = q.get()
		count = count + 1
		curri = item[1][0]
		currj = item[1][1]
		parentboxes = list(item[2])
		oldparentboxes = copy.deepcopy(parentboxes)
		if (count % 10000 == 0):
			print('Ten Thousand')
		if (isComplete(destinations, parentboxes)):
				print("All boxes in destination")
				print count
				resitem = (frozenset(parentboxes), (curri, currj))
				print(countsollength(data, camefrom, resitem, starti, startj, boxesinit))
				return

		for i in range(4):
			parentboxes = copy.deepcopy(oldparentboxes)
			row = curri + rowNum[i]
			col = currj + colNum[i]
			if (row >= numrows or  col>=numcols or data[row][col]=='%'):
				continue

			if ((row, col) in parentboxes):
				boxnextrow = row + rowNum[i]
				boxnextcol = col + colNum[i]
				if (boxnextrow >= numrows or  boxnextcol>=numcols or data[boxnextrow][boxnextcol]=='%' or (boxnextrow, boxnextcol) in parentboxes):
					continue
				tempboxes = copy.deepcopy(parentboxes)
				tempboxes.remove((row, col))
				tempboxes.append((row + rowNum[i], col + colNum[i]))
				if (iscorner(row + rowNum[i], col + colNum[i], data, tempboxes) and (row + rowNum[i], col + colNum[i]) not in destinations):
					# print('iscorner ', row + rowNum[i], col + colNum[i])
					continue
				else:
					parentboxes.remove((row, col))
					parentboxes.append((row + rowNum[i], col + colNum[i]))

			newcost = costsofar[(frozenset(oldparentboxes), (curri, currj))] + 1
			# if ((frozenset(parentboxes), (row, col)) in visited):
			# 	continue
			if (((frozenset(parentboxes), (row, col)) in costsofar) == False or newcost < costsofar[(frozenset(parentboxes), (row, col))]):
				costsofar[(frozenset(parentboxes), (row, col))] = newcost
				priority = newcost + 50 * computeheuristic(destinations, parentboxes)
				visited[(frozenset(parentboxes), (row, col))] = True
				q.put((priority, (row, col), frozenset(parentboxes)))
				camefrom[(frozenset(parentboxes), (row, col))] = (frozenset(oldparentboxes), (curri, currj))

def main():
	boxes = []
	destinations = []
	file =  open('sakoban4.txt', 'r') 
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

  