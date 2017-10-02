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

# X = ([[0, 8, 0, 3],
#      [8, 0, 2, 5],
#      [0, 2, 0, 6],
#     [3, 5, 6, 0]])

# npX = np.array(X)
# npX = csr_matrix(npX)

# Tcsr = minimum_spanning_tree(npX)
# print(sum(sum(Tcsr.toarray().astype(int))))


import numpy as np
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
 
import copy
def minimum_spanning_tree(X, copy_X=True):
    """X are edge weights of fully connected graph"""
    if copy_X:
        X = copy.deepcopy(X)
 
    if X.shape[0] != X.shape[1]:
        raise ValueError("X needs to be square matrix of edge weights")
    n_vertices = X.shape[0]
    spanning_edges = []
     
    # initialize with node 0:                                                                                         
    visited_vertices = [0]                                                                                            
    num_visited = 1
    # exclude self connections:
    diag_indices = np.arange(n_vertices)
    X[diag_indices, diag_indices] = 10000000
     
    while num_visited != n_vertices:
        new_edge = np.argmin(X[visited_vertices], axis=None)
        # 2d encoding of new_edge from flat, get correct indices                                                      
        new_edge = divmod(new_edge, n_vertices)
        new_edge = [visited_vertices[new_edge[0]], new_edge[1]]                                                       
        # add edge to tree
        spanning_edges.append(new_edge)
        visited_vertices.append(new_edge[1])
        # remove all edges inside current tree
        X[visited_vertices, new_edge[1]] = 10000000
        X[new_edge[1], visited_vertices] = 1000000                                                                   
        num_visited += 1
    return np.vstack(spanning_edges)
 
 

# P = np.random.uniform(size=(50, 2))
 
# X = squareform(pdist(P))
X = ([[0, 8, 0, 3],
     [8, 0, 2, 5],
     [0, 2, 0, 6],
    [3, 5, 6, 0]])
# print(len(X[0]))
edge_list = minimum_spanning_tree(np.array(X))
print (edge_list)
# plt.scatter(P[:, 0], P[:, 1])
 
# for edge in edge_list:
#     i, j = edge
#     plt.plot([P[i, 0], P[j, 0]], [P[i, 1], P[j, 1]], c='r')
# plt.show()
 
