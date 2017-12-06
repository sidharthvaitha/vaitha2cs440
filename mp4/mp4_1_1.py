import math
import sys
import pprint

pp = pprint.PrettyPrinter(indent=1, width=300)

trainData   = "digitdata/trainingimages"
trainLabels = "digitdata/traininglabels"

testData = "digitdata/testimages"
testLabels = "digitdata/testlabels"

num_images = 5000
num_class = 10
num_feat = 28

num_test = 1000

# training data [10][28][28] and labels
td = [[[0 for k in range(num_feat)] for j in range(num_feat)] for i in range(num_images)]
tl = []
test_images = [[[0 for k in range(num_feat)] for j in range(num_feat)] for i in range(num_test)]
test_labels = []
# weight_vector for all 10 classes: [10][28][28]: init to 1
w = [[[0 for k in range(num_feat)] for j in range(num_feat)] for i in range(num_class)]
# learning rate: should be updated on each epoch
l_rate = 100
l_const = 1000
# epoch
epoch = 10
# bias (unused for now)
bias = 0
# weight for each class
t_w = [0]*num_class 

def reset_t_w():
	for i in range(len(t_w)):
		t_w[i] = 0

def readFile():
	with open(trainData, 'r') as digits, open(trainLabels, 'r') as labels, open(testData, 'r') as t_digits, open(testLabels, 'r') as t_labels:
		# read all labels
		for line in labels:
			tl.append(int(line))
		for line in t_labels:
			test_labels.append(int(line))
		rowIdx = 0

		# read all training digits
		for line in digits:
			for col in range(num_feat):
				try:
					td[int(rowIdx/num_feat)][rowIdx%num_feat][col] = 0 if line[col] == ' ' else 1
				except IndexError:
					print("Type Error: Img #: " + str(int(rowIdx/num_feat)) + " Row: " + str(rowIdx%num_feat) + " Col: " + str(col))
					sys.exit(0)
			rowIdx += 1

		# might as well
		rowIdx = 0

		# read all test digits
		for line in t_digits:
			for col in range(num_feat):
				try:
					test_images[int(rowIdx/num_feat)][rowIdx%num_feat][col] = 0 if line[col] == ' ' else 1
				except IndexError:
					print("Type Error: Img #: " + str(int(rowIdx/num_feat)) + " Row: " + str(rowIdx%num_feat) + " Col: " + str(col))
					sys.exit(0)
			rowIdx += 1

	#pp.pprint(tl)
	#pp.pprint(td)

# do training over read images
def startTraining():
	for x in range(epoch):
		# update learning rate (diminishing)
		print ("epoch ", x)
		l_rate = l_const / (l_const + x)
		# build perceptron
		#for i in range(num_images):
		for i in range(num_images):
			reset_t_w()
			for j in range(num_class):
				for k in range(num_feat):
					for l in range(num_feat):
						t_w[j] += td[i][k][l] * w[j][k][l]	

			# if (i == 10):
			# 	# print (t_w)
			# 	# sys.exit()

			# checking class and update
			c = t_w.index(max(t_w))
			sign = 0
			# print(c)
			# if class c gets misclassified as c'
			# update c positively and c' negatively
			if tl[i] != c:
				for k in range(num_feat):
					for l in range(num_feat):
						# inc for c
						# weight[trraininglabel][row][col] += alpha * train_data[training_label][row][col]
						# should be l_rate
						w[tl[i]][k][l] += l_rate * td[i][k][l]
						# dec for c'
						# weight[guess][row][col] -= alpha * train_data[guess][row][col]
						w[c][k][l] -= l_rate * td[i][k][l]


def tryTest():
	correct = 0
	incorrect = 0

	for i in range(num_test):
		reset_t_w()
		for j in range(num_class):
			for k in range(num_feat):
				for l in range(num_feat):
					t_w[j] += test_images[i][k][l] * w[j][k][l]

		c = t_w.index(max(t_w))
		try:
			if int(test_labels[i]) == int(c):
				correct += 1
			else:
				incorrect += 1
		except IndexError:
			print("i : " + str(i) + " test_labels length: " + str(len(test_labels)))
			sys.exit(0)

	print("Total: " + str(correct+incorrect) + " correct: " + str(correct) + " incorrect: " + str(incorrect) + " rate: " + str(correct/incorrect))

def main():
	readFile()
	# print(td[50])
	# for line in td[50]:
	# 	print (' '.join(str(v) for v in line))
	startTraining()
	tryTest()

if __name__ == "__main__":
	main()
