# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import spacy
import os
import re
import argparse
import textdescriptives as td
import spacy_udpipe
from nltk import ngrams
from collections import defaultdict

parser = argparse.ArgumentParser()
# parser.add_argument("prompt", type=str, help="Prompt to use for text generation")
parser.add_argument("--corpus", "-c", type=str, required=True, help="Corpus name to use for text generation")
# parser.add_argument("--params", type=str, required=True, help="combined params to use in file naming")

args = parser.parse_args()

corpus = args.corpus
# params = args.params

spacy_udpipe.download("en")
spacy_udpipe.download("de")

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('textdescriptives/all')

Dnlp = spacy.load('de_core_news_lg')
Dnlp.add_pipe('textdescriptives/all')

def create_list_of_connectives(lang):
    # import the file of connectives from Thomas Meyer
    # the first column is the connective, the second column is the function, the third column is the frequency (if available)
    discourse_connectives_file = f'../../feature_extraction/resources/discourse_connectives_{lang.upper()}_Thomas_Meyer_2014.txt'
    # discourse_connectives_file = "../connectives_DE_frequency+20.txt"
    with open(discourse_connectives_file, 'r') as f:
        connectives = f.read().splitlines()
        connectives = [c.split('\t')[0].lower() for c in connectives]
        # print(connectives)
    return connectives

def make_ngrams(sentence, n):
    return ngrams(sentence, n)

def extract_connectives(language, file_name, average):
    
    # download the spacy model
    nlp = spacy_udpipe.load(language)

    # initialise a list of connectives from Thomas Meyer
    connectives = create_list_of_connectives(language)

    system_dict = defaultdict(lambda: {'lower': 0, 'capitalized': 0})

    # iterate through the files in the human-written directory with the language

    with open(file_name, 'r') as f:
        text = f.read()
        print(len(text.split()))
        # cut the text to the average number of tokens
        if len(text.split()) > average:
            text = " ".join(text.split()[:int(average)])
        # print(average, len(text.split()))
        all_connectives = 0
        upper_connectives = 0

        # tokenize text with spacy_udpipe
        doc = nlp(text)
        for sentence in doc.sents:
            sentence = [token.text for token in sentence]
            # iterate through 4-grams, 3-grams, bigrams and unigrams in the sentence and count the number of connectives from the list
            for n in range(4, 0, -1):
                for ngram in make_ngrams(sentence, n):
                    ngram = ' '.join(ngram)

                    if ngram.lower() in connectives and ngram[0].isupper():
                        if ngram.lower() in system_dict and system_dict[ngram.lower()]["capitalized"] != 0:
                            system_dict[ngram.lower()]["capitalized"] += 1
                        else:
                            system_dict[ngram.lower()]["capitalized"] = 1
                        all_connectives += 1
                        upper_connectives += 1
                            
                    elif ngram.lower() in connectives and ngram[0].islower():
                        if ngram.lower() in system_dict and system_dict[ngram.lower()]["lower"] != 0:
                            system_dict[ngram.lower()]["lower"] += 1
                        else:
                            system_dict[ngram.lower()]["lower"] = 1
                        all_connectives += 1

    return system_dict

def process_file(file_path, lang, average):
    with open(file_path, 'r') as file:
        content = file.read()
        # cut the text to the average number of tokens
        if len(content.split()) > average:
            content = " ".join(content.split()[:int(average)])
        if lang == 'en':
            doc = nlp(content)
        elif lang == 'de':
            doc = Dnlp(content)
        
    return td.extract_dict(doc), doc

def count_oov_words(doc, system):
    if not os.path.exists(f"../results_final/oov/"):
        os.makedirs(f"../results_final/oov/")
    with open(f"../results_final/oov/{corpus}_{system}.txt", "a") as f:
        for token in doc:
            if token.is_oov:
                f.write(token.text.strip()+"\n")

def main():

    if corpus in ["cnn", "e3c", "zora_en", "pubmed_en", "cs_en"]:
        lang = 'en'
    else:
        lang = 'de'


    num_files = len(os.listdir(f"../../data/{corpus}/human"))
    # print(corpus, num_files)
    
    for i in range(1, num_files+1):
        system_dataframes = []
        print(i)
        len_files = []
        for task in ["human", "continue", "create", "explain"]:
            with open(f"../../data/{corpus}/{task}/{i}", "r") as f:
                content = f.read()
                # replace multiple spaces with a single space
                content = content.split()
                len_files.append(len(content))
                # print(task, system, i, len(content))
        average = sum(len_files)/len(len_files)
        # print(average)
        # print("--------------")

        for task in ["human", "continue", "create", "explain"]:
            with open(f"../../data/{corpus}/{task}/{i}", "r") as f:
                print(task)

                file_path = os.path.join(f"../../data/{corpus}/{task}/", f"{i}")

                connectives = extract_connectives(lang, file_path, average)
                total_connectives = sum([connectives[key]['lower'] + connectives[key]['capitalized'] for key in connectives])
                uppper_connectives = sum([connectives[key]['capitalized'] for key in connectives])


                df = pd.DataFrame()

                # add a column with the number of connectives
                df['connectives'] = total_connectives
                df['connectives_cap'] = uppper_connectives

                print(df.head())

        #         #  drop column "text"
        #         df.drop(columns=['text'], inplace=True)
        #         # df.to_csv(output_truncated_file, index=False)

        #         #  transpose the dataframe and name the column with values as "system"
        #         df = df.transpose()               
        #         df.columns = [task]
        #         # print(df.head())

        #         system_dataframes.append(df)  # Append the DataFrame to system_dataframes

        # combined_dataframe = pd.concat(system_dataframes, axis=1)

        # print(combined_dataframe.head())

        # print(combined_dataframe.head())
        # if not os.path.exists(f"../results_final/{corpus}"):
            # os.makedirs(f"../results_final/{corpus}")

        # # Step 4: Write the resulting dataframe to a CSV file
        # combined_dataframe.to_csv(f"../results_final/{corpus}/{i}.csv", index=True)
        # combined_dataframe.to_csv(f"../results_final/{corpus}/{i}.csv", index=True)


if __name__ == "__main__":
    main()