import sys
import random
from sage.all import *
import sage.graphs.graph_plot

def make_pair(u, v):
	ls = [u, v]
	ls.sort()
	return (ls[0], ls[1])

def is_dominating_set(S, G):
	covered = []
	for v in G.vertices():
		covered.append(False)
	M = G.adjacency_matrix()
	for u in S:
		covered[u] = True
		for v in G.vertices():
			if (u != v):
				if (M[u,v] == 1):
					covered[v] = True
	for v in covered:
		if (covered[v] == False):
			return False
	return True

def is_covering_set(S, T, G):
	''' Return True if the vertices in S cover all the vertices in T.
	'''

	covered = []
	for v in T:
		covered.append(False)

	M = G.adjacency_matrix()
	for u in S:
		for v in T:
			if (u != v and M[u,v] == 1):
				covered[v] == True

	for v in covered:
		if (covered[v] == False):
			return False

	return True

def random_subset(V, size):
	subset = [ V[i] for i in sorted(random.sample(xrange(len(V)), size)) ]
	return subset

t = int(sys.argv[1]) # number of files
m = int(sys.argv[2]) # number of blocks (nodes) per file
combs = [] # list of node combinations (edges)

# Generate all C(t*m, 2) combinations of the vertices (those that will be mixed)
mixNodeId = t * m 			   # we start at t * m because all other node IDs are taken from the t sets
for i in range(t): 	 	       # item index #1
	for j in range(t):         # item index #2
		for k in range(m):     # vertex index #1
			for l in range(m): # vertex index #2
				v1 = (i * t) + k
				v2 = (j * t) + l
				if (v1 != v2):
					pair = make_pair(v1, v2)
					if not (pair in combs):
						combs.append(pair)
print(combs)
print(len(combs))

# Make the adjacency matrix for the graph
order = (t * m) + len(combs)
print(order)
rows = []
for i in range(order):
	row = []
	for j in range(order):
		row.append(0)
	rows.append(row)
M = Matrix(rows)
#print(M.str())

for pIndex in range(len(combs)):
	pair = combs[pIndex]
	mIndex = mixNodeId + pIndex
	v1 = pair[0]
	v2 = pair[1]

	# Connect v1 to mIndex and v2 to mIndex
	M[v1, mIndex] = 1
	M[mIndex, v1] = 1
	M[v2, mIndex] = 1
	M[mIndex, v2] = 1
print(M.str())

# Create the graph, output some basic properties, and then print the output
G = Graph(M)
print(G.order())

# Save the graph so it can be checked later
P = G.plot()
P.save('out.png')

T = []
M = []
for i in range(t * m):
	T.append(i)
for i in range(len(combs)):
	M.append(mixNodeId + i)

# Try to find a covering set by randomly selecting a subset of M and checking to see if it covers 
# all of the vertices in T



# Leverage Sage to find a minimum dominating set
S = G.dominating_set(independent = True)
print(is_dominating_set(S, G))
print(S)
print(len(S))

# This is how the adjacency matrix is formed
# M = Matrix ([ [0, 1, 1], [1, 0, 1], [1, 1, 0] ])
# G = Graph(M)
# print(G.order())
# domSet = G.dominating_set()
# print(domSet)
# print(len(domSet))
