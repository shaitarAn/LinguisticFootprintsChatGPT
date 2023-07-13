from pypdf import PdfReader
from pdfminer.converter import HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from io import BytesIO, StringIO

def convert_pdf_to_html(pdf_path):
    output_string = StringIO()
    with open(pdf_path, 'rb') as fp:
        resource_manager = PDFResourceManager()
        converter = HTMLConverter(resource_manager, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(resource_manager, converter)
        for page in PDFPage.get_pages(fp, check_extractable=True):
            interpreter.process_page(page)
        converter.close()

    html_content = output_string.getvalue()
    output_string.close()

    return html_content


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
    reader = PdfReader(filename)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def testrun(testfile, outfile, testfunc):
    content = testfunc(testfile)
    with open(outfile, "w", encoding="utf-8") as outfile:
        outfile.write(content)

testfile = "C:/Users/nik_b/Documents/UZH/student_assistant/Zora/data/linguistics_and_language/downloads/2006-3445b27b230257a81f9d6326373e94de9a00abfc.pdf"

testrun(testfile, "pdfminer_test3.txt", convert_pdf_to_txt)
testrun(testfile, "pdfminer_test3.html", convert_pdf_to_html)
testrun(testfile, "pypdf_test3.txt", pdfreader)

