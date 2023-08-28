### Adjusting the Zora filenaming to be in line with the rest

import os
import sys
import re

infolder = sys.argv[1]
lang = sys.argv[2]

def match_zora_name(string):
    result = re.match(r"(\d{4})-(.+?)\.txt", string)
    return result.group(1), result.group(2)

for filename in os.listdir(infolder):
    year, title = match_zora_name(filename)
    # print(filename, ": ", year, " ", title)
    with open(os.path.join(infolder, filename), "r", encoding="utf-8") as infile:
        for i in range(7):
            infile.readline()
        num_toks = len(infile.read().split())
    new_filename = f"{year}-{title}_{num_toks}_{lang}.txt"
    os.rename(os.path.join(infolder, filename), os.path.join(infolder, new_filename))


