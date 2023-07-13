
'''Scraping Articles from Zora'''

from lxml import etree
import requests
from tqdm import tqdm
import re
import hashlib
import argparse
import os
    


def parse_html(uri, get_request=False):
    """get an lxml root element, either of the web, or from a downloaded html file
    returns the root of the html, if it can be accessed, None otherwise"""
    if get_request:
        response = requests.get(uri)
        if response.status_code == 200:
            html = response.content
        else:
            print(f"\n####\nHTTP Error: {response.status_code}\n while trying to open{uri}")
            return None

    else:
        with open(uri, "r", encoding="utf-8") as infile:
            html = infile.read()

    tree = etree.HTML(html).getroottree()
    return tree.getroot()


def download_pdf(url, filepath):
    """download a pdf from Zora
    returns 1 if download was successful, 0 otherwise"""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filepath, "wb") as outfile:
            outfile.write(response.content)
        return 1
    if response.status_code == 401:
        return 0
    else:
        print(f"\n#####\nDownload failed:")
        print(f"\nHTTP Error: {response.status_code}\n"
              f"{url}")
        return 0


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("scopus_page", type=str, help="Either a link, or filepath")
    parser.add_argument("dest_folder", type=str)
    parser.add_argument("--request", "-r", action="store_true", default=False, help="getting the scopus page from the web?")
    parser.add_argument("--exclude", "-e", type=list[str], help="File with a list of Journals to ignore")
    parser.add_argument("--skip", "-s", type=int, default=0, help="skip the first entries")
    args = parser.parse_args()

    if args.exclude:
        with open(args.exclude, "r", encoding="utf-8") as infile:
            exclude_list = [line for line in infile]
    else:
        exclude_list = []

    # create the destination folder
    if not os.path.exists(args.dest_folder):
        os.makedirs(args.dest_folder)
        os.makedirs(f"{args.dest_folder}/downloads")

    # get the scopus page
    scopus_root = parse_html(args.scopus_page, args.request)
    if scopus_root is None:
        print("Can't access Scopus Page")
        exit()
    # look for the article citations
    results = scopus_root.xpath("//div[@class='ep_view_page ep_view_page_view_scopussubjects']/p")
    download_count = 0
    exception_count = 0

    for result in tqdm(results[args.skip:]):
        citation = " ".join(result.xpath(".//text()"))
        # print(citation)
        for journal in exclude_list:  # skip if forbidden
            if journal in citation:
                exception_count += 1
                continue

        title = result.xpath(".//em/text()")[0]
        # result.xpath("./text()"): ['; ', ' (2023). ', ' European Journal of Operational Research, 309(1):252-270.']
        try:
            year = re.search(r"\((\d{4})\)", citation).group(1)
        except AttributeError:  # Somehow no year is matched in one case...
            continue


        download_page_link = result.xpath("./a[em]/@href")[0]
        download_page_root = parse_html(download_page_link, get_request=True)
        if download_page_root is None:  # skip this article if download failed
            continue

        try:
            download_link = download_page_root.xpath("//a[@title='Download PDF ']/@href")[0]
        except IndexError:
            continue

        hash = hashlib.sha1(citation.encode()).hexdigest()
        download_count += download_pdf(download_link, f"{args.dest_folder}/downloads/{year}-{hash}.pdf")
        with open(f"{args.dest_folder}/downloaded_papers.txt", "a", encoding="utf-8") as outfile:
            outfile.write(f"{citation}\n")

    print("total files: ", len(results))
    print("files from the forbidden jounals: ", exception_count)
    print("files downloaded: ", download_count)






    
    
        
        
    