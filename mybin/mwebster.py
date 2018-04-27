#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
# File Name			: mwebster.py
# Description		: Definition from Merriam Webster
# Author			: Ajay
# Date				: 2017-07-13
# Python Version	: 3
#==================================================


import urllib.request, sys
from bs4 import BeautifulSoup

def process_one_sn(next_tag, pre_type): #prev_type to validate type is a<class 'bs4.element.Tag'> and not a navigableString
    while next_tag.name != "sn":
        if next_tag.name == "sd":
            print("; " + next_tag.text + " ", end="")
        else:
            print(next_tag.text, end="")
        if next_tag is None:
            return None
        next_tag = next_tag.next_sibling#.next_sibling
        while pre_type != type(next_tag):
            try:
                next_tag = next_tag.next_sibling
            except:
                return None
#         while next_tag == "":
#             next_tag = next_tag.next_sibling.next_sibling
#             print("ajay =====------=======---1", next_tag)
        if pre_type != type(next_tag):
            next_tag = next_tag.previous_sibling
#             print("ajay =====------=======---1",next_tag)
            return next_tag
        if next_tag is None:
            return None
#         elif "vt" in next_tag.previous_sibling.name:
#             return next_tag.previous_sibling
#         print("ajay =====------=======---2",next_tag)
#         print(type(next_tag.previous_sibling))
        if next_tag is not None and "dro" in next_tag.name:
            break
        
    print()
    print(next_tag.text, " ", end="")
    next_tag = next_tag.next_sibling.next_sibling
    return next_tag

def do_verbs(vt_form):
    vt_iter = 0
    vt_iter_tag = ''
    for vt in vt_form:
            date = def_item.find("date")
            if vt_form is not None:
                print("   ", vt.text, end="")
            if date is not None:
                print("  ", date.text)
            else:
                print()
            sn_start = def_item.find("sn")
            if vt_iter is 0:
                next_tag = sn_start
            else:
                next_tag = vt_iter_tag
            if sn_start is not None:
                print(sn_start.text, " ", end="")
#                 print(type(sn_start))
                next_tag = next_tag.next_sibling.next_sibling
#                 print(next_tag.name)
                while next_tag is not None and "dro" not in next_tag.name:
                    next_tag = process_one_sn(next_tag, type(next_tag))
                    if next_tag is None or "vt" in next_tag.name:
                        break
#                 while next_tag.name
#                 while next_tag.name != "sn":
#                     if next_tag.name == "sd":
#                         print("; " + next_tag.text + " ", end="")
#                     else:
#                         print(next_tag.text, end="")
#                     next_tag = next_tag.next_sibling.next_sibling
            print()
            vt_iter += 1
            vt_iter_tag = next_tag
            if next_tag is None:
#                 print("(----------------------------------------------)")
                break

def rest_one_sn(next_tag, pre_type):
    while next_tag.name != "sn":
#         if next_tag.name == "sn":
#             print(next_tag.text, end="")
        if next_tag.name == "sd":
            print("; " + next_tag.text, end="")
        else:
            print(" " + next_tag.text)#, end="")
        next_tag = next_tag.next_sibling#.next_sibling
        while pre_type != type(next_tag):
            try:
                next_tag = next_tag.next_sibling
            except:
#                 print("+++++++++++++++gottya------")
                return None
#     print("1st loop broke---", next_tag)
    print(next_tag.text, " ", end="")
#     next_tag = next_tag.next_sibling.next_sibling
    return next_tag

def do_rest(next_tag, pre_type):
    if next_tag is not None and next_tag.name == "sn":
        print(next_tag.text, end="")
    while next_tag is not None:
        next_tag = next_tag.next_sibling.next_sibling
        next_tag = rest_one_sn(next_tag, pre_type)




def parse_the_soup(soup):
    entries = soup.find_all("entry")
    for entry in entries:
        hw_entry_name = entry.find("hw")
        fl_part_of_speech = entry.find("fl")
        if hw_entry_name is not None:
            print("\t",hw_entry_name.text, end="")
        if fl_part_of_speech is not None:
            print(" \t", fl_part_of_speech.text, end="")
            if "verb" in fl_part_of_speech:
                forms = entry.find_all("in")
                if forms is not None:
                    print(",", end="")
                    for f in forms:
                        print(" ", f.find("if").text + ";", end="")
        def_block = entry.find_all("def")
    #     print("-", len(def_block), "-") 
        for def_item in def_block:
    #         vt_iter = 0
    #         vt_iter_tag = ''
            if "verb" in fl_part_of_speech.text:
                print()
                vt_form = def_item.find_all("vt")
                do_verbs(vt_form)
            else:
                date = def_item.find("date")
                next_tag = date
                pre_type = type(date)
                if date is not None:
    #                 next_tag = date.next_sibling.next_sibling
                    next_tag = date.next_sibling#.next_sibling
                    while pre_type != type(next_tag):
                        next_tag = next_tag.next_sibling
                    print("  ", date.text)#, type(next_tag), next_tag, next_tag.name)
                if next_tag is not None and next_tag.name == "sn":
                    do_rest(next_tag, type(next_tag))
                elif next_tag is not None: #just one meaning
                    print(next_tag.text)
            print()
                # break when the next siblling is vt
            # noun adj etc will not have a vt so handle that case also
    #         print(def_item.text, " - ")
    

if __name__ == '__main__':
    html_dictionary = ''
    html_response = ''
    key_dictionary = '20025eb3-dba1-4a47-a254-73f284b7abc5'
    # key_learners = '4b99aba1-21c0-4a98-9150-7b114c4751b9'

    word = "amenable"
    if len(sys.argv) > 1:
        word = str(sys.argv[1])
    else:
        word = input("Enter word now(Next time enter while running program!!!): ")
    xml_dict = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{}?key={}'.format(word, key_dictionary)
    # xml_learners = ' http://www.dictionaryapi.com/api/v1/references/learners/xml/run?key=' + key_learners

    with urllib.request.urlopen(xml_dict) as response:
        html_response = response
        html_dictionary = response.read()

    soup_dict = BeautifulSoup(html_dictionary, "xml")
    try:
        parse_the_soup(soup_dict)
    except:
        print("Error occurred")
    et_origin = soup_dict.find("et")
    if et_origin is not None:
        print(et_origin.text)