import pandas as pd
import os

corpus = "de"

def load_csv_files(file_path1, file_path2):
    df1 = pd.read_csv(file_path1)
    df2 = pd.read_csv(file_path2)
    return df1, df2

def pair_up_values_and_write(df1, df2, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    for column_name in df1.columns:
        if column_name not in ["file_id", "text"]:

            paired_values = []
            for i in range(len(df1)):
                try:
                    paired_values.append((df1.at[i, column_name], df2.at[i, column_name]))
                except KeyError:
                    print(f"Could not find {column_name} in row {i} of {file_path2}")
                    continue
            
            output_df = pd.DataFrame(paired_values, columns=['gpt', 'human'])
            output_file_path = os.path.join(output_directory, f"{column_name}.csv")
            output_df.to_csv(output_file_path, index=False)

for corpus in ["20min", "cnn", "e3c", "GGPONC", "pubmed_de", "pubmed_en", "zora_de", "zora_en"]:

    file_path1 = f"../output/{corpus}_machine.csv"
    file_path2 = f"../output/{corpus}_human.csv" 
    output_directory = f"../output/paired_features_{corpus}"

    df1, df2 = load_csv_files(file_path1, file_path2)
    pair_up_values_and_write(df1, df2, output_directory)
