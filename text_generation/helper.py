
import re
import os
import spacy
import json



def parse_filename(filename:str, date=True):
    """Parse the filename, return the year, title, num_tokens and lang"""

    match = re.match(r"(\d{4})?"  # the year?, year-month?-day?
                     r"[_-]?"  #  sometimes there is one file with a _ instead of a -
                     r"(.+?)"  # The title, 
                     r"_(\d+)(?:_\d+)?"  # the number of tokens
                     r"_(de|en)", filename)
    if not match:
        print("Problem with the filename:")
        print(filename)
        return None

    date = match.group(1)
    title = match.group(2)
    num_tokens = match.group(3)  # total number of tokens
    lang = match.group(4)
    return date, title, num_tokens, lang


class Tokenizer:
    def __init__(self, lang):
        self.lang = lang
        self.nlp = self.load_model()

    def load_model(self):
        if self.lang == "de":
            return spacy.load("de_core_news_sm")
        if self.lang == "en":
            return spacy.load("en_core_web_sm")

    def token_list(self, text):
        """returns a list of tokens, the tokens are strings"""
        doc = self.nlp.tokenizer(text)
        return [token.text for token in doc]

    def tokenize_text(self, text):
        '''
        This function tokenizes a text using spacy.
        :return length of the text and the tokenized text
        '''
        doc = self.nlp.tokenizer(text)
        return len([token.text for token in doc]), " ".join([token.text for token in doc])

    def split_text(self,text, n=100, stop_after=True):
        """Split text into 2 parts after n tokens
        makes sure, that we have full sentences
        @stop_after: bool, include the last sentence to have at minimum 100 tokens"""
        doc = self.nlp(text)
        sents = [sent for sent in doc.sents]
        count = 0
        for i, sent in enumerate(sents):
            if count < n:
                count += len(sent)
            else:
                # break the loop and return the text parts
                return " ".join(sent.text for sent in sents[:i]), " ".join(sent.text for sent in sents[i:])




