import os
import pandas as pd
from collections import defaultdict

# count the number of tokens in the English and German corpora

#   # count the number of tokens in the English and German corpora
#   # initialize a dictionnary that will hold the counts
list_of_english_corpora = ["pubmed_en", "zora_en", "cnn", "cs_en", "e3c"]
list_of_german_corpora = ["pubmed_de", "zora_de", "20min", "cs_de", "ggponc"]

count_tokens = defaultdict(lambda: defaultdict(int))

def count_tokens_in_corpus(corpus):

    persona_dict = {}
    
    for persona in os.listdir(f"../../data_2309_gpt3/{corpus}/"):
        # check if the persona is a directory
        if os.path.isdir(f"../../data_2309_gpt3/{corpus}/{persona}"):
            for file in os.listdir(f"../../data_2309_gpt3/{corpus}/{persona}/"):
                with open(f"../../data_2309_gpt3/{corpus}/{persona}/{file}", "r") as f:
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
