#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name         : mean.py
# Description       : Find, Display, Pronounces and Stores meaning of the specified word
# Author            : Ajay
# Date              : 2016-11-25
# Python Version    : 3
#==================================================


import  requests, os, sys, json, urllib, shutil, re, pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from textwrap import fill
from collections import Counter
from bs4 import BeautifulSoup
import say, spellcheck, addword

dir = '/Users/chaser/Projects/Dictionary/Meaning'
userWord = ''


class NoDefinition(ValueError):
    def __init__(self, arg):
        self.msg = arg
        self.args = {arg}


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

def getHindi(driver):
    # RESULTS_LOCATOR = "//div[@class='ellip _Axg exp-txt-c xcas']"
    # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, RESULTS_LOCATOR)))
    # driver.find_elements(By.XPATH, RESULTS_LOCATOR)[0].click()
    RESULTS_LOCATOR = "//span[@class='lr_dct_trns_sel_cnt']"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, RESULTS_LOCATOR)))
    options = driver.find_element(By.XPATH, RESULTS_LOCATOR)
    opt = options.find_element(By.XPATH, '//Select')
    for o in opt.find_elements_by_tag_name('option'):
        if o.text == 'Hindi':
            o.click() # select() in earlier versions of webdriver
            break
    RESULTS_LOCATOR = "//div[@class='lr_dct_trns']"
    trans = driver.find_element(By.XPATH, RESULTS_LOCATOR)
    level = trans.find_elements(By.XPATH, "//li[@class='vk_txt']")
    return level
    # print("\n\t\tTranslations:")
    # for l in level:
    #     print("\t\t-" + l.text)

def getSoupRenewed(oldSoup, driver, forWord):
    url = 'https://www.google.co.in/search?q=define%20' + forWord + '&expnd=1'
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    return soup


def handleGoogleDidYouMean(soup, word, driver):
    errorString = 'Did you mean:'
    msg = soup.find("span",{"class":"spell _uwb"})
    if msg != None:
        msg = msg.text
        if msg == errorString:
            word = soup.find("a",{"class":"spell"}).find({"i"}).text
            soup = getSoupRenewed(soup, driver, word)
            # url = 'https://www.google.co.in/search?q=define%20' + word + '&expnd=1'
            # driver.get(url)
            # html = driver.page_source
            # soup = BeautifulSoup(html, "lxml")
    else:
        # print("HERE")
        msg = soup.find("span",{"class":"spell"})
        errorString = "Including results for"
        if msg != None and errorString in msg.text:
            word = msg.find({"i"}).text
            soup = getSoupRenewed(soup, driver, word)
            # url = 'https://www.google.co.in/search?q=define%20' + word + '&expnd=1'
            # driver.get(url)
            # html = driver.page_source
            # soup = BeautifulSoup(html, "lxml")
        elif msg != None and "Showing results for" in msg.text:
            word = soup.find("a",{"class":"spell"}).find({"i"}).text
            # [html, soup] = getSoupRenewed(soup, driver, word) actually no need of this because the page already has the new results
        else:
            msg = soup.find("span",{"class":"_Tgc"})
            if msg != None:
                err = msg.text
                raise NoDefinition(err)
    return [soup, word]

def getPronunPOS(soup):
    basics = {}
    word = soup.find_all("div", {"class":"vk_ans"})
    if word != []:
        basics['word'] = word
    
    pronun = soup.find_all("span", {"class":"lr_dct_ph"})
    if pronun != []:
        basics['pronun'] = pronun
    
    pos = soup.find_all("div", {"class":"lr_dct_sf_h"})
    if pos != []:
        basics['pos'] = pos

    tense = soup.find_all("div", {"class":"xpdxpnd vk_gy"})
    if tense != []:
        basics['tense'] = tense
    else:
        tense = soup.find_all("div", {"class":"vk_gy"})
        if tense != []:
            basics['tense'] = tense
    # print("/" + pronun.text)
    # exit(5)
    return basics


"""Request google for the word and returns the element containing the entire definition"""
def getGoogleResponse(word, driver):
    url = 'https://www.google.co.in/search?q=define%20' + word + '&expnd=1'
    driver.get(url)
    html = driver.page_source
    final_soup = BeautifulSoup(html, "lxml")
    [final_soup, word] = handleGoogleDidYouMean(final_soup, word, driver)
    everyThing = final_soup.select("div._Jig")
    level = getHindi(driver)
    basics = getPronunPOS(final_soup)
    return [level, everyThing, word, basics]

def basicsValuePrint(basics):
    googleWord = basics.get('word', 'Fuck')
    pronun = basics.get('pronun', 'Fuck')
    pos = basics.get('pos', 'Fuck')
    tense = basics.get('tense', 'Fuck')
    i = 0
    for w in googleWord:
        print("\n\t" + w.text.title(), end="")
        
        if pronun != 'Fuck' and i < len(pronun):
            print(" || Pronunciation: /" + pronun[i].text + ", ")

        if pos != 'Fuck' and i < len(pos):
            print("\t" + "POS: " + pos[i].text + ",  ", end="")

        if tense != 'Fuck' and i < len(tense):
            print(tense[i].text + ".", end="")
        i = i + 1
    # exit(5)

'''
Extracts the meaning, examples, Synonyms and Antonyms of the word data taken from google.
'''
def extractFromGoogleElement(everyThing, level, basics):
    count = 1
    basicsValuePrint(basics)
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
                print("\t", name.text.title(), " ", end="")
                for x in n[:5]:
                    print(x.text, ", ", end="")
                print("")
        count = count + 1
    print("\n\t\tTranslations:")
    for l in level:
        print("\t\t-" + l.text)


def changeFileNameIfSearchNotSame(givenFileName, givenWord, searchedWord):
    os.chdir(dir + '/' + givenWord[0].upper())
    fileName = dir + '/' + searchedWord[0].upper() + '/' + searchedWord.lower() + ".txt"
    os.system("mv " + givenFileName + " " + fileName)
    print("Attention!!! The word searched is " + searchedWord + " instead of " + givenWord)



def findWordIfAlreadyScrapped(word, fileName):
    wordGiven = word
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
            chromedriver = "/Users/chaser/Downloads/chromedriver"
            os.environ["webdriver.chrome.driver"] = chromedriver
            driver = webdriver.Chrome(chromedriver)
            sys.stdout = Logger(fileName)
            [level, definitionElement, word, basics] = getGoogleResponse(word, driver)
            vocabResults(word)
            # print(definitionElement)
            extractFromGoogleElement(definitionElement, level, basics)
            driver.quit()
            # print("there")
            # os.system('mv ../../' + fileName + ' .') now no need to move ;)
            sys.stdout = sys.__stdout__
            addword.addWordFromMean(word)       #!!!!!!!!!!!   also in the if statement >>>>>>>>>HEY DON"T FORGET TO UNCOMMENT THIS TO ADD THE QUERIED WORD TO wordlists
            os.chdir(dir + '/' + word[0].upper())
            if wordGiven != word:
                changeFileNameIfSearchNotSame(fileName, wordGiven, word)
            # print(">>!!!!>>")
        except NoDefinition as e:
            try:
                vocabResults(word)
                print("\n\tWiki Definition:")
                print(printAligned("\t", e.msg))
                driver.quit()
                sys.stdout = sys.__stdout__
                addword.addWordFromMean(word)       #!!!!!!!!!!!   also in the if statement >>>>>>>>>HEY DON"T FORGET TO UNCOMMENT THIS TO ADD THE QUERIED WORD TO wordlists
                os.chdir(dir + '/' + word[0].upper())
            except:
                sys.stdout =sys.__stdout__
                os.system('rm ' + fileName)
                driver.quit()
        except:
            sys.stdout =sys.__stdout__
            os.system('rm ' + fileName)
            driver.quit()
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





