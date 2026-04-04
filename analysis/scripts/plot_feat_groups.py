
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfPages
from viz_helper import *
import sys
sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict

generation = "2409gpt4"

corpus_mapping = {
    'cnn': 'CNN',
    '20min': '20 Minuten',
    'pubmed_en': 'PubMed (EN)',
    'pubmed_de': 'PubMed (DE)'
}

feature_groups = {
    "readability": ['flesch_reading_ease', 'coleman_liau_index', 'lix', 'rix', 'smog', 'gunning_fog', 'automated_readability_index'],
    
    "dep_distance": ['dependency_distance_mean', 'dependency_distance_std'],
    
    # "quality": ["n_stop_words", 'alpha_ratio', 'doc_length', 'symbol_to_word_ratio_#', 'proportion_ellipsis', 'duplicate_line_chr_fraction', 'duplicate_paragraph_chr_fraction','duplicate_ngram_chr_fraction_5', 'duplicate_ngram_chr_fraction_6', 'duplicate_ngram_chr_fraction_7', 'duplicate_ngram_chr_fraction_8', 'duplicate_ngram_chr_fraction_9', 'duplicate_ngram_chr_fraction_10', 'top_ngram_chr_fraction_2','top_ngram_chr_fraction_3', 'top_ngram_chr_fraction_4', 'oov_ratio'],
    
    "descriptive_stats": ['token_length_mean', 'token_length_std', 'sentence_length_mean', 'sentence_length_std', 'proportion_unique_tokens', 'mean_word_length', 'alpha_ratio'],
    
    "information_theory": ["entropy"],

    "pos_distributions": ["pos_prop_ADJ", "pos_prop_ADP", "pos_prop_ADV", "pos_prop_CCONJ", "pos_prop_DET", "pos_prop_NOUN", "pos_prop_PUNCT", "pos_prop_SCONJ", "pos_prop_VERB"],

    "coherence":  ["first_order_coherence", "second_order_coherence"],

    "morphology": ["shannon_entropy"],
}

# Define the root path for feature extraction results
root_path = f"../../feature_extraction/{generation}/results/per_feature"

# Loop through each feature group
for group_name, group_features in feature_groups.items():

    # Create output directory if it doesn't exist
    output_dir = f"../../viz/boxplots/feat_groups/{generation}_{group_name}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through each feature in the group
    for feature_name in group_features:

        feature_dir = os.path.join(root_path, feature_name)
        if not os.path.exists(feature_dir):
            print(f"Skipping {feature_name} as directory does not exist.")
            continue

        # Loop through each corpus file in the feature directory
        for corpus_file in os.listdir(feature_dir):
            file_path = os.path.join(feature_dir, corpus_file)

            # Load the data from CSV file
            df = pd.read_csv(file_path)

            # Extract the corpus name from the file
            corpus = corpus_file.split('.')[0]

            # Plot the boxplot for the feature and save the figure
            plt.figure(figsize=(5, 6))
            sns.boxplot(data=df, palette='Set3')

            # Get the feature description from the dictionary
            feature_desc = features_to_visualize_dict.get(feature_name, feature_name)

            # Set title and labels
            plt.title(f"{corpus_mapping[corpus]}", fontsize=22)
            plt.yticks(fontsize=18)
            plt.xticks(rotation=45, fontsize=22)
            plt.tight_layout()

            # Save the figure
            outputfile = os.path.join(output_dir, f"{corpus}_{feature_name}.png")
            plt.savefig(outputfile, bbox_inches='tight')
            plt.close()

            print(f"Saved plot for {corpus} - {feature_name}")





