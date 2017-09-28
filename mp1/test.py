import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from array import array
from collections import deque
import Queue as Q

class PacmanState():
    parent = None
    pathCost = float('inf')
    def __init__(self, location=(-1,1), goalsLeft=((-1,1)), value='%'):
        self.location = location
        self.goalsLeft = tuple(goalsLeft)
        self.value = value

    def __hash__(self):
        return hash((self.location, self.goalsLeft))

    def __eq__(self, other):
        return (self.location, self.goalsLeft) == (other.location, other.goalsLeft)

    def markGoalComplete(self, goal):
        temp = []
        for g in self.goalsLeft:
            if g != goal:
                temp.append(g)
        self.goalsLeft = tuple(temp)

    def copy(self):
        newNode = PacmanState()
        newNode.parent = self.parent
        newNode.pathCost = self.pathCost
        newNode.location = self.location
        newNode.goalsLeft = self.goalsLeft
        newNode.value = self.value
        return newNode

    def getMSTWeight(self):
        nodes = [self.location] + list(self.goalsLeft)
        G = np.zeros((len(nodes), len(nodes)))
        for idx1, node1 in enumerate(nodes):
            for idx2, node2 in enumerate(nodes):
                G[idx1][idx2] = abs(node1[0]-node2[0]) + abs(node1[1]-node2[1])
                # print idx1, node1, idx2, node2, G[idx1][idx2]
        G_sparse = csr_matrix(G)
        G_MST = minimum_spanning_tree(G_sparse)
        # print G_MST.toarray().astype(int)
        return sum(sum(G_MST.toarray().astype(int)))

test = PacmanState()
q = Q.PriorityQueue()
q.put((0,test))
a = (q.get())
print (a[1].location)
