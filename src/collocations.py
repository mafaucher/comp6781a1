#!/usr/bin/env python
# coding=utf-8
"""
collocations.py

DEPENDENCIES:
	nltk
	nltk.corpus.brown

DESCRIPTION:

ISSUES:
	None

MODIFICATIONS:

Copyright (c) 2013, Marc-André Faucher
"""

import os.path as path
from os import makedirs as makedirs
import pickle

import nltk.corpus

from nltk import bigrams, FreqDist
from nltk.stem.porter import PorterStemmer
from nltk.tag import pos_tag
from nltk.metrics.association import BigramAssocMeasures

chi_sq = BigramAssocMeasures.chi_sq

# TODO: remove paths if not needed
# PATHS

DIR_ROOT = path.join(path.dirname(__file__), '..')

POSSIBLE = ["cf", "stem"]

# DEFAULT OPTIONS

options = []
filters = ['JN', 'NN']
topn = 50
corpus = nltk.corpus.brown
stemmer = PorterStemmer()

# List of frequency distributions
freqs = []

def posFilter(taggedBigram):
	"""
	Return bigram frequency distribution filtered by part of speech tag filters.
	"""
	w1, w2 = taggedBigram
	if w1[1][0] + w2[1][0] in filters:
		return True
	return False

def rmPos(taggedBigram):
	"""
	remove part of speech tag from bigram terms.
	"""
	w1, w2 = taggedBigram
	return (w1[0], w2[0])

def preprocess(token):
	"""
	Apply preprocessing options to token
	"""
	if "cf" in options:
		token = str.lower(token)
	if "stem" in options:
		token = stemmer.stem(token)
	return token

def preprocessBigram(bigram):
	"""
	Apply preprocessing options to bigram
	"""
	if "cf" in options:
		bigram = (str.lower(bigram[0]), str.lower(bigram[1]))
	if "stem" in options:
		bigram = (stemmer.stem(bigram[0]), stemmer.stem(bigram[1]))
	return bigram

def getPremarginal(collocations, token):
	"""
	Get the number of times the given token occurs in the first position of
	the bigram.
	"""
	bgs = filter(lambda x: x[0] == token, collocations)
	marginal = sum([collocations[bigram] for bigram in bgs])
	return marginal

def getPostmarginal(collocations, token):
	"""
	Get the number of times the given token occurs in the first position of
	the bigram.
	"""
	bgs = filter(lambda x: x[1] == token, collocations)
	marginal = sum([collocations[bigram] for bigram in bgs])
	return marginal

def chi_sqTest(collocations):
	results = {}
	n = collocations.N()
	for bigram in collocations:
		marginals = (getPremarginal(collocations, bigram[0]), \
				     getPostmarginal(collocations, bigram[1]))
		results[bigram] = chi_sq(collocations[bigram], marginals, n)
	return results

def compare(n=topn):
	"""
	Create a table 
	"""
	for vals in zip(*(freqs + [range(topn)])):
		row = ["|"]
		for (v, f) in zip(vals, freqs):
			row.extend([str(f[v]), v[0], v[1], "|"])
		print "\t".join(row)
