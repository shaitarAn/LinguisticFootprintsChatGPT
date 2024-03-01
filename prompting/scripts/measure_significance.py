import pandas as pd
# from scipy.stats import tukey_hsd
import itertools
import numpy as np
import os
import scikit_posthocs as sp
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from features_list import features_list
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
    
def persona_pairwise(persona, result, persona2):

    if persona == "human":
        persona = 1
    elif persona == "continue":
        persona = 2
    elif persona == "explain":
        persona = 3
    elif persona == "create":
        persona = 4

    for (i, j) in itertools.combinations(result.columns, 2):

        if result[i][j] < 0.01:

            if i == persona and j == persona2:
                return True
            elif i == persona2 and j == persona:
                return True
            else:
                continue

def make_boxplot(feature, folder, df):

    # make a boxplot with the p-values of the dunns test
    plt.figure(figsize=(4, 6))
    sns.boxplot(data=df, palette='Set3', showmeans=True)
    plt.title(f"{feature}", fontsize=20)
    plt.xticks(rotation=45)
    # increase the font size of the x
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=15)
    # plt.savefig(f"../visualizations/boxplots/{lang}/{feature}.pdf", bbox_inches='tight')
    plt.savefig(f"../visualizations/boxplots/{folder}/{feature}.png", bbox_inches='tight')
    plt.close()


def make_heatmap(feature, folder, result):

    # make a heatmap of the p-values of the dunns test
    plt.figure(figsize=(4, 6))
    # do not show the side bar

    sns.heatmap(result, annot=True, cmap='Blues', fmt='.3f', cbar=False)

    plt.xticks(np.arange(4) + 0.5, df.columns)
    plt.yticks(np.arange(4) + 0.5, df.columns)
    plt.xticks(rotation=45)
    plt.title(f"{feature}")
    # plt.savefig(f"../visualizations/heatmaps/{lang}/{feature}.pdf", bbox_inches='tight')
    plt.savefig(f"../visualizations/boxplots/{folder}/{feature}.pdf", bbox_inches='tight')
    plt.close()

def count_means(df, feature):
    
    # initialize a dataframe to store the mean of each feature for each persona
    df_mean = pd.DataFrame(columns=["feature", "human", "continue", "explain", "create"])

    human = df['human']
    cont = df['continue']
    explain = df['explain']
    create = df['create']

    # calculate the mean, convert it to float and round it to 2 decimals

    human_mean = np.format_float_positional(np.float64(np.mean(human)), precision=2)
    cont_mean = np.format_float_positional(np.float64(np.mean(cont)), precision=2)
    explain_mean = np.format_float_positional(np.float64(np.mean(explain)), precision=2)
    create_mean = np.format_float_positional(np.float64(np.mean(create)), precision=2)


    # add the means to the dataframe
    df_mean = df_mean.append({"feature": feature, "human": human_mean, "continue": cont_mean, "explain": explain_mean, "create": create_mean}, ignore_index=True)

    return df_mean

def list_corpora_per_feature(one_feature, persona):

    feature_path = f"../results/per_feature/{one_feature}/"

    corpora_with_sign_feat = []
    corpora_with_feat_persona = []

    for corpus in os.listdir(feature_path):

        if not corpus.endswith(".csv"):
            continue
        df = pd.read_csv(feature_path + corpus)

        results = kruskal_test(df)

        # print corpus name where feature is significant
        if results[1] < 0.05:
            corpora_with_sign_feat.append(corpus)

            pairwise = dunn_test(df)
            
            if persona_significance(persona, pairwise):
                corpora_with_feat_persona.append(corpus)

    return corpora_with_sign_feat, corpora_with_feat_persona


def find_significant_features_per_lang(lang, persona):
    
    count_significant_features = []
    significant_features_per_persona = []

    for feature in features_list:

        try:

            df = pd.read_csv(f"../results/per_language/{lang}/{feature}.csv")
            results = kruskal_test(df)

            # print corpus name where feature is significant
            if results[1] < 0.05:
                count_significant_features.append(feature)

                pairwise = dunn_test(df)

                if persona_significance(persona, pairwise):
                    significant_features_per_persona.append(feature)

        except FileNotFoundError:
            continue

    return count_significant_features, significant_features_per_persona

# ###########################################
# find corpora where the given feature is significant
# ###########################################

def find_corpora_one_feature(persona, one_feature):

    corpora_with_sign_feat, corpora_with_feat_persona = list_corpora_per_feature(one_feature, persona)

    print(f"Corpora with significant feature {one_feature}: ", corpora_with_sign_feat)
    print()
    print(f"{one_feature} sets *{persona}* apart from others in: ", corpora_with_feat_persona)
    print()

# ###########################################
# ## find significant features per language ##
# ###########################################

def find_features_per_lang_persona(persona):

    eng_features, eng_features_for_persona = find_significant_features_per_lang("english", persona)
    ger_features, ger_features_for_persona = find_significant_features_per_lang("german", persona)

    print("----------------------------------------")
    print("ENGLISH: ")
    print("----------------------------------------")
    # print("SIGNIFICANT FEATURES: ")
    # print(sorted(eng_features))
    # print(len(eng_features))
    # print()
    print(f"PERSONA = {persona} : ")
    print(sorted(eng_features_for_persona))
    print(len(eng_features_for_persona))
    print()
    print("----------------------------------------")
    print("GERMAN: ")
    print("----------------------------------------")
    # print("SIGNIFICANT FEATURES: ")
    # print(sorted(ger_features))
    # print(len(ger_features))
    # print()
    print(f"PERSONA = {persona} : ")
    print(sorted(ger_features_for_persona))
    print(len(ger_features_for_persona))
    print()
    # print("----------------------------------------")
    # print("BOTH LANGUAGES: ")
    # print("----------------------------------------")
    # print("SIGNIFICANT FEATURES: ")
    # print(sorted(list(set(eng_features).intersection(ger_features))))
    # print(len(set(eng_features).intersection(ger_features)))
    # print()
    # print(f"PERSONA = {persona} : ")
    # print(sorted(list(set(eng_features_for_persona).intersection(ger_features_for_persona))))
    # print(len(set(eng_features_for_persona).intersection(ger_features_for_persona)))
    # print()
    # print("----------------------------------------")



# ###########################################
# initialize a dataframe for combined means
# ###########################################

def count_means_total(persona):
    means_eng = pd.DataFrame(columns=["feature", "human", "continue", "explain", "create"])
    # means_eng_rounded = pd.DataFrame(columns=["feature", "human", "continue", "explain", "create"])
    means_ger = pd.DataFrame(columns=["feature", "human", "continue", "explain", "create"])
    for f in sorted(features_list):
        try:
            
            df_de = pd.read_csv(f"../results/per_language/german/{f}.csv")
            # measure significance for each feature and add to the dataframe
            if kruskal_test(df_de)[1] < 0.05:
                # do pairwise comparisons for personas
                pairwise = dunn_test(df_de)
                # check if the given persona is significantly different from others
                # print(f, persona, "german")
                if persona_significance(persona, pairwise):
                    # if yes, add the feature to the dataframe
                    means_ger = means_ger.append(count_means(df_de, f))

            df_en = pd.read_csv(f"../results/per_language/english/{f}.csv")
            # measure significance for each feature and add to the dataframe
            if kruskal_test(df_en)[1] < 0.05:
                # do pairwise comparisons for personas
                pairwise = dunn_test(df_en)
                # print(f, persona, "english")
                # check if the given persona is significantly different from others
                if persona_significance(persona, pairwise):
                    # if yes, add the feature to the dataframe rounding the mean to 2 decimals
                    means_eng = means_eng.append(count_means(df_en, f))
                    # means_eng_rounded = means_eng_rounded.append(count_means(df_en, f)[0])

        except FileNotFoundError:
            continue


    print("----------------------------------------")
    print(means_eng)
    print("----------------------------------------")
    print("German")
    print("----------------------------------------")
    print(means_ger)
    # print(means_eng.to_latex(index=False))
    # print(means_ger.to_latex(index=False))


# ###########################################
# create dictionary for a confusion matrix of feature counts between personas
# ###########################################

def count_pairwise_personas():

    confusion_matrix = {}

    for p in ["human", "continue", "explain", "create"]:
        if p in confusion_matrix:
            continue
        confusion_matrix[p] = {}
        for persona2 in [1,2,3,4]:
            if persona2 in confusion_matrix[p]:
                continue
            else:
                confusion_matrix[p][persona2] = []
            for feature in sorted(features_list):
                try:
                    df = pd.read_csv(f"../results/per_language/german/{feature}.csv")
                    if kruskal_test(df)[1] < 0.05:
                        pairwise = dunn_test(df)
                        if persona_pairwise(p, pairwise, persona2):
                            confusion_matrix[p][persona2].append(feature)
                except FileNotFoundError:
                    continue
            

    print("----------------------------------------")
    print("Confusion matrix")
    print("----------------------------------------")
    for k, v in confusion_matrix.items():
        print(k)
        for k1, v1 in v.items():
            print(k1, set(sorted(v1)), len(v1))
        print()

def main():

    # intitialize a list to store the dataframes of each feature
    list_of_english_corpora = ["pubmed_en", "zora_en", "cnn", "cs_en", "e3c"]
    list_of_german_corpora = ["pubmed_de", "zora_de", "20min", "cs_de", "ggponc"]


    # find which persona stands out among three others. 
    # Personas: 1=human, 2=continue, 3=explain, 4=create
    persona = "create"
    one_feature = "n_stop_words"

    count_means_total(persona)
    # count_pairwise_personas(persona)
    # find_corpora_one_feature(persona, one_feature)
    find_features_per_lang_persona(persona)

    for feature in features_list:
        try:
            make_boxplot(feature, "english", pd.read_csv(f"../results/per_language/english/{feature}.csv"))
        except FileNotFoundError:
            continue

    for feature in features_list:
        try:
            make_boxplot(feature, "german", pd.read_csv(f"../results/per_language/german/{feature}.csv"))
        except FileNotFoundError:
            continue 


if __name__ == "__main__":
    main()


        









