import argparse
import os
import sys

from tqdm import tqdm
from multiprocessing import Pool

from pypdf import PdfReader
from pdfminer.converter import HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from io import BytesIO, StringIO
from langdetect import detect as detect_lang
import shutil


def file_path(string):
    """Check if string is a valid filepath"""
    if os.path.exists(string):
        return string
    else:
        raise NotADirectoryError


def create_directory(outfolder):
    """Create a new directory, or if it exists, chech if it is empty"""
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    elif len(os.listdir(outfolder)) > 0:
        answer = input("Outfolder is not empty, continue anyway? (y/n): ")
        if answer.lower() == "n" or answer == "":
            exit()
        elif answer.lower() == "y":
            return
        else:
            print("invalid input")
            exit()


def convert_pdf_to_txt(pdf_path):
    output_string = StringIO()
    with open(pdf_path, 'rb') as fp:
        resource_manager = PDFResourceManager()
        converter = TextConverter(resource_manager, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(resource_manager, converter)
        for page in PDFPage.get_pages(fp, check_extractable=True):
            interpreter.process_page(page)
        converter.close()

    content = output_string.getvalue()
    output_string.close()

    return content


def pdfreader(filename):
    """using pyPDF to get the text from a pdf"""
    reader = PdfReader(filename)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def get_language(filename):
    """detect the language of a pdf file"""
    text = pdfreader(filename)
    return detect_lang(text)


def get_language_overview(folder):
    """get"""
    files = [os.path.join(folder, file) for file in os.listdir(folder)]
    lang_dict = {}

    with Pool(processes=8) as pool:
        results_iter = pool.imap_unordered(get_language, files)
        for lang in tqdm(results_iter, total=len(files)):
            if lang in lang_dict:
                lang_dict[lang] += 1
            else:
                lang_dict[lang] = 1

    return lang_dict


def sort_lang(infilepath, outfolder):
    lang = get_language(infilepath)
    if not os.path.exists(os.path.join(outfolder, lang)):
        os.makedirs(os.path.join(outfolder, lang))
    shutil.copy(infilepath, os.path.join(outfolder, lang))


def extract(filepath):
    """Extract the txts
    returns: new filename (with .txt extension) and the extracted text"""

    filename = os.path.basename(filepath)
    text = convert_pdf_to_txt(filepath)
    new_filename = filename.split(".")[0] +".txt"
    return new_filename, text


def testrun(testfile, outfile, testfunc):
    """for testing different methods to convert pdfs"""
    content = testfunc(testfile)
    with open(outfile, "w", encoding="utf-8") as outfile:
        outfile.write(content)


def test(filepath):
    """calling the testrun"""
    testfile = "C:/Users/nik_b/Documents/UZH/student_assistant/Zora/data/General_Material_Science/downloads/2015-baa629d43439df500116bed7b6a2a92e18c34b91.pdf"

    testrun(filepath, "2015-baa629d43439df500116bed7b6a2a92e18c34b91.txt", pdfreader)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, choices=["lang_overview", "extract", "sort_langs", "extract_one"],
                        help="lang_overview gives back a dictionary of how often which language appears,"
                             "extract creates txt files,"
                             "sort_langs sorts the pdfs into directories for each language")
    parser.add_argument("--infolder", type=file_path, required="extract_one" not in sys.argv)
    parser.add_argument("--outfolder", "-o", type=str, required="extract" in sys.argv or "sort_langs" in sys.argv)
    parser.add_argument("--infile", type=file_path, required="extract_one" in sys.argv)
    parser.add_argument("--outfile", type=str, required="extract_one" in sys.argv)
    parser.add_argument("--parser", type=str, choices=["convert_txt_to_pdf", "pdfreader"], required="extract_one" in sys.argv,
                        help="Use 'convert_txt_to_pdf' to use pdf-miner"
                             "Use 'pdfreader' to use pypdf")
    args = parser.parse_args()

    infolder = args.infolder
    mode = args.mode
    outfolder = args.outfolder

    if mode == "lang_overview":
        print(get_language_overview(args.infolder))


    elif mode == "extract":
        create_directory(outfolder)
        filepaths = [os.path.join(infolder, filename) for filename in os.listdir(infolder)]
        with Pool(processes=8) as pool:
            results = pool.imap_unordered(extract, filepaths)
            for new_filename, text in tqdm(results, total=len(filepaths)):
                with open(os.path.join(outfolder, new_filename), "w", encoding="utf-8") as outfile:
                    outfile.write(text)


    elif mode == "sort_langs":
        create_directory(outfolder)
        filepaths = [os.path.join(infolder, filename) for filename in os.listdir(infolder)]

        for filepath in tqdm(filepaths):
            sort_lang(filepath, outfolder)

    elif mode == "extract_one":
        # redo files, that did not get extracted by the script
        testrun(args.infile, args.outfile, args.parser)



