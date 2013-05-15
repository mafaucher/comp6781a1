#!/usr/bin/env python
# coding=utf-8
"""
main.py

DEPENDENCIES:
	nltk
	collocations.py

DESCRIPTION:

ISSUES:
	None

MODIFICATIONS:
"""

import argparse

parser = argparse.ArgumentParser(description="""
		""")
#parser.add_argument("-d", "--doc", action="store",
#		help="Display document with given DOC ID.")
#parser.add_argument("-q", "--query", action="store",
#		help="Query.")
#parser.add_argument("-c", "--corpus", action="store",
#		help="Define the corpus to index \
#				(default is ./corpora/reuters21578)")
#parser.add_argument("-i", "--index", action="store_true",
#		help="Overide previous index and reindex \
#				(default is False, unless CORPUS is specified then it is True)")
#parser.add_argument("-l", "--left", action="store",
#		help="Size of context window to retrieve before the token")
#parser.add_argument("-r", "--right", action="store",
#		help="Size of context window to retrieve after the token")
args = parser.parse_args()

# Define corpus
corpus =
if args.corpus:
	corpus = args.corpus
	args.index = True

# Index corpus or load index from disk
index = None
if args.index:
	index = invert(corpus)
else:
	index = loadIndex()
	if not index:
		index = invert(corpus)

# Display document
if args.doc:
	print "\n".join([read(corpus, int(docId)) for docId in args.doc.split()])



# Query mode
if args.query:

	# Define context window size (default is 10)
	L_WINDOW = int(args.left) if args.left else 5
	R_WINDOW = int(args.right) if args.right else 5
	
	# Tokenize query
	terms = set(tokenize(args.query))

	# Get list of documents with at least one query term
	results = []
	for term in terms:
		merge(results, [(posting, term) for posting in index[term]])
	
	# Score documents by TF-IDF
	docs = set([result[0].doc for result in results])
	scores = [index.tfidf(terms, doc) for doc in docs]
	docScores = {doc : score for (score, doc) in zip(scores, docs)}

	# Construct table of output
	table = [[docScores[result.doc], result.doc, result.pos, \
			" ".join(getPredList(index, term, result.doc, result.pos, L_WINDOW)), \
			term, \
			" ".join(getSuccList(index, term, result.doc, result.pos, R_WINDOW))] \
			for (result, term) in results]

	# display to STDOUT
	for row in sorted(table, reverse=True):
		print "\t".join([str(cell) for cell in row])
