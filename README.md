# ================================= 
# SDSC - RECSYS PROJECT - README
# =================================

## PROJECT DESCRIPTION: This project attempts to create a recommender system based of the research of Julian McAuley.

## DESCRIPTION OF FILES:

### 1. language.cpp and it's dependencies in the directory '/code_RecSys13':
This is julian McAuley's unmodified topic modeling code. It's written in C++. It takes as input a compressed (.gz) file containing
a set of reviews. It prints to the terminal the top found words in all 5 topics. Before runnign it, make sure to export the following:
"export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD/liblbfgs-1.10/lib/.libs/". Compile with 'make'. To run, use: ./train <inputFile>. 
An example input is is provided: Arts.votes.gz.

### 2. subCategoryFinder.py and it's dependency jsonToHash.py in the directory 'scripts/subCategoryFinder':
This is the code that creates the subCategory tree structure. It takes as input a file of reviews, its metadata, the threshold of
how many reviews should be included on a subset of reviews to be considered a category and how many sub-category files should be outputed from
the tree. Note that these files are outputed in a folder named '/OUTPUT' which will be created every time the code is runned. If the code fails,
it might be cause you have to deleted the '/OUTPUT' sub-folder from the directory. 

To run, use 'python subCategoryFinder <ReviewsToOpen.json.gz> <CategoryThreshold> <HowManyReviewFilesToOutput> <MetaDataToOpen.json.gz>'.

### 3. applyTopicModel.py in the directory 'scripts/apply':
This is the python code that takes the topic model outputed by language.cpp and applies it to a specific product in a set of
reviews. Run it like so: python applyTopicModel.py <Reviews.gz> <model.txt> . It will print the detected topic distribution
to the terminal.

### 4. language.cpp in the directorty '/code_copy'
This is the modified version of Julian McAuleys' topic modeling code. It outputs a topic model file named savedModel.txt that
can be read by 'applyTopicModel.py'.
