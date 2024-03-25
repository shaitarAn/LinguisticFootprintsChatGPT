import pandas as pd
# from scipy.stats import tukey_hsd
import itertools
import numpy as np
import os, sys
import scikit_posthocs as sp
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from viz_helper import collect_special_pngs
from PIL import Image
sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict

# ##############################################################################
# # make boxplots for the selected features in Figure 2
# ##############################################################################

feature_top = ["proportion_unique_tokens", "proportion_unique_tokens"]
feature_bottom = ["proportion_unique_tokens", "proportion_unique_tokens"]

def make_boxplot(feature, folder, df, lang, title):

    if not os.path.exists(f"../../viz/boxplots/{folder}"):
        os.makedirs(f"../../viz/boxplots/{folder}")

    # make a boxplot with the p-values of the dunns test
    plt.figure(figsize=(4, 6))
    sns.boxplot(data=df, palette='Set3', showmeans=True)

    plt.xticks(rotation=45)
    plt.title(title, fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=15)
    # plt.savefig(f"../visualizations/boxplots/{lang}/{feature}.pdf", bbox_inches='tight')
    plt.savefig(f"../../viz/boxplots/{folder}/{lang}_{feature}.png", bbox_inches='tight')
    # plt.show()
    plt.close()

def combine_pngs(pngs, output_path):

    list_of_images = []
    
    for png in pngs:

        try:

            im = Image.open(png)
            list_of_images.append(im)

            w = max(im.width for im in list_of_images)
            h = max(im.height for im in list_of_images)

        except FileNotFoundError:
            continue

        # create big empty image with a white background with 2 images per row
        new_image = Image.new('RGB', (w * 2, h * 2), color='white')

        # paste the images into the big image left to right, top to bottom
        for i, im in enumerate(list_of_images):
            new_image.paste(im, (i % 2 * w, i // 2 * h))
        
        # save big image
        new_image.save(output_path)

# for feature in feature_top:

#     try:
#         make_boxplot(feature, "special", pd.read_csv(f"../../feature_extraction/results/per_language/english/{feature}.csv"), "English", " ".join(features_to_visualize_dict[feature].split(" ")[1:]))
#     except FileNotFoundError:
#         print(f"FileNotFoundError: {feature}")

# for feature in feature_bottom:
#     try:
#         make_boxplot(feature, "special", pd.read_csv(f"../../feature_extraction/results/per_language/english/{feature}.csv"), "German", " ".join(features_to_visualize_dict[feature].split(" ")[1:]))
#     except FileNotFoundError:
#         print(f"FileNotFoundError: {feature}")

# pngs = [f'../../viz/boxplots/special/English_{feature_top[0]}.png', f'../../viz/boxplots/special/English_{feature_top[1]}.png', f'../../viz/boxplots/special/German_{feature_bottom[0]}.png',  f'../../viz/boxplots/special/German_{feature_bottom[1]}.png']
        
# combine_pngs(pngs, "../../viz/boxplots/special/combined.png")

# # #####################################################################################
feature = "proportion_unique_tokens"
corpora = ["cnn", "20min", "cs_en", "cs_de"]

corpus_dict = {
    "cnn": "CNN",
    "20min": "20 Minuten",
    "cs_en": "CSB English",
    "cs_de": "CSB German"
}

# for corpus in corpora:
#     df = pd.read_csv(f"../../feature_extraction/results/per_feature/{feature}/{corpus}.csv")
#     make_boxplot(feature, "special", df, corpus, corpus_dict[corpus])

df1 = pd.read_csv(f"../../feature_extraction/results/per_language/english/{feature}.csv")
df2 = pd.read_csv(f"../../feature_extraction/results/per_language/german/{feature}.csv")

df = pd.concat([df1, df2])

make_boxplot("uniq", "special", df, "full", "full data" )

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# List of PNG paths
pngs = ['../../viz/boxplots/special/full_uniq.png'] + [f'../../viz/boxplots/special/{corpus}_{feature}.png' for corpus in corpora]

# Create a new PDF file
with PdfPages('combined_plots.pdf') as pdf:
    # Create a figure with a horizontal layout
    fig, axs = plt.subplots(1, len(pngs), figsize=(15, 5))

    # Loop through each PNG and add it to the corresponding axis
    for i, png in enumerate(pngs):
        # Read the PNG file and display it on the corresponding axis
        img = plt.imread(png)
        axs[i].imshow(img)
        axs[i].axis('off')

    # Adjust layout
    plt.tight_layout()

    # Save the figure as a page in the PDF file
    pdf.savefig()

    # Close the figure
    plt.close(fig)

# Print message
print("PDF file saved successfully with combined plots.")



