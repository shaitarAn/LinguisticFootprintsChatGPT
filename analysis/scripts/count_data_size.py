import os
import pandas as pd
from collections import defaultdict

generation = "data_2309gpt3"
root = os.path.expanduser(f"~/switchdrive/AItextDetect/{generation}")

if generation in ["data_2309gpt3", "data_2403gpt4"]:
    list_of_english_corpora = ["pubmed_en", "zora_en", "cnn", "cs_en", "e3c"]
    list_of_german_corpora = ["pubmed_de", "zora_de", "20min", "cs_de", "ggponc"]
elif generation in ["data_2409gpt4"]:
    list_of_english_corpora = ["pubmed_en", "cnn"]
    list_of_german_corpora = ["pubmed_de", "20min"]

count_tokens = defaultdict(lambda: defaultdict(int))

def count_tokens_in_corpus(corpus):

    persona_dict = {}
    
    for persona in os.listdir(f"{root}/{corpus}/"):
        # check if the persona is a directory
        if os.path.isdir(f"{root}/{corpus}/{persona}"):
            for file in os.listdir(f"{root}/{corpus}/{persona}/"):
                with open(f"{root}/{corpus}/{persona}/{file}", "r") as f:
                    for line in f:
                        # add the persona to the dictionnary
                        if persona not in persona_dict:
                            persona_dict[persona] = len(line)
                        else:
                            persona_dict[persona] += len(line)
    return persona_dict

#   # for each corpus, count the number of tokens
for corpus in list_of_english_corpora:
    print(corpus)
    persona_count = count_tokens_in_corpus(corpus)
    # add corpus and count to the dictionnary
    count_tokens[corpus] = persona_count


for corpus in list_of_german_corpora:
    print(corpus)
    persona_count = count_tokens_in_corpus(corpus)
    # add corpus and count to the dictionnary
    count_tokens[corpus] = persona_count

#   # save the counts to a csv file
df = pd.DataFrame(count_tokens)

print(df)

# write the dataframe to a latex table
with open("../../viz/for_paper/tokens_per_corpora.tex", "w") as f:
    f.write(df.to_latex())

# count total for humans in df
df["total"] = df.sum(axis=1)//4
print(df)
