import os
import re


regex = re.compile(r"(?P<Day>\d{1,2})-(?P<Month>\d{1,2})-(?P<Year>\d{2,4})")

os.chdir("Files")
for file in os.listdir():
    if file.endswith(".txt"):
        matches = re.search(regex, file)
        if matches:
            print("Match")
            print(os.listdir())
            try:
                os.mkdir("{}-{}".format(matches.group('Year'),matches.group('Month')))
            except:
                print("Already exsists")
            os.rename(file, "{}-{}-{}.txt".format(matches.group('Year')[-2:],matches.group('Month'),matches.group('Day')))


