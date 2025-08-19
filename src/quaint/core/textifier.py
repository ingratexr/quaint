from pdf2image import convert_from_path
import pytesseract
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal
from pathlib import Path
from enum import Enum
from typing import Optional

PDF_MAGIC_HEADER = b"%PDF-"
PAGE_BREAK_DELIMITER = "<PAGE_BREAK />"

class FileType(str, Enum):
    PDF = "PDF"
    TEXT = "Plain Text"
    UNSUPPORTED = "Unsupported"


class Textifier:
    """
    Extracts text from plain text or pdf input file.
    """
    supported_filetypes = [FileType.PDF, FileType.TEXT]

    def __init__(self, log=print):
        self.log = log


    def filetype(self, file: Path) -> FileType:
        """
        Given the path to a file, returns the FileType: PDF, TEXT, or UNSUPPORTED.

        :param file
        Path of file to extract.
        """
        # If it has the pdf magic header, assume it's a pdf
        with open(file, "rb") as f:
            header = f.read(5)
            if header == PDF_MAGIC_HEADER:
                return FileType.PDF
            
        # Otherwise try to get the plain text. If no worky, give up.
        try:
            with open(file, "r") as f:
                f.read(1)
                # if it reads without an exception, assume it's plain text
                return FileType.TEXT
        except UnicodeDecodeError:
            return FileType.UNSUPPORTED


    def extract_text(self, file: Path, filetype: Optional[FileType]=None, use_ocr: bool = False) -> Optional[str]:
        """
        Extracts and returns text from the input file.

        :param file
        Path of file to extract.

        :param filetype
        File's FileType. None by default; if None will be determined when run.

        :param use_ocr
        When true, use optical character recognition for PDFs instead of direct
        text extraction. False by default.
        """
        filetype = filetype if filetype else Textifier.filetype(file)
        if not filetype in self.supported_filetypes:
            self.log("Unsupported filetype. Cannot get text.")
            return None
        elif filetype == FileType.TEXT:
            # ocr flag could be present here, but would do nothing. Ignoring for now.
            return self.text_from_text(file)
        elif filetype == FileType.PDF:
            if use_ocr:
                return self.text_from_pdf_ocr(file)
            return self.text_from_pdf_extraction(file)


    def text_from_text(self, file: Path) -> str:
        """
        Return the text contents of a file.

        :param file
        Path of the file to read and return text from.
        """
        with open(file, "r") as f:
            return f.read()


    def text_from_pdf_ocr(self, file: Path, mark_page_breaks: bool=False, progress_fn=None) -> str:
        """
        Extracts and returns text from a PDF using optical character recognition.

        :param file
        Path of the PDF to read.

        :param mark_page_break
        If true, adds a string marking each page break. False by default.

        :param progress_fn
        Function repeatedly called with progress updates for OCR process.
        """
        self.log("Starting PDF conversion for OCR...")
        pages = convert_from_path(file)
        self.log("Conversion complete.\nStarting OCR...")
        total = len(pages)
        texts = []
        for idx, page in enumerate(pages):
            if progress_fn:
                progress_fn(f"\rConverting page {idx + 1}/{total}")
                if idx + 1 == total:
                    progress_fn("\n")
            texts.append(pytesseract.image_to_string(page))
        delimiter = f"\n\n{PAGE_BREAK_DELIMITER}\n\n" if mark_page_breaks else "\n\n"
        return delimiter.join(texts) 


    def text_from_pdf_extraction(self, file: Path, mark_page_breaks=False) -> str:
        """
        Extracts and returns text directly from pdf.

        :param file
        Path of the PDF to read.

        :param mark_page_break
        If true, adds a string marking each page break. False by default.
        """
        lines = []
        self.log("Starting extraction...")
        for page_layout in extract_pages(file):
            page_lines = []
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        if isinstance(text_line, LTTextLineHorizontal):
                            # Keep y-coordinate and text
                            page_lines.append((text_line.y0, text_line.get_text()))
            # Sort top-to-bottom (highest y0 first)
            page_lines.sort(reverse=True, key=lambda x: x[0])
            lines.extend([text for _, text in page_lines])
            if mark_page_breaks:
                lines.append(f"\n\n{PAGE_BREAK_DELIMITER}\n\n")

        full_text = "".join(lines)
        self.log("Extraction complete.")
        return full_text

