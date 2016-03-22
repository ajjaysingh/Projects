import os

def translate(name):
    for i in name:
        if i in "0123456789":
            name = name.replace(i,"")        
    return name    
    

def rename_Files():
    os.chdir("/Users/chaser/Documents/Projects/Python/prank")
    file_list = os.listdir()
    print(file_list)
    for file_name in file_list:
        os.rename(file_name, translate(file_name))

#file = "16los angeles.jpg"
#print(translate(file))
rename_Files()
