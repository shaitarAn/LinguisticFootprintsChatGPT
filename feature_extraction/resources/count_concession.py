import os

concessions = []

with open("discourse_connectives_DE_Thomas_Meyer_2014.txt", "r") as f:
    for line in f:
        word, type = line.strip().split("\t")
        if type == "CONCESSION":
            concessions.append(word)

print(", ".join(sorted(concessions)))