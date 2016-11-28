#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name			: vocabularyScrapy.py
# Description		: Using Scrapy on Vocabulary.com
# Author			: Ajay
# Date				: 2016-11-25
# Python Version	: 3
#==================================================


import json, scrapy, requests, os, sys
from bs4 import BeautifulSoup


word = 'unalienable'
url = 'https://www.vocabulary.com/dictionary/' + word
response = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"})
html = response.content
vocab_soup = BeautifulSoup(html, "lxml")


# https://corpus.vocabulary.com/api/1.0/examples.json?jsonp=jQuery112408316049204578237_1480068552656&query=unalienable&maxResults=24&startOffset=0&filter=0&_=1480068552657
# https://corpus.vocabulary.com/api/1.0/examples.json?query=unalienable&maxResults=24&startOffset=24&filter=0

w = vocab_soup.find("span", {"class":"word"})
print(w.text.upper())
short = vocab_soup.find("p", {"class":"short"})
print(short.text)
lonng = vocab_soup.find("p", {"class":"long"})
print(short.text)
print(lonng.text)

url = 'https://corpus.vocabulary.com/api/1.0/examples.json?query=' + str(word) + '&maxResults=24&startOffset=0&filter=0'
print(url)
res = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"})

import json, urllib

html = urllib.request.urlopen(url).read()
# print(html)
j = json.loads(html.decode('utf-8'))
# pprint.pprint(j)
l = j['result']['sentences']
for s in l[:5]:
    print(s['sentence'])