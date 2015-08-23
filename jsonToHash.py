import sys       # Command line argument detection
import gzip      # For opening gzip compressed files 
import pickle    # For object serialization into files
import os
import string

def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield eval(l)


def start( allIds, reviewDataFile, idsPerCateg ):

	currentDir = os.getcwd()                  #current directory path
	newDir     = currentDir + "/OUTPUT"       #path of output directory
	os.makedirs( newDir )                     #create direcetory path

	idsPerCategCOPY = []
	for pairOfIdsAndCateg in idsPerCateg:
		filename   = newDir + '/subCateg_'+	pairOfIdsAndCateg["categ"] +'.gz'
		stream = gzip.open(filename,'wb')
		pairOfIdsAndCateg["stream"] = stream
		idsPerCategCOPY.append(pairOfIdsAndCateg)


	idsPerCateg = idsPerCategCOPY
	idsPerCategCOPY = []

	HASHMAP = {}

	for categ in idsPerCateg:
		print 'category %r has %r many ids' %(categ["categ"], len(categ["ids"]))
		print 'DEBUGGING'
		if( set(categ["ids"]).issubset( set(allIds) ) ):
			print 'all my ids are in allIds'
		else:
			print 'bug found brah!'
	#HASHMAPTEST = {}
	
	#Parsing file to read
	reviewDataGen = parse(reviewDataFile)

	while True:  #Keep on reading until no more lines can be parsed
		try:
			currentJSON = next(reviewDataGen)
			if( currentJSON['asin'] in allIds ):

				writeReviewerId = currentJSON['reviewerID']
				writeOverallRat = currentJSON['overall']
				writeAsin       = currentJSON['asin']
				writeTimeStamp  = currentJSON['reviewTime']
				writeReviewText = currentJSON['reviewText']
				writeReviewText = writeReviewText.lower()
				writeReviewText = "".join(l for l in writeReviewText 
					                        if l not in string.punctuation)
				writeWordCount  = len(writeReviewText.split())



				writeMe = str(writeReviewerId) + ' ' + str(writeAsin)+ ' ' + \
				          str(writeOverallRat)+' '+str(writeTimeStamp)+ ' ' + \
				          str(writeWordCount)+ ' ' +str(writeReviewText)+ '\n'

				for pairOfIdsAndCateg in idsPerCateg:
					if currentJSON['asin'] in pairOfIdsAndCateg['ids']:
						print 'writing! for category %r' %pairOfIdsAndCateg["categ"]
						pairOfIdsAndCateg["stream"].write(writeMe)

		except StopIteration: #Whenever there's no more jsons to read in file
			for pairOfIdsAndCateg in idsPerCateg:
				pairOfIdsAndCateg["stream"].close()
			break
	
