from pdf2image import convert_from_path
import pytesseract
import os

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
