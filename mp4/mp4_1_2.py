import math
import sys
import pprint

pp = pprint.PrettyPrinter(indent=1, width=300)

y_trainData = "digitdata/yes_train.txt"
n_trainData = "digitdata/no_train.txt"

y_testData = "digitdata/yes_test.txt"
n_testData = "digitdata/no_test.txt"

num_test 	= 50
num_y_train = 140
num_n_train = 131

num_class = 2
num_feat_row = 25	# each image consists of 25 row and 3 empty rows
num_feat_col = 10

# training data [10][25][10] and labels
yd = [[[0 for k in range(num_feat_col)] for j in range(num_feat_row)] for i in range(num_y_train)]
nd = [[[0 for k in range(num_feat_col)] for j in range(num_feat_row)] for i in range(num_n_train)]

yt = [[[0 for k in range(num_feat_col)] for j in range(num_feat_row)] for i in range(num_test)]
nt = [[[0 for k in range(num_feat_col)] for j in range(num_feat_row)] for i in range(num_test)]

# k-neighbors: should always be odd?
K = 3

def readFile():
	with open(y_trainData, 'r') as y_train, open(n_trainData, 'r') as n_train, open(y_testData, 'r') as y_test, open(n_testData, 'r') as n_test:
		# read tests first
		rowIdx = 0
		# readin yes tests
		for line in y_test:
			if len(line) >= num_feat_col:
				for col in range(num_feat_col):
					yt[int(rowIdx/(num_feat_row+3))][rowIdx%num_feat_row][col] = 0 if line[col] == ' ' else 1

			rowIdx += 1

		rowIdx = 0
		# readin yes tests
		for line in n_test:
			if len(line) >= num_feat_col:
				for col in range(num_feat_col):
					nt[int(rowIdx/(num_feat_row+3))][rowIdx%num_feat_row][col] = 0 if line[col] == ' ' else 1

			rowIdx += 1

		rowIdx = 0
		# readin yes tests
		for line in y_train:
			if len(line) >= num_feat_col:
				for col in range(num_feat_col):
					yd[int(rowIdx/(num_feat_row+3))][rowIdx%num_feat_row][col] = 0 if line[col] == ' ' else 1

			rowIdx += 1

		rowIdx = 0
		# readin yes tests
		for line in n_train:
			if len(line) >= num_feat_col:
				for col in range(num_feat_col):
					nd[int(rowIdx/(num_feat_row+3))][rowIdx%num_feat_row][col] = 0 if line[col] == ' ' else 1

			rowIdx += 1

	#pp.pprint(nd)
	#pp.pprint(yt)

def try_no(i):
	diff_counts = [sys.maxsize] * K
	u_array = [0] * K
	
	# with yes_trains
	for j in range(num_y_train):
		diff = 0
		for k in range(num_feat_row):
			for l in range(num_feat_col):
				diff += abs(nt[i][k][l] - yd[j][k][l])

		if diff < max(diff_counts):
			index = diff_counts.index(max(diff_counts))
			u_array[index] = 'Y'
			diff_counts[index] = diff

	# with no_trains
	for j in range(num_n_train):
		diff = 0
		for k in range(num_feat_row):
			for l in range(num_feat_col):
				diff += abs(nt[i][k][l] - nd[j][k][l])

		if diff < max(diff_counts):
			index = diff_counts.index(max(diff_counts))
			u_array[index] = 'N'
			diff_counts[index] = diff

	y_count = 0
	for c in u_array:
		if c == 'Y':
			y_count += 1
		else:
			y_count -= 1

	if y_count < 0:
		return True
	return False



def try_yes(i):
	diff_counts = [sys.maxsize] * K
	u_array = [0] * K
	
	# with yes_trains
	for j in range(num_y_train):
		diff = 0
		for k in range(num_feat_row):
			for l in range(num_feat_col):
				diff += abs(yt[i][k][l] - yd[j][k][l])

		if diff < max(diff_counts):
			index = diff_counts.index(max(diff_counts))
			u_array[index] = 'Y'
			diff_counts[index] = diff

	# with no_trains
	for j in range(num_n_train):
		diff = 0
		for k in range(num_feat_row):
			for l in range(num_feat_col):
				diff += abs(yt[i][k][l] - nd[j][k][l])

		if diff < max(diff_counts):
			index = diff_counts.index(max(diff_counts))
			u_array[index] = 'N'
			diff_counts[index] = diff

	y_count = 0
	for c in u_array:
		if c == 'Y':
			y_count += 1
		else:
			y_count -= 1

	if y_count > 0:
		return True
	return False

def runTest():
	
	y_correct = 0
	n_correct = 0

	for i in range(num_test):
		y_success = try_yes(i)
		n_success = try_no(i)

		y_correct += 1 if y_success == True else 0
		n_correct += 1 if n_success == True else 0

	print("y_correct (out of 50): " + str(y_correct) + " n_correct (out of 50): " + str(n_correct) + " accuracy: " + str( (y_correct+n_correct) / 100 ) )

def main():
	readFile()
	runTest()			

if __name__ == "__main__":
	main()
