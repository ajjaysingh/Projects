#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name			: show.py
# Description		: shows the meaning of the word just notified
# Author			: Ajay
# Date				: 2016-12-20
# Python Version	: 3
#==================================================

import os, sys, difflib

def displayMeaning(word):
    dir = '/Users/chaser/Projects/Dictionary/Meaning'
    os.chdir(dir + '/' + word[0].upper())
    fileName = word.lower() + ".txt"
    files = os.listdir()

    if fileName in files:
        file = fileName.replace(" ", "\\ ")
        print("Found!")
        os.system("cat " + file)
    else:
        close = difflib.get_close_matches(fileName, files)
        print(close)
        close_index  = input("Select the index of the list if you want to open a file otherwise press enter to exit: ")
        if close_index.isdigit():
            file = close[int(close_index)].replace(" ", "\\ ")
            print("Found!!!")
            os.system("cat " + file)
        else:
            print("Exiting without opening")

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        word = str(sys.argv[1])
    else:
        word = str(input("Enter the word: "))
    displayMeaning(word)



# import applescript

# scpt = applescript.AppleScript('''
#     on foo()
#         return "bar"
#     end foo

#     on Baz(x, y)
#         return x * y
#     end bar

#     on run()
        # tell application "Terminal"
        #     do script "alter.py accord"
        # end tell
#     end run
# ''')

# scpt.run()
# print(scpt.run('Hello', 'World')) #-> None
# print(scpt.call('foo')) #-> "bar"
# print(scpt.call('Baz', 3, 5)) #-> 15

# from Foundation import *
# word = "accord"
# # cmd = "tell app \"Finder\" to activate"
# cmd = """tell application "Terminal"
#   do script "alter.py """ + word + """"
# end tell
#         """
# s = NSAppleScript.alloc().initWithSource_(cmd)
# s.executeAndReturnError_(None)


