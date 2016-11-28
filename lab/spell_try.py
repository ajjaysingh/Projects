# File Name			: spell_try.py
# Description		: try run for norvig spell.py
# Author			: Ajay
# Date				: 2016-11-19
#==================================================
import re, os, pickle
from collections import Counter

# def words(text): return re.findall(r'\w+', text.lower())
# WORDS = Counter(words(open('big.txt').read()))

# import nltk
# from nltk.corpus import brown
# WORDS = Counter(brown.words())

WORDS = Counter()
os.chdir("/Users/chaser/Projects/Dictionary")
with open("corpus", 'rb') as corpora:
    WORDS = pickle.load(corpora)

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))



''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''
import urllib.request
def find(x):
    srch=str(x)
    x=urllib.request.urlopen("http://dictionary.reference.com/browse/"+srch+"?s=t")
    x=x.read().decode('utf-8')
    items=re.findall('<meta name="description" content="'+".*$",x,re.MULTILINE)
    for x in items:
        y=x.replace('<meta name="description" content="','')
        z=y.replace(' See more."/>','')
        m=re.findall('at Dictionary.com, a free online dictionary with pronunciation,              synonyms and translation. Look it up now! "/>',z)
        if m==[]:
            if z.startswith("Get your reference question answered by Ask.com"):
                print("Word not found! :(")
            else:
                print(z)
    else:
            print("Word not found! :(")
# x=raw_input("Enter word to find: ")




# print(correction('speling'))
find(correction('speling'))
print(correction('korrectud'))
print(correction('those'))
print(correction('thos'))
print(correction('hes'))


print(candidates('Deomcray'))

find('defiance')



