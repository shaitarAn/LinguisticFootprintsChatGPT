import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Your data
data = {
    'corpus': ['20min', 'cs_de', 'zora_de', 'pubmed_de', 'ggponc', 'e3c', 'pubmce_en', 'zora_en', 'cs_en', 'cnn'],
    'human': [33, 23, 2, 20, 18, 30, 27, 5, 29, 29],
    'continue': [6, 11, 1, 11, 7, 13, 14, 0, 17, 14],
    'explain': [8, 6, 0, 10, 3, 9, 15, 0, 17, 18],
    'create': [20, 13, 0, 10, 7, 9, 27, 2, 25, 28]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Set 'corpus' as index
df.set_index('corpus', inplace=True)

# Create a heatmap
plt.figure(figsize=(6, 7))

# Customize annotation font size and weight
annot_kws = {'fontsize': 12, 'fontweight': 'bold'}

ax = sns.heatmap(df, annot=True, cmap='Greens', cbar=False, linewidths=.5, annot_kws=annot_kws)
# Adding the second layer of y-axis labels
ax.set_yticks([x + 0.5 for x in range(len(df.index))])
ax.set_yticklabels(df.index, rotation=0, fontsize=10)
ax2 = ax.twinx()
ax2.set_yticks([x for x in range(len(df.index))])
ax2.set_yticklabels(['journal']*2 + ['academ']*2 + ['clinic']*2 + ['academ']*2 +['journal']*2, rotation=0, fontsize=10)
# Draw a thick horizontal line between rows 5 and 6
ax.axhline(y=5, color='black', linewidth=3)
plt.title('Number of significant features per corpus')
plt.show()