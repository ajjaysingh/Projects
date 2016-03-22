#!/usr/bin/python
# File Name			: addpysg.py
# Description		: This command adds a python shebang to all the python files in the current directory.
# Author			: Ajay
# Date				: 2016-Mar-22
#==================================================



import os

file_list = os.listdir('.')

for files in file_list:
    if files[-3:] == '.py':
        with open(files, 'r') as head:#To make sure that the file gets closed when an exception occurs
            file_name = files.split('/')[-1]
            line1 = head.readline()
            shebang = '#!/usr/bin/python'
            if line1[0:-1] != shebang:
                with open(files, 'r+') as original:
                    with open('.temp_flie', 'w+') as temp:
                        temp.write('#!/usr/bin/python\n')
                        for line in original:
                            temp.write(line)
                        os.remove(files)
                        os.rename('.temp_flie', file_name)
                        print file_name
                        os.chmod(file_name, 0o700)
                        # os.chdir('/Users/chaser/mybin')
