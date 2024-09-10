import argparse
from tqdm import tqdm
from Bio import Entrez
import time
import os

Entrez.email = "hailyyeugng1997@gmail.com"

class BatchIterator:
    def __init__(self, lst, batch_size=100):
        self.lst = lst
        self.index = 0
        self.batch_size = batch_size
        self.total = int(len(self.lst) / 100) + 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.lst):
            raise StopIteration

        end_index = min(self.index + self.batch_size, len(self.lst))
        elements = self.lst[self.index:end_index]
        self.index = end_index

        return elements


def write_articles(infile_name, out_folder, batch_size=100):
    """
    @infile: file with the pcmids
    @batch_size: amount of articles per file to write
    @out_folder: folder to write in"""

    with open(infile_name, "r", encoding="utf-8") as infile:
        pcmids = [line.strip() for line in infile.readlines()]

    batch_pcmids = BatchIterator(pcmids, batch_size)

    for i, batch in tqdm(enumerate(batch_pcmids), total=batch_pcmids.total):
        xml_str = download_articles(batch)
        file_path = f"{out_folder}/batch{i + 1}.xml"

        with open(file_path, "w", encoding="utf-8") as outfile:
            outfile.write(xml_str)

        time.sleep(1)


def download_articles(pmcids):
    handle = Entrez.efetch(db='pmc', id=pmcids, retmode='xml')
    results = handle.read()
    handle.close()
    return results.decode()
    # with open(outfile_name, "w", encoding="utf-8") as outfile:
    #     outfile.write(results.decode())


def get_pcmids(source, dest):
    """Getting the pcmids for the articles
    The search from pubmed only returned the pmids, but to retrieve the full text we need the pcmids
    @source: text file with the pmids on every line
    @dest: text file to save the pcmids
    @returns: None, the ids are saved in a file"""

    with open(source, "r", encoding="utf-8") as infile:
        pmids = [line.strip() for line in infile.readlines()]
    batch_pmids = BatchIterator(pmids)
    for batch in tqdm(batch_pmids, total=len(pmids) / 100):
        try:
            handle = Entrez.esummary(db="pubmed", id=batch, retmode="xml")
            records = Entrez.read(handle)
            for record in records:
                print(record)
                try:
                    pmcid = record["ArticleIds"]["pmc"]
                except KeyError:
                    continue
                with open(dest, "a", encoding="utf-8") as outfile:
                    outfile.write(f"{pmcid}\n")
                    # to not overload the api...
            time.sleep(1)
        
        except Exception as e:
            print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["get_pcmids", "write_articles"])
    parser.add_argument("infile", type=str)
    parser.add_argument("outfile", type=str, help="put a filepath for results from get_pcmids"
                                                  "put a folderpath for the results from write_articles")

    args = parser.parse_args()
    infilepath = args.infile
    outfilepath = args.outfile
    if args.mode == "get_pcmids":
        get_pcmids(infilepath, outfilepath)
    else:
        write_articles(infilepath, outfilepath)

    # get_pcmids("pmid-EnglishLan-set.txt", "pmcid-EnglishLan-set.txt")

    # write_articles("pcmid-EnglishLan-set.txt", "en/xml-files")

    # output = download_articles(["PMC9646605", "PMC9559163"])
    # print(output)
# handle = Entrez.efetch(db='pubmed', id=33766997, rettype="medline", retmode="text")