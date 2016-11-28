#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name         : mywords.py
# Description       : Shows the words that are most frequently appearing in my Dictionary
# Author            : Ajay
# Date              : 2016-11-21
# Python Version    : 3
#==================================================


import sys, os
from collections import Counter

os.chdir("/Users/chaser/Projects/Dictionary")

def printWords(charc='1'):
    totalWords = 0
    for f in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        WORDS = Counter()
        with open(f, 'r') as dictFile:
            WORDS = Counter(dictFile.read().split())
        if charc == '1' or charc.lower() == f.lower():
            totalWords = totalWords + len(WORDS)
            print(f + " has " + str(len(WORDS)))
            for key, value in WORDS.most_common():
                print(key, value, "\t" ,end='')
            print('\n\n')
    print("Total words : " + str(totalWords))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        printWords(str(sys.argv[1]))
    else:
        printWords()