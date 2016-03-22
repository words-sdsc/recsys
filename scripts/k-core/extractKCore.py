import networkx as nx
from sys import argv
import linecache
from sets import Set
import gzip
import pickle
import pyfora

#ufora = pyfora.connect("http://52.53.229.96:3000")


def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield eval(l)

def get_k_core(reviews_path,k_val):
	# Report start of process
	print "=================================="
	print "EXTRACTING K-CORE OF PID GRAPH    "
	print "=================================="

	print "AT STEP #1: Determine which reviewer reviewed which products"
#	with ufora.remotely.downloadAll():
	(PID_to_lines,PID_to_reviewerID) = get_PID_facts(reviews_path)	

	print "At STEP #2: Created weighted edges"
#	with ufora.remotely.downloadAll():
	weighted_edges = get_weighted_edges(PID_to_reviewerID)

	print "AT STEP #3: Create PID graph structure"
#	with ufora.remotely.downloadAll():
	PID_graph = create_graph(PID_to_reviewerID,weighted_edges)	
	print nx.info(PID_graph)	

	print "AT STEP #4: Extracting K-core"
#	with ufora.remotely.downloadAll():
	k_core_graph = nx.k_core(PID_graph,k_val)
	print nx.info(k_core_graph)
	pickle.dump(graph,open("graph",'w'))
	
	print "DONE!"

# OPTIMIZE
def get_weighted_edges(reviewers):
	weighted_edges = []
	keys = reviewers.keys()
	total = len(keys)
	counter = 0
	for index in range(0,len(keys)):
		counter = counter +1
		if( counter == 300):
			break
		print "** "+str(counter)+"/"+str(total)
		PID = keys[index]
		curr_reviewers = Set(reviewers[PID])
		for index2 in range(index, len(keys)):
			comp_PID = keys[index2]
			comp_reviewers = set(reviewers[comp_PID])
			intersection = curr_reviewers.intersection(comp_reviewers)
			if(len(intersection) > 1):
				edge = (PID,compare_PID,{"weight":len(intersection)})
				weighted_edges.append(edge)
	return weighted_edges

def create_graph(PID_to_reviewerID,weighted_edges):
	graph = nx.Graph()
	
	#Adding vertices
	vertices = PID_to_reviewerID
	graph.add_nodes_from(vertices)

	#Adding edges
	graph.add_edges_from(weighted_edges)
	return graph

def get_PID_facts(file_path):
	PID_to_reviewerID = {}
	PID_to_lines = {}
	
	gen_reviews = parse(file_path)
	for review_JSON in gen_reviews:
		PID = review_JSON["asin"]
		reviewerID = review_JSON["reviewerID"]

		if PID not in PID_to_lines.keys():
			PID_to_reviewerID[PID] = []
		PID_to_reviewerID[PID].append(reviewerID)

	return (PID_to_lines,PID_to_reviewerID)

def set_review_threshold(k_val,nodes):
	Graph = nx.Graph()
	G.add_nodes_from(nodes)
	G.add_eges
	k_core_graph = nx.k_core(Graph,k_val)
	return k_core_graph

def main():
	reviews_path = argv[1]
	min_edges = argv[2]
	get_k_core(reviews_path,min_edges)

# Standalone execution start
if __name__ == "__main__":
	main() #Start standalone execution
