import pandas as pd
from scipy.stats import tukey_hsd
import itertools
import numpy as np
import os
import scikit_posthocs as sp
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from feature_extraction.scripts.features_list import features_list
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def kruskal_test(df):

    human = df['human']
    cont = df['continue']
    explain = df['explain']
    create = df['create']

    # A p-value less than alpha (e.g., p < 0.05) suggests that there is significant evidence to reject the null hypothesis (H0), indicating that there is a statistically significant difference between the two groups being compared.

    results = stats.kruskal(human, cont, explain, create)

    return results

def dunn_test(df):

    human = df['human']
    cont = df['continue']
    explain = df['explain']
    create = df['create']
    
    show = sp.posthoc_dunn([human, cont, explain, create], p_adjust='holm')

    return show


def persona_significance(persona, result):

    if persona == "human":
        persona = 1
    elif persona == "continue":
        persona = 2
    elif persona == "explain":
        persona = 3
    elif persona == "create":
        persona = 4

    count = 0
    for (i, j) in itertools.combinations(result.columns, 2):

        if result[i][j] < 0.05:

            if i == persona or j == persona:
                count += 1

    if count == 3:
        return True
    else:
        return False 

def list_corpora_per_feature(one_feature, persona):

    feature_path = f"../results/per_feature/{one_feature}/"

    corpora_with_sign_feat = []
    corpora_with_feat_persona = []

    for corpus in os.listdir(feature_path):

        if not corpus.endswith(".csv"):
            continue
        # print(corpus)
        df = pd.read_csv(feature_path + corpus)

        results = kruskal_test(df)

        if results[1] < 0.05:
            corpora_with_sign_feat.append(corpus)

            pairwise = dunn_test(df)
            
            if persona_significance(persona, pairwise):
                corpora_with_feat_persona.append(corpus)

    return corpora_with_sign_feat, corpora_with_feat_persona

# intitialize a list to store the dataframes of each feature
list_of_english_corpora = ["pubmed_en", "zora_en", "cnn", "cs_en", "e3c"]
list_of_german_corpora = ["pubmed_de", "zora_de", "20min", "cs_de", "ggponc"]

# create a nested dictionnary that will hold counts [feature][persona][lang]
count_feat_persona = {}
personas = ["human", "continue", "explain", "create"]

# create dictionary with corpora names as keys and number of features as values
count_corpora = {}

# for each feature, initialize a dictionnary that will hold counts [persona][lang]
for feature in features_list:
    count_feat_persona[feature] = {}
    print("------------------------------")
    print(feature)
    for persona in personas:
        if not persona in count_corpora:
            count_corpora[persona] = {}
        
        print(persona, "+++++++++++")
        try:
            _, corpora = list_corpora_per_feature(feature, persona)
            print(corpora)
            eng_corpora = [corpus for corpus in corpora if corpus[:-4] in list_of_english_corpora]
            ger_corpora = [corpus for corpus in corpora if corpus[:-4] in list_of_german_corpora]
            count_feat_persona[feature][persona+"_english"] = int(len(eng_corpora))
            count_feat_persona[feature][persona+"_german"] = int(len(ger_corpora))

            for corpus in corpora:
                if corpus[:-4] in count_corpora[persona]:
                    count_corpora[persona][corpus[:-4]] += 1
                else:
                    count_corpora[persona][corpus[:-4]] = 1
        except FileNotFoundError:
            continue

    print("------------------------------")
    print("------------------------------")
    print(count_corpora)

print(count_feat_persona)

# create a dataframe from the dictionnary
df = pd.DataFrame.from_dict(count_feat_persona)
# transpose the dataframe
df = df.transpose()

print(df)

# save the dataframe to a csv file
df.to_csv("../results/feature_persona_lang.csv")

for persona in personas:
    print(persona)
    print(count_corpora[persona])
    print("------------------------------")
