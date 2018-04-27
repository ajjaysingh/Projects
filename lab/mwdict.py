import urllib.request
import xml.etree.ElementTree as ET
# from key import *
import json

def process_dt(dt):
    return_str = ""
    if dt.text:
        return_str+= dt.text.strip('\n')
    for each_child in dt:
        if each_child.tag == 'it':
            return_str += process_dt(each_child)
        else:
            return_str += (" " + process_dt(each_child)+ " ")
    if dt.tail:
        return_str+= dt.tail.strip('\n')
    return_str = return_str.strip('\n')
    if dt.tag == 'sxn':
        return_str = ''
    elif dt.tag == 'sx':
        return_str = "#Synonymous: "+ return_str
    elif dt.tag == 'un':
        return_str = "\n  #Usage: " + return_str
    elif dt.tag == 'pr':
        return_str = ""
    elif dt.tag == 'vi':
        return_str = "\n  #Ex: " + return_str
    elif dt.tag == 'aq':
        return_str = ""
    return return_str

def process_def(definition):
    return_list = []
    for each_tag in definition:
        if each_tag.tag == "dt":
            return_list.append(process_dt(each_tag))
    return return_list

def process_entry(entry):
    entry_dict = {"definition":[]}
    entry_dict["word"] = entry[0].text
    fl_tag = entry.find('fl')   
    if fl_tag is not None:
        entry_dict["part"] = fl_tag.text
    for eachDef in entry.findall('def'):
        entry_dict["definition"].append(process_def(eachDef))
    return entry_dict

def process_root(root):
    for child in root:
        process_entry(child)

def load_json(filename):
    try:
        file = open(filename,'r')
        return_json = json.load(file)
        file.close()
        return return_json
    except Exception as e:
        print(e)
        return None

def print_definition(definition):
    for each_tag in definition:
        print(each_tag)

def print_explanation(explanation):
    print("@Word:{}".format(explanation['word']))
    if 'part' in explanation:
        print("@This is {}".format(explanation['part']))
    i = 0
    for each in explanation['definition']:
        print("#{}. ".format(str(i)))
        print_definition(each)
        i+=1
    


def print_word(word_dict, explanations = True, extensions =False):
    explanation_list = word_dict['explanations']
    if explanations:
        print("Explanations:")
        i = 0
        for each in explanation_list:
            print("----------------{}------------------".format(str(i)))
            print_explanation(each)
            print("----------------------------------" + '-' * ((i//10)+1) )
            i+=1
    extentions_list = word_dict['extensions']
    if extensions or len(explanation_list) == 0:
        print("Extentions:")
        i = 0
        for each in extentions_list:
            print("----------------{}------------------".format(str(i)))
            print_explanation(each)
            print("----------------------------------" + '-' * ((i//10)+1) )
            i+=1

def print_suggestions(suggestions):
    print("Not found, maybe you mean?")
    i = 0
    for each in suggestions:
        print("{}. {}".format(str(i), each))
        i+=1

def search_word(user_input, database):
    input_list = user_input.strip().split('@')
    word = input_list[0]
    should_show_extension = False
    should_update = False
    if len(input_list) > 1:
        if input_list[1] == 'e':
            should_show_extension = True
        elif input_list[1] == 'r':
            if word in database:
                del database[word]
                print('Word deleted')
                return
        elif input_list[1] == 'u':
            should_update = True
    print("You are searching for {}".format(word))
    if word in database and not should_update:
        database[word]['hit'] += 1
        print("Find local cache:")
        print("You have search for {} times".format(word), database[word]['hit'])
        print_word(database[word], extensions = should_show_extension)
    else:
        url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{}?key={}".format(word, '20025eb3-dba1-4a47-a254-73f284b7abc5')
        try:
            response = urllib.request.urlopen(url)
            response_str = response.read()
            root = ET.fromstring(response_str)
            suggestions = []
            explanations = []
            extensions = []
            for child in root:
                if child.tag == 'suggestion':
                    suggestions.append(child.text)
                    print(">>>>", suggestions)
                elif child.tag == 'entry':
                    if (child[0].text.lower() == word.lower()):
                        explanations.append(process_entry(child))
                        print(">>>>", explanations)
                    else:
                        extensions.append(process_entry(child))
                        print(">>>>", extensions)
            if len(explanations) == 0 and len(extensions) == 0:
                if len(suggestions) == 0:
                    print("Not found")
                else:
                    print_suggestions(suggestions)
            else:
                hit_count = 1
                if word in database:
                    hit_count = database[word]['hit'] + 1
                word_dict = {'explanations':explanations, 'extensions':extensions, 'hit':hit_count}
                database[word] = word_dict
                print_word(word_dict, extensions = should_show_extension)
        except Exception as e:
            print("Error", e)

def save(database, filename):
    f = open(filename, 'w')
    json.dump(database,f ,sort_keys=True,indent=4, separators=(',', ': '))
    f.close()

def search_word_longman(user_input,database):
    input_list = user_input.strip().split('@')
    word = input_list[0]
    should_show_extension = False
    should_update = False
    if len(input_list) > 1:
        if input_list[1] == 'e':
            should_show_extension = True
        if input_list[1] == 'u':
            should_update = True
    if word in database and not should_update:
        database[word]['hit'] += 1
        print("Find local cache:")
        print("You have search for {} times".format(word), database[word]['hit'])
        print_word(database[word], extensions = should_show_extension)
    else:
        url = "http://api.pearson.com/v2/dictionaries/ldoce5/entries?headword={}".format(word)
        try:
            response = urllib.request.urlopen(url)
            response_str = response.read()
            response_json = json.loads(response_str)
            if response_json and "results" in response_json and len(response_json["results"]) > 0:
                explanations = []
                extensions = []
                for each_explanation in response_json['results']:
                    new_explanatoin = {}
                    add_to_extensions = False
                    if "headword" in each_explanation:
                        new_explanatoin["word"] = each_explanation["headword"]
                    else:
                        new_explanatoin["word"] = word
                    if new_explanatoin["word"].lower() == word.lower():
                        add_to_extensions = False
                    else:
                        add_to_extensions = True
                    if "part_of_speech" in each_explanation:
                        new_explanatoin["part"] = each_explanation["part_of_speech"]
                    new_explanatoin["definition"] = [];
                    if "senses" in each_explanation and each_explanation['senses'] is not None:
                        for each_sense in each_explanation["senses"]:
                            if "definition" in each_sense:
                                for each_definition in each_sense["definition"]:
                                    new_explanatoin["definition"].append([each_definition])
                    else:
                        continue
                    if add_to_extensions:
                        extensions.append(new_explanatoin)
                    else:
                        explanations.append(new_explanatoin)
                hit_count = 1
                if word in database:
                    hit_count = database[word]['hit'] + 1
                word_dict = {"explanations":explanations, 'extensions':extensions, 'hit':hit_count}
                database[word] = word_dict
                print_word(word_dict, extensions = should_show_extension)
            else:
                print("No results")
        except Exception as e:
            print("Error", e)



if __name__ == '__main__':
    stored_json = load_json("word.json")
    longman_json = load_json("longman.json")
    if stored_json is None:
        stored_json = {}
    if longman_json is None:
        longman_json = {}

    while 1:
        entered = input("Please enter your word\n")
        if not entered:
                break
        else:
            print("****Merriem webster*****")
            search_word(entered, stored_json)
            save(stored_json, storage_file)
            print("****Longman*****")
            search_word_longman(entered, longman_json)
            save(longman_json, longman_file)