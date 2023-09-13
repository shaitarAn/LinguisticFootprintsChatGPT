from lxml import etree
import argparse
from tqdm import tqdm
import os
from multiprocessing import Pool



def extract_conclusion(infilepath, outfolder, n=500):
    """Takes an xml document from pubmed and saves the title and the conclusion in a txt in the specified outfolder.
    Only saves conclusion longer than n tokens (naive tokenization)
    """

    xml = etree.parse(infilepath)
    articles = xml.xpath("//article[//sec[title='Conclusion']]")
    for article in articles:
        text = ''.join(article.xpath(".//sec[title='Conclusion']/p//text()"))  # getting the conlcusion as string
        try:
            title = article.xpath(".//title-group/article-title/text()")[0]
            pmid = article.xpath(".//article-id[@pub-id-type='pmid']/text()")[0]
            year = article.xpath(".//pub-date[1]/year/text()")[0]
        except IndexError:
            continue
        num_toks = len(text.split())
        if num_toks > n:

            outfilepath = os.path.join(outfolder, f"{year}-{pmid}_{num_toks}_en.txt")
            with open(outfilepath, "w", encoding="utf-8") as outfile:
                outfile.write(f"{title}\n\nConclusion\n{text}")

        else:  # if the conclusion is not long enough, go look for other sections
            sections = article.xpath(".//sec")
            for section in sections[1:]:  # all sections except the first one
                text = ''.join(section.xpath("./p//text()"))
                num_toks = len(text.split())
                if num_toks > n:
                    try:
                        section_title = section.xpath("./title/text()")[0]
                    except IndexError:
                        continue

                    outfilepath = os.path.join(outfolder, f"{year}-{pmid}_{num_toks}_en.txt")
                    with open(outfilepath, "w", encoding="utf-8") as outfile:
                        outfile.write(f"{title}\n\n{section_title}\n{text}")
                    break  # break inner loop, go to next article




def wrapper(args):
    """to make passing multiple arguments in pool possible
    lambda does not work"""
    return extract_conclusion(*args)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infolder")
    parser.add_argument("outfolder")
    args = parser.parse_args()
    infolder = args.infolder
    outfolder = args.outfolder

    infilepaths = [os.path.join(infolder, filename) for filename in os.listdir(infolder)]
    inputs = [(infilepath, outfolder) for infilepath in infilepaths]
    with Pool(processes=8) as pool:
        results = pool.imap_unordered(wrapper, inputs)
        for _ in tqdm(results, total=len(inputs)):
            pass
    # for input in tqdm(inputs):
    #     extract_conclusion(input[0], input[1])
    #     break

