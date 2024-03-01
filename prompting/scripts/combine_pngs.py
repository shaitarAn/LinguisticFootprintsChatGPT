# collect pngs from a directory and put them into one pdf file

import os
import sys
from PIL import Image
import glob
from pathlib import Path

language = "english"

if not os.path.exists(f"../visualizations/boxplots/{language}"):
    os.makedirs(f"../visualizations/boxplots/{language}")

# get the path to the directory where the pdf file will be saved
output_dir = "../visualizations/boxplots/"

# german_features_to_visualize = ["pos_prop_NOUN",  "prop_unique_tokens", "sent_length_std", "dep_distance_std", "shannon_entropy"]

german_features_to_visualize = ["lix", "sentence_length_mean"]

english_features_to_visualize = ["lix", "sentence_length_mean"]

features_to_visualize = german_features_to_visualize

def collect_pngs(language, features_to_visualize):

    pngs = []
    # check if path is a directory
    if os.path.isdir(f"../visualizations/boxplots/{language}"):    
        for png in os.listdir(f"../visualizations/boxplots/{language}"):
            # print(png)
            feature = png.split(".")[0]
            # print(feature)
            if feature in features_to_visualize:
                if png.endswith(".png"):
                    pngs.append(f"../visualizations/boxplots/{language}/{png}")

    return pngs

def collect_special_pngs():
    pngs = []
    # check if path is a directory
    if os.path.isdir(f"../visualizations/boxplots/special"):    
        for png in os.listdir(f"../visualizations/boxplots/special"):
            print(png)
            feature = png.split(".")[0]
            # print(feature)
            if png.endswith(".png"):
                pngs.append(f"../visualizations/boxplots/special/{png}")

    return pngs
                
# pngs_en = collect_pngs(language, english_features_to_visualize)
# pngs_de = collect_pngs("german", german_features_to_visualize)
pngs_special = collect_special_pngs()
print(pngs_special)

# pngs = pngs_en + pngs_de

# organize the pngs in the directory by their name
# organize the names based on this list
# corpora_names = ["pubmed_en", "zora_en", "cnn", "cs_en", "e3c", "pubmed_de", "zora_de",  "20min", "cs_de", "ggponc"]

# pngs = sorted(pngs, key=lambda x: features_to_visualize.index(x.split("/")[-1].split(".")[0]))
pngs = sorted(pngs_special)
print(pngs)


list_of_images = []

for png in pngs:
    # print(type(png))
    # open the png file

    try:

        im = Image.open(png)
        list_of_images.append(im)

        w = max(im.width for im in list_of_images)
        h = max(im.height for im in list_of_images)

    except FileNotFoundError:
        continue

    # create big empty image with a white background with 5 images per row
    new_image = Image.new('RGB', (w * 2, h * 2), color='white')

    # paste the images into the big image
    for i, im in enumerate(list_of_images):
        new_image.paste(im, (w * (i % 2), h * (i // 2)))


    # save big image
    new_image.save(f"{output_dir}/{language}_german_boxplots.pdf")





