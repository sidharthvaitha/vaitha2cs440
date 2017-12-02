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
info = [2, 1, 1, False, 2, 70, 60, ' ', '+', '#']
# info = [0.2, 2, 2, False, 10, 28, 28, ' ', '+', '#']
#info = [0.1, 4, 4, True, 10, 28, 28, ' ', '+', '#']


train_data = open("facedata/facedatatrain","r")
train_labels = open("facedata/facedatatrainlabels","r")

testdata1 = open("facedata/facedatatest","r")
testlabels = open("facedata/facedatatestlabels","r")


def prettyfloat(x):
	return "%0.2f" % x


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

for i in range(0, info[5]):
	for j in range(0, info[6]):
		for k in range(0, info[4]):
			data[i][j].append({})
			#prob[i][j].append([])

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

print('Percentage is ', correct/(correct + wrong))

