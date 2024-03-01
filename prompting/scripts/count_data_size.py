import os

# count the number of tokens in the English and German corpora

#   # count the number of tokens in the English and German corpora
#   # initialize a dictionnary that will hold the counts
list_of_english_corpora = ["pubmed_en", "zora_en", "cnn", "cs_en", "e3c"]
list_of_german_corpora = ["pubmed_de", "zora_de", "20min", "cs_de", "ggponc"]

count_tokens = {}

def count_tokens_in_corpus(corpus):
    # initialize a counter
    count = 0
    # open the corpus
    
    for persona in os.listdir(f"../../data/{corpus}/"):
        # print(persona)
        # check if the persona is a directory
        if os.path.isdir(f"../../data/{corpus}/{persona}"):
            print(persona)
            for file in os.listdir(f"../../data/{corpus}/{persona}/"):
                with open(f"../../data/{corpus}/{persona}/{file}", "r") as f:
                    for line in f:
                        # print(line)
                        count += len(line.split())

    return count

#   # for each corpus, count the number of tokens
for corpus in list_of_english_corpora:
    print(corpus)
    corpus_count = count_tokens_in_corpus(corpus)
    print(corpus_count)
    count_tokens[corpus] = corpus_count

for corpus in list_of_german_corpora:
    print(corpus)
    corpus_count = count_tokens_in_corpus(corpus)
    print(corpus_count)
    count_tokens[corpus] = corpus_count


print(count_tokens)

# add the counts of tokens for each corpus in the count_corpora dictionnary
total_tokens = 0
for corpus in count_tokens:
    total_tokens += count_tokens[corpus]

print(total_tokens)
