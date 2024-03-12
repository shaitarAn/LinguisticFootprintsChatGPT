import pandas as pd
# from scipy.stats import tukey_hsd
import itertools
import numpy as np
import os
import scikit_posthocs as sp
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from viz_helper import collect_special_pngs
from PIL import Image

# ##############################################################################
# # make boxplots for the selected features in Figure 2
# ##############################################################################

feature_top = ["lix"]
feature_bottom = ["sentence_length_mean"]

def make_boxplot(feature, folder, df, lang):

    if not os.path.exists(f"../../viz/boxplots/{folder}"):
        os.makedirs(f"../../viz/boxplots/{folder}")

    # make a boxplot with the p-values of the dunns test
    plt.figure(figsize=(4, 6))
    sns.boxplot(data=df, palette='Set3', showmeans=True)
    if feature == "lix":
        plt.title(f"{lang}", fontsize=20)

    plt.xticks(rotation=45)
    # increase the font size of the x
    # remove the xticks
    # plt.xticks([])
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=15)
    # plt.savefig(f"../visualizations/boxplots/{lang}/{feature}.pdf", bbox_inches='tight')
    plt.savefig(f"../../viz/boxplots/{folder}/{lang}_{feature}.png", bbox_inches='tight')
    plt.show()
    plt.close()

for feature in feature_top:
    try:
        make_boxplot(feature, "special", pd.read_csv(f"../../feature_extraction/results/per_language/english/{feature}.csv"), "English")
        make_boxplot(feature, "special", pd.read_csv(f"../../feature_extraction/results/per_language/german/{feature}.csv"), "German")
    except FileNotFoundError:
        print(f"FileNotFoundError: {feature}")

for feature in feature_bottom:
    try:
        make_boxplot(feature, "special", pd.read_csv(f"../../feature_extraction/results/per_language/english/{feature}.csv"), "English")
        make_boxplot(feature, "special", pd.read_csv(f"../../feature_extraction/results/per_language/german/{feature}.csv"), "German")
    except FileNotFoundError:
        print(f"FileNotFoundError: {feature}")

# #####################################################################################
# # collect pngs from a directory and put them into one pdf file
# #####################################################################################

pngs = ['../../viz/boxplots/special/English_lix.png', '../../viz/boxplots/special/German_lix.png', '../../viz/boxplots/special/English_sentence_length_mean.png', '../../viz/boxplots/special/German_sentence_length_mean.png']

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
    new_image.save(f"../../viz/for_paper/Figure2_lix+sentLenMean_De+En.pdf")


