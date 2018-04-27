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
import say, spellcheck, addword, time

dir = '/Users/chaser/Projects/Dictionary/Meaning'
userWord = ''

class color:
    MAGENTA     = '\033[35m'
    CYAN        = '\033[36m'
    BLUE        = '\033[34m'
    BRIGHT      = '\033[37m'
    DARKYELLOW  = '\033[33m'
    GREEN       = '\033[32m'
    DARKRED     = '\033[31m'
    DULL        = '\033[30m'
    PURPLE      = '\033[95m'
    DARKCYAN    = '\033[36m'
    RED         = '\033[91m'
    BOLD        = '\033[1m'
    ITALICS     = '\033[3m'
    UNDERLINE   = '\033[4m'
    END         = '\033[0m'
    def getMagenta(string):
        return color.MAGENTA + string + color.END
        
    def getCyan(string):
        return color.CYAN + string + color.END
        
    def getBlue(string):
        return color.BLUE + string + color.END
        
    def getBright(string):
        return color.BRIGHT + string + color.END
        
    def getDarkYellow(string):
        return color.DARKYELLOW + string + color.END
        
    def getGreen(string):
        return color.GREEN + string + color.END
        
    def getRed(string):
        return color.RED + string + color.END
        
    def getItalics(string):
        return color.ITALICS + string + color.END
        
    def getUnderline(string):
        return color.UNDERLINE + string + color.END
        
    def getBold(string):
        return color.BOLD + string + color.END
        
    def getDarkRed(string):
        return color.DARKRED + string + color.END
        
    def getDull(string):
        return color.Dull + string + color.END
        
    def getPurple(string):
        return color.PURPLE + string + color.END
        
    def getDarkCyan(string):
        return color.DARKCYAN + string + color.END


class NoDefinition(ValueError):
    def __init__(self, arg1, arg2):
        self.msg = arg1
        self.word = arg2
        self.args = {arg1, arg2}


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




# table_data = [['a', 'b', 'c'], ['aaaaaaaaaa', 'b', 'c'], ['a', 'bbbbbbbbbb', 'c']]
# for row in table_data:
#     print("{: >20} {: >20} {: >20}".format(*row))
#
#                    a                    b                    c
#           aaaaaaaaaa                    b                    c
#                    a           bbbbbbbbbb                    c
# Retruns aligned concatenated left and right strings and you have to print them where the funciton is called
def printAligned(left, right):
    screen_width = shutil.get_terminal_size().columns - 20
    wrapped = fill(right, width=screen_width, subsequent_indent=' '*15)
    return '  {0:>13}{1}'.format(left, wrapped)

def printSynAntons(left, right):
    screen_width = shutil.get_terminal_size().columns - 25
    wrapped = fill(right, width=screen_width, subsequent_indent=' '*21)
    return '  {0:>13}{1}'.format(left, wrapped)

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
    [vocab_soup, suggestedWord] = handleVocabDidYouMean(vocab_soup, word)
    columns = shutil.get_terminal_size().columns
    print(color.getMagenta(word.upper().center(columns)))
    short = vocab_soup.find("p", {"class":"short"})
    if short != None:
        print(color.getRed(printAligned("SHORT  ", short.text)))
    lonng = vocab_soup.find("p", {"class":"long"})
    if lonng != None:
        print(color.getDarkCyan(printAligned("LONG  ", lonng.text)))

    json_url = 'https://corpus.vocabulary.com/api/1.0/examples.json?query=' + str(word) + '&maxResults=24&startOffset=0&filter=0'
    json_url = json_url.replace(' ', '%20')
    html = urllib.request.urlopen(json_url).read()
    j = json.loads(html.decode('utf-8'))
    if j['result'] != None:
        l = j['result']['sentences']
        print("Examples from Vocabulary:".upper().center(columns))
        for s in l[:5]:
            print(color.getItalics(printAligned("  > ", s['sentence'])))
    return word

def raiseDefinitionException(soup, word):
    msg = soup.find("span",{"class":"_Tgc"})
    if msg != None:
        err = msg.get_text(' ')
        raise NoDefinition(err, word)


def getHindi(driver):
    RESULTS_LOCATOR = "//span[@class='lr_dct_trns_sel_cnt']"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, RESULTS_LOCATOR)))
    options = driver.find_element(By.XPATH, RESULTS_LOCATOR)
    opt = options.find_element(By.XPATH, '//Select')
    for o in opt.find_elements_by_tag_name('option'):
        if o.text == 'Hindi':
            o.click() # select() in earlier versions of webdriver
            break
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    trans = soup.find("div", {"class":"lr_dct_trns vmod"})
    return trans

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
    else:
        msg = soup.find("span",{"class":"spell"})
        errorString = "Including results for"
        if msg != None and errorString in msg.text:
            word = msg.find({"i"}).text
            soup = getSoupRenewed(soup, driver, word)
        elif msg != None and "Showing results for" in msg.text:
            word = soup.find("a",{"class":"spell"}).find({"i"}).text
            word = soup.find("span", {"data-dobid":"hdw"}).text # Earlier I was using the word in the error message but if we search for "privy counsil" then only the spelling of cousil is wrong therefore in the above statement only "council" will appear rather than "privy council".
        else:
            raiseDefinitionException(soup, word)
    return [soup, word]



"""Request google for the word and returns the element containing the entire definition"""
def getGoogleResponse(word, driver):
    url = 'https://www.google.co.in/search?q=define%20' + word + '&expnd=1'
    driver.get(url)
    html = driver.page_source
    final_soup = BeautifulSoup(html, "lxml")
    [final_soup, word] = handleGoogleDidYouMean(final_soup, word, driver)
    everyThing = final_soup.select("div.lr_dct_ent")
    # print(everyThing)
    if everyThing == []:
        return [everyThing, word, final_soup.find("span", {"class":"Y0NH2b CLPzrc"})] # Alternate definitions provided by google search (for example words like Odyssey, Zero sum game, etc.).
        # In such a case we return the alternate definition in the trans field, print it out and exit.
    else:
        trans = getHindi(driver)
        return [everyThing, word, trans]


def extractHindi(translations):
    posHeading = translations.find_all("div", {"class":"lr_dct_tg_pos vk_txt"})
    transWords = translations.find_all("ol", {"class":"lr_dct_tg_trns"})
    translation_table = []
    translation_heading_subBlock = []
    for pos in posHeading:
        translation_heading_subBlock.append(pos.text)
    # print("also")
    translation_word_subBlock = {}
    subBlockMinLength = 100
    listNumber = 1
    maxLen = 0
    for trans in transWords:
        wordList = trans.get_text('||').split('||')
        wordList = [x for x in wordList if not (x.isdigit() or x[0] == '.')]
        # print(wordList)
        if len(wordList) < subBlockMinLength:
            subBlockMinLength = len(trans)
        wordNumber = 1
        for listWord in wordList:
            # print (listWord)
            if len(listWord) > maxLen:
                maxLen = len(listWord)
            translation_word_subBlock[listNumber, wordNumber] = listWord
            wordNumber = wordNumber + 1
        listNumber = listNumber + 1

    # print("atleast")
    translation_table = []
    translation_table.append(translation_heading_subBlock)
    for nWord in range(1, subBlockMinLength+1):
        tempList = []
        for nList in range(1, listNumber):
            tempList.append(translation_word_subBlock.get((nList, nWord)))
        # print(tempList)
        translation_table.append(tempList)

    offset = maxLen + 10
    
    # I don't understand why but sometimes only blank spaces are printed.
    prevent_just_blank = False
    for t in translation_word_subBlock:
        if translation_word_subBlock.get(t) != ' ':
            prevent_just_blank = True
            break

    if prevent_just_blank:
        for i in range(len(translation_table)):
            for j in range(len(translation_table[0])):
                if translation_table[i][j] == None:
                    translation_table[i][j] = ""
                if i == 0:
                    translation_table[i][j] = color.getUnderline(color.getBlue(translation_table[i][j]))
                indented = ' {:{align}{width}}'.format(color.getDarkRed(translation_table[i][j]), align='^', width=offset)
                print(" " +  indented, end="")
            print()
        # exit(5)

def alignBullets(left, right):
    screen_width = shutil.get_terminal_size().columns - 15
    wrapped = fill(right, width=screen_width, subsequent_indent=' '*12)
    return '  {0:<10}{1}'.format(left, wrapped)

def wrapLineNumberDfn(right):
    screen_width = shutil.get_terminal_size().columns - 15
    wrapped = fill(right, width=screen_width, subsequent_indent=' '*11)
    return wrapped

'''
Extracts the meaning, examples, Synonyms and Antonyms of the word data taken from google.
'''
def extractFromGoogleElement(everyThing):
    print()
    for block in everyThing:
        name = block.find("span", {"data-dobid":"hdw"})
        subBlock_POS = block.find_all("div", {"class":"lr_dct_sf_h"})
        subBlock_pronun = block.find_all("span", {"class":"lr_dct_ph"})  # less than or equal to the no of sub blocks(POS)
        subBlock_lineBelowPOS = block.find_all("div", {"class":"xpdxpnd vk_gy"})
        subBlock_crux = block.find_all("ol", {"class":"lr_dct_sf_sens"})
        subBlock_wordForm = block.find("div", {"class":"vmod vk_gy"})   # e.g. in words like 'edgewise' which are directly not present in google dictionary "adverb: edgewise" was missing so for that line.
        print(color.getMagenta(name.text.title()), end = "") # print the word for the block
        # print the pronunciation with the word in the block if there is only one otherwise print it with the sub-block content for that use a flag
        pronun_done_flag = False
        if len(subBlock_pronun) == 1:
            pronun_done_flag = True
            print(color.getCyan(" /" + subBlock_pronun[0].text + ","), end="")
        # print(len(subBlock_POS))
        iterator = 0
        for subName in subBlock_POS:
            if iterator == 0:
                print(" " + color.getRed(color.getItalics(subName.getText(separator=u' '))), end="")   # the prints the part of speech which defines a sub block
            else:
                print("    " + color.getRed(color.getItalics(subName.getText(separator=u' '))), end="")   # the prints the part of speech which defines a sub block        
            if iterator < len(subBlock_lineBelowPOS):
                print(" | " + subBlock_lineBelowPOS[iterator].text, end="")
            if (pronun_done_flag == False) and (iterator < len(subBlock_pronun)):
                print("    /" + subBlock_pronun[iterator].text, end="")
            if subBlock_wordForm != None:
                print("\n\t" + subBlock_wordForm.text, end="")
            # print("\t" + subBlock_crux.text)
            lines = subBlock_crux[iterator].find_all("div", {"class":"lr_dct_sf_sen vk_txt"})
            iterator = iterator + 1
            # print(iterator)
            for line in lines: # line means the line that has a number assigned to it some lines are a part of the line assigned the number in a bulleted list class="_Jig"
                number = line.find("strong")
                bullets = line.find_all("div", {"class":"PNlCoe"})
                another = 0 # becasue the first dfn will be printed next to the number
                if number != None:
                    print("\n      " + color.getGreen(number.text + ".") + " ", end="")
                else:
                    print()
                    another = 1 # since number is not there so no need of this flag
                for bullet in bullets:
                    dfn = bullet.find("div", {"data-dobid":"dfn"}) # the definition in the bullet
                    first_eg = bullet.find("div", {"class":"vk_gy"}) # the first example of the bullet
                    syns_antons = bullet.find_all("table", {"class":"vk_tbl vk_gy"})
                    if another == 0: # also the printing of the first bullet will be different
                        print(color.getBright(wrapLineNumberDfn(dfn.text)))
                        another = 1
                    else:
                        print(alignBullets("        \u2022", color.getBright(dfn.text)))
                        # print("\t  " + "\u2022 ", end="")
                        # print(color.getBright(dfn.text))
                    if first_eg != None: #Sometimes the example just after the definition is absent
                        print("\t   " + first_eg.text)
                    if syns_antons != None:
                        for item in syns_antons:
                            title = item.find("td", {"class":"lr_dct_nyms_ttl"})
                            nyms = item.find_all("span")
                            eg = item.find("div", {"class":"vk_gy"})
                            # print("\t   " + color.getItalics(title.text) + " " ,end="")
                            syn_antons_title = "\t   " + color.getItalics(title.text) + " "
                            syn_antons_words = set()
                            for nym in nyms:
                                if nym.text[-1] != "\"" and nym.text != 'More': # since taking all the span will get the examples also and since examples end in " therefore we need to skip them
                                    syn_antons_words.add(nym.text.strip('\n').strip('\t').strip('  ').strip(',').strip(';'))# + nym.text.strip('\n').strip('\t').strip('  ') + ' '  # print(nym.text, end="")
                            sinn_words = ''
                            for t in syn_antons_words:
                                if t is not "" and t is not ";":
                                    sinn_words = sinn_words + t + ', '
                            print(printSynAntons(syn_antons_title, sinn_words), end="")
                            if eg != None:
                                print("\n\t\t    " + eg.text)
                            else:
                                print()


def extractOrigin(everyThing):
    origin = everyThing[0].find_all("div", {})
    print()
    print(printAligned("Origin:  ", origin[-1].text))

def changeFileNameIfSearchNotSame(givenFileName, givenWord, searchedWord):
    os.chdir(dir + '/' + givenWord[0].upper())
    givenFileName = givenFileName.replace(" ", "\\ ")
    fileName = dir + '/' + searchedWord[0].upper() + '/' + searchedWord.lower() + ".txt"
    os.system("mv " + givenFileName + " " + fileName.replace(" ", "\\ "))
    print("Attention!!! The word searched is " + searchedWord + " instead of " + givenWord)



def findWordIfAlreadyScrapped(word, fileName, wordToSave):
    wordGiven = word
    os.chdir(dir + '/' + word[0].upper())
    files = os.listdir()
    if fileName in files:
        file = fileName.replace(" ", "\\ ")
        print("Found!!")
        os.system("cat " + file)
        addword.addWordFromMean(wordToSave)
        os.chdir(dir + '/' + word[0].upper())
    else:
        try:
            chromedriver = "/Users/chaser/Projects/mybin/chromedriver"
            os.environ["webdriver.chrome.driver"] = chromedriver
            driver = webdriver.Chrome(chromedriver)
            sys.stdout = Logger(fileName)
            [definitionElement, word, trans] = getGoogleResponse(word, driver) # word will contain the word returned from search.
            if definitionElement == []:
                # print("trans :", trans )
                columns = shutil.get_terminal_size().columns
                print(color.getMagenta(word.upper().center(columns)))
                print("\n\tDefinition:")
                print(printAligned("\t", ".".join(trans.text.split(".")[1:])))
            else:
                vocabResults(word)
                # print(definitionElement)
                # print("there")
                extractFromGoogleElement(definitionElement)
                extractHindi(trans)
                extractOrigin(definitionElement)
            # print("here")
            # exit(5)
            driver.quit()
            # os.system('mv ../../' + fileName + ' .') now no need to move ;)
            sys.stdout = sys.__stdout__
            if wordGiven != word:  # If the word is changed by google then the changed word should be saved instead of the wrong user supplied word.
                wordToSave = word.replace(" ", "-")
            addword.addWordFromMean(wordToSave)       #!!!!!!!!!!!   also in the if statement >>>>>>>>> HEY DON"T FORGET TO UNCOMMENT THIS TO ADD THE QUERIED WORD TO wordlists
            os.chdir(dir + '/' + word[0].upper())
            if wordGiven != word:
                changeFileNameIfSearchNotSame(fileName, wordGiven, word)
            # print(">>!!!!>>")
        except NoDefinition as e:
            try:
                # print("Its in wiki")
                vocabResults(e.word)
                print("\n\tWiki Definition:")
                print(printAligned("\t", e.msg))
                driver.quit()
                sys.stdout = sys.__stdout__
                if wordGiven != e.word:  # If the word is changed by google then the changed word should be saved instead of the wrong user supplied word.
                    wordToSave = e.word.replace(" ", "-")
                addword.addWordFromMean(wordToSave)       #!!!!!!!!!!!   also in the if statement >>>>>>>>>HEY DON"T FORGET TO UNCOMMENT THIS TO ADD THE QUERIED WORD TO wordlists
                os.chdir(dir + '/' + e.word[0].upper())
                if wordGiven != e.word:
                    changeFileNameIfSearchNotSame(fileName, wordGiven, e.word)
            except:
                # print("Its in wiki")
                sys.stdout =sys.__stdout__
                os.system('rm ' + fileName.replace(" ", "\\ "))
                driver.quit()
        except:
            # for words like Odyssey the exception is returning here.
            # print("never went to wiki")
            # try:
            # except:
            sys.stdout =sys.__stdout__
            os.system('rm ' + fileName.replace(" ", "\\ "))
            driver.quit()
        # say()




# files = os.listdir()
# pattern = re.compile(r'[\w]+.txt')
# last_word = [x for x in files if re.search(pattern, x)]
# os.system('mv ' + last_word[0] + '.txt Meaning/' + last_word[0][0].upper())
if __name__ == '__main__':
    if len(sys.argv) > 1:
        word = str(sys.argv[1])
    else:
        word = input("Enter word now(Next time enter while running program!!!): ")

    wordToSave = word  # To handle the cases of words like banana-republic
    word = word.replace("-", " ") # we should save it as banana-republic and search it as banana repuiblic
    os.chdir(dir + '/' + word[0].upper())
    fileName = word.lower() + ".txt"  # because the saved word should not have a space between them
    files = os.listdir()
    if fileName in files:
        file = fileName.replace(" ", "\\ ")
        print("Found!!")
        os.system("cat " + file)
        addword.addWordFromMean(wordToSave) # To avoid saving space in the saved word
        os.chdir(dir + '/' + word[0].upper())
    else:
        [userWord, did_word_change] = spellcheck.checkOnline(word)
        if did_word_change:
            wordToSave = userWord.replace(" ", "-")
        fileName = userWord.lower() + ".txt"
        
        findWordIfAlreadyScrapped(userWord, fileName, wordToSave)
