import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming you have loaded your data into a DataFrame named df
df = pd.read_csv('../results/loglin_results.csv')

# select only the rows where label==1
df = df[df['label'] == 1]

# Filter the DataFrame for the specified pairs of persona1 and persona2
pairs_of_interest = [('human', 'continue'), ('human', 'explain'), ('human', 'create'),
                     ('continue', 'explain'), ('continue', 'create'), ('explain', 'create')]
filtered_df = df[df[['persona1', 'persona2']].apply(tuple, axis=1).isin(pairs_of_interest)]

# Pivot the filtered DataFrame to have personas1 and personas2 as columns and f1-score as values
pivot_df = filtered_df.pivot_table(index='persona1', columns='persona2', values='f1-score')

# Create a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(pivot_df, annot=True, cmap='viridis', fmt=".2f", annot_kws={"size": 20})
plt.title('F1-Score Comparison Between Personas', fontsize=20)
plt.xlabel('')
plt.ylabel('')
# make the font size larger
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.show()

