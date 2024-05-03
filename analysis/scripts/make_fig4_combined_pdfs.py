import pandas as pd
import os, sys
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict
from viz_helper import corpus_dict

def make_boxplot(feature, outputfolder, df, corpus, filetype="pdf"):

    if not os.path.exists(f"../../viz/boxplots/{outputfolder}"):
        os.makedirs(f"../../viz/boxplots/{outputfolder}")

    plt.figure(figsize=(4, 6))
    sns.boxplot(data=df, palette='Set3', showmeans=True)

    plt.xticks(rotation=45)
    plt.title(corpus_dict[corpus], fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=15)
    plt.savefig(f"../../viz/boxplots/{outputfolder}/{corpus}_{feature}.{filetype}", bbox_inches='tight')
    # plt.show()
    plt.close()

def combine_pngs(pngs, output_path):

    list_of_images = []
    
    for png in pngs:
        print(png)

        try:

            im = Image.open(png)
            list_of_images.append(im)

            w = max(im.width for im in list_of_images)
            h = max(im.height for im in list_of_images)

        except FileNotFoundError:
            continue

        # create big empty image with a white background with 2 images per row
        new_image = Image.new('RGB', (w * 3, h * 2), color='white')

        # paste the images into the big image left to right, top to bottom
        for i, im in enumerate(list_of_images):
            new_image.paste(im, (i % 3 * w, i % 2 * h))
        
        # save big image
        new_image.save(output_path)

def make_boxplot_one_row(pngs, output_path):
    
    # Create a new PDF file
    with PdfPages(output_path) as pdf:
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

def main():

    # ##############################################################################
    # # make boxplots for the selected features in Figure 4
    # ##############################################################################

    feature = "proportion_unique_tokens"
    corpora = ["cnn", "20min", "cs_de", "pubmed_en", "pubmed_de"]

    for corpus in corpora:
        df = pd.read_csv(f"../../feature_extraction/results/per_feature/{feature}/{corpus}.csv")
        make_boxplot(feature, "special", df, corpus, "png")

    df1 = pd.read_csv(f"../../feature_extraction/results/per_language/english/{feature}.csv")
    df2 = pd.read_csv(f"../../feature_extraction/results/per_language/german/{feature}.csv")

    df = pd.concat([df1, df2])

    make_boxplot("uniq", "special", df, "full", "png")

    # List of PNG paths
    pngs = ['../../viz/boxplots/special/full_uniq.png'] + [f'../../viz/boxplots/special/{corpus}_{feature}.png' for corpus in corpora]

    # Combine PNGs into a single PDF
    combine_pngs(pngs, "../../viz/boxplots/special/unique_tokens_3x2.pdf")

    make_boxplot_one_row(pngs, "../../viz/boxplots/special/unique_tokens.pdf")

    # ##############################################################################
    # # make boxplots with the top and bottom features
    # ##############################################################################

    # feature_top = ["proportion_unique_tokens", "proportion_unique_tokens"]
    # feature_bottom = ["proportion_unique_tokens", "proportion_unique_tokens"]

    # for feature in feature_top:

    #     try:
    #         make_boxplot(feature, "special", pd.read_csv(f"../../feature_extraction/results/per_language/english/{feature}.csv"), "English")
    #     except FileNotFoundError:
    #         print(f"FileNotFoundError: {feature}")

    # for feature in feature_bottom:
    #     try:
    #         make_boxplot(feature, "special", pd.read_csv(f"../../feature_extraction/results/per_language/english/{feature}.csv"), "German")
    #     except FileNotFoundError:
    #         print(f"FileNotFoundError: {feature}")

    # # pngs = [f'../../viz/boxplots/special/English_{feature_top[0]}.png', f'../../viz/boxplots/special/English_{feature_top[1]}.png', f'../../viz/boxplots/special/German_{feature_bottom[0]}.png',  f'../../viz/boxplots/special/German_{feature_bottom[1]}.png']
            
    # combine_pngs(pngs, "../../viz/boxplots/special/unique_tokens.pdf")

main()



