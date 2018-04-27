#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name         : notify.py
# Description       : notification of a word experiment
# Author            : Ajay
# Date              : 2016-12-19
# Python Version    : 3
#==================================================

# ps aux | grep notify
# notify.py & disown

import os, time, show, subprocess, applescript
from random import randint
from random import shuffle
from Foundation import *

scpt = applescript.AppleScript('''
        on run()
            tell application "Terminal"
                do script "alter.py accord"
            end tell
        end run
    ''')

apple_cmd = "osascript -e '{0}'"
while True:
    os.chdir("/Users/chaser/Projects/Dictionary/initial_files/")
    wordsList = []
    with open("allWords.txt", 'r') as wordsAll:
        wordsList = wordsAll.read().replace("\"", "").split()
    shuffle(wordsList)
    index = randint(0, len(wordsList)) % len(wordsList) 
    score = wordsList[index][0]
    word = wordsList[index][1:]
    base_cmd = 'display notification "{0}" with title "{1}"'.format("score of " + word.title() + " is " + str(score), word.title())
    cmd = apple_cmd.format(base_cmd)
    subprocess.Popen([cmd], shell=True)
    showMeaning = """tell application "Terminal"
  do script "show.py """ + word + """"
end tell"""
    s = NSAppleScript.alloc().initWithSource_(showMeaning)
    s.executeAndReturnError_(None)
    # print(word, score)
    # show.displayMeaning(word)
    time.sleep(3600) # 60 min




'''

To strictly answer your question, the application icon can be removed by setting LSUIElement to YES in the Info.plist for the Python application wrapper.

sudo defaults write /System/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/Info "LSUIElement" -string "1"
Should do it, but it will hide it for any Python applications. The changes can be reverted by substituting the 1 for a 0.

I also had to chmod the Info.plist file afterwards for some reason, not sure if that was just my configuration or what.


'''






"""
import os

word = "Accord"
mean = "1. give or grant someone (power, status, or recognition)."

print("osascript -e \"display notification \\\"$text\\\" with title \\\"$title\\\"\"")
print("osascript -e 'display notification \"Lorem ipsum dolor sit amet\" with title \"" + word + "\"'")

os.system("osascript -e 'display notification \""+ mean +"\" with title \"" + word + "\"'")


os.system("tell application \"Terminal\"\
    do script \"show accord\"\
end tell")


import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
"""



# import subprocess
# import time
# import sys


# notification_delay = 5
# check_delay = 60
# title = "Ruddra Website"
# # rss = 'https://feedity.com/ruddra-com/VFZQWlFU.rss'

# # if '-nt' in sys.argv:
# #     notification_delay = int(sys.argv[sys.argv.index('-nt') + 1])

# # if '-ct' in sys.argv:
# #     check_delay = int(sys.argv[sys.argv.index('-ct') + 1])

# # if '-t' in sys.argv:
# #     title = sys.argv[sys.argv.index('-t') + 1]

# # if '-u' in sys.argv:
# #     rss = sys.argv[sys.argv.index('-u') + 1]

# apple_cmd = "osascript -e '{0}'"
# while True:
#     _notification = "1. give or grant someone (power, status, or recognition)."
#     print(_notification)
#     base_cmd = 'display notification "{0}" with title "{1}"'.format(_notification, title)
#     cmd = apple_cmd.format(base_cmd)
#     subprocess.Popen([cmd], shell=True)
#     time.sleep(notification_delay)
#     time.sleep(check_delay)





# import applescript

# scpt = applescript.AppleScript('''
#     on foo()
#         return "bar"
#     end foo

#     on Baz(x, y)
#         return x * y
#     end bar

#     on run()
#         tell application "Terminal"
#             do script "alter.py accord"
#         end tell
#     end run
# ''')

# scpt.run()
# print(scpt.run('Hello', 'World')) #-> None
# print(scpt.call('foo')) #-> "bar"
# print(scpt.call('Baz', 3, 5)) #-> 15