import sys # Command line argument detection
import gzip #For opening gzip compressed files 
import pickle #For object serialization into files

HASHMAP = {}

#Constant strings
DONE_STRING        = "Done writting to file: %s"
START_WRITE_STRING = "Writing to file: %s"

def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield eval(l)


def main():
	#Parsing file to read
	fileToParse = sys.argv[1]
	outPutFile  = 'PRE-PROCESSED_' + fileToParse[10:]

	generator = parse(fileToParse)

	while True:
		try:
			currentJSON = next(generator)
			currentKey = currentJSON['asin']

			if( currentKey in HASHMAP ):
				HASHMAP[currentKey].append(currentJSON)
			else:
				HASHMAP[currentKey] = []
				HASHMAP[currentKey].append(currentJSON)
			print( HASHMAP )
		except StopIteration:
			break

	with open( outPutFile , 'wb') as handle:
		pickle.dump(HASHMAP, handle)

	'''with open('file.txt', 'rb') as handle:
		b = pickle.loads(handle.read())'''

	#print HASHMAP == b # True

#Execution Start...
main()