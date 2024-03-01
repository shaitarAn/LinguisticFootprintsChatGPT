
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("../results/per_feature/connectives_cap/connectives_upper_pubmed_de.csv")

print(data.head(20))

# sort 
sns.set_theme(style="white")

# use the first 25 rows
data = data.iloc[:30]

# make heat map for the values in the columns hu-co, hu-ex, hu-cr

data = data.set_index('connective')

# set the size of the plot
plt.figure(figsize=(5, 10))

# create a heatmap
ax = sns.heatmap(data=data[['HU-CO', 'HU-EX', 'HU-CR']], annot=True, fmt="d", linewidths=.5, cbar=False, cmap="YlGnBu")

# add extra y axis label to the right, use "human_upper" column values as labels
ax2 = ax.twinx()
# ax2.set_ylabel(data['human_upper'].name, fontsize=15)
ax2.set_yticklabels(data['human_upper'], fontsize=15)

# set the font size of the x and y axis labels
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)


# place the x axis labels on the top
ax.xaxis.tick_top()

# change the text of the x axis labels
# ax.set_xticklabels(['HU-CO', 'HU-EX', 'HU-CR'], fontsize=15)


# set font size for the labels
ax.tick_params(labelsize=15) 

# set the color palette to set3
sns.set_palette("Set3")

# remove the y axis label
plt.ylabel("")

# save the plot as a pdf file
plt.savefig("../visualizations/pdfs/connectives_cap_pubmed_de_heatmap.pdf", bbox_inches='tight')

# show the plot
plt.show()


# # sort by human_total in descending order and only from row 2 to 30
# data = data.sort_values(by='human_total', ascending=False).iloc[2:32]

# # create a stacked horizontal bar plot
# data.plot(x="connective", kind="barh", stacked=True, figsize=(10, 10), title="Connectives in the German PubMed corpus", width=0.8, fontsize=15)
# # flip the y axis
# plt.gca().invert_yaxis()

# # create a legend with large font
# plt.legend(loc='center right', prop={'size': 15}, labels=['human', 'continue', 'explain', 'create'])
# # place legend higher in the middle of the y axis
# # plt.legend(loc='middle right', bbox_to_anchor=(1, 0.5), ncol=1, fancybox=True, shadow=True)

# plt.subplots_adjust(hspace=0.1)

# # do not label the y axis
# plt.ylabel("")
# # set the color palette to set3
# sns.set_palette("Set3")

# plt.tight_layout()

# # save the plot as a pdf file
# plt.savefig("../visualizations/pdfs/connectives_all_pubmed_de.pdf", bbox_inches='tight')



# plt.show()