from array import array
from collections import deque
import Queue as Q

def isValid(data, i, j, visited):
	numcols = max(len(r) for r in data)
	numrows = len(data)
	if (i< numrows and j <numcols and data[i][j]!='%' and visited[i][j] == False):
		return True;
	return False;

# print(data[21][1])
def bfs(data, starti, startj, numrows, numcols):
	rowNum = [-1, 0, 0, 1]
	colNum = [0, -1, 1, 0]
	q = deque()
	q.append((starti, startj))
	visited = [[False for i in range(numcols)] for j in range(numrows)]
	visited[starti][startj] = True
	while (len(q) != 0 ):
		item = q.pop();
		curri = item[0]
		currj = item[1]
		if (data[curri][currj] == '.'):
			print('found')
			print(curri, " ", currj)
			break
		for i in range(4):
			row = curri + rowNum[i]
			col = currj + colNum[i]
			if (isValid(data, row, col, visited)):
				visited[row][col] = True
				q.append((row, col))

# def dfs(data, starti, startj, numrows, numcols):

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
	writefile = open('output.txt', 'w')
	for line in duplicate:
		writefile.write(line)
		writefile.write('\n')
	writefile.close()

def astarsearch(data, starti, startj, numrows, numcols, endi, endj):
	h = computeh(data, starti, startj, numrows, numcols, endi, endj)
	rowNum = [-1, 0, 0, 1]
	colNum = [0, -1, 1, 0]
	q = Q.PriorityQueue()
	q.put(((0,(starti,startj))  ))
	camefrom = {}
	costsofar = {}
	camefrom[(starti, startj)] = (starti, startj)
	costsofar[(starti, startj)] = 0
	while (q.qsize() > 0):
		item = q.get()
		curri = item[1][0]
		currj = item[1][1]
		if (data[curri][currj] == '.'):
			print('found')
			print(curri, " ", currj)
			writemazetofileastar(data, endi, endj, starti, startj, camefrom)
			break
		for i in range(4):
			row = curri + rowNum[i]
			col = currj + colNum[i]
			newcost = costsofar[(curri, currj)] + 1
			if (row> numrows or  col>numcols or data[row][col]=='%'):
				continue
			if (((row, col) in costsofar) == False or newcost < costsofar[(row, col)]):
				costsofar[(row, col)] = newcost
				priority = newcost + h[row][col]
				q.put((priority, (row, col)))
				camefrom[(row, col)] = (curri, currj)

def main():
	file =  open('maze1.txt', 'r') 
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
				endi = i
				endj = j
	# bfs(data, starti, startj, numrows, numcols)
	astarsearch(data, starti, startj, numrows, numcols, endi, endj)

if __name__== "__main__":
  main()

