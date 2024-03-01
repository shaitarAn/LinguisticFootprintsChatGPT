import pandas as pd
import numpy as np
import spacy
import os
import re
import argparse
import spacy_udpipe
from nltk import ngrams
from collections import defaultdict

spacy_udpipe.download("de")

Dnlp = spacy.load('de_core_news_sm')

german_vowels = "aeiouäöüAEIOUÄÖÜ"
german_diphthongs = ['ai', 'au', 'ei', 'eu', 'äu', 'ie', 'ue']

# flesch_reading_ease = 180 - (words/sentences) - 58,5 * (syllables/words)

for corpus in ["pubmed_de", "zora_de", "20min", "cs_de", "ggponc"]:
    print(corpus)

    # initialize a large dataframe for all files   
    corpus_dataframes = []

    num_files = len(os.listdir(f"../../data/continue/{corpus}/human"))

    for i in range(1, num_files+1):
        system_dataframes = {"human": float, "continue": float, "explain": float, "create": float}
        for task in ["continue", "create", "explain"]:
            for system in ["human", "machine"]:
                
                total_words = 0
                total_sentences = 0
                total_syllables = 0
                diphtongs = 0
                total_vowels = 0

                with open(f"../../data/{task}/{corpus}/{system}/{i}", "r") as f:
                    human_content = f.read()
                    doc = Dnlp(human_content)
                    # count the number of sentences in the text
                    num_sentences = len(list(doc.sents))
                    # count the number of words in the text
                    num_words = sum(1 for token in doc if token.is_alpha)
                    # count the number of vowels in the text
                    total_vowels += len(re.findall(r'[aeiouäöü]', doc.text.lower()))
                    # # count the number of diphthongs in the text
                    diphtongs += len(re.findall(r'ai|au|ei|eu|äu|ie|ue', doc.text.lower()))
                    # # count the number of syllables in the text
                total_syllables = total_vowels - diphtongs
                flesch_reading_ease = 180-(num_words/num_sentences)- (58.5*(total_syllables/num_words))
                # print(task, system, i, flesch_reading_ease)
                if system == "human":
                    system_dataframes["human"] = flesch_reading_ease
                else:
                    system_dataframes[task] = flesch_reading_ease

        df = pd.DataFrame.from_dict(system_dataframes, orient="index")
        df = df.transpose()
        print(df)
        corpus_dataframes.append(df)

    corpus_dataframes = pd.concat(corpus_dataframes)
    if not os.path.exists(f"../visualization/combined_results/flesch/"):
        os.makedirs(f"../results_final/combined_results/flesch/")
    corpus_dataframes.to_csv(f"../results_final/combined_results/flesch/{corpus}.csv", index=False)
    print(corpus_dataframes.head())



                    


