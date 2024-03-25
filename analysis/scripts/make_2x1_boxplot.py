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
from PIL import Image, ImageDraw
sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict

# ##############################################################################
# # make boxplots for the selected features in Figure 2
# ##############################################################################

features = ["mean_word_length", "proportion_unique_tokens"]

def make_boxplot(feature, folder, df):

    if not os.path.exists(f"../../viz/boxplots/{folder}"):
        os.makedirs(f"../../viz/boxplots/{folder}")

    # make a boxplot with the p-values of the dunns test
    plt.figure(figsize=(4, 6))
    sns.boxplot(data=df, palette='Set3', showmeans=True)

    plt.xticks(rotation=45)
    plt.title(" ".join(features_to_visualize_dict[feature].split(" ")[1:]), fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=15)
    # plt.savefig(f"../visualizations/boxplots/{lang}/{feature}.pdf", bbox_inches='tight')
    plt.savefig(f"../../viz/boxplots/{folder}/En+De_{feature}.png", bbox_inches='tight')
    plt.show()
    plt.close()

for f in features:
    f1 = f"../../feature_extraction/results/per_language/english/{f}.csv"
    f2 = f"../../feature_extraction/results/per_language/german/{f}.csv"

    df = pd.read_csv(f1)
    df_other_lang = pd.read_csv(f2)

    # combine the dataframes
    df = pd.concat([df, df_other_lang])

    try:
        make_boxplot(f, "special", df)
    except FileNotFoundError:
        print(f"FileNotFoundError: {f}")

# #####################################################################################
# # collect pngs from a directory and put them into one pdf file
# #####################################################################################

pngs = [f'../../viz/boxplots/special/En+De_{features[0]}.png', f'../../viz/boxplots/special/En+De_{features[1]}.png']

list_of_images = []

# pngs = ["../../viz/effect_size/cohen_d_english_language.png", "../../viz/effect_size/cohen_d_german_language.png"]

# create a pdf with two images side by side
for i in range(0, len(pngs), 2):
    # open the images
    img1 = Image.open(pngs[i])
    img2 = Image.open(pngs[i+1])

    # create a new image with twice the width
    new_image = Image.new('RGB', (img1.width + img2.width, img1.height))
    new_image.paste(img1, (0, 0))
    new_image.paste(img2, (img1.width, 0))
    # insert a black line between the images
    draw = ImageDraw.Draw(new_image)
    draw.line((img1.width, 0, img1.width, img1.height), fill=0, width=2)

    # add the new image to the list
    list_of_images.append(new_image)

# create a new pdf
pdf_path = "../../viz/boxplots/special/En+De_boxplots.pdf"
# pdf_path = "../../viz/boxplots/special/En+De_effect_size.pdf"
list_of_images[0].save(pdf_path, save_all=True, append_images=list_of_images[1:])


        


