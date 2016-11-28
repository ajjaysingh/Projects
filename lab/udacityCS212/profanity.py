import os
import urllib.request
import urllib.parse
from urllib.request import urlopen

def check_profanity(txt):
    query = urllib.parse.quote(txt)
    req = "http://www.wdyl.com/profanity?q=" + query #urllib.request.Request("http://www.wdyl.com/profanity?q=%s" % (query))
    print(req)
    connection = urllib.request.urlopen(req)
    output = connection.read()
    print(output)
    connection.close()
    

def read_txt():
    dir = os.getcwd()
    quotes = open(dir + "/movie_quotes.txt")
    content = quotes.read()
    print(content)
    check_profanity(content)
    quotes.close()

read_txt()



"""
# Written for Python 3.4.3
#
# Checking a text file for profane words via the online webpage:
# http://www.wdyl.com/profanity?q=
#
# Alternatively text file to pirate lingo via the webpage:
# http://isithackday.com/arrpi.php?text=

from urllib.request import FancyURLopener
import os

class MyOpener(FancyURLopener):
  version = 'Chrome/37.0.2049.0 Safari/537.36' # Set for a different user agent

def fileContents(fname):
  getFile = open(fname)
  return getFile.read()
  getFile.close()

def checkProfanity(text):
  myopener = MyOpener()
  page = myopener.open('http://www.wdyl.com/profanity?q=' + text)
  output = page.read() # Webpage output in byte type
  outputStr = output.decode("utf-8") # Convert to string type
  if "true" in outputStr:
    print("Profanity alert!")
  elif "false" in outputStr:
    print("No cursewords found.")
  else:
    print("There was a problem reading the file.")

def makePiraty(text):
  myopener = MyOpener()
  page = myopener.open('http://isithackday.com/arrpi.php?text=' + text)
  output = page.read()
  print(output)

def main(fname):
  checkProfanity(fileContents(fname))
#  makePiraty(fileContents(fname))

filepath = os.getcwd() + "/movie_quotes.txt"
main(filepath)
"""
