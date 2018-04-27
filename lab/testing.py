#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name			: testing.py
# Description		: concurrent testing of google definition project
# Author			: Ajay
# Date				: 2016-12-09
# Python Version	: 3
#==================================================


import  requests, os, sys, json, urllib, shutil, re, pickle
from textwrap import fill
from collections import Counter
from bs4 import BeautifulSoup

from time import sleep

def alignBullets(left, right):
    screen_width = shutil.get_terminal_size().columns - 15
    wrapped = fill(right, width=screen_width, subsequent_indent=' '*12)
    return '  {0:<10}{1}'.format(left, wrapped)

def wrapLineNumberDfn(right):
    screen_width = shutil.get_terminal_size().columns - 15
    wrapped = fill(right, width=screen_width, subsequent_indent=' '*11)
    return wrapped

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
        
    def getDarkRed(string):
        return color.DARKRED + string + color.END
        
    def getItalics(string):
        return color.ITALICS + string + color.END
        
    def getUnderline(string):
        return color.UNDERLINE + string + color.END
        
    def getBold(string):
        return color.BOLD + string + color.END
        
    def getRed(string):
        return color.RED + string + color.END
        
    def getDull(string):
        return color.Dull + string + color.END
        
    def getPurple(string):
        return color.PURPLE + string + color.END
        
    def getDarkCyan(string):
        return color.DARKCYAN + string + color.END
        


dir = '/Users/chaser/Projects/Dictionary/Meaning' #,"adhoc"
# WORDS = ["palpable","partisan","profound","petition","perils","progeny","peddler","paltry","percolate","preclude","precedent","pioneering","plaint","premises","pedestal","persecuted","prejudice","parched","persecute","pervasive","prudent","proliferate","persecution","premise","plenary","parochial","procreate","providential","punitive","perplexed","pleaded","protend","petrified","putative","pernicious","pertaining","predicament","peril","purge","pertinent","parlays","proactive","piqued","purgatory","proscribe","petty","peddle","purview","provisio","protracted","prevalence","peer","precarious","quell","quantum","replete","rendered","rhetoric","remit","resentment","respondent","reprisal","remand","resurgent","ratify","red-herring","refuting","rattle","remittances","reconcile","repatriated","reaking","reticent","reveals","retrograde","reprieve","remuneration","resolute","resentful","ramparts","reckoning","reeling","redress","rampage","rhetorical","repressive","reticence","reinstate","retaliate","respite","resuscitation","statutory","stringent","staggered","scourge","spurt","sinister","sacrilege","skeptical","strident","shroud","scuffle","synergy","slew","shrouded","stumped","spree","soared","savoury","sump","subversive","spooked","surreal","stench","surge","stimulus","solemnise","stature","solemn","skewed","stray","sparring","supercilious","severed","strenuous","subjugate","subdued","serene","stubble","supplication","spur","subvert","swarm","sanctum","snag","stride","slingshot","scrap","suo-moto","splurge","stance","solicit","slumped","strata","slate","stem","shoddy","sprawling","stipulated","stalemated","spanner","solidarity","sway","sporadic","sectarian","surely","suffrage","sated","shrink","sabotage","soiled","thwart","tandem","toil","triad","tender","trough","tyranny","tethered","tanneries","tirade","tinkering","traumatised","truce","transpire","tussle","unprecedented","upheaval","upsurge","unabated","utterance","vigilantes","vehement","vitiate","vanquish","viable","viability","wield","wanes","wilt",]
# WORDS = ["ANECDOTAL","ARBITRARY","ABHORRENT","APPREHENDED","AMISS","ALOFT","ASSERTIVE","ASSUAGE","ASSIDUOUSLY","AVERT","AMICABLE","AVERSE","APPRISE","ARCUATE","ABSTAIN","ASCENDANCY","ACQUIT","ASUNDER","ADHOC","ACCRUED","ACQUITTED","ASSEMBLAGE","ALBEIT","ALLURE","AFFLUENT","AGGREGATION","AMNESTY","ALTAR","AFFRONT","AMNESIA","ADJUDICATE","ADJUDICATION","ABRASIVELY","ALLEGEDLY","ABRASION","ABYSMAL","ADDUCTED","APPROPRIATED","ABATING","ABDICATION","ACCENTUATING","ABOMINABLE","ACCRUING","ARBITRATION","APPRAISAL","ABYSMALLY","ABODE","APPELLATE","ABEYANCE","ABRASIVE","ARDENT","ANGUISH","APPALLING","ACRIMONY","ACCEDE","ACREAGE","ABUT","APPROPRIATE","ANOINTED","ARBITER","AFFLUENCE","ADVERSARIES","ARCHAIC","AMID","ACCORD","ASCETIC","ABREAST","BEST","BLEACHING","BRAID","BECKON","BLATANT","BARB","BOULDER","BEGET","BRACKISH","BENEVOLENT","BROOK","BOLSTERING","BATTER","BUDGE","BLEAK","BLEAKER","BEHEST","BARON","BASIN","BIGOTRY","BRAIDED","BULGE","BENIGN","BARRED","BEST","CADRE","CONCERTED","CORPUS","CONSTRUE","CORPORATION","CONDUIT","CONSENT","CENTENARY","CURTAIL","CONTINGENCY","COHERENCE","CANING","COVETED","CONDONED","CANDID","CRUNCH","CONFER","COLLEGIUM","CONJECTURE","CALLOUS","CASH-CRUNCH","CYNICAL","CONNIVING","CONNOTATION","CONSTRUED","COARSE","CULL","CHORES","CONTENTIOUS","CLERGY","CARCASS","CRUTCH","CHATTEL","CUE","CONSPICUOUS","COERCION","COGENT","CALLOUSNESS","COMPLACENT","CHASTITY","CARDINAL","COLLATERAL","CIRCUMSPECT","COERCIVE","CONTENDED","CONTUSION","COGNIZANCE","COARSER","CUMULONIMBUS","COUNTERFEIT","CONTRARY","CONFLATES","CONGREGATE","CONTRITE","CREEK","CONVENE","CUMULUS","CONDUCIVE","CULT","CARICATURE","COHERENT","CARTEL","DISSENT","DEEM","DEPOSE","DISCORD","DETENTION","DEBILITATING","DEMEANING","DIDACTIC","DWINDLE","DESPOTISM","DISCLOSURE","DEPRAVED","DIRE","DENUDE","DISCOURSE","DELIBERATE","DENUDED","DISMAL","DENUDATION","DEPLORE","DISQUIET","DESPITE","DAUNT","DETERRENCE","DISCERNIBLE","DESPICABLE","DEMOCRACY","DETERRENT","DECIDUOUS","DISCERN","DEFERRED","DISPARITIES","DISPARITY","DENUDATE","DICHOTOMY","DUBBED","DEFUNCT","DISARRAY","DETER","DESPAIR","DIURNAL","DELVE","DISDAIN","DEPREDATION","DISGORGING","DISCRETIONARY","DELINEATE","DWELT","ELICIT","ERSTWHILE","EXFOLIATE","EXFOLIATION","ESTUARY","ELEMENT","EVICTION","EVASION","ENVISAGE","ENSUE","ENDEAVOUR","EBB","EXONERATED","EMANCIPATE","EGREGIOUS","EXIGENCY","EXACERBATE","ENTAILS","ENTRENCHED","EMANCIPATION","EMBARK","EMANATE","ENTAIL","ENVISAGED","EVOKES","ELECTORATE","EFFLUENT","EVINCED","EFFICACY","ECHELON","ENTENTE","EVICT","EMANATING","EXPATRIATES","ENCAPSULATED","EMANCIPATOR","EFFIGY","ENTRAILS","ESTRANGED","FULCRUM","FRANTICALLY","FEUDAL","FLURRY","FEUD","FACET","FRINGE","FRITTER","FRAUGHT","FRANTIC","FLANK","FIAT","FRENZIED","FESTERING","FLANKED","FLAK","FAB","FRISSON","FELICITATE","FARCE","FEDERAL","FLUVIAL","FISCAL","FRET","FEUDALISM","GOURMET","GEOID","GIBE","GLEAM","GULLIBLE","GUTTED","GIBBER","GARGANTUAN","GALVANISED","GRAPPLE","GRIEVANCE","HOSTILITY","HOUND","HOLLOW","HEINOUS","HASSLES","HIDES","HYSTERIA","HOVERED","HAUL","HEAVING","INFLICT","INTRIGUE","INSTATE","INSOLVENCY","INTIMIDATE","IMPERATIVE","INTERVENE","INEBRIATED","IMPUNITIES","INCREDULOUS","INDELIBLE","INCARCERATED","INTIMIDATING","INCIDENTAL","INTERLOCUTOR","INSTIL","INHIBITION","IMPLICATED","INUNDATE","INGENIOUS","IMPUNITY","IMPETUS","IMPELLING","IMPASSE","ISTHMUS","INCLEMENT","IMPIGNED","INJUNCTION","IMPEDE","INFUSION","INSOLATION","INURED","INCARCERATE","INIMICAL","ILK","IMPERIAL","IMPEDIMENT","JINGOISM","LURCH","LITTORAL","LAUNDERING","LEAVEN","LIBERAL","LAMENT","LUMINARY","LANDSCAPE","LAXITY","LOFTY","LIABLE","LEISURE","LEVYING","LITTER","LARGESSE","LANGUISH","LEEWARD","LEVEES","LAMENTS","LEVERAGE","LINCHPIN","MOURNED","MULL","MISCREANT","MULTIFACETED","MISSIVE","MORAINE","MAGGOTS","MAVERICK","MEANDER","MANDATE","MOROSE","MALIGN","MIRE","MORSE","METAPHOR","MANGLE","MOORING","MUZZLE","NODAL","NUDGED","NONBINDING","NOCTURNAL","NAIVE","NEPOTISM","NONCOMMITTAL","NOMINAL","OFFENSIVE","OGLING","OPINE","OBSTINATE","ORCHARD","OBLIVIOUS","OUTLAY","OBITUARY","ORCHIDS","OSTENSIBLE","OVERWHELM","PARADIGM","PLENARY","PROGENY","PETTY","PURGATORY","PROTEND","PERCOLATE","PAROCHIAL","PURVIEW","PEER","PREVALENCE","PLAINT","PERIL","PROPRIETARY","PEDIGREE","PROPRIETY","PUTATIVE","PRONOUNCE","PERTAINING","PRECLUDE","physiography","PRUDENT","PERTINENT","PERNICIOUS","PARCHED","PEDESTAL","PERSECUTION","PROSCRIBE","PETRIFIED","PERSECUTE","POST-TRUTH","PREDICAMENT","PRECEDENT","PARTISAN","PETER","PARLAYS","PIEDMONT","PLEADED","PROVIDENTIAL","PROFOUND","PROTRACTED","PROLIFERATE","PEDDLER","PETITION","PELICAN","PERSECUTED","PALPABLE","PREJUDICE","PERPLEXED","PICTURESQUE","PREMISES","PLUMMETED","PERTURB","PIONEERING","PEDDLE","PROMULGATE","PREMISE","PIQUED","PALTRY","PERILS","PAMPER","PERPETUAL","PERPETUATE","PROCREATE","PROVISION","PRECARIOUS","PERPLEX","PURPORT","PURGE","PROACTIVE","PUNITIVE","PERVASIVE","QUANTUM","QUELL","RED-HERRING","REMITTANCES","REMAND","REPARATION","REMIT","REPRIEVE","REMNANTS","RECONCILE","REDRESS","RESPITE","REPEALING","RESUSCITATION","RETROGRADE","RHETORIC","REFUTING","RECKONING","REPLETE","REPRESSIVE","RESENTMENT","RESENTFUL","REQUISITION","RETICENCE","RESPONDENT","RAMPARTS","REMUNERATION","REVERENCE","RHETORICAL","REELING","RETICENT","RATIFY","RENDERED","REPRISAL","REFERENDUM","REINSTATE","RESOLUTE","RELICT","REPATRIATION","RATIONALIZE","RATTLE","RAMPAGE","RETALIATE","REEKING","REPATRIATED","REVEALS","RESURGENT","SHROUD","SOILED","STEM","SPUR","SCOURGE","SLATE","SUO-MOTO","STRINGENT","STRATA","SPOOKED","SURREAL","STIPULATED","SHODDY","SOLEMNISE","SAVOURY","SLUMPED","SKEWED","SURELY","SPREE","SECTARIAN","SUBJUGATE","SPANNER","SCRAP","SHREDDING","SHROUDED","SURGE","SANCTUM","SYNERGY","SONOROUS","SWARM","STATUTORY","SLUMP","STAGGERED","STRIDENT","SATED","STENCH","SUFFRAGE","SUMMIT","SPURT","SPARRING","SHRINK","SNAG","SUBVERT","SUPPLICATION","STRAY","SUBSIDE","STATURE","SACRILEGE","SOLICIT","SERRATED","STANCE","SCUFFLE","SERENE","SKEPTICAL","SUBSIDING","SPORADIC","STEPPE","SOLIDARITY","SPRAWLING","SOARED","SOLEMN","STRIDE","STUBBLE","SLINGSHOT","STIMULUS","SYNCLINAL","STALEMATE","SUPERCILIOUS","SEVERED","SUBDUED","SENTINEL","SABOTAGE","SLEW","SINISTER","SWAY","STRENUOUS","SUMP","SUBVERSIVE","STUMPED","SPLURGE","TROUGH","TANNERIES","THROES","TANDEM","TOIL","TETHERED","THWART","TIRADE","TRIBUNE","TRIBUNAL","TENDER","TYRANNY","TUSSLE","TRAUMATISED","TOPOGRAPHY","TRENCH","TRIAD","TINKERING","TRUCE","TRANSPIRE","UPHEAVAL","UNPRECEDENTED","UPSURGE","UNABATED","UTTERANCE","VERNACULAR","VITIATE","VIABLE","VANQUISH","VIRTUE","VEHEMENT","VAGUE","VIABILITY","VIGILANTES","VINDICTIVE","VENAL","VOCATIONAL","WANES","WIELD","WILT"]
WORDS = ["edgewise","apprehended","element","emanating","feudalism","like","make","conduct","bar","shoal","abode"]#"UPHEAVAL","UNPRECEDENTED","UTTERANCE","UNABATED","UPSURGE"]

def check(word):
    url = 'https://www.google.co.in/search?q=define%20' + word + '&expnd=1'
    response = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"})
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    new = soup.select("div.lr_dct_ent")

    for block in new:
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
            print(color.getCyan(" /" + subBlock_pronun[0].text), end="")
        iterator = 0
        # print(len(subBlock_POS))
        for subName in subBlock_POS:
            print("  " + color.getRed(color.getItalics(subName.getText(separator=u' '))), end="")   # the prints the part of speech which defines a sub block        
            if iterator < len(subBlock_lineBelowPOS):
                print(" | " + subBlock_lineBelowPOS[iterator].text, end="")
            if (pronun_done_flag == False) and (iterator < len(subBlock_pronun)):
                print("   " + color.getCyan("/" + subBlock_pronun[iterator].text), end="")
            if subBlock_wordForm != None:
                print("\n\t" + subBlock_wordForm.text, end="")
            # print("\t" + subBlock_crux.text)
            lines = subBlock_crux[iterator].find_all("div", {"class":"lr_dct_sf_sen vk_txt"})
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
                        # print("\t  " + "\u2022 ", end="") #prints the bullet
                        print(alignBullets("        \u2022", color.getBright(dfn.text)))
                    if first_eg != None: #Sometimes the example just after the definition is absent
                        print("\t   " + first_eg.text)
                    if syns_antons != None:
                        for item in syns_antons:
                            title = item.find("td", {"class":"lr_dct_nyms_ttl"})
                            nyms = item.find_all("span")
                            eg = item.find("div", {"class":"vk_gy"})
                            print("\t   " + color.getItalics(title.text) + " " ,end="")
                            for nym in nyms[:5]:
                                if nym.text[-1] != "\"": # since taking all the span will get the examples also and since examples end in " therefore we need to skip them
                                    print(nym.text, end="")
                            if eg != None:
                                print("\n\t\t    " + eg.text)
                            else:
                                print()
                            # print(item.text)
                    # print()
                # second = line.find("div", {"class":"vk_gy"})
                # print(first.text)
                # print("\t   " + second.text)
                # print("\t   " + line.text)
                # print()
            iterator = iterator + 1
            # print()





for word in WORDS:
    print("The word is :", word)
    check(word.lower())
    print()