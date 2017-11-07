import pprint
import time
# >>> n = 3
# >>> distance = [[[0 for k in xrange(n)] for j in xrange(n)] for i in xrange(n)]
# >>> pprint.pprint(distance)


data = [[[0 for k in range(28)] for j in range(28)] for i in range(10)]
count = [0] * 10

def readtraindata():
	start = 0
	end = 28
	with open('digitdata/traininglabels') as f:
	    trainlabels = f.readlines()
	trainlabels = [int(x.strip()) for x in trainlabels]
	for i in range(len(trainlabels)):
		with open('digitdata/trainingimages', 'r') as infile:
			lines = [line for line in infile][start:end]
			for i in range(len(lines)):
				lines[i] = lines[i][:-1]
			# print(len(lines))
			# print(len(lines[0]))
			value = trainlabels[i]
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

def main():
	starttime = time.time()
	readtraindata()
	print(time.time() - starttime)
	print(count)


if __name__== "__main__":
  main()