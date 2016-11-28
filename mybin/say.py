#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name			: say.py
# Description		: Pronounce the given word
# Author			: Ajay
# Date				: 2016-11-26
# Python Version	: 3
#==================================================

import  requests, os, sys, json, urllib, shutil, re, pickle, spellcheck
from bs4 import BeautifulSoup

dir = '/Users/chaser/Projects/Dictionary/Meaning/sounds'

def macmillan(word):
    url = 'http://www.macmillandictionary.com/dictionary/british/' + word.lower()
    response = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"})
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    pron = soup.find("span",{"class":"PRONS"})
    img = pron.find("img")
    link = img.get('data-src-mp3')

'''Says the word out loud'''
def say(word):
    os.chdir(dir)
    files = os.listdir()
    fileName = word.lower() + '.mp3'
    if fileName in files:
        file = fileName.replace(" ", "\\ ")
        print("Found!!")
        os.system('afplay ' + fileName)
    else:
        try:
            url = 'https://ssl.gstatic.com/dictionary/static/sounds/de/0/' + fileName
            response = os.system('wget ' + url) #wget -O will output the downloaded content to specified file
            # print("\n\n>>>>",response)
            if response != 2048:
                os.system('afplay ' + fileName)
                # os.system('rm ' + fileName)
            else:
                try:
                    url = macmillan(word)
                    response = os.system('wget ' + url + ' -O ' + fileName) #wget -O will output the downloaded content to specified file
                except:
                    os.system('say ' + word)

        except:
            print("\n\nSound not available at Google!")
            os.system('say ' + word)


# if we don't write this then since we have imported this in mean.py so everytime mean.py will be run
# the below code will also be executed.
if __name__ == '__main__':
    if len(sys.argv) > 1:
        userWord = spellcheck.checkOnline(str(sys.argv[1]))
    else:
        userWord = spellcheck.checkOnline(int(input("Enter word now(Next time enter while running program!!!): ")))
    say(userWord)
