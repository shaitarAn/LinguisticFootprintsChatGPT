import json
import os
import sys
from collections import defaultdict
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from viz_helper import *
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict

# features = ['MTLD', 'mean_word_length', 'token_length_mean', 'Yules', 'proportion_unique_tokens', ]

features = ['alpha_ratio', 'pos_prop_PUNCT', 'dependency_distance_std', 'proportion_unique_tokens', 'sentence_length_mean']

lexical_density = ["pos_prop_NOUN", "pos_prop_VERB", "pos_prop_ADJ", "pos_prop_ADV", "pos_prop_PRON"]

readability = ["flesch_reading_ease", "flesch_kincaid_grade", "coleman_liau_index", "automated_readability_index", "lix"]

syntax = ["dependency_distance_mean", "dependency_distance_std", "prop_adjacent_dependency_relation_mean", "prop_adjacent_dependency_relation_std", "first_order_coherence"]

descriptives = ["mean_word_length", "token_length_mean", "proportion_unique_tokens", "sentence_length_mean", "sentence_length_std"]

pos = ["pos_prop_ADP", "pos_prop_CCONJ", "pos_prop_DET", "pos_prop_PUNCT", "alpha_ratio"]

conjunctions = ["pos_prop_CCONJ", "pos_prop_SCONJ", "sentence_length_mean", "sentence_length_std", "first_order_coherence"]

connectives = ["pos_prop_CCONJ", "pos_prop_SCONJ", "first_order_coherence", "connectives", "connectives_cap"]

for_prezi = ["mean_word_length", "pos_prop_PUNCT", "sentence_length_mean", "mtld", "proportion_unique_tokens"]

features = lexical_density

# domain = 'news'
language = 'german'
generation = '2403gpt4'

# Set up a PDF file to save the plots
pdf_path = f"../../viz/domains_{generation}_{language}_lexical_density.pdf"
pdf_pages = PdfPages(pdf_path)

# Create a figure
fig = plt.figure(figsize=(22, 16))
# Add a title
# fig.suptitle('Comparison of English and German features', fontsize=16)

# Add a grid
gs = gridspec.GridSpec(3, 5, width_ratios=[1, 1, 1, 1, 1], height_ratios=[1, 1, 1])

# Add the news features
for i, feature in enumerate(features):
    # import the data into a dataframe
    df = pd.read_csv(f'../../feature_extraction/{generation}/results/per_domain/news/{language}/{feature}.csv')
    ax = fig.add_subplot(gs[0, i])
    sns.boxplot(data=df, palette='Set3', showmeans=True, ax=ax)
    ax.set_title(' '.join(features_to_visualize_dict[feature].split(" ")[1:]), fontsize=20)
    ax.tick_params(axis='y', labelsize=14)  # Use tick_params to adjust y-axis labels
    ax.set_ylabel('')
    ax.set_xlabel('')

# Add the science features
for i, feature in enumerate(features):
    # import the data into a dataframe
    df = pd.read_csv(f'../../feature_extraction/{generation}/results/per_domain/science/{language}/{feature}.csv')
    ax = fig.add_subplot(gs[1, i])
    sns.boxplot(data=df, palette='Set3', showmeans=True, ax=ax)
    ax.set_title(' '.join(features_to_visualize_dict[feature].split(" ")[1:]), fontsize=20)
    # ax.tick_params(axis='x', labelsize=16)  # Control x-tick label font and rotation
    ax.tick_params(axis='y', labelsize=14)  # Adjust y-tick font size
    ax.set_xlabel('')  # Set to an empty string if you don't want a label for x-axis
    ax.set_ylabel('')

# Add the clinical features
for i, feature in enumerate(features):
    # import the data into a dataframe
    df = pd.read_csv(f'../../feature_extraction/{generation}/results/per_domain/clinical/{language}/{feature}.csv')
    ax = fig.add_subplot(gs[2, i])
    sns.boxplot(data=df, palette='Set3', showmeans=True, ax=ax)
    ax.set_title(' '.join(features_to_visualize_dict[feature].split(" ")[1:]), fontsize=20)
    # ax.tick_params(axis='x', labelsize=16)  # Control x-tick label font and rotation
    ax.tick_params(axis='y', labelsize=14)  # Adjust y-tick font size
    ax.set_xlabel('')  # Set to an empty string if you don't want a label for x-axis
    ax.set_ylabel('')


# Adjust layout to reduce margins
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)

# Save the figure to the pdf
pdf_pages.savefig(fig)

# Close the pdf
pdf_pages.close()

# ########################################################################################
# for feature in features_to_visualize_dict:
#     # import the data into a dataframe
#     df = pd.read_csv(f'../../feature_extraction/{generation}/results/per_domain/{domain}/{language}/{feature}.csv')

#     # output directory
#     outputdir = '../../viz/per_domain/news'

#     # make a boxplot with the p-values of the dunns test
#     plt.figure(figsize=(12, 6))
#     sns.boxplot(data=df, palette='Set3', showmeans=True)
#     plt.title(f'{feature}', fontsize=20)
#     plt.ylabel('')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()
#     # plt.savefig(f'{outputdir}/{feature}.png')
#     plt.close()
