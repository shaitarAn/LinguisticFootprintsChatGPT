import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns
from viz_helper import *

features_read = [
    "flesch_reading_ease",
    "flesch_kincaid_grade",
    "gunning_fog",
    "automated_readability_index",
    "coleman_liau_index",
    "lix",
    "rix"
]

features_morph = [
    "shannon_entropy",
    "simpson_diversity",
    "connectives",
    "connectives_cap"
]

features_led = [
    "mean_word_length",
    "mtld",
    "alpha_ratio",
    "pos_prop_PUNCT",
]

features = ["connectives", "connectives_cap"]
            # "dependency_distance_mean", "prop_adjacent_dependency_relation_mean", "first_order_coherence", "second_order_coherence"]

for f in features:

    feature = f"../../feature_extraction/results/per_language/english/{f}.csv"
    feature_other_lang = f"../../feature_extraction/results/per_language/german/{f}.csv"

    dfe = pd.read_csv(feature)
    dfg = pd.read_csv(feature_other_lang)

    # combine the dataframes
    df = pd.concat([dfe, dfg])

    print("feature", "corpus", "mean_human", "std_human", "mean_continue", "std_continue", "mean_explain", "std_explain", "mean_create", "std_create")

    for corpus in ["pubmed_en", "pubmed_de", "zora_en", "zora_de", "cnn", "20min", "cs_en", "cs_de", "e3c", "ggponc"]:
        feature = f"../../feature_extraction/results/per_feature/{f}/{corpus}.csv"
        dfc = pd.read_csv(feature)
        dfc = dfc.dropna()
        # print measn and std of human, continue, explain, create in a latex table
        
        print(f"\\textbf{{{f}}} & {corpus} & {dfc.mean().values[0]:.2f} & {dfc.std().values[0]:.2f} & {dfc.mean().values[1]:.2f} & {dfc.std().values[1]:.2f} & {dfc.mean().values[2]:.2f} & {dfc.std().values[2]:.2f} & {dfc.mean().values[3]:.2f} & {dfc.std().values[3]:.2f} \\\\")

        # plot the means
        plot_means("../../viz", dfc, " ".join([f, corpus]), 0.05)

    # plot the means

    # plot_means("../../viz/boxplots/special", df, "full_data", 0.05)
    # plot_means("../../viz", dfg, f, 0.05)

