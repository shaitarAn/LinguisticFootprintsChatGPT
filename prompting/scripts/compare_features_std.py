import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import defaultdict
import statistics
import numpy as np
import seaborn as sns

for corpus in ["pubmed_en", "pubmed_de", "zora_en", "zora_de", "cnn", "20min", "cs_en", "cs_de", "e3c", "ggponc"]:

    # Define a list of CSV file paths
    file_paths = f"../results/final/{corpus}/"# Add your file paths here

    # collect values for each feature and system from all files in the directory
    # means_dict = {"feature": {"human": [], "continue": [], "explain": [], "create": []}}

    means_dict = defaultdict(lambda: defaultdict(list))

    list_of_files = sorted(os.listdir(file_paths))

    for file_name in list_of_files:
        # print(file_name)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(os.path.join(file_paths, file_name))
        # make sure that the columns are in the following order (human, continue, explain, create)

        # iterate through the values of the first column
        for feature in df.iloc[:, 0]:
            # print(feature)
            # if the feature is not in the dictionary, add it   
            if feature not in means_dict:
                means_dict[feature] = defaultdict(list)
            
            # iterate through the columns
            for system in df.columns[1:]:
                
                # print the value of the cell in the row of the current feature and the current column
                value = df.loc[df.iloc[:, 0] == feature, system].values[0]

                # add the value to the dictionary if it is not NaN and not string
                if not pd.isna(value):
                    try:
                        means_dict[feature][system].append(float(value))
                    except ValueError:
                        pass
                    except TypeError:
                        pass
                    except IndexError:
                        pass

    # create a new dictionary to store the means
    if not os.path.exists(f"../plots_seaborn/{corpus}"):
        os.makedirs(f"../plots_seaborn/{corpus}")


    # Iterate through features
    for feature, systems in means_dict.items():
        # Create a DataFrame for the current feature
        data = {'human': [], 'continue': [], 'explain': [], 'create': []}
        for system, values in systems.items():
            data[system] = values

        try:

            df_plot = pd.DataFrame(data)

            # Create a Seaborn box plot for the current feature
            plt.figure(figsize=(4, 6))
            sns.boxplot(data=df_plot, palette='Set3', showmeans=True)
            plt.title(feature)
            plt.xticks(rotation=45)
            plt.savefig(f"../plots_seaborn/{corpus}/{feature}.png", bbox_inches='tight')
        except ValueError as e:
            # print(f"Skipping {feature}: {e}")
            pass




