#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name			: expo.py
# Description		: experimenting with google definitions
# Author			: Ajay
# Date				: 2016-12-09
# Python Version	: 3
#==================================================

import  requests, os, sys, json, urllib, shutil, re, pickle
from textwrap import fill
from collections import Counter
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys


# chromedriver = "/Users/chaser/Downloads/chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver
# driver = webdriver.Chrome(chromedriver)

# word = 'range'
# word = 'bar'
# word = 'emanating'
word = 'edgewise'
url = 'https://www.google.co.in/search?q=define%20' + word + '&expnd=1'

# driver.get(url)
# html = response.page_source

response = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"})
html = response.content

soup = BeautifulSoup(html, "lxml")

new = soup.select("div.lr_dct_ent")
# print(new[0].prettify())
# img = new[0].find("img",{"id":"lr_dct_img_origin_range0"})
block = new[0].find_all("ol",{"class":"lr_dct_sf_sens"})


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
