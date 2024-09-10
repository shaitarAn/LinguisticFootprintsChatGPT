import sys, os
from check_output import repetition

infolder = sys.argv[1]
filepaths = [os.path.join(infolder, filename) for filename in os.listdir(infolder)]

count = 0
for filepath in filepaths:
    with open(filepath, "r", encoding="utf-8") as infile:
        text = infile.read()
    if repetition(text):
        count += 1
        print(filepath)
print(count)