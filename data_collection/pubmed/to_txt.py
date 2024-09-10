import sys
import os
import xml.etree.ElementTree as ET
import spacy
from tqdm import tqdm

infile_name = sys.argv[1]
outfolder = sys.argv[2]
lang = sys.argv[3]
num_art = int(sys.argv[4]) # number of articles to process (for the process bar)



if lang == "de":
    nlp = spacy.load("de_core_news_sm")
elif lang == "en":
    nlp = spacy.load("en_core_web_sm")


def tokenize_text(text):
    '''
    This function tokenizes a text using spacy.
    :return length of the text and the text itself
    '''

    doc = nlp.tokenizer(text)
    return len([token.text for token in doc]), " ".join([token.text for token in doc])

def get_text(node):
    """Get all text nodes within <p> elements, ignore the rest"""
    full_text = ""
    for sub_node in node.iter("p"):
        text = "".join(sub_node.itertext())
        full_text += text
    return full_text



with open(infile_name, "r", encoding="utf-8") as infile:
    tree = ET.parse(infile)

articles = tree.getroot()

for article in tqdm(articles.iter("article"), total=num_art):
    article_iter = iter(article)
    pmid = next(article_iter).text
    year = next(article_iter).text
    title = next(article_iter).text
    
    abstract = next(article_iter)
    introduction = next(article_iter)
    
    abstract_text = get_text(abstract)
    intro_text = get_text(introduction)
    # intro_text = re.sub(r"[„“]", "'", intro_text)  # weird quotes, make program crash :/
    intro_len = tokenize_text(intro_text)[0]
    
    
    if intro_len > 500:
        outfile_name = f"{year}-{pmid}_{intro_len}_{lang}.txt"
        filepath = os.path.join(outfolder, outfile_name)
        
        with open(filepath, "w", encoding="utf-8") as outfile:
            outfile.write(f"#{title}\n\n{abstract_text}\n\n{intro_text}")

    
        
    
    




