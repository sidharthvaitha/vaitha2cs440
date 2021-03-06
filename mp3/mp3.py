import time
import math
import sys
import numpy as np
import copy
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go




# plotly.tools.set_credentials_file(username='vaitha2', api_key='JLt6NeaQ3o3YOUSaVxit')
#k, f height, f width, overlap, numclass, height, width, chars
#info = [.2, 1, 1, False, 10, 28, 28, ' ', '+', '#']
# info = [0.2, 2, 2, False, 10, 28, 28, ' ', '+', '#']
#info = [0.1, 4, 4, True, 10, 28, 28, ' ', '+', '#']



# 1x1 Feature K set
#info = [0.2, 1, 1, 0, 10, 28, 28, ' ', '+', '#' ]
# 2x2 Feature with no overlap K set
info = [0.1, 2, 2, 0, 10, 28, 28, ' ', '+', '#' ]
# 2x4 Feature with no overlap K set
#info = [0.1, 2, 4, 0, 10, 28, 28, ' ', '+', '#' ]
# 4x2 Feature with no overlap k set
#info = [0.1, 4, 2, 0, 10, 28, 28, ' ', '+', '#' ]
# 4x4 Feature with no overlap kset
#info = [0.1, 4, 4, 0, 10, 28, 28, ' ', '+', '#' ]
# Overlapping Features
# 2x2 Feature with Overlap
#info = [0.1, 2, 2, 1, 10, 28, 28, ' ', '+', '#' ]
# 2x4 Feature with overlap
#info = [0.1, 2, 4, 1, 10, 28, 28, ' ', '+', '#' ]
# 4x2 Feature with overlap
#info = [0.1, 4, 2, 1, 10, 28, 28, ' ', '+', '#' ]
# 4x4 Feature with overlap
#info = [0.1, 4, 4, 1, 10, 28, 28, ' ', '+', '#' ]
# 2x3 Feature with overlap
#info = [0.1, 2, 3, 1, 10, 28, 28, ' ', '+', '#' ]
# 3x2 Feature with overlap
#info = [0.1, 3, 2, 1, 10, 28, 28, ' ', '+', '#' ]
# 3x3 Feature with overlap
#info = [0.2, 3, 3, 1, 10, 28, 28, ' ', '+', '#' ]

train_data = open("digitdata/trainingimages","r")
train_labels = open("digitdata/traininglabels","r")

testdata1 = open("digitdata/testimages","r")
testlabels = open("digitdata/testlabels","r")


def prettyfloat(x):
	return "%0.2f" % x


highvalues = [-1 * float('inf')] * info[4]
lowvalues = [float('inf')] * info[4]

highs = []
lows = []


smooth = info[0]
V = pow(2, info[1] * info[2])
count = []
testcount = []
data = []
testdata = []
prob = []
curimage = []
curtestimage = []

confmatrix = []
confdata = []

rowinc = 0
colinc = 0

countprob = []

for i in range(info[4]):
	count.append(0)
	testcount.append(0)
	countprob.append([])
	highs.append([])
	lows.append([])

for i in range(info[5]):
	data.append([])
	testdata.append([])
	prob.append([])
	curimage.append([])
	curtestimage.append([])


for i in range(0, info[6]):
	for j in range(0, info[5]):
			data[j].append([])
			testdata[j].append([])
			prob[j].append([])
			curimage[j].append([])
			curtestimage[j].append([])


for i in range(0, info[6]):
	for j in range(0, info[5]):
		for k in range(0, info[4]):
			data[i][j].append({})
			#prob[i][j].append([])


for i in range(0, info[4]):
	for j in range(0, info[5]):
		highs[i].append([])
		lows[i].append([])


for i in range(0, info[4]):
	for j in range(0, info[5]):
		for K in range(0, info[6]):
			highs[i][j].append([])
			lows[i][j].append([])


# for i in range(0, info[6]):
# 	for j in range(0, info[5]):
# 		for k in range(0, info[4]):
# 			for l in range(V):
# 				data[i][j][k].append(0)
# 				prob[i][j][k].append([])

for i in range(0, info[4]):
	confmatrix.append([])
	confdata.append([])

for i in range(0, info[4]):
	for j in range(0, info[4]):
		confmatrix[j].append([])
		confdata[j].append(0)

if (info[3] == False):
	rowinc = info[1]
	colinc = info[2]
else:
	rowinc = 1
	colinc = 1

while(1):
	c = train_labels.read(1)
	if not c:
		break
	value = int(c)
	count[value] += 1
	train_labels.read(1)
	for i in range(info[5]):
		for j in range(info[6] + 1):
			c = train_data.read(1)
			if (c != '\n'):
				if c == info[7]:
					curimage[i][j] = 0
				if c == info[8]:
					curimage[i][j] = 1
				if c == info[9]:
					curimage[i][j] = 1

	if (info[3] == True):
		buffr = info[1] - 1
		buffc = info[2] - 1
	else:
		buffr = 0
		buffc = 0

	for i in range(0, info[5] - buffr, rowinc):
		for j in range(0, info[6] - buffc, colinc):
			index = 0
			for r in range(info[1]):
				for c in range(info[2]):
					index |= curimage[i + r][j + c] << r * info[2] + c

			dictvalue = data[i][j][value].get(index, -1)
			if (dictvalue == -1):
				data[i][j][value][index] = 1
			else:
				data[i][j][value][index] = dictvalue + 1

train_data.close()
train_labels.close()

# for i in range(0, info[5], rowinc):
# 	for j in range(0, info[6], colinc):
# 		for k in range(info[4]):
# 			for l in range(V):
# 				prob[i][j][k][l] = (data[i][j][k][l] + smooth)/(count[k] + V * smooth)


total = sum(count)
for i in range(info[4]):
	countprob[i] = count[i]/total

# print(prob[0][0])

correct = 0
wrong = 0

while(1):
	c = testlabels.read(1)
	if not c:
		break
	value = int(c)
	testcount[value] += 1
	testlabels.read(1)

	for i in range(info[5]):
		for j in range(info[6] + 1):
			c = testdata1.read(1)
			if (c != '\n'):
				if c == info[7]:
					curtestimage[i][j] = 0
				if c == info[8]:
					curtestimage[i][j] = 1
				if c == info[9]:
					curtestimage[i][j] = 1


	for i in range(0, info[5] - buffr, rowinc):
		for j in range(0, info[6] - buffc, colinc):
			index = 0
			for r in range(info[1]):
				for c in range(info[2]):
					index |= curtestimage[i + r][j + c] << r * info[2] + c

			testdata[i][j] = index

	maxp = -100000
	best = -1
	# for line in testdata:
	# 	print (' '.join(str(v) for v in line))
	# sys.exit()
	for x in range(info[4]):
		p = math.log(countprob[x])
		# print(p)
		# sys.exit()
		#p = 0
		for i in range(0, info[5] - buffr, rowinc):
			for j in range(0, info[6] - buffc, colinc):
				dictvalue = data[i][j][x].get(testdata[i][j], -1)
				if (dictvalue == -1):
					p += math.log((0 + smooth)/(count[x] + V * smooth))
				else:
					p += math.log((dictvalue + smooth)/(count[x] + V * smooth))
		if (p > maxp):
			maxp = p
			best = x

	if (best == value):
		correct += 1
		if (maxp > highvalues[best]):
			highvalues[best] = maxp
			highs[best] = copy.deepcopy(testdata)

		if (maxp < lowvalues[best]):
			lowvalues[best] = maxp
			lows[best] = copy.deepcopy(testdata)
	else:
		wrong += 1

	confdata[value][best] += 1

testlabels.close()
testdata1.close()


for i in range(info[4]):
	for j in range(info[4]):
		confmatrix[i][j] = 100 * confdata[i][j]/testcount[i]

for line in confmatrix:
		print (' '.join(str(prettyfloat(v)) for v in line))


# for item in lows:
# 	for line in item:
# 		print (''.join(str(v) for v in line))
# 	print()
# 	print()


print('Percentage is ', correct/(correct + wrong))


# dup = copy.deepcopy(confmatrix)
# for i in range(info[4]):
# 	dup[i][i] = 0


# if (info[1] != 1 or info[2]!=1):
# 	sys.exit()


# odds = []
# minval = -1 * float('inf')
# first = (minval, -1 , -1)
# second = (minval, -1 , -1)
# third = (minval, -1 , -1)
# fourth = (minval, -1 , -1)
# for i in range(info[4]):
# 	for j in range(info[4]):
# 		item = dup[i][j]
# 		if (item > first[0]):
# 			fourth = third
# 			third = second
# 			second = first
# 			first = (item, i, j)
# 		elif (item > second[0]):
# 			fourth = third
# 			third = second
# 			second = (item, i, j)
# 		elif (item > third[0]):
# 			fourth = third
# 			third = (item, i, j)
# 		elif (item > fourth[0]):
# 			fourth = (item, i, j)

# # print(first, second, third)
# odds.append((first[1], first[2]))
# odds.append((second[1], second[2]))
# odds.append((third[1], third[2]))
# odds.append((fourth[1], fourth[2]))

# print(odds)


# for item in odds:
# 	x1 = item[0]
# 	x2 = item[1]
# 	p = -1
# 	prob1 = copy.deepcopy(prob)
# 	prob2 = copy.deepcopy(prob)
# 	for i in range(0, info[5] - buffr, rowinc):
# 		for j in range(0, info[6] - buffc, colinc):
# 			dictvalue = data[i][j][x1].get(1, -1)
# 			if (dictvalue == -1):
# 				prob1[i][j] = math.log((0 + smooth)/(count[x1] + V * smooth))
# 			else:
# 				prob1[i][j] = math.log((dictvalue + smooth)/(count[x1] + V * smooth))

# 			dictvalue2 = data[i][j][x2].get(1, -1)
# 			if (dictvalue == -1):
# 				prob2[i][j] = math.log((0 + smooth)/(count[x2] + V * smooth))
# 			else:
# 				prob2[i][j] = math.log((dictvalue + smooth)/(count[x2] + V * smooth))

# 	trace = go.Heatmap(z=prob2)
# 	data = [trace]
# 	py.plot(data, filename = 'test1')




	# for i in range(0, info[5] - buffr, rowinc):
	# 	for j in range(0, info[6] - buffc, colinc):
	# 		dictvalue = data[i][j][x1].get(testdata[i][j], -1)
	# 		if (dictvalue == -1):
	# 			prob[i][j] = prob1[i][j]/prob2[i][j]
	# 		else:
	# 			prob[i][j] = prob1[i][j] - prob2[i][j]







