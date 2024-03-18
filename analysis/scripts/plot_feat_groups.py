
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfPages
from viz_helper import *

feature_groups = {
    "readability": ['flesch_reading_ease_en', 'flesch_reading_ease_de', 'coleman_liau_index', 'lix', 'rix', 'smog'],
    
    "dep_distance": ['dependency_distance_mean', 'dependency_distance_std'],
    
    "quality": ["n_stop_words", 'alpha_ratio', 'doc_length', 'symbol_to_word_ratio_#', 'proportion_ellipsis', 'duplicate_line_chr_fraction', 'duplicate_paragraph_chr_fraction','duplicate_ngram_chr_fraction_5', 'duplicate_ngram_chr_fraction_6', 'duplicate_ngram_chr_fraction_7', 'duplicate_ngram_chr_fraction_8', 'duplicate_ngram_chr_fraction_9', 'duplicate_ngram_chr_fraction_10', 'top_ngram_chr_fraction_2','top_ngram_chr_fraction_3', 'top_ngram_chr_fraction_4', 'oov_ratio'],
    
    "descriptive_stats": ['token_length_mean', 'token_length_std', 'sentence_length_mean', 'sentence_length_std', 'syllables_per_token_mean', 'syllables_per_token_std', 'proportion_unique_tokens', 'n_characters', 'n_sentences', 'mean_word_length'],
    
    "information_theory": ["entropy", "perplexity", "per_word_perplexity"],

    "pos_distributions": ["pos_prop_ADJ", "pos_prop_ADP", "pos_prop_ADV", "pos_prop_AUX", "pos_prop_CCONJ", "pos_prop_DET", "pos_prop_NOUN", "pos_prop_NUM", "pos_prop_PART", "pos_prop_PRON", "pos_prop_PROPN", "pos_prop_PUNCT", "pos_prop_SCONJ", "pos_prop_VERB"],

    "coherence":  ["first_order_coherence", "second_order_coherence"]
}

for group_name, group_features in feature_groups.items():

    # initialize a dataframe to store the feature, t-statistic, and p-value

    for dir_name in os.listdir(f"../../feature_extraction/results/per_feature"):

        feature_name = dir_name.split('.')[0]

        print(feature_name)

        # Skip features not in the current group
        if feature_name not in group_features:
            continue

        for corpus in os.listdir(f"../../feature_extraction/results/per_feature/{feature_name}"):

            file_path = os.path.join(f"../../feature_extraction/results/per_feature/{feature_name}", corpus)

            corpus = corpus.split('.')[0]

            df = pd.read_csv(file_path)

            print(corpus, df.columns)

            if not os.path.exists(f"../visualizations/boxplots/feat_groups/{group_name}"):
                os.makedirs(f"../visualizations/boxplots/feat_groups/{group_name}")





