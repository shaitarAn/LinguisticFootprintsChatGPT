import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
from fpdf import FPDF
import sys
sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict
from viz_helper import corpus_dict

def make_boxplot(feature, outputfolder, df, corpus, generation, show_labels=True, show_title=True, filetype="png"):
    outputfile = f"../../viz/boxplots/{outputfolder}/{generation}_{corpus}_{feature}.{filetype}"

    if not os.path.exists(f"../../viz/boxplots/{outputfolder}"):
        os.makedirs(f"../../viz/boxplots/{outputfolder}")

    plt.figure(figsize=(5, 6))
    sns.boxplot(data=df, palette='Set3', showmeans=True)

    if show_title:
        plt.title(corpus_dict[corpus], fontsize=22)
    plt.yticks(fontsize=18)

    if not show_labels:
        plt.xticks([])
    else:
        plt.xticks(rotation=45, fontsize=22)
    
    plt.tight_layout()
    plt.savefig(outputfile, bbox_inches='tight')
    plt.close()

    return outputfile

def combine_pngs_into_pdf(pngs, output_path, nrows=2, ncols=5):
    with PdfPages(output_path) as pdf:

        fig, axs = plt.subplots(nrows, ncols, figsize=(23,11))
        # ncols * 4, nrows * 6
        axs = axs.flatten()

        for i, png in enumerate(pngs):
            img = plt.imread(png)
            axs[i].imshow(img)
            axs[i].axis('off')  # Turn off axis lines and labels

        plt.tight_layout()
        pdf.savefig(fig)
        # show the combined plots
        plt.show()
        plt.close(fig)

    print("PDF file saved successfully with combined plots.")

def main(root, generations):
    feature = "proportion_unique_tokens"
    corpora = ["cnn", "20min", "cs_en", "cs_de"]
    pngs = []

    for generation in generations:
        show_labels = generation != "2309gpt3"  # Only show x-axis labels for generations other than 2309gpt3
        show_title = generation != "2403gpt4"  # Only show titles for generations other than 2403gpt4
        df1 = pd.read_csv(f"{root}/{generation}/results/per_language/english/{feature}.csv")
        df2 = pd.read_csv(f"{root}/{generation}/results/per_language/german/{feature}.csv")
        df = pd.concat([df1, df2])

        pngs.append(make_boxplot(feature, "special", df, "full", generation, show_labels, show_title))

        for corpus in corpora:
            df = pd.read_csv(f"{root}/{generation}/results/per_feature/{feature}/{corpus}.csv")
            pngs.append(make_boxplot(feature, "special", df, corpus, generation, show_labels, show_title))

    combine_pngs_into_pdf(pngs, f"../../viz/boxplots/special/{'_'.join(generations)}_{feature}.pdf")

if __name__ == "__main__":
    generations = ["2309gpt3", "2403gpt4"]
    root = "../../feature_extraction"
    main(root, generations)
