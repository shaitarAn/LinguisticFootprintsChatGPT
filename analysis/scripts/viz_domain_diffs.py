import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import os

generation = "2403gpt4"

# Create a figure with 2 rows and 3 columns
fig = plt.figure(figsize=(18, 9))

# Add a grid specification
gs = fig.add_gridspec(2, 3, width_ratios=[1, 1, 1])

# Define the domains and features
domains = ['news', 'science', 'clinical']
english_feature = 'pos_prop_PRON'
german_feature = 'pos_prop_PRON'
english_language = 'english'
german_language = 'german'

# Top row: English for feature 'dependency_distance_mean'
for i, domain in enumerate(domains):
    # Import the English data for the domain
    df = pd.read_csv(f'../../feature_extraction/{generation}/results/per_domain/{domain}/{english_language}/{english_feature}.csv')
    ax = fig.add_subplot(gs[0, i])
    sns.boxplot(data=df, palette='Set3', showmeans=True, ax=ax)
    ax.set_title(f'{domain.capitalize()}', fontsize=25, fontweight='bold')  
    ax.tick_params(axis='y', labelsize=16)
    # ax.set_xlabel('')
    # remove furthest outliers for better visualization
    ax.set_ylim(0, 0.06)
    # add line at 3
    ax.axhline(y=0.03, color='lime', linestyle='-', linewidth=3)
    
    # remove the x-axis labels
    ax.set_xticklabels([])
    # remove the x-axis ticks
    ax.set_xticks([])
    ax.set_yticks(ax.get_yticks()[1:])

    
    # Add y-label for the first subplot only (English feature name)
    if i == 0:
        ax.set_ylabel('ENGLISH', fontsize=20)

# Bottom row: German for feature 'sentence_length_mean'
for i, domain in enumerate(domains):
    # Import the German data for the domain
    df = pd.read_csv(f'../../feature_extraction/{generation}/results/per_domain/{domain}/{german_language}/{german_feature}.csv')
    ax = fig.add_subplot(gs[1, i])
    sns.boxplot(data=df, palette='Set3', showmeans=True, ax=ax)
    ax.set_title('')  # Only the domain as the title
    ax.tick_params(axis='y', labelsize=16)
    ax.tick_params(axis='x', labelsize=20, rotation=45)  

    # remove furthest outliers for better visualization
    ax.set_ylim(0.0, 0.06)
    # add line at 16
    ax.axhline(y=0.03, color='lime', linestyle='-', linewidth=3)
    # do not show the lowest y-tick
  

    
    # Add y-label for the first subplot only (German feature name)
    if i == 0:
        ax.set_ylabel('GERMAN', fontsize=20)
        # set the y-axis label position further to the left
        # ax.yaxis.set_label_coords(-0.1, 0.5)

# Adjust the layout to reduce margins
plt.subplots_adjust(left=0.25, right=0.95, top=0.8, bottom=0.05)

# tight_layout() 
plt.tight_layout()

# save a png version of the figure
output_png_path = "../../viz/for_paper/comparison_en-de.png"

plt.savefig(output_png_path, bbox_inches='tight')

# Save the figure to a PDF
output_pdf_path = "../../viz/for_paper/comparison_en-de.pdf"
with PdfPages(output_pdf_path) as pdf:
    pdf.savefig(fig)
    plt.close()

print(f"PDF saved at: {output_pdf_path}")
