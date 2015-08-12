''' 
================================ FILE HEADER ==================================
Author        : David Justo 
Last Modified : July 21st 2015
File Name     : subCategoryFinder.py
Purpose       : To construct subDatasets of Julian McAuley's Amazon dataset 
===============================================================================
'''

# IMPORTING DEPENDENCIES
import sys                       # Command line argument detection
import gzip                      # For opening gzip compressed files 
import random                    # For random number generation
import os                        # For I/O
import pickle #For object serialization into files

from operator import itemgetter  

#AT LEAST 1100, AT THE MINIMUM

# START OF VARIABLE DECLARATION ... 

#  GLOBAL VARIABLE(S)
CATEGORY_THRESHOLD = 0; # Minimum number of products per category

# Constant strings
TITLE_STRING        = "SUB-CATEGORY SCRIPT FOR SDSC WORKFLOWS"
DIVIDER_STRING      = "\n=======================================\n"
OPENING_FILE_STRING = "Opening the following file: "
OPTIONS_STRING      = ("OPTIONS: Exactly %d output files will be produced.\n"
                      "Each with aprox %d reviews per product.")

# Non-constants global variables
numItemsCategory  = {}
orderedCateg      = []
categoryHierarchy = {}

# START OF FUNCTION DELCARATIONS ... 

''' 
============================= FUNCTION HEADER =================================
Name        : parse
Purpose     : To parse the '.json.gz' file one line (or json) at a time into a
              string
Arguments   : path - string path of the '.json.gz' file
Description : Read one line at a time with a generator
Output      : The '.next()' method of the generator will output one line of the
              file at a time. In Julian's dataset, this equates to one json at
              a time
===============================================================================
'''
def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield eval(l)

''' 
============================= FUNCTION HEADER =================================
Name        : outputFiles()
Purpose     : To output the sub-category datasets
Arguments   : CategArray - Array of the random categories and subcategories 
              selected for output
Description : At first we create the output directory in the directory of 
              execution. We then loop through the CategArray categories, create
              a writting stream to a file named after each category and dump
              the raw data of each category's product ids in their 
              corresponding files. 
Output      : raw data of each category inside the output directory
===============================================================================
'''

def outputFiles( CategArray, FILENAME ):

	with open(FILENAME, 'rb') as handle:
		b = pickle.loads(handle.read())

	currentDir = os.getcwd()                  #current directory path
	newDir     = currentDir + "/OUTPUT"       #path of output directory
	os.makedirs( newDir )                     #create direcetory path


	'''Looping through all sub-categories selected, creating files for them
	   inside OUTPUT dir and writting the raw data of each category in them.'''

	for category in CategArray: 
		filename   = newDir + '/subCateg_'+category+'.json.gz'
		targetFile = gzip.open(filename, 'wb')
		for idVal in numItemsCategory[category]:
			try:
					for json in b[idVal]:
						targetFile.write(str(json))
						targetFile.write('\n')
			except:
				continue
		targetFile.close()

''' 
============================= FUNCTION HEADER =================================
Name        : updateDicts()
Purpose     : To populate the numItemsCategory dictionary with the ids that
              correspond with each category key.
Arguments   : 1.) categoriesArr - Array with all categories in the meta-data
              2.) id            - id that maps to all categories
Output      : The global variable named numItemsCategory is populated as a 
              dictionary where each key is a category mapped to an array with
              all the product ids that correspond to that category
===============================================================================
'''

def updateDicts( categoriesArr, id ):

	for category in categoriesArr:
		if category in numItemsCategory:             #If this the category key
			(numItemsCategory[category]).append(id)  #exists, just append id
		else:
			numItemsCategory[category] = []          #Else, initialize id array
			(numItemsCategory[category]).append(id)

''' 
============================= FUNCTION HEADER =================================
Name        : binarySearch()
Purpose     : To truncate the orderedList such that the categories with less
              reviews than the threshold are eliminated
Arguments   : 1.) orderedList - An array of tuples (Category,[id1,id2...idx])
              that has been ordered ascendingly by the number of items in the 
              second element of the tuple
              2.) threshold   - The minimum amount of products per category in
              order to have, as an average, the minimum amount of reviews
              specificied through the terminal
Description : A classic binary search implementation is used to find where to 
              truncate the array.
Output      : The truncated orderedList
===============================================================================
'''

def binarySearch( orderedList, threshold ):

	first = 0                  # Leftmost index to search at
	last = len(orderedList)-1  # Rightmost index to search at
	found = False              # Flag to check if point of truncation was found

	while first <= last and not found:
		midpoint   = (first+last)//2
		currentLen = len(orderedList[midpoint][1])

		if( currentLen <= threshold and 
		len(orderedList[midpoint+1][1]) > threshold):

			index = midpoint
			found = True
		else:
			if( threshold < currentLen):
				last = midpoint-1
			else:
				first = midpoint+1

	#Truncate array and return it
	orderedList[0:midpoint] = []   
	return orderedList
			
''' 
============================= FUNCTION HEADER =================================
Name        : constructCategTree()
Purpose     : To construct the category tree 
Arguments   : orderedList - An array of tuples (Category,[id1,id2...idx])
              that has been ordered ascendingly by the number of items in the 
              second element of the tuple
Description : Starting from the end of the array, we compare the current entry
              with the previous one and determine if the ids in the previous
              are all contained within the current entry. If so, then the
              current entry is a superset of the previous one. Else, they
              are both at the same level of 'deepness' in the tree. 
              We repeat this process to determine the category tree, which is 
              constructed as nested dictionaries
===============================================================================
'''

def constructCategTree( sortedArray ):

	currentIndex = len(sortedArray) -1           #index of entry being compared
	currentCateg = sortedArray[currentIndex][0]  #categ of entry being compared
	currentLevel = categoryHierarchy             #current depth in 
	                                             #categoryHierarchy

	'''Set last entry in sortedArray to be part of the biggest categories by
	   default, also pop it from the array '''

	categoryHierarchy[sortedArray[currentIndex][0]] = {} 
	sortedArray.pop()

	# loop through all entries in the array 
	while( currentIndex > 0 ):

		reset = True    #Reseting means to compary against the outer most layer
						#of category the tree

		#Printing current category tree for debugging purposes
		print( '============================')
		print( categoryHierarchy )
		print( '============================')

		# Cast array of ids as set
		smallerSet = set(numItemsCategory[currentCateg])	

		#For all categories at the current 'deepness' level in the tree
		for probableParent in currentLevel.keys():
			#We cast each category in the current 'deepness' level as a set
			biggerSet = set(numItemsCategory[probableParent])

			'''If the set of products on the current array entry is contained
			   within the set of one of the categories in the category tree'''
			if( smallerSet.issubset(biggerSet) ):
				''' go one level deeper into that category to compare against
				    its subcategories '''
				currentLevel = currentLevel[probableParent]
				reset = False  #No reset because won't be comparing against
				break          #the outer most layer of the tree

		'''To reset is to compare against the outer most layer of the tree in
		   the iteration of the while loop. It also means that we found the 
		   appropiate place for the previous entry in the array '''

		if(reset):

			'''Set the subCategories of the already allocated category in the 
			tree to nothing '''
			currentLevel[currentCateg] = {}   
			
			#Take out already allocated category from the array
			sortedArray.pop()

			#set the next category to allocate in the tree
			currentIndex = len(sortedArray) -1 
			currentCateg = sortedArray[currentIndex][0]

			#Set current deepness to the outer-most layer of the tree
			currentLevel = categoryHierarchy  

''' 
============================= FUNCTION HEADER =================================
Name        : main()
Purpose     : To direct the execution of the program
===============================================================================
'''

def main():

	#Parsing command-line arguments
	FILE_TO_OPEN       = sys.argv[1]      # Meta-data file to read
	CATEGORY_THRESHOLD = int(sys.argv[2]) # How many reviews per output category
	HOW_MANY_FILES     = int(sys.argv[3]) # How many subCategories to output
	PRE_PROCESS_FILE   = sys.argv[4]

	# Prompting user of selected options
	print( DIVIDER_STRING + TITLE_STRING +  DIVIDER_STRING        )
	print( OPENING_FILE_STRING + FILE_TO_OPEN                     )
	print( OPTIONS_STRING ) % (HOW_MANY_FILES, CATEGORY_THRESHOLD )

	#Parsing meta-data file with a generator
	generator = parse(FILE_TO_OPEN)

	while True:  #Keep on reading until no more lines can be parsed
		try:
			currentJSON = next(generator)
			updateDicts( (currentJSON['categories'][0]), currentJSON["asin"]  )
		except StopIteration: #Whenever there's no more jsons to read in file
			break

	

	''' We sort the numItemsCategory dictionary ascendingly based on the amount
	of ids in the array that's associated with each category '''
	orderedCateg   = sorted([(k,v) for k,v in numItemsCategory.items()], 
		             key=lambda _: len(_[1]))

	''' We locate the start of the categories that are above the review 
	threshold and truncate the array at that point '''
	truncatedArray = binarySearch( orderedCateg, CATEGORY_THRESHOLD )

	# We construct the category tree based on the truncated array
	constructCategTree( truncatedArray )
	print numItemsCategory

	print( "**************************************************************")
	print( "               SELECTING CATEGORIES TO OUTPUT                 ")
	print( "**************************************************************")

	#Select output categories
	outputTree = selectOutputCategs( HOW_MANY_FILES )
	

	print "\n###############################################################\n"
	print "                       OUTPUTING FILES"
	print "#################################################################\n"

	#Output files based on selected categories
	outputFiles( outputTree, PRE_PROCESS_FILE)



def selectOutputCategs( HOW_MANY_FILES ):
	remainingFiles   = HOW_MANY_FILES	#Number of categories to be selected
	currentLevel     = categoryHierarchy.keys()
	currentDepth     = categoryHierarchy
	currentPath      = []
	outputTree       = []
	KeysUsedPerLevel = []
	depthIndex       = 0
	categorySequence = []

	KeysUsedPerLevel.append([])

	currentPath.append(categoryHierarchy)

	while remainingFiles > 0:

		print 'There are %d files remaining'            %remainingFiles
		print 'Our current level has these options  %r' %currentLevel

		numKeys       = len(currentLevel)

		try:
			selectedIndex = random.randint(0,len(currentLevel)-1)
		except ValueError:
			depthIndex     = depthIndex - 1
			currentPath.pop()
			currentDepth   = currentPath[depthIndex]
			currentLevel   = currentDepth.keys()
		print selectedIndex

		print currentLevel
		print currentDepth is categoryHierarchy
		print KeysUsedPerLevel
		print depthIndex
		print range(0, numKeys) 
		print range(0, numKeys) in KeysUsedPerLevel[depthIndex]
		if(currentDepth is categoryHierarchy  and 
			( range(0, numKeys) in KeysUsedPerLevel[depthIndex] or
			  range(0, numKeys) == [] ) ):
			break


		elif( range(0, numKeys) in KeysUsedPerLevel[depthIndex] or
			len(currentLevel) == 1 
			and selectedIndex in KeysUsedPerLevel[depthIndex]) :
			depthIndex   = depthIndex -1
			currentPath.pop()
			currentDepth = currentPath[depthIndex]
	
		elif( selectedIndex not in KeysUsedPerLevel[depthIndex] ):
			KeysUsedPerLevel[depthIndex].append(selectedIndex)

			selectedCateg  = currentLevel[selectedIndex]
			depthIndex     = depthIndex + 1
			remainingFiles = remainingFiles -1
			currentDepth   = currentDepth[selectedCateg]
			currentPath.append( currentDepth )
			currentLevel   = currentDepth.keys()

			outputTree.append(selectedCateg)
			KeysUsedPerLevel.append([])


	return outputTree


# BEGINNING OF EXECUTION
main()


