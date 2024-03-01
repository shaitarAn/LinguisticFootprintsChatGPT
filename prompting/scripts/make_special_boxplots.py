import pandas as pd
# from scipy.stats import tukey_hsd
import itertools
import numpy as np
import os
import scikit_posthocs as sp
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from features_list import features_list


def make_boxplot(feature, folder, df, lang):

    if not os.path.exists(f"../visualizations/boxplots/{folder}"):
        os.makedirs(f"../visualizations/boxplots/{folder}")

    # make a boxplot with the p-values of the dunns test
    plt.figure(figsize=(4, 6))
    sns.boxplot(data=df, palette='Set3', showmeans=True)
    plt.title(f"{lang}", fontsize=20)
    plt.xticks(rotation=45)
    # increase the font size of the x
    # remove the xticks
    # plt.xticks([])
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=15)
    # plt.savefig(f"../visualizations/boxplots/{lang}/{feature}.pdf", bbox_inches='tight')
    plt.savefig(f"../visualizations/boxplots/{folder}/{lang}_{feature}.png", bbox_inches='tight')
    plt.show()
    plt.close()


feature_top = ["lix"]
feature_bottom = ["sentence_length_mean"]

for feature in feature_top:
    try:
        make_boxplot(feature, "special", pd.read_csv(f"../results/per_language/english/{feature}.csv"), "English")
        make_boxplot(feature, "special", pd.read_csv(f"../results/per_language/german/{feature}.csv"), "German")
    except FileNotFoundError:
        print(f"FileNotFoundError: {feature}")


