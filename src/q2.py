import os

from nltk import *
from nltk.corpus import brown
from nltk.collocations import *

topic1 = 'talk.politics.mideast'
topic2 = 'sci.crypt'
topn = 50
filters = ['JN', 'NN']

def readCorpus(topic):
	dirpath = os.path.join(os.path.dirname(__file__), '..', 'data', '20_newsgroups', topic)
	words = []
	for path, dirs, files in os.walk(dirpath):
		for f in files:
			with open(os.path.join(path, f)) as infile:
				body = False
				for line in infile.readlines():
					if body:
						words.extend(tokenize.word_tokenize(line))
					elif line[:5] == "Lines":
						body = True
	return words

def resetBigrams(grams):
	return collocations.BigramCollocationFinder.from_words(grams)

def posFilter(taggedBigram):
	bg, score = taggedBigram
	w1, w2 = bg
	if w1[1][0] + w2[1][0] in filters:
		return True
	return False

def test(finder, freq):
	print("")
	print("Raw Frequency:")
	display(finder, freq, measures.raw_freq)
	print("")
	print("Student's T Test:")
	display(finder, freq, measures.student_t)
	print("")
	print("Chi Squared Test:")
	display(finder, freq, measures.chi_sq)

def display(finder, freq, measure, n=topn):
	results = finder.nbest(measure, n*100)
	results = [(result, finder.score_ngram(measure, *result))\
			for result in results]
	if not results: return
	if type(results[0][0][0]) is tuple:
		results = filter(posFilter, results)[:n]
		print "\n".join([str(freq[result[0]])+"\t"+"%f"%result[1]\
				+"\t"+result[0][0][0]+" "+result[0][1][0] for result in results])
	else:
		results = results[:n]
		print "\n".join([str(freq[result[0]])+"\t"+"%f"%result[1]\
				+"\t"+result[0][0]+" "+result[0][1] for result in results])

measures = collocations.BigramAssocMeasures()

## CORPUS 1
# No POS filtering
print "Corpus 1:", topic1
print "Without part-of-speech filtering"
print ""
corpus1 = readCorpus(topic1)
finder1 = resetBigrams(corpus1)
freq1 = FreqDist(bigrams(corpus1))
test(finder1, freq1)

print ""
print "With part-of-speech filtering"
print ""
# With POS filtering
tags1 = pos_tag(corpus1)
finder1 = resetBigrams(tags1)
bigrams1 = bigrams(tags1)
freq1 = FreqDist(bigrams1)
test(finder1, freq1)

print ""
print ""
print "Corpus 2:", topic2
print "Without part-of-speech filtering"
print ""
## CORPUS 2
# No POS filtering
corpus2 = readCorpus(topic2)
finder2 = resetBigrams(corpus2)
freq2 = FreqDist(bigrams(corpus2))
test(finder2, freq2)

print ""
print "With part-of-speech filtering"
print ""
# With POS filtering
tags2 = pos_tag(corpus2)
finder2 = resetBigrams(tags2)
bigrams2 = bigrams(tags2)
freq2 = FreqDist(bigrams2)
test(finder2, freq2)
