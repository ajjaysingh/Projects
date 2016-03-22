#!/usr/bin/python
# File Name			: mycmds.py
# Description		: This command lists all the commnads and their description.
# Author			: Ajay
# Date				: 2016-Mar-22
#==================================================



import os
from os import path

file_list = os.listdir("/Users/chaser/Projects/mybin")

file_list = filter(path.isfile, file_list)

os.chdir('/Users/chaser/Projects/mybin')
count = 1
print 'SCRIPTS'
for files in file_list:
    head = open(files, 'r')
    description = ''#head.readline()
    for line in head:
        if line[0:13] == '# Description':
            description = line
            break;
    #print description
    #print count, '.', files + '\t\t:', description.split(':')[1]
    if description != '':
        print files + '\t\t:', description.split(':')[1],# trailing comma to supress newline
    #print ''#----x----x----x----x----x----x----'
    count += 1
    head.close()
print ''
print 'ALIASES'
os.chdir('/Users/chaser')
with open('.bash_profile','r') as bash:
    for lines in bash:
        if lines[0:6] == 'alias ':
            parts = lines.split('=')
            print parts[0].split()[1] + '\t\t\t:' , parts[1].split('#')[1],    # [0:-1] to escape printing of newline from file
