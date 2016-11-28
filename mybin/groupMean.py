#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name			: groupMean.py
# Description		: find meanings of a group of words
# Author			: Ajay
# Date				: 2016-11-27
# Python Version	: 3
#==================================================
import mean, spellcheck
import sys
from time import sleep

dir = '/Users/chaser/Projects/Dictionary/Meaning' #,"adhoc"
WORDS = ["palpable","partisan","profound","petition","perils","progeny","peddler","paltry","percolate","preclude","precedent","pioneering","plaint","premises","pedestal","persecuted","prejudice","parched","persecute","pervasive","prudent","proliferate","persecution","premise","plenary","parochial","procreate","providential","punitive","perplexed","pleaded","protend","petrified","putative","pernicious","pertaining","predicament","peril","purge","pertinent","parlays","proactive","piqued","purgatory","proscribe","petty","peddle","purview","provisio","protracted","prevalence","peer","precarious","quell","quantum","replete","rendered","rhetoric","remit","resentment","respondent","reprisal","remand","resurgent","ratify","red-herring","refuting","rattle","remittances","reconcile","repatriated","reaking","reticent","reveals","retrograde","reprieve","remuneration","resolute","resentful","ramparts","reckoning","reeling","redress","rampage","rhetorical","repressive","reticence","reinstate","retaliate","respite","resuscitation","statutory","stringent","staggered","scourge","spurt","sinister","sacrilege","skeptical","strident","shroud","scuffle","synergy","slew","shrouded","stumped","spree","soared","savoury","sump","subversive","spooked","surreal","stench","surge","stimulus","solemnise","stature","solemn","skewed","stray","sparring","supercilious","severed","strenuous","subjugate","subdued","serene","stubble","supplication","spur","subvert","swarm","sanctum","snag","stride","slingshot","scrap","suo-moto","splurge","stance","solicit","slumped","strata","slate","stem","shoddy","sprawling","stipulated","stalemated","spanner","solidarity","sway","sporadic","sectarian","surely","suffrage","sated","shrink","sabotage","soiled","thwart","tandem","toil","triad","tender","trough","tyranny","tethered","tanneries","tirade","tinkering","traumatised","truce","transpire","tussle","unprecedented","upheaval","upsurge","unabated","utterance","vigilantes","vehement","vitiate","vanquish","viable","viability","wield","wanes","wilt",]

for word in WORDS:
    sys.stdout = sys.stdout
    print(word)
    word = spellcheck.checkOnline(word)
    fileName = word.lower() + ".txt"
    mean.findWordIfAlreadyScrapped(word, fileName)
    sys.stdout.flush()
    # sleep(5)