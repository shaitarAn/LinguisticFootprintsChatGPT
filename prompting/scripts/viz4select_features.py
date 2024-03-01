import os
import sys
from PIL import Image
import glob
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import features_list

features_to_visualize = features_list.features_list

# for feature in features_to_visualize:
    # directory = f"../results/per_feature/{feature}"
directory = f"../results/per_language/english"

# if not os.path.exists(f"../visualizations/boxplots/selected/{feature}"):
    # os.makedirs(f"../visualizations/boxplots/selected/{feature}")
output_dir = f"../visualizations/per_lang/english"
for file in os.listdir(directory):
    if file.endswith(".csv"):
        # print(file)
        df = pd.read_csv(os.path.join(directory, file))
        feature = file.split(".")[0]
        print(feature)

        # make a boxplot from the dataframe
        plt.figure(figsize=(4, 6))
        # sns.set_fontsize(1.3)
        # make white background
        sns.set_style("white")
        sns.set_context("paper")
        # make larger font
        
        sns.boxplot(data=df, palette='Set3', showmeans=True)
        plt.title(f"{feature}", fontsize=16)
        plt.xticks(rotation=45, fontsize=16)
        plt.savefig(f"{output_dir}/{feature}.png", bbox_inches='tight')
        # plt.show()
        plt.close()
