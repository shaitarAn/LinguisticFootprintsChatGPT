import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

methods = {'bh': 'Benjamini-Hochberg', 'holm': 'Holm', 'bon': 'Bonferroni'}

corpus_dict = {
    "cnn": "CNN",
    "20min": "20 Minuten",
    "cs_en": "CSB English",
    "cs_de": "CSB German", 
    "pubmed_de": "PubMed German",
    "pubmed_en": "PubMed English",
    "full": "Full data"
}

def collect_special_pngs(path):
    pngs = []
    # check if path is a directory
    if os.path.isdir(path):    
        for png in os.listdir(path):
            print(png)
            if png.endswith(".png"):
                pngs.append(f"{path}{png}")

    return pngs

def plot_means(outputdir, df, title, alpha):
    # if not os.path.exists(f'{outputdir}/{language}'):
    #     os.makedirs(f'{outputdir}/{language}')
    # make a boxplot with the p-values of the dunns test
    plt.figure(figsize=(4, 6))
    # plot the four boxplots for the four personas
    sns.boxplot(data=df, palette='Set3', showmeans=True)
    # ignore severe outliers
    # plt.yscale('log')
    plt.title(f"{title}", fontsize=20)
    plt.xticks(rotation=45)
    # increase the font size of the x
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=15)
    plt.savefig(f"{outputdir}/means_{title}.png")
    plt.show()
    plt.close()

def plot_distribtuions(outputdir, pvalues, corrected, p, language, method, alpha):
    if not os.path.exists(f'{outputdir}/{language}'):
        os.makedirs(f'{outputdir}/{language}')

    sns.kdeplot(pvalues, color="red", shade=True, label='raw')
    ax = sns.kdeplot(corrected, color="green", shade=True, label='adujusted')
    ax.set(xlim=(0, 1))
    plt.title('distribution of p-values for ' + p)
    plt.legend()
    # save the plot
    plt.savefig(f'{outputdir}/{language}/dist_{method}_{p}_{alpha}.pdf')
    # plt.show()
    plt.close()


def plot_values(outputdir, dfp, p, language, method, alpha):

    if not os.path.exists(f'{outputdir}/{language}'):
        os.makedirs(f'{outputdir}/{language}')
        
    # drop the rows with NaN and None values in place
    dfp = dfp.dropna() 

    # sort the dataframe by the p-value in ascending order
    dfp = dfp.sort_values(by='pvalue', ascending=False)

    # plot the corrected p-values
    sns.set(style="whitegrid")
    # make scatter plot
    ax = sns.scatterplot(x="pvalue", y="feature", data=dfp, color='b', label='t-test p-values')
    # add a line for B-H correction q-values
    ax = sns.scatterplot(x=method, y="feature", data=dfp, color='g', label=f'{methods[method]} multiple testing correction')
    # increase the size of the plot
    fig = plt.gcf()
    fig.set_size_inches(15, 10)

    # change x-axis label
    plt.xlabel(f'feature significance for {p}')

    # add the alpha level to the plot in light gray
    plt.axvline(x=alpha, color='r', linestyle='--', label=f'alpha = {alpha}')
    # give more space to the y-axis labels
    plt.tight_layout()
    plt.savefig(f'{outputdir}/{language}/{method}_{p}_{alpha}.pdf')
    # close the plot
    plt.close()


def plot_feat_groups(outputdir, feature_name, corpus, df):
# make a boxplot with the p-values of the t-test
    plt.figure(figsize=(4, 6))
    sns.boxplot(data=df, palette='Set3', showmeans=True)
    plt.title(f"{feature_name} for {corpus}")
    plt.xticks(rotation=45)
    # save the plot as a pdf file
    plt.savefig(f"{outputdir}/{feature_name}.pdf", bbox_inches='tight')