#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name			: alter.py
# Description		: Add some extra information to the file of a word.
# Author			: Ajay
# Date				: 2016-12-18
# Python Version	: 3
#==================================================


import os, sys, difflib

dir = '/Users/chaser/Projects/Dictionary/Meaning'

if len(sys.argv) > 1:
    word = str(sys.argv[1])
else:
    word = input("Enter word now(Next time enter while running program!!!): ")

os.chdir(dir + '/' + word[0].upper())
fileName = word.lower() + ".txt"
files = os.listdir()
# close = difflib.get_close_matches(fileName, files)
# print(close)
if fileName in files:
    file = fileName.replace(" ", "\\ ")
    print("Found!!")
    os.system("subl " + file)
    os.system("cat " + file)
else:
    close = difflib.get_close_matches(fileName, files)
    print(close)
    close_index  = input("Select the index of the list if you want to open a file otherwise press enter to exit: ")
    if close_index.isdigit():
        file = close[int(close_index)].replace(" ", "\\ ")
        print("Found!!")
        os.system("subl " + file)
        os.system("cat " + file)
    else:
        print("Exiting without opening")
