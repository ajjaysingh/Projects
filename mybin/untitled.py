import  requests, os, sys, json, urllib, shutil, re, pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from textwrap import fill
from collections import Counter
from bs4 import BeautifulSoup


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



chromedriver = "/Users/chaser/Projects/mybin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

word = 'forfeit'#'vest'#'bestow'
url = 'https://www.google.co.in/search?q=define%20' + word + '&expnd=1'
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, "lxml")

RESULTS_LOCATOR = "//span[@class='lr_dct_trns_sel_cnt']"
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, RESULTS_LOCATOR)))
options = driver.find_element(By.XPATH, RESULTS_LOCATOR)
opt = options.find_element(By.XPATH, '//Select')
for o in opt.find_elements_by_tag_name('option'):
    if o.text == 'Hindi':
        o.click() # select() in earlier versions of webdriver
        break

RESULTS_LOCATOR = "//div[@class='lr_dct_trns']"
# trans = driver.find_element(By.XPATH, RESULTS_LOCATOR)
html = driver.page_source
soup = BeautifulSoup(html, "lxml")
translations = soup.find("div", {"class":"lr_dct_trns"})
head = translations.find_all("div", {"class":"lr_dct_tg_pos vk_txt"})
for h in head:
    print(h.text)


posHeading = translations.find_all("div", {"class":"lr_dct_tg_pos vk_txt"})
transWords = translations.find_all("ol", {"class":"lr_dct_tg_trns"})
translation_heading = []
for pos in posHeading:
    translation_heading.append(pos.text)

translation_table = []
translation_table.append(translation_heading)

for trans in transWords:
    print(trans.find("span").text)

translation_word_subBlock = {}
subBlockMinLength = 100
listNumber = 1
maxLen = 0
for trans in transWords:
    wordList = trans.get_text('||').split('||')
    print(wordList)
    no_integers = [x for x in wordList if not (x.isdigit() or x[0] == '.')]
    print(no_integers)
    # no_dots = [x for x in wordList if not (x[0] == '.')]
    # print(no_dots)
    wordList = no_integers
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

translation_table = []
translation_table.append(translation_heading)
for nWord in range(1, subBlockMinLength+1):
    tempList = []
    for nList in range(1, listNumber):
        tempList.append(translation_word_subBlock.get((nList, nWord)))
    print(tempList)
    translation_table.append(tempList)


offset = maxLen + 10
for i in range(len(translation_table)):
    for j in range(len(translation_table[0])):
        # print(translation_table[i][j])
        if translation_table[i][j] == None:
            translation_table[i][j] = ""
        if i == 0:
            translation_table[i][j] = color.getUnderline(color.getBlue(translation_table[i][j]))
        indented = ' {:{align}{width}}'.format(color.getDarkRed(translation_table[i][j]), align='^', width=offset)
        print(" " +  indented, end="")
    print()


driver.quit()
# offset = maxLen + 9
# for i in range(len(translation_table)):
#     for j in range(len(translation_table[0])):
#         if translation_table[i][j] == None:
#             translation_table[i][j] = ""
#         indented = '{:{align}{width}}'.format(translation_table[i][j], align='^', width=offset)
#         print(" " +  indented, end="")
#     print()

print(maxLen)


'{0: >15}{0: >15}'.format('noun','verb')

# for i in range(len(translation_table)):
#     for j in range(len(translation_table[0])):
#         if translation_table[i][j] != None:
#             offset = 20 - len(translation_table[i][j])
#             if i == 0:
#                 translation_table[i][j] = color.getUnderline(color.getBlue(translation_table[i][j]))
#                 offset -= 2
#             print(" " +  color.getDarkRed(translation_table[i][j]) + ' '*offset, end="")
#     print()



# lr_dct_tg_pos vk_txt
# word = soup.find_all("div", {"class":"vk_ans"})
# pronun = soup.find_all("span", {"class":"lr_dct_ph"})
# pos = soup.find_all("div", {"class":"lr_dct_sf_h"})
# tense = soup.find_all("div", {"class":"xpdxpnd vk_gy"})
# if tense == []:
#     tense = soup.find_all("div", {"class":"vk_gy"})


# i = 0
# for w in word:
#     print "\n\t" + w.text.title(), " || Pronunciation: /",
#     if pronun != [] and i < len(pronun):
#         print pronun[i].text + ", "
#     if pos != [] and i < len(pos):
#         print "\t" + "POS: " + pos[i].text + ",  ",
#     if tense != [] and i < len(tense):
#         print tense[i].text + "."
#     i = i + 1

# i = 0
# for w in word:
#     print "\n\t" + w.text.title(),
#     if pronun != [] and i < len(pronun):
#         print " || Pronunciation: /" + pronun[i].text + ", "
#     if pos != [] and i < len(pos):
#         print "\t" + "POS: " + pos[i].text + ",  ",
#     if tense != [] and i < len(tense):
#         print tense[i].text + "."
#     i = i + 1