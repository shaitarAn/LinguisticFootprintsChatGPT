# config.py

"""
These variables are imported in extract_features.py, combine_results_per_lang_domain.py, transform_dataframe.py and count_connectives.py
"""

# 2309gpt3, 2403gpt4
GERMAN_CORPORA = ['20min', 'cs_de', 'ggponc', 'pubmed_de', 'zora_de']
ENGLISH_CORPORA = ['cnn', 'e3c', 'zora_en', 'pubmed_en', 'cs_en']
SCIENCE_CORPORA = ["pubmed_en", "pubmed_de", "zora_en", "zora_de"]
NEWS_CORPORA = ["cnn", "20min", "cs_en", "cs_de"]
CLINICAL_CORPORA = ["e3c", "ggponc"]
tasks = ['human', 'continue', 'explain', 'create']

# 2409gpt4
# GERMAN_CORPORA = ['20min', 'pubmed_de']
# ENGLISH_CORPORA = ['cnn', 'pubmed_en']
# SCIENCE_CORPORA = ["pubmed_en", "pubmed_de"]
# NEWS_CORPORA = ["cnn", "20min"]
# CLINICAL_CORPORA = []
# tasks = ['human', 'ashuman', 'asmachine']
