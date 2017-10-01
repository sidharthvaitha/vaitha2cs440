import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree



def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def ispow2(value):
	return value & (value - 1)

def set_all_bits(n):
	value = 0
	for i in range(n):
		value = set_bit(value, i)
	print(value)

def check_if_bitset(val, n):
	return val & (1<<n)

#print(check_if_bitset(6, 0))

# nodes = [(i, j)] + fruits
# G = np.zeros((len(nodes), len(nodes)))
# for idx1, node1 in enumerate(nodes):
# 	for idx2, node2 in enumerate(nodes):
# 		node2 = nodes[idx2]
# 		G[idx1][idx2] = abs(node1[0]-node2[0]) + abs(node1[1]-node2[1])
# G_sparse = csr_matrix(G)
# G_MST = minimum_spanning_tree(G_sparse)
# return sum(sum(G_MST.toarray().astype(int)))

# X = csr_matrix([[0, 8, 0, 3],
#                  [0, 0, 2, 5],
#                  [0, 0, 0, 6],
#                 [0, 0, 0, 0]])

X = ([[0, 8, 0, 3],
     [8, 0, 2, 5],
     [0, 2, 0, 6],
    [3, 5, 6, 0]])

npX = np.array(X)
npX = csr_matrix(npX)

Tcsr = minimum_spanning_tree(npX)
print(sum(sum(Tcsr.toarray().astype(int))))