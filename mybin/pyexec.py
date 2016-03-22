#!/usr/bin/python
# File Name			: pyexec.py
# Description		: This command changes the permission of all files ending in .py to 700.
# Author			: Ajay
# Date				: 2016-Mar-22
#==================================================




import os

file_list = os.listdir(".")

for file in file_list:
    ending = file[-3:]
    # print ending
    if ending == '.py':
        print file
        os.chmod(file, 0o700)
