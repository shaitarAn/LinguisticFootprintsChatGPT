import os
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacy
from spacy.tokenizer import Tokenizer
from spacy.util import compile_prefix_regex, compile_infix_regex, compile_suffix_regex
from termcolor import colored
import re

### ------------------------------------
### Section 1: Custom Tokenizer Setup
### ------------------------------------

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Customize the Tokenizer to keep hyphenated words intact
def custom_tokenizer(nlp):
    prefix_re = compile_prefix_regex(nlp.Defaults.prefixes)
    suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)
    infix_patterns = [pattern for pattern in nlp.Defaults.infixes if pattern != r"(?<!\d)\-(?!\d)"]
    infix_re = compile_infix_regex(infix_patterns)

    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                     suffix_search=suffix_re.search,
                     infix_finditer=infix_re.finditer, token_match=None)

# Set the new tokenizer for the nlp pipeline
nlp.tokenizer = custom_tokenizer(nlp)

### ------------------------------------
### Section 2: Load Texts
### ------------------------------------

# Set paths for generated and human-written texts
dir_path_generated = os.path.expanduser("~/switchdrive/AItextDetect/data_2403gpt4/cnn/continue")
dir_path_human = os.path.expanduser("~/switchdrive/AItextDetect/data_2403gpt4/cnn/human")
text_num = "42"

def clean_text(text):
    # Remove newlines and extra spaces
    text = text.replace("\n", " ").replace("  ", " ")
    text = text.replace("«", '"').replace("»", '"')
    text = text.replace("„", '"').replace("“", '"')
    text = text.replace("‚", "'").replace("‘", "'")
    return text

# Load generated and human-written text files
with open(f"{dir_path_generated}/{text_num}.txt", "r") as f:
    generated_text = f.read()

with open(f"{dir_path_human}/{text_num}.txt", "r", encoding='utf8') as f:
    human_text = f.read()
    
### ------------------------------------
### Section 3: Word Length Frequency Analysis
### ------------------------------------

# Function to calculate word length frequencies
def get_word_length_frequencies(text):
    word_lengths = defaultdict(lambda: {'words': set(), 'frequency': 0})
    for token in nlp(clean_text(text)):
        if token.is_alpha:
            word_lengths[len(token.text)]['words'].add(token.text)
            word_lengths[len(token.text)]['frequency'] += 1
    return word_lengths

# Get word length frequencies for both texts
word_lengths_generated = get_word_length_frequencies(generated_text)
word_lengths_human = get_word_length_frequencies(human_text)

# Extract frequencies for plotting
frequencies_generated = {k: v['frequency'] for k, v in word_lengths_generated.items()}
frequencies_human = {k: v['frequency'] for k, v in word_lengths_human.items()}

### ------------------------------------
### Section 4: Visualizations
### ------------------------------------

# Create side-by-side bar charts to compare word lengths
plt.figure(figsize=(20, 5))
max_y_value = max(max(frequencies_human.values()), max(frequencies_generated.values()))

# Human-Written Text Bar Chart
plt.subplot(1, 2, 1)
plt.bar(frequencies_human.keys(), frequencies_human.values(), color='gray')
plt.xlabel('')
plt.ylabel('Frequency', fontsize=16)
plt.title('Human Text', fontsize=25)
plt.xticks(range(1, max(frequencies_human.keys()) + 1), fontsize=16)
plt.ylim(0, max_y_value)
plt.axhline(y=50, color='r', linestyle='--')
if 6 in frequencies_human:
    plt.bar(6, frequencies_human[6], color='red')

# Generated Text Bar Chart
plt.subplot(1, 2, 2)
plt.bar(frequencies_generated.keys(), frequencies_generated.values(), color='gray')
plt.xlabel('')
plt.ylabel('')
plt.title('Generated Text', fontsize=25)
plt.xticks(range(1, max(frequencies_generated.keys()) + 1), fontsize=16)
plt.ylim(0, max_y_value)
plt.axhline(y=50, color='r', linestyle='--')
if 6 in frequencies_generated:
    plt.bar(6, frequencies_generated[6], color='red')

plt.tight_layout()
# plt.savefig('word_length_comparison.png')
# plt.show()

# Create side-by-side Word Clouds
# remove stopwords
stopwords = nlp.Defaults.stop_words
generated_text = clean_text(generated_text)
human_text = clean_text(human_text)
generated_text_cloud = " ".join([word for word in generated_text.split() if word.lower() not in stopwords])
human_text_cloud = " ".join([word for word in human_text.split() if word.lower() not in stopwords])
wordcloud_generated = WordCloud(width=800, height=400, max_words=100, background_color='white').generate(generated_text_cloud)
wordcloud_human = WordCloud(width=800, height=400, max_words=100, background_color='white').generate(human_text_cloud)

# Plot both word clouds side by side
plt.figure(figsize=(16, 8))
plt.subplot(1, 2, 1)
plt.imshow(wordcloud_generated, interpolation='bilinear')
plt.axis('off')
plt.title('Generated Text', fontsize=25)
plt.subplot(1, 2, 2)
plt.imshow(wordcloud_human, interpolation='bilinear')
plt.axis('off')
plt.title('Human Text', fontsize=25)
plt.tight_layout()
# plt.savefig('word_cloud_comparison.png')
# plt.show()

### ------------------------------------
### Section 5: Highlight Repeated Words for LaTeX
### ------------------------------------

# Function to escape LaTeX special characters
def escape_latex_special_chars(word):
    replacements = {
        "&": "\\&",
        "%": "\\%",
        "$": "\\$",
        "#": "\\#",
        "_": "\\_",
        "{": "\\{",
        "}": "\\}",
        "–": "-",
        "-": "-",
    }
    for char, replacement in replacements.items():
        word = word.replace(char, replacement)
    return word

def highlight_repeated_words(text, format_type="latex"):
    words = [w.text for w in nlp(text)]
    word_count = Counter([word.strip(",.?!;:\"()").lower() for word in words])
    highlighted_text = []

    sentence_number = 2  # Start the sentence numbering at 1

    for word in words[:180]:
        word = word.replace("’", "'").replace("”", '"').replace("“", '"').replace("‘", "'")
        if word in ["\n", "\n\n"]:
            continue
        cleaned_word = word.strip(",.?!;:\"()").lower()

        # LaTeX formatted highlighting
        if format_type == "latex":
            word_for_latex = escape_latex_special_chars(word)
            if word_count[cleaned_word] > 1:  # Check if the word is repeated
                if len(word_for_latex) >= 8:
                    # Underline and highlight in red if the word is repeated and longer than 7 characters
                    highlighted_text.append(f"\\underline{{\\textcolor{{red}}{{{word_for_latex}}}}}")
                else:
                    # Highlight in red only for repeated words less than 7 characters
                    highlighted_text.append(f"\\textcolor{{red}}{{{word_for_latex}}}")
            else:
                # Check if non-repeated words are longer than 7 characters to underline them
                if len(word_for_latex) >= 7:
                    highlighted_text.append(f"\\underline{{\\textcolor{{green}}{{{word_for_latex}}}}}")
                else:
                    # No special formatting for short, non-repeated words
                    highlighted_text.append(f"\\textcolor{{green}}{{{word_for_latex}}}")


            # Add sentence number after a period
            if word == ".":
                highlighted_text.append(f" \\circled{{{sentence_number}}}")
                sentence_number += 1

        # Terminal formatted highlighting
        elif format_type == "terminal":
            if word_count[cleaned_word] > 1:
                highlighted_text.append(f"\033[91m{word}\033[0m")  # repeated word highlighted in red
            else:
                highlighted_text.append(f"\033[92m{word}\033[0m")  # unique word highlighted in green

        # Default behavior: plain text
        else:
            highlighted_text.append(word)

    return " ".join(highlighted_text)


# Highlight repeated words in both texts for LaTeX
highlighted_generated_text_latex = highlight_repeated_words(generated_text, format_type="latex")
highlighted_human_text_latex = highlight_repeated_words(human_text, format_type="latex")

# Highlight repeated words in both texts for Terminal
highlighted_generated_text_terminal = highlight_repeated_words(generated_text, format_type="terminal")
highlighted_human_text_terminal = highlight_repeated_words(human_text, format_type="terminal")

# Print LaTeX-formatted text for Overleaf
print("Human Text LaTeX:\n", highlighted_human_text_latex)
print("\nGenerated Text LaTeX:\n", highlighted_generated_text_latex)

# Print the regular text for the first 140 words
print("\nHuman Text (First 140 words):\n", " ".join(human_text.split()[:140]))
print("\nGenerated Text (First 140 words):\n", " ".join(generated_text.split()[:140]))

# Print the colored text in the terminal
print("\nHuman Text Terminal:\n", highlighted_human_text_terminal)
print("\nGenerated Text Terminal:\n", highlighted_generated_text_terminal)

import math
from collections import Counter

def calculate_entropy_per_word(text):
    # Tokenize text into words
    words = text.split()
    
    # Count the frequency of each word
    word_counter = Counter(words)
    
    # Calculate the total number of words
    total_words = len(words)
    
    # Calculate the entropy contribution of each word
    word_entropy = {}
    for word, count in word_counter.items():
        # Calculate the probability of the word
        p_i = count / total_words
        
        # Calculate entropy contribution
        entropy_contribution = -p_i * math.log2(p_i)
        
        # Store the word and its entropy contribution
        word_entropy[word] = entropy_contribution
    
    return word_entropy

# word_entropy = calculate_entropy_per_word(" ".join(human_text.split()))

# # Print the entropy of each word
# print("Entropy contribution per word:")
# # print the first 100 words
# for word, entropy in list(word_entropy.items())[:100]:
#     print(f"{word}: {entropy:.4f}")

