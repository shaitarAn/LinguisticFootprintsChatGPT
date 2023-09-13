# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import spacy
import os
import textdescriptives as td

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('textdescriptives/all')

Dnlp = spacy.load('de_core_news_lg')
Dnlp.add_pipe('textdescriptives/all')

directory_path = "../data/"

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
        
    return td.extract_dict(doc)


def process_text_files_in_directory(directory_path, output_csv_path, lang):
    data = []
    file_counter = 1
    
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(directory_path, file_name)
            feature_values_list = process_file(file_path, lang)
            
            for feature_values in feature_values_list:
                feature_values["file_id"] = file_counter
                data.append(feature_values)
            file_counter += 1
    
    # Create a pandas DataFrame and write it to a CSV file
    df = pd.DataFrame(data)
    #  drop columns that have NaN
    df.dropna(axis=1, inplace=True)
    # drop columns that have only 0
    df = df.loc[:, (df != 0).any(axis=0)]
    
    df.to_csv(output_csv_path, index=False)


    # itarate over subdirectories in directory_path
for subdirectory in os.listdir(directory_path):
    # itarate over files in subdirectory
    corpus = subdirectory
    if corpus in ['20min', 'GGPONC', "pubmed_de", "zora_de"]:
        lang = 'de'
    else:
        lang = 'en'
    print(lang)
    if not os.path.isdir(os.path.join(directory_path, subdirectory)):
            continue
    for system in os.listdir(os.path.join(directory_path, subdirectory)):
        # check if system is a directory
        print(corpus, system)
        output_csv_path = "../output/" + corpus + "_" + system + ".csv"
        input_path = os.path.join(directory_path, subdirectory, system)
        process_text_files_in_directory(input_path, output_csv_path, lang)