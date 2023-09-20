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

# expand root directory with os.path.expanduser()
root = os.path.expanduser('~/switchdrive/IMAGINE_files/chatGPT/project_2/final_files_simple_prompt_2')

def create_list_of_connectives(lang):
    # import the file of connectives from Thomas Meyer
    # the first column is the connective, the second column is the function, the third column is the frequency (if available)
    discourse_connectives_file = f'../resources/discourse_connectives_{lang.upper()}_Thomas_Meyer_2014.txt'
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

    system_dict = defaultdict(lambda: {'lower': 0, 'capitalized': 0})
    file_dict = defaultdict(lambda: {'total': 0, 'capitalized': 0})

    # Create a Path object for the directory
    directory_path = pathlib.Path(root, corpus, system)
    file_count = 0

    # Use a list comprehension to generate a list of file paths
    file_list = [file_path for file_path in directory_path.iterdir() if file_path.is_file() and file_path.suffix == '.txt']

    # iterate through the files in the human-written directory with the language
    for f in sorted(file_list):

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
        if corpus in ['20min', 'GGPONC', "pubmed_de", "zora_de"]:
            lang = 'de'
        else:
            lang = 'en'
        
        if not os.path.isdir(os.path.join(root, subdirectory)):
                continue 

        print("-------------------")
        # print(corpus)      

        human_dict = {}
        machine_dict = {}  
        combined_dict = {} 
        combined_file_dict = {}    

        for system in os.listdir(os.path.join(root, subdirectory)):
    
            # print(system)

            if system == 'human':
                human_dict, human_file_dict = extract_connectives(lang, corpus, system)

            elif system == 'machine':
                machine_dict, machine_file_dict = extract_connectives(lang, corpus, system)
            
            else:
                continue

        # Combine the two dictionaries
        for key in set(human_dict.keys()) | set(machine_dict.keys()):
            combined_dict[key] = {
            'human_upper': human_dict.get(key, {}).get('capitalized', 0),
            'human_total': human_dict.get(key, {}).get('capitalized', 0) + human_dict.get(key, {}).get('lower', 0),
            'machine_upper': machine_dict.get(key, {}).get('capitalized', 0),
            'machine_total': machine_dict.get(key, {}).get('capitalized', 0) + machine_dict.get(key, {}).get('lower', 0),} 


        #  combine the human_file_dict and machine_file_dict based on keys
        for key in set(human_file_dict.keys()) | set(machine_file_dict.keys()):
            combined_file_dict[key] = {
            'human_upper': human_file_dict.get(key, {}).get('capitalized', 0),
            'human_total': human_file_dict.get(key, {}).get('total', 0),
            'machine_upper': machine_file_dict.get(key, {}).get('capitalized', 0),
            'machine_total': machine_file_dict.get(key, {}).get('total', 0),}

        with open(f'../output/connectives_all_{corpus}.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['connective', 'human_upper', 'human_total', 'gpt_upper', 'gpt_total'])
            for key, values in combined_dict.items():
                writer.writerow([key, values["human_upper"], values["human_total"], values["machine_upper"], values["machine_total"]])

        with open(f'../output/paired_features_{corpus}/connectives_upper.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['gpt', 'human'])
            for key, values in combined_file_dict.items():
                writer.writerow([values["machine_upper"], values["human_upper"]])

        with open(f'../output/paired_features_{corpus}/connectives_total.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['gpt', 'human'])
            for key, values in combined_file_dict.items():
                writer.writerow([values["machine_total"], values["human_total"]])

main()
