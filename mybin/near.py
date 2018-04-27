#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name			: near.py
# Description		: Find the words closest to a given word.
# Author			: Ajay
# Date				: 2017-06-13
# Python Version	: 3
#==================================================


import os, sys, difflib

def closestTo(word):
    all_words_file = '/Users/chaser/Projects/Dictionary/initial_files/allWords.txt'
    allWords = []
    with open(all_words_file, "r") as f:
        allWords = f.readlines()

    for w in allWords:
        new_w = w.replace("\"", "").strip("\n")
        new_w = "".join([i for i in new_w if not i.isdigit()])
        allWords[allWords.index(w)] = new_w.lower()
    # print(allWords[:10])
    print (difflib.get_close_matches(word, allWords, 10))
        # print(w.replace("\"", "").translate(digits))
    # os.chdir(dir + '/' + word[0].upper())
    # fileName = word.lower() + ".txt"
    # files = os.listdir()

    # if fileName in files:
    #     file = fileName.replace(" ", "\\ ")
    #     print("Found!")
    #     os.system("cat " + file)
    # else:
    #     close = difflib.get_close_matches(fileName, files)
    #     print(close)
    #     close_index  = input("Select the index of the list if you want to open a file otherwise press enter to exit: ")
    #     if close_index.isdigit():
    #         file = close[int(close_index)].replace(" ", "\\ ")
    #         print("Found!!!")
    #         os.system("cat " + file)
    #     else:
    #         print("Exiting without opening")

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        word = str(sys.argv[1])
    else:
        word = str(input("Enter the word: "))
    closestTo(word)
