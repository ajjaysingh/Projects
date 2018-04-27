#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name         : mean.py
# Description       : Find, Display, Pronounces and Stores meaning of the specified word
# Author            : Ajay
# Date              : 2016-11-25
# Python Version    : 3
#==================================================


import  requests, os, sys, json, urllib, shutil, re, pickle
from textwrap import fill
from collections import Counter
from bs4 import BeautifulSoup
import say, spellcheck, addword

dir = '/Users/chaser/Projects/Dictionary/Meaning'
userWord = ''


"""Logs what is outputed at the terminal to a file"""
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout          # here it defines vaiable terminal initialised to the standard stdout
        self.log = open(filename, "a")      # here it defines a vauable initialised to a file

    def write(self, message):               # the write function writes to terminal and file and also flushes 
        self.terminal.write(message)        # so that updates to file are simultaneous to the updates in terminal
        self.log.write(message)
        self.log.flush()

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass




# print(userWord)
# exit(5)




def printAligned(left, right):
    screen_width = shutil.get_terminal_size().columns - 20
    # Right-justifies a single line
    # f = lambda x : x.rjust(screen_width)
    # wrap returns a list of strings of max length 'screen_width'
    # 'map' then applies 'f' to each to right-justify them.
    # '\n'.join() then combines them into a single string with newlines.
    # print('\n'.join(map(f, textwrap.wrap(str, screen_width))))
    # str = textwrap.dedent(str).strip()
    wrapped = fill(right, width=screen_width, subsequent_indent=' '*15)
    return '  {0:<13}{1}'.format(left, wrapped)


def anagram(word1, word2):
    # print(">>>>", word1)
    word1 = word1.replace(" ", "")
    word1 = word1.replace("-", "")
    word2 = word2.replace(" ", "")
    word2 = word2.replace("-", "")
    return Counter(word1) == Counter(word2)

def handleVocabDidYouMean(soup, word):
    msg = soup.find("span", {"class":"word"})
    if msg.text.lower() != word:
        url = 'https://www.vocabulary.com/dictionary/' + msg.text.lower()
        response = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"})
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        word  = msg.text.lower()
    return [soup, word]

"""REsults form Vocabulary.com"""
def vocabResults(word):
    url = 'https://www.vocabulary.com/dictionary/' + word
    response = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"})
    html = response.content
    vocab_soup = BeautifulSoup(html, "lxml")
    # vocabWord = vocab_soup.find("span", {"class":"word"})

    # print(">>>>", word)
    [vocab_soup, suggestedWord] = handleVocabDidYouMean(vocab_soup, word)
    # if anagram(suggestedWord.lower(), word):
    #     word = suggestedWord
    # if anagram(vocabWord.text.lower(), word):
    #     word = vocabWord.text
    columns = shutil.get_terminal_size().columns
    print(word.upper().center(columns))
    # print(vocabWord.text.upper())
    short = vocab_soup.find("p", {"class":"short"})
    if short != None:
        print(printAligned("SHORT", short.text))
    lonng = vocab_soup.find("p", {"class":"long"})
    if lonng != None:
        print(printAligned("LONG", lonng.text))

    json_url = 'https://corpus.vocabulary.com/api/1.0/examples.json?query=' + str(word) + '&maxResults=24&startOffset=0&filter=0'
    json_url = json_url.replace(' ', '%20')
    # print(word,json_url)
    html = urllib.request.urlopen(json_url).read()
    j = json.loads(html.decode('utf-8'))
    # print(j)
    if j['result'] != None:
        l = j['result']['sentences']
        print("Examples from Vocabulary:".upper().center(columns))
        for s in l[:5]:
            print(printAligned("   >", s['sentence']))
    return word


def handleGoogleDidYouMean(soup, word):
    errorString = 'Did you mean:'
    msg = soup.find("span",{"class":"spell _uwb"})
    if msg != None:
        msg = msg.text
    if msg == errorString:
        word = soup.find("a",{"class":"spell"}).find({"i"}).text
        url = 'https://www.google.co.in/search?q=define%20' + word
        response = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"})
        html = response.content
        soup = BeautifulSoup(html, "lxml")
    return [soup, word]


"""Request google for the word and returns the element containing the entire definition"""
def getGoogleResponse(word):
    url = 'https://www.google.co.in/search?q=define%20' + word
    response = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"})
    html = response.content
    final_soup = BeautifulSoup(html, "lxml")
    [final_soup, word] = handleGoogleDidYouMean(final_soup, word)
    everyThing = final_soup.select("div._Jig")
    return [everyThing, word]



'''
Extracts the meaning, examples, Synonyms and Antonyms of the word data taken from google.
'''
def extractFromGoogleElement(everyThing):
    count = 1
    for line in everyThing[:9]:
        mean = line.find("div", {"data-dobid":"dfn"})
        eg = line.find_all("div", {"class":"vk_gy"})
        nyms = line.find_all("table", {"class":"vk_tbl vk_gy"})
        print("\n",count, "  " ,end="")
        print(mean.text.title())
        for x in eg:
            print("\t", "Eg. " ,x.text.title())
        if nyms != None:
            for p in nyms:
                name = p.find("td", {"class":"lr_dct_nyms_ttl"})
                n = p.find_all("a")
                print("\t", name.text.title(), " ",end="")
                for x in n[:5]:
                    print(x.text, ", ", end="")
                print("")
        count = count + 1




def findWordIfAlreadyScrapped(word, fileName):
    os.chdir(dir + '/' + word[0].upper())
    files = os.listdir()
    if fileName in files:
        file = fileName.replace(" ", "\\ ")
        print("Found!!")
        os.system("cat " + file)
        addword.addWordFromMean(word)
        os.chdir(dir + '/' + word[0].upper())
    else:
        try:
            sys.stdout = Logger(fileName)
            [definitionElement, word] = getGoogleResponse(word)
            vocabResults(word)
            # print(definitionElement)
            extractFromGoogleElement(definitionElement)
            # os.system('mv ../../' + fileName + ' .') now no need to move ;)
            sys.stdout =sys.__stdout__
            addword.addWordFromMean(word)
            os.chdir(dir + '/' + word[0].upper())
            # print(">>!!!!>>", word)
        except:
            sys.stdout =sys.__stdout__
            os.system('rm ' + fileName)
        # say()




# files = os.listdir()
# pattern = re.compile(r'[\w]+.txt')
# last_word = [x for x in files if re.search(pattern, x)]
# os.system('mv ' + last_word[0] + '.txt Meaning/' + last_word[0][0].upper())
if __name__ == '__main__':
    if len(sys.argv) > 1:
        userWord = spellcheck.checkOnline(str(sys.argv[1]))
    else:
        userWord = spellcheck.checkOnline(int(input("Enter word now(Next time enter while running program!!!): ")))
    fileName = userWord.lower() + ".txt"
    findWordIfAlreadyScrapped(userWord, fileName)





