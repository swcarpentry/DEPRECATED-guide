import numpy.linalg as linalg

from scipy.stats import f

from numpy import *

def readData(fileName):
	''' Read data from fileName and store as follows: 
			
		Each line is of form n, k where n is the index of the 
		particle and k is the number of steps before resolution.
		If k is negative, then abs(k) is the number of steps.
	
		Return a vector containing abs(k) and a matrix where column
		1 is n and column 2 is sign(k) != negative
	
	'''

	file = open(fileName, 'r')
	
	response = []
	index = []
	sign = []
	
	for line in file:
		
		line = line.strip()
		if line[0] == '#':
			continue
		fields = line.split(',')
		
		response.append(abs(float(fields[1])))
		index.append( float( fields[0] ))
		sign.append( float(float(fields[1]) >= 0 ))
		
	
	responseArray = array(response).T
	dataArray = array([ index , sign] ).T
	
	return (responseArray, dataArray)
	

def linRegStats(A, b):
	''' Use linear regression to solve for Ax=b where A and b are known.
	Also report stats from Wald test.
	'''
	o = ones(b.size)
	A = column_stack((A, o))
	lstsqStats = linalg.lstsq(A,b)
	
	x = lstsqStats[0]
	SSE = lstsqStats[1][0]
	
	meanResponse = sum(b) / b.size
	computedResponse = dot(A,x)
	SSR = dot( computedResponse - meanResponse, computedResponse - meanResponse )
	fstat = SSR / (SSE / (b.size - 2 ));
	
	p = 1.0 - f.cdf(fstat, 1, b.size - 2)
	
	return {'betas' : x , 'F' : fstat, 'p' : p, 'df1' : 1 , 'df2' : b.size-2}
	
	
if __name__ == "__main__":
	import sys
	(b,A) = readData(sys.argv[1])
	
	x = linRegStats(A[:,0], b)
	print 'Test for decrease in resolution time: beta = %f, p = %s' % (x['betas'][0], x['p'])
	
	# test for decrease in resolution time using just those that resolved to hits
	mask = A[:,1] > 0
	xHits = linRegStats( A[mask, 0], b[mask] )
	print 'Test for decrease in resolution time - hits only: beta = %f, p = %s' % (xHits['betas'][0], xHits['p'])
	
	# test for decrease in resolution time using just those that resolved to misses
	mask = A[:,1] < 1
	xMisses = linRegStats( A[mask, 0], b[mask] )
	print 'Test for decrease in resolution time - misses only: beta = %f, p = %s' % (xMisses['betas'][0], xMisses['p'])
	
	# test for difference in slopes of previous two tests
	xDiff = linRegStats( column_stack((A, A[:,0]*A[:,1])), b )
	print 'Test for difference in change in resolution time: beta = %f, p = %s' % (xDiff['betas'][2], xDiff['p'])
	
	
