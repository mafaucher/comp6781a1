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

from nltk import bigrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.tag import pos_tag


DIR_ROOT = path.join(path.dirname(__file__), '..')
DIR_DATA = path.join(DIR_ROOT, "data")

if not path.exists(DIR_DATA):
	makedirs(DIR_DATA)

POSSIBLE = ["raw", "cf", "lemma", "tok"]

def show(freqNames, corpus, topn):
	"""

	"""
	for name in freqNames:
		assert name in POSSIBLE
	freq = [None] * len(freqNames)
	# Calculate frequencies or load precalculated frequencies
	for i in range(len(freqNames)):
		filename = path.join(DIR_DATA, corpus+"_"+freqNames[i]+".dat")
		try:
			freq[i] = pickle.load(open(filename))
		except IOError:
			freq[i] = collocations(freqNames[i], getattr(nltk.corpus, corpus))
			pickle.dump(freq[i], open(filename, 'w'))
		finally:
			assert freq[i]

	# Create a table to compare top collocations
	compare(freq, topn)


def collocations(type, corpus):
	"""
	Calculates collocations using a method type.
	"""
	if type == "raw":
		bg = bigrams(corpus.words())
		return FreqDist(bg)
	if type == "cf":
		bg = bigrams(map(str.lower, corpus.words()))
		return FreqDist(bg)
	if type == "lemma":
		l = WordNetLemmatizer()
		bg = bigrams(map(l.lemmatize, corpus.words()))
		return FreqDist(bg)
	if type == "tk":
		bg = bigrams(corpus)
	if type == "pos":
		# FIXME: filters are a mess...
		bg_raw = bigrams(corpus.tagged_words())
		bg_pos = filter(lambda x: x[0][1][0]+x[1][1][0] in filters, bg_raw)
		bg = [(w1[0], w2[0]) for (w1, w2) in bg_pos]
		return FreqDist(bg)
	return None


def compare(lists, topn=50):
	"""
	Create a table 
	"""
	for vals in zip(*(lists + [range(topn)])):
		row = ["|"]
		for (v, l) in zip(vals, lists):
			row.extend([str(l[v]), v[0], v[1], "|"])
		print "\t".join(row)
