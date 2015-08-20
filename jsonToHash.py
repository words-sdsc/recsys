import sys # Command line argument detection
import gzip #For opening gzip compressed files 
import pickle #For object serialization into files


#Constant strings
DONE_STRING        = "Done writting to file: %s"
START_WRITE_STRING = "Writing to file: %s"

def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield eval(l)


def main():
	HASHMAP = {}
	HASHMAPTEST = {}
	print 'here'

	#Parsing file to read
	fileToParse = sys.argv[1]
	outPutFile  = 'PRE-PROCESSED_' + fileToParse[10:]

	generator = parse(fileToParse)
	flag = True

	handle = open( outPutFile , 'wb')
	threshold = 50000
		
	nextJSON = next(generator)
	currentKey = nextJSON['asin']
	numDumps = 0

	while flag:
		c = 0
		try:
			
			while not( c > threshold and currentKey != nextJSON['asin']): 
				try:
					c = c + 1
					currentJSON = nextJSON
					
					currentKey = currentJSON['asin']

					if( currentKey in HASHMAP ):
						HASHMAP[currentKey].append(currentJSON)
						#HASHMAPTEST[currentKey].append(currentJSON)
					else:
						HASHMAP[currentKey] = []
						HASHMAP[currentKey].append(currentJSON)
						#HASHMAPTEST[currentKey] = []
						#HASHMAPTEST[currentKey].append(currentJSON)
					#print( HASHMAP )

					nextJSON 	= next(generator)
				except StopIteration:
					flag = False 
					break

			pickle.dump(HASHMAP, handle)
			numDumps = numDumps + 1
			print 'dumping %d' %numDumps
			HASHMAP = {}

		except StopIteration:
			flag = False 
			break

	handle.close()

	'''with open( outPutFile, 'rb') as handle:
		b = pickle.loads(handle.read())

	print HASHMAPTEST == b # True'''

#Execution Start...
main()
