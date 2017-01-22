import os
from os.path import join

print(os.listdir())
os.chdir("Files")
print(os.listdir())

number_list =[]

for numbers, name in enumerate(os.listdir()):
    number_list.append(int(os.path.splitext(name)[0]))

number_list.sort()
alphabet = 96
for number in number_list:
    alphabet += 1
    str_numb = str(number) + ".txt"
    if os.path.isfile(str_numb):
        os.rename(str_numb, chr(alphabet) + ".txt")
    else:
        print("Error on", + number)
        break


# print(number_list)
# number_list.sort()
# print(number_list)
# number_list.reverse()
# print(number_list)
