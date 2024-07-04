import pandas as pd
import os, sys
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict

def combine_pngs(pngs, draw_line=True):
    
    list_of_images = []
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
        if draw_line:
            draw = ImageDraw.Draw(new_image)
            draw.line((img1.width, 0, img1.width, img1.height), fill=0, width=2)

        # add the new image to the list
        list_of_images.append(new_image)

    return list_of_images

def make_boxplot(feature, folder, df):

    if not os.path.exists(f"../../viz/boxplots/{folder}"):
        os.makedirs(f"../../viz/boxplots/{folder}")

    plt.figure(figsize=(4, 6))
    sns.boxplot(data=df, palette='Set3', showmeans=True)

    plt.xticks(rotation=45)
    plt.title(" ".join(features_to_visualize_dict[feature].split(" ")[1:]), fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=15)
    plt.savefig(f"../../viz/boxplots/{folder}/En+De_{feature}.png", bbox_inches='tight')
    # plt.show()
    plt.close()


def make_figure1(features):
    # ##############################################################################
    # # Make Figure 1: boxplots for 2 selected features on front page
    # ##############################################################################

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

    pngs = [f"../../viz/boxplots/special/En+De_{features[0]}.png", f"../../viz/boxplots/special/En+De_{features[1]}.png"]

    list_of_images = combine_pngs(pngs, draw_line=False)

    # create a new pdf
    pdf_path = "../../viz/for_paper/Figure1_En+De_2features.pdf"
    list_of_images[0].save(pdf_path, save_all=True, append_images=list_of_images[1:])
    png_path = "../../viz/for_paper/Figure1_En+De_2features.png"
    list_of_images[0].save(png_path, save_all=True, append_images=list_of_images[1:])

def make_figure2():
    # #####################################################################################
    # # Make Figure 2: combine 2 images of cohen's d effect size into one pdf
    # #####################################################################################

    pngs = ["../../viz/effect_size/cohen_d_english_language.png", "../../viz/effect_size/cohen_d_german_language.png"]

    list_of_images = combine_pngs(pngs, draw_line=True)

    # create a new pdf
    pdf_path = "../../viz/for_paper/Figure2_En+De_effect_size.pdf"
    list_of_images[0].save(pdf_path, save_all=True, append_images=list_of_images[1:])

def main():
    features = ["mean_word_length", "pos_prop_PUNCT"]
    make_figure1(features)
    # make_figure2()

if __name__ == "__main__":
    make_figure1(["mean_word_length", "pos_prop_PUNCT"])
    # make_figure2()


        


