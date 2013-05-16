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
from sys import exit

from collocations import *

parser = argparse.ArgumentParser(description="""
		""")
parser.add_argument("-r", "--raw", action="store_true",
		help="Use raw tokens without preprocessing.")
parser.add_argument("-c", "--casefold", action="store_true",
		help="Ignore case when processing tokens.")
parser.add_argument("-l", "--lemma", action="store_true",
		help="Use raw tokens without preprocessing.")
parser.add_argument("-p", "--posfilter", action="store_true",
		help='Filter bigrams by part of speech.')
parser.add_argument("-f", "--filters", action="store",
		help='Specify a list of part of speech filters (default is "JN NN").')
parser.add_argument("-t", "--text", action="store",
		help="Specify a corpus included with NLTK (default is 'brown').")
parser.add_argument("-n", "--number", action="store",
		help="Limit the number of results (default is 50).")
args = parser.parse_args()

# Get collocation types
options = []

if args.casefold:
	options.append('cf')
if args.lemma:
	options.append('lemma')

filters = ["JN", "NN"]
if args.posfilter or args.filters:
	options.append('pos')
	if args.filters:
		filters = args.filters.split()
		# TODO: remove .dat file

if args.raw or not options:
	options.append('raw')

# Load corpus
corpus = "brown"
if args.text:
	try:
		getattr(corpus, args.text)
		corpus = args.text
	except AttributeError:
		print "Error: Corpus does not exist."
		exit(0)

topn = 50 if not args.number else int(args.number)

show(options, corpus, topn)
