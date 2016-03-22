import os

file_list = os.listdir()

for file in file_list:
    os.chmod(file, 0o700)
