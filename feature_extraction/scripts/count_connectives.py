# !/usr/bin/env python3
# -*- coding: utf8 -*-

'''This script will compare the number of connectives in chatGPT-written text with the number of connectives in human-written text. It will count the total number of connectives for English and German in the root directory. The list of connectives is from the tab-separated imported txt fils'''

import os
import pathlib
import csv
import re
from nltk import ngrams
import spacy_udpipe
from collections import defaultdict

spacy_udpipe.download("en")
spacy_udpipe.download("de")

# Create a Path object for the directory
root = pathlib.Path('../../data/')

# check if output directory exists
if not os.path.exists('../results/connectives/'):
    os.makedirs('../results/connectives/')

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

def extract_connectives(language, corpus, system):
    
    # download the spacy model
    nlp = spacy_udpipe.load(language)

    # initialise a list of connectives from Thomas Meyer
    connectives = create_list_of_connectives(language)
    # print(connectives)

    system_dict = defaultdict(lambda: {'lower': 0, 'capitalized': 0})
    file_dict = defaultdict(lambda: {'total': 0, 'capitalized': 0})

    # Create a Path object for the directory
    directory_path = pathlib.Path(root, corpus, system)
    print(directory_path)
    file_count = 0

    # Use a list comprehension to generate a list of file paths
    file_list = [file_path for file_path in directory_path.iterdir() if file_path.is_file()]

    # iterate through the files in the human-written directory with the language
    for f in sorted(file_list):
        print(f)

        with open(f, 'r') as f:
            text = f.read()
            all_connectives = 0
            upper_connectives = 0
            file_count += 1

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

            file_dict[file_count]["total"] = all_connectives
            file_dict[file_count]["capitalized"] = upper_connectives
            # print(file_count, all_connectives, upper_connectives)

    return system_dict, file_dict
    
def main():

    # itarate over subdirectories in directory_path
    for subdirectory in os.listdir(root):
        # itarate over files in subdirectory
        corpus = subdirectory
        if corpus in ['20min', 'ggponc', "pubmed_de", "zora_de", "cs_de"]:
            lang = 'de'
        else:
            lang = 'en'
        
        if not os.path.isdir(os.path.join(root, subdirectory)):
                continue 

        print("-------------------")
        # print(corpus)      

        human_dict = {}
        continue_dict = {} 
        explain_dict = {}
        create_dict = {} 
        combined_dict = {} 
        combined_file_dict = {}    

        for system in os.listdir(os.path.join(root, subdirectory)):
    
            print(lang, corpus, system)

            if system == 'human':
                human_dict, human_file_dict = extract_connectives(lang, corpus, system)

            elif system == 'continue':
                continue_dict, continue_file_dict = extract_connectives(lang, corpus, system)

            elif system == 'explain':
                explain_dict, explain_file_dict = extract_connectives(lang, corpus, system)

            elif system == 'create':
                create_dict, create_file_dict = extract_connectives(lang, corpus, system)
            
            else:
                continue

        # combine 4 dictionaries into one based on keys
        for key in set(human_dict.keys()) | set(continue_dict.keys()) | set(explain_dict.keys()) | set(create_dict.keys()):
            combined_dict[key] = {
            'human_upper': human_dict.get(key, {}).get('capitalized', 0),
            'human_total': human_dict.get(key, {}).get('capitalized', 0) + human_dict.get(key, {}).get('lower', 0),
            'continue_upper': continue_dict.get(key, {}).get('capitalized', 0),
            'continue_total': continue_dict.get(key, {}).get('capitalized', 0) + continue_dict.get(key, {}).get('lower', 0),
            'explain_upper': explain_dict.get(key, {}).get('capitalized', 0),
            'explain_total': explain_dict.get(key, {}).get('capitalized', 0) + explain_dict.get(key, {}).get('lower', 0),
            'create_upper': create_dict.get(key, {}).get('capitalized', 0),
            'create_total': create_dict.get(key, {}).get('capitalized', 0) + create_dict.get(key, {}).get('lower', 0),}

        print(combined_dict)
        print(combined_file_dict)

        # write the dictionaries to csv files
        with open(f'../results/connectives/connectives_all_{corpus}.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['connective', 'human_upper', 'human_total', 'continue_upper', 'continue_total', 'explain_upper', 'explain_total', 'create_upper', 'create_total'])
            for key, values in combined_dict.items():
                writer.writerow([key, values["human_upper"], values["human_total"], values["continue_upper"], values["continue_total"], values["explain_upper"], values["explain_total"], values["create_upper"], values["create_total"]])

main()
