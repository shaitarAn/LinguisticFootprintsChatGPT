import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Example data from your table
data = {
    'Text Pair': ['Human - Continue', 'Human - Explain', 'Human - Create', 'Continue - Explain', 'Continue - Create', 'Explain - Create', 'Human - AsHuman', 'Human - AsMachine', 'AsHuman - AsMachine'],
    'English 3.5 ': [42, 45, 44, 37, 42, 42, None, None, None],
    'German 3.5': [43, 44, 36, 27, 18, 29, None, None, None],
    'English 4': [56, 50, 55, 28, 15, 47, 49, 48, 7],
    'German 4': [45, 43, 50, 40, 17, 36, 33, 29, 1]
}

# Create a DataFrame
df = pd.DataFrame(data).set_index('Text Pair')

# Create a heatmap
plt.figure(figsize=(12, 6))
sns.set(font_scale=1.2)  # Set the font scale larger to emphasize annotations
sns.heatmap(df, annot=True, cmap="coolwarm", cbar_kws={'label': 'Number of Significant Features'}, fmt='.0f', linewidths=.5)

# Add the title
plt.title('')
# remove y-axis title
plt.ylabel('')

# Annotate the groupings for GPT-3.5 and GPT-4
# Use plt.text() to add text annotations at the top
plt.text(0.25, 1.05, 'GPT-3.5', ha='center', va='bottom', fontsize=16, fontweight='bold', transform=plt.gca().transAxes)
plt.text(0.75, 1.05, 'GPT-4', ha='center', va='bottom', fontsize=16, fontweight='bold', transform=plt.gca().transAxes)

# Add vertical lines to separate GPT-3.5 and GPT-4
plt.axvline(x=2, color='black', linestyle='-', linewidth=2)
# Add horizontal line to separate rows "Human - Create" and "Continue - Explain"
plt.axhline(y=3, color='black', linestyle='-', linewidth=2)
plt.axhline(y=6, color='black', linestyle='-', linewidth=2)

# Show plot
plt.tight_layout()
plt.show()


# import numpy as np

# # Bar Chart Parameters
# labels = df.index
# x = np.arange(len(labels))  # Label locations
# width = 0.2  # Width of the bars

# # Create Subplots
# fig, ax = plt.subplots(figsize=(12, 6))

# # Plot the bars for each group
# ax.bar(x - width * 1.5, df['GPT-3.5 English'], width, label='GPT-3.5 English', color='skyblue')
# ax.bar(x - width / 2, df['GPT-3.5 German'], width, label='GPT-3.5 German', color='lightblue')
# ax.bar(x + width / 2, df['GPT-4 English'], width, label='GPT-4 English', color='coral')
# ax.bar(x + width * 1.5, df['GPT-4 German'], width, label='GPT-4 German', color='orange')

# # Formatting
# ax.set_xlabel('Text Pair')
# ax.set_ylabel('Number of Significant Features')
# ax.set_title('Number of Significant Features by GPT Version and Language')
# ax.set_xticks(x)
# ax.set_xticklabels(labels, rotation=45, ha='right')
# ax.legend()

# plt.tight_layout()
# plt.show()
