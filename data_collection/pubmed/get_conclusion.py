from lxml import etree
import argparse
from tqdm import tqdm
import os



def extract_conclusion(infilepath, outfolder, n=500):
    """Takes an xml document from pubmed and saves the title and the conclusion in a txt in the specified outfolder.
    Only saves conclusion longer than n tokens (naive tokenization)
    """

    xml = etree.parse(infilepath)
    articles = xml.xpath("//article[//sec[title='Conclusion']]")
    for article in articles:
        text = ''.join(article.xpath(".//sec[title='Conclusion']//text()"))  # getting the conlcusion as string
        num_toks = len(text.split())
        if num_toks > n:
            title = article.xpath(".//title-group/article-title/text()")[0]
            pmid = article.xpath(".//article-id[@pub-id-type='pmid']/text()")[0]
            year = article.xpath(".//pub-date[1]/year/text()")[0]
            outfilepath = os.path.join(outfolder, f"{year}-{pmid}_{num_toks}_en.txt")
            with open(outfilepath, "w", encoding="utf-8") as outfile:
                outfile.write(f"{title}\n\n{text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infolder")
    parser.add_argument("outfolder")
    args = parser.parse_args()
    infolder = args.infolder
    outfolder = args.outfolder

    infilepaths = [os.path.join(infolder, filename) for filename in os.listdir(infolder)]
    inputs = [(infilepath, outfolder) for infilepath in infilepaths]
    for input in tqdm(inputs):
        extract_conclusion(input[0], input[1])

