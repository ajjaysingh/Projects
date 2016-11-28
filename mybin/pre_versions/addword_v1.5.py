#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name			: addword.py
# Description		: This is the new repository of the words that I encounter daily. It will just store the word to a file.
#                     You can enter the new word like ./addword.py WORD  or ./addword.py and then entering at the prompt
# Author			: Ajay
# Date				: 2016-11-20
# Python Version	: 3
#==================================================


import re, os, pickle, sys
from collections import Counter


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

def check(word):
    correct = correction(word)
    if word == correct:
        print(correct)
        return word
    else:
        print("The word \""+ word +"\" should have been > " + correct)
        decide = input("Press 'y' if you want to change\n\t 'n' if continue with the same word.")
        if decide == 'y':
            return correct
        else:
            return word

def addTheWord():
    try:
        temp_name = ".myWords" #name of the temporary duplicate file in case some exception occurs
        os.system("cp "+ "myWords "+ temp_name)
        with open("myWords", 'a') as dictionary: #always use this because if opening of file fails the file will not get overwritten
            if len(sys.argv) > 1:
                i = 1
                while i < len(sys.argv):
                    new_word = check(str(sys.argv[i]))
                    dictionary.write("\t")
                    dictionary.write(new_word.lower())
                    i = i + 1
            else:
                new_word = input("Enter the word : ")
                dictionary.write("\t")
                dictionary.write(new_word.lower())



    except:
        files = os.listdir()
        if temp_name in files:
            os.system("cp " + temp_name + " myWords")
            print("try agian!")

    finally:                                            # always executed whether try suceeds or not
        files = os.listdir()
        if temp_name in files:
            os.system("rm " + temp_name)

def sortIt():
    try:
        temp_name = ".myWords" #name of the temporary duplicate file in case some exception occurs
        os.system("cp "+ "myWords "+ temp_name)
        previousWords = []
        with open("myWords", 'r+') as dictionary: #always use this because if opening of file fails the file will not get overwritten
            previousWords = sorted(dictionary.read().split())
        # print(type(previousWords))
        with open("myWord_sorted", 'w+') as dictionary: #always use this because if opening of file fails the file will not get overwritten
            prev = 'a'
            for w in previousWords:
                dictionary.write(w.lower())
                dictionary.write("\n")

    except:
        files = os.listdir()
        if temp_name in files:
            os.system("cp " + temp_name + " myWords")
            print("try agian!")

    finally:                                            # always executed whether try suceeds or not
        files = os.listdir()
        if temp_name in files:
            os.system("rm " + temp_name)

# returns the words from a list beginning with the specified character 'char'
def getWords(wordList, char):
    filteredList = [word for word in wordList if word[0] == char]
    return filteredList

# seperates the myWord file
def seperateFiles():
    try:
        temp_name = ".myWords" #name of the temporary duplicate file in case some exception occurs
        os.system("cp "+ "myWords "+ temp_name)
        previousWords = []
        with open("myWords", 'r+') as dictionary: #always use this because if opening of file fails the file will not get overwritten
            previousWords = sorted(dictionary.read().split())
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            filteredList = getWords(previousWords, char.lower())
            with open(char, 'w+') as dictFile:
                for w in filteredList:
                    dictFile.write(w.lower())
                    dictFile.write("\n")


        # with open("myWord_sorted", 'w+') as dictionary: #always use this because if opening of file fails the file will not get overwritten
        #     prev = 'a'
        #     for w in previousWords:
        #         dictionary.write(w.lower())
        #         dictionary.write("\n")

    except:
        files = os.listdir()
        if temp_name in files:
            os.system("cp " + temp_name + " myWords")
            print("try agian!")

    finally:                                            # always executed whether try suceeds or not
        files = os.listdir()
        if temp_name in files:
            os.system("rm " + temp_name)

if __name__ == '__main__':
    # addTheWord()
    # sortIt()
    seperateFiles()
