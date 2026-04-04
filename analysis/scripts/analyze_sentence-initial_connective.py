import os
import spacy

connective = "Darüber hinaus"
directory_path = os.path.expanduser(f"~/switchdrive/AItextDetect/data_2403gpt4/pubmed_de/create")

nlp = spacy.load("de_core_news_sm")

def count_occurrences_and_tokens(directory):
    total_occurrences = 0
    total_tokens = 0

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                text = file.read()

                # Process the text using SpaCy
                doc = nlp(text)

                # Count tokens
                total_tokens += len(doc)

                # Count occurrences of "Darüber hinaus" at the beginning of sentences
                occurrences = sum(1 for sent in doc.sents if sent.text.strip().startswith(connective))
                total_occurrences += occurrences

    # Calculate the ratio of occurrences per thousand tokens
    if total_tokens > 0:
        ratio_per_thousand = (total_occurrences / total_tokens) * 1000
    else:
        ratio_per_thousand = 0

    return total_occurrences, total_tokens, ratio_per_thousand


occurrences, tokens, ratio = count_occurrences_and_tokens(directory_path)
print(f"Directory: {directory_path.split('/')[-1]}")
print(f"Total 'Darüber hinaus' occurrences: {occurrences}")
print(f"Total token count: {tokens}")
print(f"Occurrences per 1,000 tokens: {ratio:.2f}")
