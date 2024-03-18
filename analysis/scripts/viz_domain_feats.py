import json
import os
import sys
from collections import defaultdict
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from viz_helper import *
sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict

# features = ['MTLD', 'mean_word_length', 'token_length_mean', 'Yules', 'proportion_unique_tokens', ]

features = ['alpha_ratio', 'pos_prop_PUNCT', 'dependency_distance_std', 'proportion_unique_tokens', 'duplicate_ngram_chr_fraction_5']

domain = 'news'
language = 'german'

for feature in features:
    # import the data into a dataframe
    df = pd.read_csv(f'../../feature_extraction/results/per_domain/{domain}/{language}/{feature}.csv')

    # output directory
    outputdir = '../../viz/per_domain/news'

    # make a boxplot with the p-values of the dunns test
    plot_means(outputdir, df, " ".join(features_to_visualize_dict[feature].split()[1:]), 0.01)




