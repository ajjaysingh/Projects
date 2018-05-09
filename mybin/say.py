#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name			: say.py
# Description		: Pronounce the given word
# Author			: Ajay
# Date				: 2016-11-26
# Python Version	: 3
#==================================================

import  requests, os, sys, json, urllib, shutil, re, pickle, spellcheck
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


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
        print("Found!")
        os.system('afplay ' + fileName)
    else:
        try:
            url = 'https://www.google.co.in/search?q=define%20' + word + '&expnd=1'
            response = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"})
            # print("\n\n>>>>",response)
            html = response.content
            sound_soup = BeautifulSoup(html, 'html.parser')
            sound_url = "http:" + sound_soup.find("audio").get("src") # get the url of the sound from the google search result.
            if len(sound_url) > 5:
                sound_response = os.system('wget ' + sound_url)
                sound_name = sound_soup.find("audio").get("src").split("/")[-1] # name of the file that will be downloaded.
                if sound_response != 2048:
                    os.system('mv ' + sound_name + ' ' + fileName)
                    os.system('afplay ' + fileName)
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
        word = str(sys.argv[1])
    else:
        word = str(input("Enter word now(Next time enter while running program!!!): "))
    os.chdir(dir)
    files = os.listdir()
    fileName = word.lower() + '.mp3'
    if fileName in files:
        file = fileName.replace(" ", "\\ ")
        print("Found!!!")
        os.system('afplay ' + fileName)
    else:
        [userWord, didItChanges]= spellcheck.checkOnline(word)
        say(userWord)