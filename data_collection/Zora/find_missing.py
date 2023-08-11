# find the files, that did not get converted for some reason or another

import os
import sys

infolder1 = sys.argv[1]  # pdf originals
infolder2 = sys.argv[2]  # txt files

files1 = [filename.split(".")[0] for filename in os.listdir(infolder1)]
files2 = [filename.split(".")[0] for filename in os.listdir(infolder2)]

for file in files1:
    if file not in files2:
        print(file)