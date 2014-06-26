import sys
import random
from sage.all import *
import sage.graphs.graph_plot

def weight(row):
	wt = 0
	for i in range(len(row)):
		if row[i] > 0:
			wt = wt + 1
	return wt

def hw(n):
	return bin(n).count("1")

def xor(r1, r2):
	r = []
	for i in range(len(r1)):
		r.append(r1[i] ^ r2[i])
	return r

def xorRows(rows):
	r = rows[0]
	for i in range(1, len(rows)):
		r = xor(r, rows[i])
	return r

def checkRows(rows, k, targetSum = 0):
	target = []
	found = []
	for i in range(k):
		row = []
		found.append(False)
		for j in range(i):
			row.append(0)
		row.append(1)
		for j in range(k - i - 1):
			row.append(0)
		target.append(row)

	# Convert rows to lists instead of tuples

	for i in range(len(rows)):
		for j in range(k):
			if rows[i] == target[j]:
				found[j] = True
	
	# Try all linear combinations of the rows, trying to get target...
	for i in range(2**(len(rows))):
		if i > 0:
			r = []
			for j in range(len(rows)):
				if ((1 << j) & i) > 0:
					r.append(rows[j])
			xr = xorRows(r)
			for j in range(k):
				if xr == target[j]:
					found[j] = True

	# See if we found every one!
	count = 0
	for i in range(k):
		if found[i] == True:
			count = count + 1
		# if (found[i] == False):
		# 	return False
	if (count >= targetSum):
		return True
	else:
		return False
	# return True

def checkCombinations(M, n, k, pickCount, target):
	numEncodings = 0
	for i in range(2**n):
		if i > 0:
			if hw(i) <= pickCount:
				rows = []
				for r in range(n):
					if ((1 << r) & i) > 0:
						rows.append(M[r])
				if checkRows(rows, k, target):
					print >> sys.stderr, "Rows " + str(i) + ": " + str(rows)
					print >> sys.stderr, "Valid combination: " + str(i) + " - " + bin(i)
					numEncodings = numEncodings + 1

				# xorResult = xorRows(rows)
				# if (weight(xorResult) == k):
				# 	print("Valid combination: " + str(i) + " - " + bin(i))
					# exists = True
	return numEncodings

# Grab the input parameters
cols = int(sys.argv[1])
pickCount = int(sys.argv[2])
target = int(sys.argv[3])

# Dumb check to see that they're actually valid
if (target > cols):
	print >> sys.stderr, "Error: target (" + str(target) + ") should not be larger than the number of columns (" + str(cols) + ")"
else:
	rows = []
	numCols = 2**cols
	numCombinations = 0
	for i in range(pickCount):
		numCombinations = numCombinations + binomial(numCols, i + 1)
	for i in range(numCols):
		# Iterate over every bit and use it as a mask 
		row = []
		for b in range(cols):
			if ((1 << b) & i) > 0:
				row.append(1)
			else:
				row.append(0)
		rows.append(row)

	# Display the matrix for peace of mind
	M = Matrix(rows)

	# Run the checker to see if we can decode by hitting the target while choosing cat blocks
	print >> sys.stderr, "Content matrix"
	print >> sys.stderr, M.str()
	numEncodings = checkCombinations(rows, 2**cols, cols, pickCount, target)
	print >> sys.stderr, numCombinations, numEncodings, float(numEncodings) / float(numCombinations)

# Try all C(2^cols, cols) row selections and see if XORing them together will give us 
# #cols rows with weight 1 (i.e. allow us to decode the final result)

