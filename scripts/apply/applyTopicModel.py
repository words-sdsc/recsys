# ======================================================
# FileName: applyTopicModel.py
# Description: applies the topic model file created by 
# language.cpp and calculates the topic distribution
# on another set of reviews.
# ======================================================


import sys
import gzip
import math
import random

def main():
	# Unpacking argv
	reviewPath = sys.argv[1] # Review to open
	modelPath  = sys.argv[2] # model to open

	# Opening files
	fileStream = gzip.open(reviewPath, 'rb') # review stream
	fileData = fileStream.read()             # parsed review data

	# At this point, we'll choose a random productID and calculate it's topic distribution
	print "Appending reviews..."

	counter = 0
	chosedID  = '' #randomly chosenID
	currentItemIndex = 0 #current product being visited in file
	allReviews = fileData.split('\n') # A line/ a review in the review file
	chosenItemIndex = random.randint(0, len(allReviews) )   #product index of the chosenID


	# Loop through all reviews until the randomly chosen product is found...
	for line in allReviews:
		if(counter == chosenItemIndex):
			elements = line.split(' ')
			chosenID = elements[1] # set chosenID to the productID (2nd element)
			break
		else:
			counter = counter + 1
	

	appendedR = [] # All reviews of the chosen product

	# Collecting/appending reviews of the chosen productID
	for line in allReviews:
		elements = line.split(' ')
		if len(elements) > 1 and chosenID == elements[1]:
			appendedR = appendedR + elements[7:]
	print "Appended reviews!"


	# Reporting how many topics were found it topic model
	numTopics = sum(1 for line in open(modelPath))
	print "Found %d topics in topic model" %numTopics

	# Open topic model
	savedModelStream = open(modelPath)
	savedModel =savedModelStream.read()

	#Spliting the model into topics
	topics = savedModel.split('\n')

	#RELEVANT VARS
	topicModelWords = []
	topicModel = {}
	counter = 0
	word = ''


    #FOR A GIVEN TOPIC, GET ITS WORDS AND FREQS

    #Loop though each topic distribution
	for model in topics:
		words = model.split()
		for token in words:
			#If the word
			if counter % 2 != 1 or counter == 0:
				word = token
				#APPEND ITS FREQ TO THE VOCABULARY LIST FOR THE FIRST TIME
				if word not in topicModelWords:
					topicModelWords.append( word )
					topicModel[word] = []
			#append its freq to the vocabulary list
			else:
				topicModel[word].append(token)
			counter = counter + 1

	print "Loaded topic model!"
	print topicModel

	print "Applying topic model to appended reviews"
	topicDist = [0,0,0,0,0]
	a = []
	print "Current topic distribution: %r" % topicDist
	for word in appendedR:
		try:
			row = [ float(x) for x in  topicModel[word] ]
			for index in range (0,5):
				topicDist[index] = topicDist[index] + row[index]
			#topicDist = [ math.exp(x) for x in topicDist]
			#denominator = sum(topicDist)
			#topicDist = [ float(x/denominator) for x in topicDist ]
			print "Current topic distribution: %r" % topicDist
		except Exception:
			a.append(word)

	topicDist = [ math.exp(x) for x in topicDist]
	denominator = sum(topicDist)
	topicDist = [ float(x/denominator) for x in topicDist ]

	# Reporting final status
	print "Chosen id was %s" % chosenID
	print "Final topic distribution %r" % topicDist
	print "Distribution adds up to %d" % sum(topicDist)

#START EXECUTION
main()
