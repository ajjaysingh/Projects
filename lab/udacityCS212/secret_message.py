import os, sys
import random
import shutil

cities = ["abidjan","addis","ahmedabad","alexandria","ankara","baghdadh","bangkok","bengaluru","berlin","bogotán","busan","capetown","casablanca","changsha","chengdu","chongqing","dar","dhaka","dongguan","durban","ekurhuleni","faisalabad","foshan","giza","guangzhou","hangzhou","hanoi","harbin","hefei","hochimin","hongkong","jaipur","jakarta","jeddah","johannesburg","kabul","kinshasa","kolkata","lagos","lahore","lima","mexico city","moscow","mumbai","nairobio","nanjing","new taipei city","newyork","ningbo","peshawar","pune","pyongyang","quanzhou","rawalpindi","rio","riyadh","saint petersburg","santiago","seoul","shanghai","shantou","shenyang","shenzhen","singapore","surat","suzhou","sãopaulo","tehran","tianjin","tokyo","wenzhouvue","wuhan","xi'an","xiamen","yangon","yokohama","zhengzhou","zhongshan","zunyi","genua","ancona","messana","norfolk","charleston","providence","albany","andover","hertford","shefford","spalding","tenduk","heret","sari","tsingshui","maragheh","turfan","beshbalik","almalik","bukhara","bangor","clonfert","wexford","galway","bantry","waterford","derry","galway","kinsale","kildare","carrick","drogheda","aldorg","ringsted","lejre","nidaros","breman","murcia","corunna","badajoz","christchurch","greymouth","hokitika","westport","blenheim","canberra","wollongon","taree","rockhampton","kalgoorlie","wanneroo","perth","eyre","durban","pretoria","windhoek","haalenberg","toliara","muang","bhamo","mandalay","henzada","sittwe","namtur","heho","prome","bago","nan","falam","kalewa","menghai","hekou","lampang","toungoo"]

#os.chdir("/Users/chaser/Documents/Projects/Python/alphabet")
image_dir = "alphabet"
msg_dir = "prank"
file_list = os.listdir(image_dir)

def rename_files(message):
    city_index = 0
    space_index = 28
    full_stop = 27
    message = message.lower();
    directory = os.getcwd()
    cwd_list = os.listdir()
    if msg_dir in cwd_list:
        shutil.rmtree(msg_dir)
    os.mkdir(msg_dir, 0o777 )
    for character in message:
        if character == ' ':
            src_path = file_list[space_index]
        elif character == '.':
            src_path = file_list[full_stop]
        else:
            print(character)
            alpha_index = "abcdefghijklmnopqrstuvwxyz".index(character)
            src_path = file_list[alpha_index + 1]
        src_path = image_dir + "/" + src_path
        dst_path = msg_dir + "/" + str(random.randint(1,10000)) + cities[city_index] + ".jpg"
        print(dst_path)
        shutil.copyfile(src_path, dst_path)
        city_index = city_index + 1       
    print(message)


for i in file_list[1:]:
    cities.append(i.replace(".jpg",""))
cities.sort()

message = "hope you are well just in case you forgot i still love you"

arg = ""
if len(sys.argv) >=2:
    arg = arg + sys.argv[1]
    for input in sys.argv[2:]:
        arg = arg + " " + input
    message = arg   

print(message)     
rename_files(message)
    
