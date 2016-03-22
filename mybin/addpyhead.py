#!/usr/bin/python
# File Name			: addpyhead.py
# Description		: adds a python header to previously created python files in the current directory
# Author			: Ajay
# Date				: 2016-03-21
# Python Version	: 2.7
#==================================================


import os
from subprocess import call

file_list = os.listdir('.')

for files in file_list:
    if files[-3:] == '.py':
        with open(files, 'r') as head:#To make sure that the file gets closed when an exception occurs
            file_name = files.split('/')[-1]
            line1 = head.readline()
            line2 = head.readline()
            shebang = '#!/usr/bin/python'
            shebang_flag = 0
            if line1[0:-1] != shebang:
                shebang_flag = 1
                        # os.chdir('/Users/chaser/mybin')

            if line1[0:11] == '# File Name':
                with open(files, 'r+') as original:
                    with open('.temp_flie', 'w+') as temp:
                        print file_name
                        temp.write('#!/usr/bin/python\n')
                        for line in original:
                            temp.write(line)
                        os.remove(files)
                        os.rename('.temp_flie', file_name)
                        os.chmod(file_name, 0o700)
            elif line2[0:11] != '# File Name':#line1[0:11] != '# File Name' and line2[0:11] != '# File Name':
                with open(files, 'r+') as original:
                    with open('.temp_flie', 'w+') as temp:
                        print file_name
                        temp.write('#!/usr/bin/python\n')
                        
                        
                        cmd = os.popen('ls -lT ' + file_name)# ls = call(['ls','-l',file_name])
                        ls = cmd.read()
                        items = ls.split()
                        date = items[8] + '-' + items[5] + '-' + items[6]
                        Author_Name = "Ajay"
                        division = '==================================================' # 50
                        temp.write('# File Name\t\t\t: ' + file_name)
                        temp.write('\n# Description\t\t: ' + '')
                        temp.write('\n# Author\t\t\t: ' + Author_Name)
                        temp.write('\n# Date\t\t\t\t: ' + date)
                        temp.write('\n#' + division)
                        temp.write('\n\n\n')

                        if shebang_flag == 0:
                            lines = []
                            for line in original:
                                lines.append(line)
                            length = len(lines)
                            for line in range(1, length):
                                temp.write(lines[line])

                        elif shebang_flag == 1:
                            for line in original:
                                temp.write(line)
                        os.remove(files)
                        os.rename('.temp_flie', file_name)
                        os.chmod(file_name, 0o700)
            # elif line1[0:11] == '# File Name':
            #     with open(files, 'r+') as original:
            #         with open('.temp_flie', 'w+') as temp:
            #             print file_name
            #             temp.write('#!/usr/bin/python\n')

                        