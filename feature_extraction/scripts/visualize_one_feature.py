import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

type = "total"
feature = "connectives_" + type

for corpus in ['20min', 'GGPONC', "pubmed_de", "zora_de", "pubmed_en", "zora_en", "e3c", "cnn"]:

    file_path = f"../output/{feature}_{corpus}.csv"
    images_directory = f"../results/feature_visualizations_{corpus}"

    df = pd.read_csv(file_path)

    plt.figure(figsize=(10, 5))
    plt.plot(df[f'machine_{type}'], label="gpt")
    plt.plot(df[f'human_{type}'], label="human")
    plt.title(feature)
    plt.xlabel("Document")
    plt.ylabel("count")
    plt.legend()

    # Save the figure as a PNG file
    image_file_name = f"{feature}_{corpus}.png"
    image_file_path = os.path.join(images_directory, image_file_name)
    plt.savefig(image_file_path)

    # Add the figure to the PDF file
    plt.close()
