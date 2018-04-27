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
os.system("rm initial_files/words_with_frequency/*")
os.system('cp [A-Z] initial_files/words_with_frequency/')

def printWords(charc='1'): # '1' means print words starting with all alphabets
    # print(charc)
    # exit(5)
    totalWords = 0
    wordList = []
    for f in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        WORDS = Counter()
        normalWords = []
        with open(f, 'r') as dictFile:
            normalWords = dictFile.read().split()
            WORDS = Counter(normalWords)
        fileNameZero = "initial_files/words_without_frequency/" + f
        with open(fileNameZero, 'w+') as zeroFile:
            normalWords = list(set(normalWords))
            normalWords.sort()
            for w in normalWords:
                zeroFile.write(w + "\n")
        if charc == '1' or charc.lower() == f.lower():
            totalWords = totalWords + len(WORDS)
            print(f + " has " + str(len(WORDS)))
            noOfWordsInLine = 0
            for key, value in WORDS.most_common():
                if noOfWordsInLine == 9:
                    print("")
                    noOfWordsInLine = 0
                # print("{:15}-{} {}".format(key, value, "\t") ,end='') # 6 words per line
                print("{:20} ".format(key) ,end='')   # 9 words per line
                keyValueCombined = str(value) + key
                wordList.append(str(keyValueCombined))
                noOfWordsInLine = noOfWordsInLine + 1
            print('\n\n')
    
    wordList.sort()
    
    os.chdir("/Users/chaser/Projects/Dictionary/initial_files/")
    with open("allWords.txt", 'w+') as wordsAll:
        for word in wordList:
            wordsAll.write("\"" +  word + "\"" + "\n")
    
    print("Total words : " + str(totalWords))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        printWords(str(sys.argv[1]))  # argument can be the alphabet whose words you want to print
    else:
        printWords()