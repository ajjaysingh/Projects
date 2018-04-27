class color:
     MAGENTA     = '\033[35m'
     CYAN        = '\033[36m'
     BLUE        = '\033[34m'
     BRIGHT      = '\033[37m'
     DARKYELLOW  = '\033[33m'
     GREEN       = '\033[32m'
     DARKRED     = '\033[31m'
     DULL        = '\033[30m'
     PURPLE      = '\033[95m'
     DARKCYAN    = '\033[36m'
     RED         = '\033[91m'
     BOLD        = '\033[1m'
     ITALICS     = '\033[3m'
     UNDERLINE   = '\033[4m'
     END         = '\033[0m'
     def getItalics(string):
        return color.ITALICS + string + color.END

posHeading = translations.find_all("div", {"class":"lr_dct_tg_pos vk_txt"})
translation_heading = []
for pos in posHeading:
    translation_heading.append(pos.text)

translation_table = []
translation_table.append(translation_heading)

for trans in transWords:
    print(trans.get_text(' '))

translation_word_subBlock = {}
subBlockMinLength = 100
listNumber = 1
for trans in transWords:
    wordList = trans.get_text('||').split('||')
    # print(wordList)
    if len(wordList) < subBlockMinLength:
        subBlockMinLength = len(trans)
    wordNumber = 1
    for listWord in wordList:
        print (listWord)
        translation_word_subBlock[listNumber, wordNumber] = listWord
        wordNumber = wordNumber + 1
    listNumber = listNumber + 1

translation_table = []
translation_table.append(translation_heading)
for nWord in range(1, subBlockMinLength+1):
    tempList = []
    for nList in range(1, listNumber):
        tempList.append(translation_word_subBlock.get((nList, nWord)))
    print(tempList)
    translation_table.append(tempList)

for i in range(3):
    for j in range(3):
        print("\t\t " + translation_table[i][j], end="")
    print()

for row in translation_table:
    print("{: >25} {: >25} {: >25}".format(*row))

