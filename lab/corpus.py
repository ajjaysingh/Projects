# File Name			: corpus.py
# Description		: This creates a collection of words with their frequency
# Author			: Ajay
# Date				: 2016-11-19
#==================================================

import os, sys, pickle
from nltk.corpus import brown, movie_reviews, reuters, gutenberg, abc
from collections import Counter

w1 = gutenberg.words()
w2 = brown.words()
w3 = movie_reviews.words()
w4 = reuters.words()
w5 = abc.words()
ww = w1 + w2 + w3 + w4 + w5


WORDS = Counter(ww)

# print(len(Counter(w5)))
# print(len(WORDS))
os.chdir("/Users/chaser/Projects/Dictionary")
with open("corpus", 'wb') as corpora: #always use this because if opening of file fails the file will not get overwritten
    pickle.dump(WORDS, corpora)
