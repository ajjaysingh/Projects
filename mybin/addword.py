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

def sortIt(file_name):
    try:
        temp_name = "." + file_name #name of the temporary duplicate file in case some exception occurs
        os.system("cp "+ file_name + " " + temp_name)
        previousWords = []
        with open(file_name, 'r+') as dictionary: #always use this because if opening of file fails the file will not get overwritten
            previousWords = sorted(dictionary.read().split())
        with open(file_name, 'w+') as dictionary: #always use this because if opening of file fails the file will not get overwritten
            for w in previousWords:
                dictionary.write(w.upper())
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

def addToCorrespondingFiles(wordList):
    for l in wordList:
        if len(l) > 1:
            try:
                file_name = l[0]
                temp_name = "." + file_name #name of the temporary duplicate file in case some exception occurs
                os.system("cp "+ file_name + " " + temp_name)
                with open(file_name, 'a') as dictionary: #always use this because if opening of file fails the file will not get overwritten
                    i = 1
                    while i < len(l):
                        new_word = str(l[i])
                        dictionary.write(new_word.upper())
                        dictionary.write("\n")
                        i = i + 1
                sortIt(file_name)

            except:
                files = os.listdir()
                if temp_name in files:
                    os.system("cp " + temp_name + " " + file_name)
                    print("try agian!")

            finally:                                            # always executed whether try suceeds or not
                files = os.listdir()
                if temp_name in files:
                    os.system("rm " + temp_name)


def addWordFromMean(word):
    try:
        os.chdir("/Users/chaser/Projects/Dictionary")
        fileName = word[0]
        tempName = "." + fileName
        os.system("cp " + fileName + " " + tempName)
        with open(fileName, 'a') as dictionary:
            dictionary.write(word.upper())
            dictionary.write("\n")
        sortIt(fileName)
        # print("HELLOOOO")
    except:
        files = os.listdir()
        if tempName in files:
            os.system("cp " + tempName + " " + fileName)
            print("try agian!")

    finally:                                            # always executed whether try suceeds or not
        files = os.listdir()
        if tempName in files:
            os.system("rm " + tempName)

""" Adds the words passed through command line or a single word."""
def addTheWord():
    if len(sys.argv) > 1:
        i = 1
        listOfLists = [['A'],['B'],['C'],['D'],['E'],['F'],['G'],['H'],['I'],['J'],['K'],['L'],['M'],['N'],['O'],['P'],['Q'],['R'],['S'],['T'],['U'],['V'],['W'],['X'],['Y'],['Z']]
        while i < len(sys.argv):
            new_word = check(str(sys.argv[i])).lower()
            listOfLists[ord(new_word[0]) - ord('a')].append(new_word)
            i = i + 1
        # print(listOfLists)
        addToCorrespondingFiles(listOfLists)
    else:
        new_word = input("Enter the word : ")
        file_name = new_word[0].upper()
        try:
            temp_name = "." + file_name #name of the temporary duplicate file in case some exception occurs
            os.system("cp "+ file_name + " " + temp_name)
            with open(file_name, 'a') as dictionary: #always use this because if opening of file fails the file will not get overwritten
                dictionary.write("\n")
                dictionary.write(new_word)

        except:
            files = os.listdir()
            if temp_name in files:
                os.system("cp " + temp_name + " " + file_name)
                print("try agian!")

        finally:                                            # always executed whether try suceeds or not
            files = os.listdir()
            if temp_name in files:
                os.system("rm " + temp_name)

if __name__ == '__main__':
    addTheWord()