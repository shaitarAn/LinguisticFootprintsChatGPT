import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns
from viz_helper import *

corpus = "20min"
corpus_name = "20 Minuten"
generation = "2403gpt4" # "2403gpt4" # "2309gpt3" # 2407gpt4o

feature_dict = {"sentence_length_mean": "Average Sentence Length",
                "sentence_length_std": "Standard Deviation of Sentence Length"}

features = ["sentence_length_mean", "sentence_length_std"]
            # "dependency_distance_mean", "prop_adjacent_dependency_relation_mean", "first_order_coherence", "second_order_coherence"]

for f in features:

    feature_other_lang = f"../../feature_extraction/{generation}/results/per_feature/{f}/{corpus}.csv"

    # dfe = pd.read_csv(feature)
    df = pd.read_csv(feature_other_lang)

    # Step 2: male a boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, showfliers=False)
    # plt.title(f'{feature_dict[f]} in {corpus_name}', fontsize=20)
    plt.title('')
    plt.ylabel('')
    # make x labels larger
    plt.xticks(fontsize=20)
    # tight layout
    plt.tight_layout()
    # save the plot
    plt.savefig(f'../../viz/{corpus}_{f}_{generation}.png')
    # show the plot
    plt.show()
    plt.close()


    

