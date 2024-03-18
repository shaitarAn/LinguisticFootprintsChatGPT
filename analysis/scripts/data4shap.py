import os
import pandas as pd
import numpy as np

# iterate over dirs and combine files into a single dataframe with two columns: text and persona label

corpora = ['20min', 'cnn', 'pubmed_en', 'pubmed_de', 'zora_en', 'zora_de', 'cs_en', 'cs_de', 'e3c', 'ggponc']

for corpus in corpora:

    input_dir = f'../../data/{corpus}/'

    # initialize the dataframe
    df = pd.DataFrame(columns=['text', 'persona'])

    for subdir in os.listdir(input_dir):
        if os.path.isdir(input_dir + subdir):
            # print(subdir)
            files = os.listdir(input_dir + subdir)
            for f in files:
                with open(input_dir + subdir + '/' + f, 'r') as file:
                    text = file.read()
                    text = text.replace('\n', ' ')
                    df = pd.concat([df, pd.DataFrame({'text': [text], 'persona': [subdir]})], ignore_index=True)

    # create the output directory if it does not exist
    if not os.path.exists('../shapdata'):
        os.makedirs('../shapdata')
    # save the dataframe to a csv file
    df.to_csv(f'../shapdata/{corpus}.csv', index=False)import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming you have loaded your data into a DataFrame named df

# Pivot the DataFrame to have personas1 and personas2 as columns and f1-score as values
pivot_df = df.pivot_table(index='persona1', columns='persona2', values='f1-score')

# Create a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(pivot_df, annot=True, cmap='viridis', fmt=".2f")
plt.title('F1-Score Comparison Between Personas')
plt.xlabel('Persona 2')
plt.ylabel('Persona 1')
plt.show()


# combine all feature files into a single dataframe
# columns: text, persona, feature1, feature2, ...
# rows contain the text, persona, and the values of the features from each file

# iterate over the corpora
for corpus in corpora:
    # initialize the dataframe
    df = pd.DataFrame()
    input_dir = f'../../feature_extraction/results/per_corpus/{corpus}/'
    files = os.listdir(input_dir)
    for f in files:
        file = f.split('.')[0]
        # read the file
        df_file = pd.read_csv(input_dir + f)
        # rename the first column to 'persona'
        df_file = df_file.rename(columns={df_file.columns[0]: 'persona'})
        # reset the index of the dataframe
        df_file = df_file.reset_index(drop=True)
        # make persona column the index
        df_file = df_file.set_index('persona')
        
        # # transpose the dataframe and drop the first row
        df_file = df_file.T
        # # add the file name as a column
        df_file['file'] = file
        # rename the index to 'persona'
        df_file.index.name = 'persona'
        # reset the index of the dataframe
        df_file = df_file.reset_index()

        # append the dataframe to the main dataframe    
        df = pd.concat([df, df_file], ignore_index=True)



    print(df.head())

    # create the output directory if it does not exist
    if not os.path.exists('../shapdata/features'):
        os.makedirs('../shapdata/features')

    # save the dataframe to a csv file
    df.to_csv(f'../shapdata/features/{corpus}.csv', index=False)

        