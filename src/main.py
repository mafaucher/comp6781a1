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
import nltk.corpus
from nltk import bigrams, FreqDist
from sys import exit

from collocations import *

parser = argparse.ArgumentParser(description="""
		Show most used collocations in a corpus, using different measures.
		First show for all tokens, then filter by part of speech tags
		""")
parser.add_argument("-c", "--casefold", action="store_true",
		help="Apply case folding (ignore case).")
parser.add_argument("-s", "--stem", action="store_true",
		help="Apply Porter's stemmer.")
parser.add_argument("-f", "--filters", action="store",
		help='Specify a list of part of speech filters (default is "JN NN").')
parser.add_argument("-t", "--text", action="store",
		help="Specify a corpus included with NLTK (default is 'brown').")
parser.add_argument("-n", "--number", action="store",
		help="Limit the number of results (default is 50).")
args = parser.parse_args()

# Set options

if args.text:
	try:
		corpus = getattr(corpus, args.text)
	except AttributeError:
		print "Error: Corpus does not exist."
		exit(0)

if args.number:
	topn = int(args.number) if int(args.number) else topn

if args.casefold:
	options.append('cf')
if args.stem:
	options.append('stem')

if args.filters:
	filters = args.filters.split()

# Vocabulary
words = map(preprocess, corpus.words())
vocabulary = FreqDist(words)

# Collocations using all bigrams
bg = bigrams(words)                 # Get processed bigrams
bigramFreq = FreqDist(bg)
freqs.append(bigramFreq)

# Collocations filtered by part of speech
bg = bigrams(corpus.tagged_words()) # Get all tagged bigrams
bg = filter(posFilter, bg)          # Filter bigrams by POS
bg = map(rmPos, bg)                 # Remove tags
bg = map(preprocessBigram, bg)      # Process bigrams
posFreq = FreqDist(bg)
freqs.append(posFreq)

# Collocations using chi^2 test
#freqs.append(chi_sqTest(bigramFreq))
#freqs.append(chi_sqTest(posFreq))

compare()
