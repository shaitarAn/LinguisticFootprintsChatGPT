# iterate through the directory of csv files and concatenate them into one dataframe

import pandas as pd
import os
import scikit_posthocs as sp
from scipy import stats

feautures = ['flesch', 'smog', 'coleman_liau', 'lix', 'rix']

concatenated_dataframes = []

for f in os.listdir(f'../results_final/combined_results/flesch'):
    print(f)
    f = f'../results_final/combined_results/flesch/{f}'
    df = pd.read_csv(f)
    print(df.shape)
    concatenated_dataframes.append(df)

concatenated_dataframes = pd.concat(concatenated_dataframes)
print(concatenated_dataframes.head())
print(concatenated_dataframes.shape)

concatenated_dataframes.to_csv(f'../results_final/combined_results/flesch/german.csv', index=False)
