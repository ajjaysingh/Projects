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
import say, spellcheck
import time

dir = '/Users/chaser/Projects/Dictionary/Meaning'
userWord = ''
incorrect_words = []

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
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    trans = soup.find("div", {"class":"lr_dct_trns"})
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
        raiseDefinitionException(final_soup, word) # we need to pass word to this also because sometimes the word will be changed.
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
                bullets = line.find_all("div", {"class":"_Jig"})
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
                            syn_antons_words = ""
                            for nym in nyms:
                                if nym.text[-1] != "\"" and nym.text != 'More': # since taking all the span will get the examples also and since examples end in " therefore we need to skip them
                                    # print(nym.text, end="")
                                    syn_antons_words = syn_antons_words + nym.text.strip('\n').strip('\t').strip('  ') + ' '
                            print(printSynAntons(syn_antons_title, syn_antons_words), end="")
                            if eg != None:
                                print("\n\t\t    " + eg.text)
                            else:
                                print()


def changeFileNameIfSearchNotSame(givenFileName, givenWord, searchedWord):
    os.chdir(dir + '/' + givenWord[0].upper())
    fileName = dir + '/' + searchedWord[0].upper() + '/' + searchedWord.lower() + ".txt"
    os.system("mv " + givenFileName + " " + fileName)
    print("Attention!!! The word searched is " + searchedWord + " instead of " + givenWord)



def findWordIfAlreadyScrapped(word, fileName, wordToSave):
    wordGiven = word
    os.chdir(dir + '/' + word[0].upper())
    files = os.listdir()
    if fileName in files:
        file = fileName.replace(" ", "\\ ")
        print("Found!!")
        os.system("cat " + file)
        os.chdir(dir + '/' + word[0].upper())
    else:
        try:
            chromedriver = "/Users/chaser/Projects/mybin/chromedriver"
            os.environ["webdriver.chrome.driver"] = chromedriver
            driver = webdriver.Chrome(chromedriver)
            sys.stdout = Logger(fileName)
            [definitionElement, word, trans] = getGoogleResponse(word, driver)
            vocabResults(word)
            # print(definitionElement)
            # print("there")
            extractFromGoogleElement(definitionElement)
            extractHindi(trans)
            # print("here")
            # exit(5)
            driver.quit()
            # os.system('mv ../../' + fileName + ' .') now no need to move ;)
            sys.stdout = sys.__stdout__
            if wordGiven != word:  # If the word is changed by google then the changed word should be saved instead of the wrong user supplied word.
                wordToSave = word.replace(" ", "-")
                incorrect_words.append(wordGiven)
                incorrect_words.append(word)
            # addword.addWordFromMean(wordToSave)       #!!!!!!!!!!!   also in the if statement >>>>>>>>>HEY DON"T FORGET TO UNCOMMENT THIS TO ADD THE QUERIED WORD TO wordlists
            os.chdir(dir + '/' + word[0].upper())
            print(word, wordGiven)
            if wordGiven != word:
                changeFileNameIfSearchNotSame(fileName, wordGiven, word)
            # print(">>!!!!>>")
        except NoDefinition as e:
            try:
                vocabResults(e.word)
                print("\n\tWiki Definition:")
                print(printAligned("\t", e.msg))
                driver.quit()
                sys.stdout = sys.__stdout__
                if wordGiven != e.word:  # If the word is changed by google then the changed word should be saved instead of the wrong user supplied word.
                    wordToSave = e.word.replace(" ", "-")
                    incorrect_words.append(wordGiven)
                    incorrect_words.append(e.word)
                addword.addWordFromMean(wordToSave)       #!!!!!!!!!!!   also in the if statement >>>>>>>>>HEY DON"T FORGET TO UNCOMMENT THIS TO ADD THE QUERIED WORD TO wordlists
                os.chdir(dir + '/' + e.word[0].upper())
                if wordGiven != e.word:
                    changeFileNameIfSearchNotSame(fileName, wordGiven, e.word)
            except:
                sys.stdout =sys.__stdout__
                os.system('rm ' + fileName)
                driver.quit()
        except:
            sys.stdout =sys.__stdout__
            os.system('rm ' + fileName)
            driver.quit()
        # say()




all_words_List = ["SCANTY","SCATHE","SCATHING","SCEPTIC","SCEPTICISM","SCEPTICS","SCHADENFREUD","SCHADENFREUDE","SCHEMATIC","SCHEMATISE","SCHEMING","SCHMISM","SCOFF","SCOFFER","SCOOCH","SCORE","SCORNFUL","SCRAP","SCREECH","SCREED","SCRIBE","SCRUFFY","SCRUPULOUS","SCUMB","SCUTTLE","SEAR","SEARING","SEARINGLY","SECESSION","SEDULOUS","SEISMIC","SEIZURE","SELECTION-BIAS","SEMBLANCE","SEMINATE","SENILE","SENILITY","SENSOR","SENTENTIOUS","SENTINEL","SERENDIPITY","SERMON","SERRATED","SERVIENT","SERVITUDE","SETT","SETTLEMENT","SEVER","SEVERED","SEVERITY","SEXAGENARIAN","SEXIST","SEXUALITY","SHACK","SHACKLE","SHAM","SHAMAN","SHBBY","SHEER","SHELVE","SHILL","SHOOT","SHOVEL","SHREDDING","SHREWD","SHRIEK","SHRINK","SHRIVEL","SHROUD","SHROUDED","SHUDDER","SHUDDERING","SHUN","SIEVE","SIFT","SILAGE","SILO","SINECURE","SINISTER","SIRE","SITTING-DUCKS","SKEPTICISM","SKEWED","SKIRMISH","SKORMISH","SLACK","SLAPDASH","SLATE","SLAVIC","SLEAZE","SLEAZY","SLENDER","SLEUTH","SLEW","SLICK","SLINGSHOT","SLOPPY","SLOVEN","SLOVENLY","SLUMBER","SLY","SMARITAN","SMATTER","SMATTERING","SMEAR","SMITE","SMOTHER","SNAFFLE","SNAG","SNAP","SNEAK","SNEERING","SNIDE","SNIPE","SNOBBISH","SNOOT","SNOOTY","SNUB","SNUCK","SOARED","SOCIAL-DARWINISM","SOCIAL-DARWINIST","SOCIOPATH","SOILED","SOLECISM","SOLEMNISE","SOLEMNLY","SOLICITOR","SOLIVAGANT","SOLSTICE","SOMBER","SONOROUS","SOPHISTICATE","SOPHISTICATED","SORDID","SOUGHT","SOUVENIR","SOVEREIGN","SPANK","SPANNER","SPARING","SPARK","SPARRING","SPASM","SPECTRE","SPELL","SPELLING","SPEW","SPIEL","SPIRITUAL","SPITE","SPITEFUL","SPLATTER","SPLINE","SPLINTER","SPLURGE","SPOOKED","SPORT","SPRAWLING","SPREE","SPURIOUS","SQUANDER","SQUANDREL","SQUASH","SQUEAKY","SQUEAL","SQUEE","STAGGERED","STAGNANT","STALEMATE","STALWART","STANCE","STATE","STATE","STATESMAN","STATUESQUE","STATURE","STATUS","STATUS-QUO","STATUTORY","STAUNCH","STAY-PUT","STEAK","STEGANOGRAPHY","STEGNOGRAPHY","STEM","STENCH","STENOGRAPHER","STEREOTYPICAL","STERN","STEROTYPE","STEWARD","STIMULUS","STINT","STIPEND","STIPULATE","STIPULATED","STOCHASTIC","STOW","STRATA","STRATAGEM","STRATEGIC","STRENUOUS","STREW","STRIDENT","STRINGENT","STROKE","STROLL","STRONG","STUBBLE","STUMBLE","STUMPED","STUMPET","STUPEFY","STUPENDOUS","SUBDUED","SUBJECTIVE","SUBJECTIVITY","SUBJUGATION","SUBLIMATION","SUBLIME","SUBSIDENCE","SUBSIDING","SUBSTANCIATE","SUBSTANTIAL","SUBSTATIATE","SUBSTRATE","SUBTLETY","SUBVERSE","SUBVERSION","SUCCINCT","SUCCOUR","SUCCULENT","SUFFICE","SUFFRAGE","SULK","SULLEN","SUMP","SUNDRY","SUO-MOTTO","SUPERCILIOUS","SUPERFLUITIES","SUPPLE","SUPPLICATION","SUPREMACIST","SUPREMACY","SURELY","SURLINESS","SURREAL","SURROGATE","SWAG","SWAMP","SWAT","SWATH","SYCOPHANT","SYMBIOSIS","SYMPATHISER","SYMPATHY","SYNAGOGUE","SYNAGOUGE","SYNCLINAL","SYNCLINE","SYNDICATE","SYNECDOCHE","SYNOPSIS","SYNTHESIS","TACKY","TACT","TACTIC","TACTICAL","TACTLESS","TALISMAN","TANGIBLE","TANNERIES","TANNERY","TATTLE","TAUNT","TAXONOMIC","TAXONOMY","TEDIOUS","TEMINISCE","TEMPERAMENT","TEMPT","TEMPTATION","TENABLE","TENTMENT","TERTIARY","TESTIMONIAL","TESTY","TETHERED","THAW","THEO","THEOLOGIST","THESPIAN","THRASH","THRESH","THRIFT","THROWBACK","TIMID","TINGLE","TINKERING","TITRATE","TITRATED","TOIL","TOME","TOPOGRAPHY","TORMENT","TOUT","TRANS","TRANSCENDENT","TRANSCENDENTAL","TRANSGRESS","TRANSGRESSION","TRANSGRESSIONS","TRANSHUMANCE","TRANSIENT","TRANSITIVE","TRANSUBSTANTIATE","TRANSUBSTANTIATION","TRAUMATISED","TRENCH","TRIAD","TRIAGE","TRIBULATION","TRIBUNAL","TRIBUNE","TRIFLING","TRIUMPHALISM","TRIUMPHALIST","TROLL","TROT","TRUCE","TRUCULENT","TRUDGE","TRUSTAFARIAN","TUMBLE","TUMULTUOUS","TURMOIL","TUSSLE","TWEAK","TWEAKER","TWINGE","TYRANNY","TYRO","UMPROBABLE","UMPTEEN","UNABATED","UNABRIDGE","UNCONSCIONABLE","UNCONTRITE","UNDERDONG","UNDERHAND","UNDERSCORE","UNDERWRITE","UNDULATED","UNFATHOMABLE","UNFLAPPABLE","UNGAINLY","UNHERALD","UNILATERAL","UNINTERESTED","UNITARY","UNIVERSALISE","UNIVERSALISING","UNKEMPT","UNPRECEDENT","UNPRECEDENTED","UNRAVEL","UNREQUITE","UNSAVORY","UNSAVOURY","UNSCATHED","UNSCRUPULOUS","UNSCURPULOUS","UNSPARING","UNTENABLE","UNWARY","UNWITTING","UPEND","UPSURGE","UTILITARIANISM","UTOPIAN","UTTER","VAGARY","VAGUE","VAIN","VALEDICTION","VALEDICTORIAN","VALEDICTORY","VALENCE","VALIANT","VALOROUS","VALOUR","VANQUISH","VANTAGE","VASCETOMY","VASECTOMY","VEIN","VENALITY","VENEER","VENERATE","VENIAL","VENT","VENTURE","VERACIOUS","VERBAL","VERDICT","VERILY","VERITABLE","VERNAL","VERSATILE","VEST","VESTIGE","VETTING","VEX","VIABILITY","VIADUCT","VICARIOUS","VICE","VICEROY","VICIOUS","VIGIL","VIGILANTES","VILE","VILIFICATION","VILIFY","VINDICTION","VIRTUOUS","VIRTUOUSITY","VISTA","VITIATE","VITUPERATE","VITUPERATIVE","VIVIDNESS","VOCATIONAL","VOCIFEROUS","VORTEX","VOTARY","VOW","WACKY","WADE","WADED","WADING","WAFK","WAIL","WAIVE","WALLOW","WANES","WAX","WEARINESS","WEARY","WEASEL","WEED","WELTER","WELTSCHMERZ","WHACK","WHEEDLE","WHEREBY","WHEREIN","WHIMP","WHIMPER","WHIMSY","WHIP","WHITE-PICKET-FENCE","WHITHER","WICKED","WIELD","WILE","WILLY-WILLY","WILTING","WILY","WINCH","WISHFUL-THINKING","WITHER","WITHHOLD","WITTING","WOBBLE","WOE","WOUND","WOUND-UP","WREAK","WRECKED","WRENCH","WREST","WRETCH","WRETCHED","WRIT","WROUGHT","WUMP","XENOPHOBE","XENOPHOBIA","ZEALOT","ZEITGEIST","ZEITGIST","ZEST","ABBERATION","ABOMINABLE","ABREAST","ABSTRUCE","ACCOMPLICE","ACCRETION","ACQUIANT","ACUTE","ADDENDUM","ADHOC","ADJOURN","AFFIRMATIVE","AFFLICT","AFFLUENT","AGONY","ALOOF","ALPINE","AMBIT","AMID","AMNESTY","AMULET","ANALOGOUS","ANECDOTE","ANNEXURE","ANNULLED","APPENDAGE","APPRISE","APPROPRIATENESS","APPROPRIATING","ARBITRARY","ARDENT","ASCENDANCY","ASPERSION","ASSEMBLAGE","ASSIDUOUSLY","ASSIMILATE","ATONE","ATTIC","AUSTERE","BAIL","BAIT","BANAL","BANANA-REPUBLIC","BARON","BARRAGE","BENIGN","BEREAVE","BEREFT","BESET","BICAMERAL","BIGOTRY","BLATANT","BLINKER","BOURGEOISIE","BRACKISH","BRISTLE","BUDGE","CALLOUS","CALLOUSNESS","CAPTIVATE","CARCASS","CARICATURE","CASTIGATE","CAUCASIAN","CAUCASUS","CENSOR","CENSURE","CHIVALROUS","CIRCUMSPECT","CIRCUMSTANTIAL-EVIDENCE","CLEMENT","CLICHE","COARSE","COAST","COERCIVE","COGENT","COGNIZANCE","COLLEGIUM","COLLOQUAL","COLLUDER","COMPETENCE","COMPLIANT","COMPREHEND","COMPREHENSIVE","CONCOCTION","CONCORD","CONDONE","CONDUCIVE","CONFERRED","CONNIVE","CONNOTE","CONSECRATE","CONSORT","CONSPICUOUS","CONSPICUOUSLY","CONTENTIOUS","CONTINGENCY","CONTRIVE","CONUNDRUM","CONVENTION","COROLLARY","CORROBORATE","COUP","COVENANT","COVERT","COVET","CREDENCE","CRUTCH","CURTAIL","CYNIC","DECADENT","DEFECATE","DEFER","DELIBERATE","DELVE","DEMEANOUR","DEPLORE","DEPOSE","DEPOSITION","DEPREDATION","DERANGE","DERELICT","DERELICTION","DESICCATE","DETERRENCE","DETERRENT","DETRIMENT","DETRIMENTAL","DEVOLUTION","DIATRIBE","DIDACTIC","DIGRESSION","DILAPIDATE","DIRE","DISCLOSURE","DISCRETION","DISCRETIONARY","DISPARAGING","DITHER","DIURNAL","DIVIDEND","DOGMA","DOGMATIC","DROOPY","DRUDGERY","DWELL","ECCEDENTESIAST","ECCENTRIC","ECCENTRICITY","ECHELON","ECSTASY","EGOISM","EGOIST","ELITIST","ELUDE","ELUSIVE","EMANCIPATION","ENRAGE","ENTAIL","ENTHRALL","ENUNCIATE","EPISTEMOLOGY","EQUIVOCAL","ERUDITION","ESCHEW","ESPOUSE","EUPHEMISM","EVICTION","EXALT","EXCREPT","EXEMPLAR","EXORABLE","EXPEDITE","FABLE","FACET","FARE","FARSE","FAWN","FEND","FEROCIOUS","FERRET","FEUDAL","FIDELITY","FLABBERGASTED","FLAK","FLAMBOYANT","FLEE","FORAGE","FORMIDABLE","FRANCHISE","GALVANIZE","GIBE","GLIB","GLOAT","GRISLY","GUTTED","HAUGHTY","HAUL","HERESY","HERETIC","HOLISTIC","HOSTILE","HOSTILITY","HUBRIS","HUMBLE","ICONOCLAST","IDOSYNCRACY","IMPERATIVE","IMPLEMENT","IMPUDENT","INCUMBENT","INDICTMENT","INEBRIATED","INEQUITY","INFURIATE","INQUISITIVE","INSEMINATION","INSINUATION","INSULAR","INTERLOCUTOR","INTERMITTENT","INTIMIDATE","INTRIGUE","JAYWALK","JUBILATE","JUXTAPOSE","KIN","KIOSK","KNEEJERK","LAMBAST","LEISURE","LINGER","LITIGATE","LUCID","LULL","LUMINARIES","LUMINARY","MALIGNANT","MARAUDERS","MAVERICK","MAXIM","MAYHEM","MEADOW","MEDDLE","MERITOCRACY","MIRE","MORTGAGE","MUNDANE","NATION","NATION-STATE","NEMESIS","NEOLIBERALISM","NEPOTISM","NEUROTIC","NICHE","NIMBLE","NOCTURNAL","NODAL","OBITUARY","OBSCURITY","OBSTINATE","OBTUSE","OFFICIOUS","OPINE","ORDEAL","ORIENTALIST","ORNATE","OSTENSIBLE","OSTENTATIOUS","OSTRACISE","OUTRIGHT","PALEOLITHIC","PALEONTOLOGIST","PALTRY","PAN","PANACHE","PARABLE","PARADIGM","PARANOIA","PARTAKE","PARTISAN","PATHETIC","PATHOS","PATRIARCHY","PATRONIZE","PECULIAR","PEDAGOGY","PEDANTIC","PEDERASTY","PEDIGREE","PEG","PELICAN","PERCOLATE","PERFUNCTORY","PERHAPS","PERJURY","PERPLEX","PERVASIVE","PETULANT","PICKET","PICKET-FENCE","PILLORY","PITHY","PLAUSIBLE","PLEBISCITE","PONDERABLE","POPULISM","POSTHUMOUS","PRECOCIOUS","PREDOMINANT","PRELUDE","PREPOSTEROUS","PREROGATIVE","PRESCIENT","PREVALENCE","PREVARICATE","PRIVY","PROACTIVE","PROCURE","PROFANITY","PROGNOSIS","PROLE","PROLETARIAN","PROLETARIAT","PROLIFERATE","PROMISCUOUS","PROMULGATE","PROPRIETARY","PROSTRATE","PROSTRATION","PROTAGONIST","PROVISION","PRUDE","PRY","PUNITIVE","PURGATORY","PURVIEW","QUAINT","QUANDARY","QUIRK","RAMBLE","RECENCY-BIAS","RECKON","RECKONING","REDEEM","REDRESS","RELENT","REMNANT","REMUNERATION","RENEGADE","REPATRIATION","REPUBLIC","REPUDIATE","REQUISITION","RESENTFUL","RESENTMENT","RESILIENCE","RESOLUTION","RESPITE","RESUSCITATION","RETICENT","RETROGRADE","RHETORIC","RIGHTEOUS","ROSETTA","SACROSANCT","SAG","SALIENT","SANCTUM","SANGFROID","SANGUINE","SCEPTICAL","SCHMEGEGGE","SCORN","SCOUNDREL","SCRUPLE","SCURRY","SECTARIAN","SECTARIANISM","SERENE","SERENITY","SERVILE","SERVILITY","SHAMBLE","SHODDY","SKEPTICAL","SLOG","SLUMPED","SLUR","SMUG","SMUGNESS","SNEER","SNOB","SOLEMN","SOLICIT","SOLIDARITY","SPAR","SPECIOUS","SPIRITUALITY","SPORADIC","SPRAWL","SPUR","SPURN","SPURT","SQUABBLE","SQUATTER","STAGGER","STEPPE","STIGLE","STRAY","SUBJUGATE","SUBSUME","SUBTERFUGE","SUBVERSIVE","SUBVERTED","SULTRY","SUO-MOTO","SUPERFLUOUS","SURLY","SURREPTITIOUSLY","SWARM","SWAY","SYNCRETISM","SYNERGY","TANDEM","TENDER","TENET","TENSOR","THEOLOGY","THROES","THWART","TIRADE","TITILLATE","TOTALITARIAN","TRANSPIRE","UBIQUITOUS","UNANIMOUS","UNBRIDLE","UNCANNY","UNDERMINE","UNDERTONE","UNEQUIVOCAL","UNFETTER","UNFOUNDED","UPBRAID","UPHEAVAL","UTOPIA","UTTERANCE","VANDALISE","VENAL","VERBATIM","VESTED","VET","VIABLE","VISCERA","VIVID","VOCATION","VORACIOUS","VOUCH","WANE","WAR","WARY","WEDGE","WIT","ZENITH","ABSOLVE","ACCENTUATE","AESTHETIC","ALLEGIANCE","ALLURE","AMISS","ANARCHY","APPALLING","APPELLATE","APPREHENSIVE","APPROPRIATION","ARTEFACT","ASTUTE","ATTENUATE","AVENUE","BABBLE","BENEVOLENT","CAJOLE","CAPRICE","CAPRICIOUS","CARNAGE","CATER","CAVEAT","COHERENT","COHORT","COLLATERAL","COMPLACENCY","COMPLICITY","CONDESCENDING","CONFER","CONGREGATE","CONSORTIUM","CORDIAL","CULMINATE","DECREE","DELINEATE","DENIGRATE","DESPISE","DETER","DIASPORA","DILIGENT","DISCORD","DISCOURSE","DOMINION","EDIFICE","EFFICACY","ELOQUENT","EMANATE","ENERVATE","ENSEMBLE","ENSUE","EPHEMERAL","EXACERBATE","EXPEDIENT","FARCE","FEDERATION","FEEBLE","FELICITATE","FERVOUR","FETTER","FRANTIC","FRAY","HEED","HEINOUS","HYSTERIA","IDENTITY-POLITICS","IMPEDIMENT","IMPERTINENT","IMPROVISE","IMPUNITY","INCLEMENT","INFLICT","INGENIOUS","INIMICAL","INTONATION","INUNDATE","INVETERATE","LAMENT","LIBEL","LIBERAL","LIBERTY","MALIGN","MANDATE","MEAN","MELANCHOLY","MORBID","MULL","NAIVE","NEO","NIHILIST","NUANCE","OBNOXIOUS","OBSCURE","PALPABLE","PANTHEON","PAUCITY","PEDESTAL","PERTAINING","PERTURB","PETTY","PIETY","PLUMMETED","POIGNANCY","POIGNANT","PROLIFIC","PROPENSITY","PURGE","PURIST","QUASI","RATTLE","RAVEN","RAVENOUS","RECONCILE","REDEMPTION","REFERENDUM","REMAND","REPARATION","RESENT","REVERENCE","SAVAGE","SCOURGE","SCUFFLE","SECEDE","SILVER-LINING","SLUMP","STARTLE","STATUTE","STRIDE","SUBSIDE","SUBTLE","SUBVERT","SUMMIT","SURGE","TRIADE","TRITE","TROUGH","UBIQUITY","UNFETTERED","VEHEMENT","VERNACULAR","VINDICATE","VINDICTIVE","VIRTUE","WILT","ACCORD","ALLEGORY","APPROPRIATE","ASSIDUOUS","CLEMENCY","COLLUDE","CONCEIT","CONDESCEND","CONSTRUE","DAUNT","DESPICABLE","DICHOTOMY","DISCERN","DISSENT","DISSIDENT","EBB","EPITHET","FEDERAL","FRINGE","IMPASSE","IMPEDE","OBLITERATE","OMINOUS","OVERWHELM","PERIL","PERTAIN","PERTINENT","POLEMIC","POST-TRUTH","PRECARIOUS","PROGENY","PROSCRIBE","PRUDENCE","RAMPANT","SLANDER","VISCERAL","WHIM","ABROGATE","ASSUAGE","BLEAK","CYNICAL","DISDAIN","DISPARAGE","EGALITARIAN","EGREGIOUS","OXYMORON","PAROCHIAL","PREDICAMENT","PRUDENT","REPRIMAND","AUSTERITY","BUSTLE","COMPLACENT","CONNOTATION","PERNICIOUS","PROPRIETY","VANITY"]



for word in all_words_List:
    wordToSave = word  # To handle the cases of words like banana-republic
    word = word.replace("-", " ") # we should save it as banana-republic and search it as banana repuiblic
    os.chdir(dir + '/' + word[0].upper())
    fileName = word.lower() + ".txt"  # because the saved word should not have a space between them
    failed_word = []
    try:
        findWordIfAlreadyScrapped(word.lower(), fileName, wordToSave)
    except:
        failed_word.append(word.lower)
    time.sleep(3) # delays for 5 seconds
    os.chdir("..")
print("\n\nFailed Words :\n\n", failed_word)
print("\n\nFailed Words :\n\n", incorrect_words)

# # files = os.listdir()
# # pattern = re.compile(r'[\w]+.txt')
# # last_word = [x for x in files if re.search(pattern, x)]
# # os.system('mv ' + last_word[0] + '.txt Meaning/' + last_word[0][0].upper())
# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         word = str(sys.argv[1])
#     else:
#         word = input("Enter word now(Next time enter while running program!!!): ")

#     wordToSave = word  # To handle the cases of words like banana-republic
#     word = word.replace("-", " ") # we should save it as banana-republic and search it as banana repuiblic
#     os.chdir(dir + '/' + word[0].upper())
#     fileName = wordToSave.lower() + ".txt"  # because the saved word should not have a space between them
#     files = os.listdir()
#     if fileName in files:
#         file = fileName.replace(" ", "\\ ")
#         print("Found!!")
#         os.system("cat " + file)
#         addword.addWordFromMean(wordToSave) # To avoid saving space in the saved word
#         os.chdir(dir + '/' + word[0].upper())
#     else:
#         userWord = spellcheck.checkOnline(word)
#         fileName = userWord.lower() + ".txt"
        
#         findWordIfAlreadyScrapped(userWord, fileName, wordToSave)
