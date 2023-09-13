import argparse
from lxml import etree
import os
from tqdm import tqdm
import json


def write_file(text, year, pmid, section_title, num_toks, title, outfolder):
    outfilepath = os.path.join(outfolder, f"{year}-{pmid}_{num_toks}_en.txt")
    with open(outfilepath, "w", encoding="utf-8") as outfile:
        outfile.write(f"{title}\n\n{section_title}\n{text}")


def get_section(outfolder, n, title, pmid, year):
    """get a section with more than n words from article
    Goes from the beginning, and takes the first section that is long enough
    Writes the files to disk and returns the section title"""


    # go through all sections and find one that is long enough, stop as soon as one is reached
    sections = article.xpath(".//sec")
    for section in sections:
        text = ''.join(section.xpath("./p//text()"))
        if len(text.split()) > n:
            try:
                section_title = section.xpath("./title/text()")[0].strip()
            except IndexError:
                continue
            num_toks = len(text.split())
            write_file(text, year, pmid, section_title, num_toks, title, outfolder)
            return section_title



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infolder", type=str, help="path to the folder with the xml files with batches of pubmed articles")
    parser.add_argument("outfolder", type=str, help="Folder to save the resulting txts")
    parser.add_argument("-n", type=int, default=500, help="how many words?")
    args = parser.parse_args()
    infolder = args.infolder
    outfolder = args.outfolder
    n = args.n

    section_title_dict = {}
    for infilepath in tqdm([os.path.join(infolder, filename) for filename in os.listdir(infolder)]):

        xml = etree.parse(infilepath)
        articles = xml.xpath("//article")
        for article in articles:
            # try to get article meta data
            try:
                title = article.xpath(".//title-group/article-title/text()")[0]
                pmid = article.xpath(".//article-id[@pub-id-type='pmid']/text()")[0]
                year = article.xpath(".//pub-date[1]/year/text()")[0]
            except IndexError:
                continue
            section_title = get_section(outfolder, n, title, pmid, year)

            # save section titles
            if section_title:
                if section_title in section_title_dict:
                    section_title_dict[section_title] += 1
                else:
                    section_title_dict[section_title] = 1


    with open("section_names.json", "w", encoding="utf-8") as outjson:
        json.dump(section_title_dict, outjson)

