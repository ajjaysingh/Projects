#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name			: spellcheck.py
# Description		: Checks whether a spelling is correct or not if not then give suggestions. It first check online and if it fails then offline.
# Author			: Ajay
# Date				: 2016-11-27
# Python Version	: 3
#==================================================

import  requests, os, sys, json, urllib, shutil, re, pickle
from collections import Counter
from bs4 import BeautifulSoup


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
    if word.lower() == correct.lower():
        print(correct)
        return [word, False]
    else:
        print("The word \""+ word +"\" should have been > " + correct)
        decide = input("Press 'y' if you want to change\n\t 'n' if continue with the same word.")
        if decide == 'y':
            return [correct.lower(), True] # True because word change and you need to change the word to be saved.
        else:
            return [word, False] # False because we did not change the word.


# def checkOnline(word):
#     errorString = 'Did you mean'
#     url = 'http://www.dictionary.com/browse/' + word.lower()
#     response = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"})
#     html = response.content
#     soup = BeautifulSoup(html, "lxml")
#     msg = soup.find("header", {"class":"head-entry"})
#     suggestions = []
#     if msg != None and errorString in msg.text:
#         suggestions.append(msg.text.rsplit(None, 1)[-1].replace("?", ""))
#         more = soup.find("ul", {"class":"suggestions head-entry"})
#         more_list = more.find_all("li")
#         for entry in more_list:
#             suggestions.append(entry.text.replace("\n","").replace("\r","").replace(" ",""))
#             # print(str(entry.text))
#         print("Select Suggestion. Press 0 to retain your word: ")
#         count = 1
#         for suggestion in suggestions:
#             print(count, suggestion)
#             count = count + 1
#     return word


def checkOnline(word):
    try:
        errorString = 'Did you mean:'
        url = 'http://www.macmillandictionary.com/dictionary/british/' + word.lower()
        response = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"})
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        msg = soup.find("div", {"id":"didyoumean"})
        # print(msg.text)
        suggestions = [word]
        did_word_change = False
        if msg != None and errorString in msg.text:
            search_results = soup.find_all("div", {"id":"search-results"})[1]
            # print(search_results)
            list_results = search_results.find_all("li")
            for entry in list_results:
                suggestions.append(entry.text)
                # print(str(entry.text))
            count = 1
            size = 9
            if len(suggestions) < size:
                size = len(suggestions)
            for suggestion in suggestions[1:9]:
                print(count, suggestion)
                count = count + 1
            choice_entered = int(input("Select Suggestion. Press 0 to retain your word: "))
            word = suggestions[choice_entered]
            if choice_entered > 0:
                did_word_change = True
        return [word, did_word_change]
    except:
        # exit(5)
        print("Problem with online check")
        [word, did_word_change] = check(word)
        return [word, did_word_change]