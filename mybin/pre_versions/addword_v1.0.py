#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name			: addword.py
# Description		: It adds the provided word to my custom dictionary. The new words that I learn.
# Author			: Ajay
# Date				: 2016-05-03
# Python Version	: 3
#==================================================

import os
import sys


def instructions():
    print("\n\t***Please Follow the prompts, If you want to enter multiple meanings seperate them using simicolon(;).")
    print("\n\t***You can add any additional information you want to add ")
# move to directory containg the dictionary
# IMPORTANT - while handling files always do this => first make a temp copy of file then proceed if try fails the you should restore the file
os.chdir("/Users/chaser/Projects/")
# print(os.system("ls"))

try:
    temp_name = ".myDict_temp" #name of the temporary duplicate file
    os.system("cp "+ "myDict "+ temp_name)
    print(instructions())
    # print("copied")
    # os.system("ls " + "-la")
    with open("myDict", 'a') as dictionary: #always use this because if opening of file fails the file will not get overwritten
        new_word = str(sys.argv[1])
        meaning = input("\nEnter the meaning for the word " + new_word + ": ") #raw_input renamed to input, take input the m
        example = input("\nEnter some example for the word: ")
        count = 0 # count the total no of words already present
        with open("myDict", 'r') as read_file: # open the file just for reading the number of words already present, we can not read a file in append mode
            for line in read_file :
                if line[0:3] == ">>>" :         # [0:3] is like [)
                    count = count + 1           # the line is read as an array, [0:3] means 0,1,2    here 3 is not include
                if (len(line) > 4) and new_word.upper() == line[3:-1]:
                    print("Word already present")
                    exit(1)                     # on exit 1 it will go to except
            # print(count)
        dictionary.write(">>>\n")
        dictionary.write(str(count + 1) + ". " + new_word.upper() + "\n")
        dictionary.write("Meaning: " + meaning + '\n')
        dictionary.write("Example: " + example + '\n' + '\n')
        # os.system("rm "+ temp_name) #we need to remove the temp file whether try suceeds or fails

except:
    files = os.listdir()
    if temp_name in files:
        os.system("cp " + temp_name + " myDict")
        print("try agian!")

finally:                                            # always executed whether try suceeds or not
    files = os.listdir()
    if temp_name in files:
        os.system("rm " + temp_name)


