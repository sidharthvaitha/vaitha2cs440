import pprint
import time
import math
# >>> n = 3
# >>> distance = [[[0 for k in xrange(n)] for j in xrange(n)] for i in xrange(n)]
# >>> pprint.pprint(distance)


data = [[[0 for k in range(28)] for j in range(28)] for i in range(10)]
count = [0] * 10
results = []
countsum = 0

def readtraindata():
	start = 0
	end = 28
	with open('digitdata/traininglabels') as f:
	    trainlabels = f.readlines()
	trainlabels = [int(x.strip()) for x in trainlabels]
	for x in range(len(trainlabels)):
		with open('digitdata/trainingimages', 'r') as infile:
			lines = [line for line in infile][start:end]
		for k in range(len(lines)):
			lines[k] = lines[k][:-1]
		# print(len(lines))
		# print(len(lines[0]))
		value = trainlabels[x]
		count[value] += 1
		item = data[value]
		for i in range(len(lines)):
			line = lines[i]
			for j in range(len(line)):
				c = line[j]
				if (c == '+' or c=='#'):
					item[i][j] += 1
		item = data[value]
		start += 28
		end += 28

def normalize():
	for x in range(10):
		item = data[x]
		for i in range(len(item)):
			for j in range(len(item[0])):
				item[i][j] = item[i][j]/count[x]
		# for line in item:
		# 	print(''.join(str(v) for v in line))

def getcountsum():
	s = 0
	for i in range(len(count)):
		s += count[i]
	countsum = s


def classifyhelper(item, n):
	train = data[n]
	p = 0
	s = 0
	for i in range(len(count)):
		s += count[i]
	countsum = s
	p = math.log1p(count[n]/countsum)
	for i in range(len(item)):
		for j in range(len(item[0])):
			c = item[i][j]
			x = train[i][j]
			if (x > 1):
				print('error')
			if(c == '+' or c =='#'):
				p += math.log1p(x)
			elif (c == ' '):
				p += math.log1p(1-x)
			else:
				print('here' + c)
	return p


def classify():
	start = 0
	end = 28
	with open('digitdata/testlabels') as f:
	    testlabels = f.readlines()
	testlabels = [int(x.strip()) for x in testlabels]
	for x in range(len(testlabels)):
		with open('digitdata/testimages', 'r') as infile:
			lines = [line for line in infile][start:end]
		for k in range(len(lines)):
			lines[k] = lines[k][:-1]
		if (len(lines)!=28):
			print('not 28')
		if (len(lines[0])!=28):
			print('not 28[0]')
		maxp = 0
		maxn = -1
		for i in range(10):
			p = classifyhelper(lines, i)
			if (p > maxp):
				maxp = p
				maxn = i
			# print(maxp)
		#print(maxp)
		results.append(maxn)
		start += 28
		end += 28
	# print(results)

def reporting():
	with open('digitdata/testlabels') as f:
	    testlabels = f.readlines()
	testlabels = [int(x.strip()) for x in testlabels]
	totalcount = [0] * 10
	correctcount = [0] * 10
	for i in range(len(testlabels)):
		global results
		actual = testlabels[i]
		mine = results[i]
		totalcount[actual] += 1
		if (actual == mine):
			correctcount[actual] += 1
	for i in range(10):
		print(correctcount[i]/totalcount[i])


			
def main():
	starttime = time.time()
	readtraindata()
	normalize()
	getcountsum()
	classify()
	reporting()
	print(time.time() - starttime)
	#print(count)


if __name__== "__main__":
  main()