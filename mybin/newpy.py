#!/usr/bin/python
# File Name			: newpy.py
# Description		: To create a new python file with permissions and header set.
# Author			: Ajay
# Date				: 2016-Mar-22
#==================================================
# add purpose like to  what course or site the code is related to and the usage i.e how to run the file whether it requires some cmd line args


import os
from time import strftime

# get file name as input from the user and add .py at the end of it
title = raw_input("Enter the name of the file: ")
title = title + '.py'

# remove any space from the title by replacing it by underscore
title = title.replace(' ', '_')

# Check if file exists then exit with a warning
if os.path.exists(title):
    print '\nFile named  \"%s\"  already exists!!!\nPlease try again with a different name.\n' %title
    exit(0)

description = raw_input("Enter a description: ")
Author_Name = "Ajay"
division = '==================================================' # 50

shebang_choice = 1
shebang_choice = raw_input('\nDo you want to add shebang(/usr/bin/python) to this file?\nPress 1 for YES (DEFAULT)\nPress 2 for NO\n: ')
shebang = '/usr/bin/python'
if int(shebang_choice) == 1:
    version_choice = raw_input('\nPress 2 for Python 2.7\nPress 3 for Python 3\n: ')
    version = 2.7
    if int(version_choice) == 3:
        version = 3
        shebang = '/Library/Frameworks/Python.framework/Versions/3.4/bin/python3'

date = strftime("%Y-%m-%d")

try:
    # create a new file
    file = open(title, 'w')

    # write to file
    # file.write('#' + division)

    if int(shebang_choice) == 1:
        file.write('#!' + shebang)
        file.write('\n')
    file.write('# File Name\t\t\t: ' + title)
    file.write('\n# Description\t\t: ' + description)
    file.write('\n# Author\t\t\t: ' + Author_Name)
    file.write('\n# Date\t\t\t\t: ' + date)
    print "asssss"
    if int(shebang_choice) == 1:
        file.write('\n# Python Version\t: ' + str(version))
    file.write('\n#' + division)
    file.write('\n\n\n')

    os.chmod(title, 0o700)
    os.system('subl '+ title)

except:
    print "\n\t Please Try Again!!\n"
    if os.path.exists(title):
        os.remove(title)
