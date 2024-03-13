import os
import pandas as pd
import numpy as np

# iterate over dirs and combine files into a single dataframe with two columns: text and persona label

corpora = ['20min', 'cnn', 'pubmed_en', 'pubmed_de', 'zora_en', 'zora_de', 'cs_en', 'cs_de', 'e3c', 'ggponc']

for corpus in corpora:

    input_dir = f'../../data/{corpus}/'

    # initialize the dataframe
    df = pd.DataFrame(columns=['text', 'persona'])

    for subdir in os.listdir(input_dir):
        if os.path.isdir(input_dir + subdir):
            print(subdir)
            files = os.listdir(input_dir + subdir)
            for f in files:
                with open(input_dir + subdir + '/' + f, 'r') as file:
                    text = file.read()
                    text = text.replace('\n', ' ')
                    df = pd.concat([df, pd.DataFrame({'text': [text], 'persona': [subdir]})], ignore_index=True)

    # create the output directory if it does not exist
    if not os.path.exists('../shapdata'):
        os.makedirs('../shapdata')
    # save the dataframe to a csv file
    df.to_csv(f'../shapdata/{corpus}.csv', index=False)
