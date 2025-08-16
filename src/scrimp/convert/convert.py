from pdf2image import convert_from_path
import pytesseract
import os

PDF_MAGIC_HEADER = b"%PDF-"
PAGE_BREAK_STR = "<PAGE_BREAK />"

def pdf_to_text_ocr(filepath: str, discard_page_breaks: bool = False) -> str:
    """
    Takes the filepath to a pdf and returns an OCR scan of the pdf as a string.

    :param filepath
    Full path to the pdf.

    :param discard_page_breaks
    When true, pages from the original pdf will be joined with "\\n\\n". When 
    false, they'll be joined with the constant PAGE_BREAK_STR defined in this
    file. False by default.
    """
    if not os.path.isfile(filepath):
        raise Exception(f"{filepath} is not a file")
    pages = convert_from_path(filepath)
    texts = [pytesseract.image_to_string(page) for page in pages]
    delimiter = "\n\n" if discard_page_breaks else f"\n\n{PAGE_BREAK_STR}\n\n"
    return delimiter.join(texts)


def get_from_pdf(filepath: str) -> str:
    """
    Placeholder - in the future extract text where possible; for now use ocr for
    everything.
    """
    return pdf_to_text_ocr(filepath)


def file_to_text(filepath: str) -> str:
    """
    Takes the path to a file and returns the contents of the file as plain text
    if the file is supported (currently plain text filetypes or pdf). 
    """
    if not os.path.isfile(filepath):
        raise Exception(f"{filepath} is not a file")
    # If it has the pdf magic header, assume it's a pdf
    with open(filepath, "rb") as f:
        header = f.read(5)
        if header == PDF_MAGIC_HEADER:
            return get_from_pdf(filepath)
    
    # Otherwise try to get the plain text. If no worky, give up.
    try:
        with open(filepath, "r") as f:
            return f.read()
    except:
        raise Exception(f"Does not compute! Could not decode {os.path.abspath(filepath)} as pdf or plain text.")

