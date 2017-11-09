import time
import math

#k, f height, f width, overlap, numclass, height, width, chars
info = [.2, 1, 1, False, 10, 28, 28, ' ', '+', '#']


train_data = open("digitdata/trainingimages","r")
train_labels = open("digitdata/traininglabels","r")

testdata = open("digitdata/testimages","r")
testlabels = open("digitdata/testlabels","r")


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

for i in range(0, info[6]):
	for j in range(0, info[5]):
		for k in range(0, info[4]):
			data[i][j].append([])
			prob[i][j].append([])

for i in range(0, info[6]):
	for j in range(0, info[5]):
		for k in range(0, info[4]):
			for l in range(V):
				data[i][j][k].append(0)
				prob[i][j][k].append([])

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
		buffr = info[1]
		buffc = info[2]
	else:
		buffr = 0
		buffc = 0

	for i in range(0, info[5] - buffr, rowinc):
		for j in range(0, info[6] - buffc, colinc):
			index = 0
			for r in range(info[1]):
				for c in range(info[2]):
					index |= curimage[i + r][j + c] << r + c

			data[i][j][value][index] += 1

train_data.close()
traininglabels.close()

for i in range(0, info[5], rowinc):
	for j in range(0, info[6], colinc):
		for k in range(info[4]):
			for l in range(V):
				prob[i][j][k][l] = (data[i][j][k][l] + smooth)/(count[k] + V * smooth)


total = sum(count)

for i in range(info[4]):
	countprob[i] /= total

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
			c = testimages.read(1)
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
					index |= curimage[i + r][j + c] << r + c

			testdata[i][j] = index

	maxp = -1
	best = -1
	for x in range(info[4]):
		p = math.log(countprob[x])
		for i in range(0, info[5] - buffr, rowinc):
			for j in range(0, info[6] - buffc, colinc):
				p += math.log(prob[i][j][testdata[i][j]])
	if (p > maxp):
		maxp = p
		best = x

	if (best == value):
		correct += 1
	else:
		wrong += 1

	confdata[value][best] += 1

testlabels.close()
testimages.close()


for i in range(info[4]):
	for j in range(info[4]):
		confmatrix[i][j] = 100 * confdata[i][j]/testcount[i]





