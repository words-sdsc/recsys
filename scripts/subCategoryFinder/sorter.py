# =========================================================================
# FileName: Sorter.py
# Purpose: To generate a sample of reviews out of a subCategory such that
#          the number of reviews per reviewer increases by selecting only
#          the top 5000 reviewers per category.
# Author: David Justo
# =========================================================================

import sys #CLI args
from collections import Counter 
import linecache
import math
import gzip
import os

# Generator to open files (need to be decompressed)
def getReviewer(fileName):
	with open(fileName,'r') as f:
		for line in f:
			reviewerID = line.split(' ')[0]
			yield reviewerID

def main():
	fileName = sys.argv[1]
	currLine = 0
	IDToLine = {}
	IDCount = Counter()
	gen = getReviewer(fileName)
	
	for reviewer in gen:
		print currLine
		currLine += 1
		IDCount[reviewer] += 1
		if(reviewer not in IDToLine.keys()):
			IDToLine[reviewer] = []
		IDToLine[reviewer].append(currLine)

	print "Done counting reviewerIDs"
        
        #Obtain the 5000 most common reviewers 
	mostCommon = IDCount.most_common(int(math.ceil(5000)))
	IDCount = Counter()
	print "Freeing up memory"
	
	# Write all reviews of the 5000 most common reviweers in output.gz
	output = gzip.open(os.getcwd() + '/output.gz','wb')
	for IDTuple in mostCommon:
		ID = IDTuple[0]
		for line in IDToLine[ID]:
			currLine = linecache.getline(fileName,line)
			print 'A'+ str(line)
			output.write(currLine)
		del IDToLine[ID]
	output.close()
main()	
	
	
