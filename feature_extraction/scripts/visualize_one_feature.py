import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

type = "total"
feature = "connectives_" + type
if not os.path.exists("../results/feature_visualizations"):
    os.makedirs("../results/feature_visualizations")

for corpus in ['20min', 'GGPONC', "pubmed_de", "zora_de", "pubmed_en", "zora_en", "e3c", "cnn"]:

    file_path = f"../../prompting/results/per_feature/{feature}/{corpus}.csv"
    images_directory = f"../results/feature_visualizations"

    df = pd.read_csv(file_path)

    sns.lineplot(data=df, palette="tab10", linewidth=1.5)
    plt.title(feature)
    plt.xlabel(corpus)
    # show
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(df[f'human'], label="human")
    plt.plot(df[f'continue'], label="continue")
    plt.plot(df[f'explain'], label="explain")
    plt.plot(df[f'create'], label="create")
    plt.title(feature)
    plt.xlabel(corpus)
    # plt.ylabel()
    plt.legend()

    # Save the figure as a PNG file
    image_file_name = f"{feature}_{corpus}.png"
    image_file_path = os.path.join(images_directory, image_file_name)
    plt.savefig(image_file_path)

    # Add the figure to the PDF file
    plt.close()
