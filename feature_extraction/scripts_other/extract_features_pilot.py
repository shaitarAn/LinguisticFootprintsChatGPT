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

spacy_udpipe.download("en")
spacy_udpipe.download("de")

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('textdescriptives/all')

Dnlp = spacy.load('de_core_news_lg')
Dnlp.add_pipe('textdescriptives/all')

parser = argparse.ArgumentParser()
# parser.add_argument("prompt", type=str, help="Prompt to use for text generation")
parser.add_argument("--corpus", "-c", type=str, required=True, help="Corpus name to use for text generation")
parser.add_argument("--params", type=str, required=True, help="combined params to use in file naming")

args = parser.parse_args()

corpus = args.corpus
params = args.params
print("params:", params)

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

def extract_connectives(language, file_name):
    
    # download the spacy model
    nlp = spacy_udpipe.load(language)

    # initialise a list of connectives from Thomas Meyer
    connectives = create_list_of_connectives(language)

    system_dict = defaultdict(lambda: {'lower': 0, 'capitalized': 0})

    # iterate through the files in the human-written directory with the language

    with open(file_name, 'r') as f:
        text = f.read()
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

def process_file(file_path, lang):
    with open(file_path, 'r') as file:
        content = file.read()
        # replace multiple spaces with a single space
        content = " ".join(content.split())
        # print(content)
        if lang == 'en':
            doc = nlp(content)
        elif lang == 'de':
            doc = Dnlp(content)
        
    return td.extract_dict(doc), doc

def count_oov_words(doc, system):
    if not os.path.exists(f"../output_truncated/oov/"):
        os.makedirs(f"../output_truncated/oov/")
    with open(f"../output_truncated/oov/{corpus}_{params}.txt", "a") as f:
        # f.write("--------------------\n")
        # f.write(f"{system}\n")
        for token in doc:
            if token.is_oov:
                f.write(token.text+"\n")
                # print(token.text)

def main():

    if corpus in ["cnn", "e3c", "zora_en", "pubmed_en", "cs_en"]:
        lang = 'en'
    else:
        lang = 'de'

    df_total = pd.DataFrame()

    # Create a list of file identifiers
    file_identifiers = ["file1", "file2", "file3", "file4", "file5"]

    # initialise a dataframe to store the results for all files in the corpus
    # df_total = pd.DataFrame()
    
    for identifier in file_identifiers:
        # print("--------------------------------------------------")
        print(f"Identifier: {identifier}")

        system_dataframes = []  # Initialize the list before the loop

        for file_name in os.listdir(f"../output_truncated/{corpus}/"):


            # Iterate through each file identifier
            
            # Check if the file contains the current identifier
            if identifier in file_name:
                # output_truncated_file = ""
                data = []

                # only process files with the target extensions
                if "human" in file_name or params in file_name:
                # Process the file based on its contents
                    system = file_name.split("_")[0]
                    # print(f"File: {file_name}")
                    # print(f"System: {system}")


                    connectives = extract_connectives(lang, os.path.join(f"../output_truncated/{corpus}", file_name))
                    total_connectives = sum([connectives[key]['lower'] + connectives[key]['capitalized'] for key in connectives])
                    uppper_connectives = sum([connectives[key]['capitalized'] for key in connectives])

                    # print(connectives)


                    # output_truncated_file = "../results_truncated/" + {corpus} + "/" + file_name[:-3] + "csv"
                    # print(output_truncated_file)
                    file_path = os.path.join(f"../output_truncated/{corpus}", file_name)
                    feature_values_list, obj = process_file(file_path, lang)
                    count_oov_words(obj, system)

                    for feature_values in feature_values_list:
                        # print(feature_values)
                        data.append(feature_values)
                    
                    # add all data to the dataframe 
                    df = pd.DataFrame(data)

                    # Drop columns that have NaN
                    df.dropna(axis=1, inplace=True)
                    # Drop columns that have only 0
                    df = df.loc[:, (df != 0).any(axis=0)]

                    # add a column with the number of connectives
                    df['connectives'] = total_connectives
                    df['connectives_cap'] = uppper_connectives

                    #  drop column "text"
                    df.drop(columns=['text'], inplace=True)
                    # df.to_csv(output_truncated_file, index=False)

                    #  transpose the dataframe and name the column with values as "system"
                    df = df.transpose()               
                    df.columns = [system]
                    print(df.head())

                    system_dataframes.append(df)  

        # Step 3: Combine the dataframes keeping the index
        combined_dataframe = pd.concat(system_dataframes, axis=1)
       
        # add file name as a column
        combined_dataframe['file'] = identifier.replace("file", "")
        print(combined_dataframe.head())

        # concatenate the dataframes for all files in the corpus
        df_total = pd.concat([df_total, combined_dataframe])

    # name the index as "feature"
    df_total.index.name = "feature"

    # reorganize the columns as 'file', 'feature', 'human', 'continued', 'explain', 'create'
    df_total = df_total[['file', 'human', 'continue', 'explain', 'create']]

        # print(combined_dataframe.head())
    if not os.path.exists(f"../results_pilot"):
        os.makedirs(f"../results_pilot")

    # # Step 4: Write the resulting dataframe to a CSV file
    df_total.to_csv(f"../results_pilot/{corpus}_{params}.csv", index=True)


if __name__ == "__main__":
    main()