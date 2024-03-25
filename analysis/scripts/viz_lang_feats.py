import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns
from matplotlib import gridspec
from matplotlib.backends.backend_pdf import PdfPages
sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict

# English features
english_features = ['mean_word_length', 'mtld', 'token_length_mean', 'coleman_liau_index', 'prop_adjacent_dependency_relation_mean']

# German features
german_features = ['alpha_ratio', 'pos_prop_PUNCT', 'proportion_unique_tokens', 'sentence_length_std', 'dependency_distance_std']

# Set up a PDF file to save the plots
pdf_path = "../../viz/combined_lang_features.pdf"
pdf_pages = PdfPages(pdf_path)

# Create one pdf page for all the features
# Pdf has 2 rows and 4 columns
# top row is for English features

# Create a figure
fig = plt.figure(figsize=(22, 12))
# Add a title
# fig.suptitle('Comparison of English and German features', fontsize=16)

# Add a grid
gs = gridspec.GridSpec(2, 5, width_ratios=[1, 1, 1, 1, 1], height_ratios=[1, 1])

# Add the English features
for i, feature in enumerate(english_features):
    # import the data into a dataframe
    df = pd.read_csv(f'../../feature_extraction/results/per_language/english/{feature}.csv')
    ax = fig.add_subplot(gs[0, i])
    sns.boxplot(data=df, palette='Set3', showmeans=True, ax=ax)
    ax.set_title(' '.join(features_to_visualize_dict[feature].split(" ")[1:]), fontsize=20)
    ax.set_ylabel('', fontsize=14)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=14)


# Add the German features
for i, feature in enumerate(german_features):
    # import the data into a dataframe
    df = pd.read_csv(f'../../feature_extraction/results/per_language/german/{feature}.csv')
    ax = fig.add_subplot(gs[1, i])
    sns.boxplot(data=df, palette='Set3', showmeans=True, ax=ax)
    ax.set_title(' '.join(features_to_visualize_dict[feature].split(" ")[1:]), fontsize=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=16)
    ax.set_xlabel('', fontsize=14)
    ax.set_ylabel('', fontsize=14)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=14)

# Adjust layout to reduce margins
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)

# Save the figure to the pdf
pdf_pages.savefig(fig)

# Close the pdf
pdf_pages.close()










