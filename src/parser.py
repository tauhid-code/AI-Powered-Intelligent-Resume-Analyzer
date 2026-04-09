"""
this file is responsible for extracting relevant information
from PDF resume files and converting it into a structured format that can be easily processed by the rest of the application.
supports both PyMuPDF and pdfplumber libraries for PDF parsing, allowing for flexibility in handling different types of PDF files.
"""

import os 
import logging 
from pathlib import Path 
from typing import Optional 


logger = logging.getLogger(__name__)
def extract_text_pymupdf(pdf_path: str) -> str:
    """
    Extract from a PDF file using PyMuPDF library.
    """

    try:
        import fitz
    except ImportError:
        raise ImportError("PyMuPDF library is not installed. Please install it using 'pip install PyMuPDF'.")
    
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"The file {pdf_path} does not exist.")
    
    full_text : list[str] = []
    
    with fitz.open(str(pdf_path)) as doc:
        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text("text")
            if page_text.strip():
                full_text.append(page_text)
            else:
                logger.warning(f"Page {page_num} of {pdf_path} is empty or contains only whitespace.")

    extracted = "\n".join(full_text).strip()

    if not extracted:
        raise ValueError(
            f"No text could be extracted from {pdf_path}'." 
            "The file may be empty or contain only non-text elements."
        )
    logger.info(f"Extracted text from {pdf_path} using PyMuPDF.")

    return extracted

def extracted_text_pdfplumber(pdf_path: str) -> str:

    """
    Extract text from a PDF file using pdfplumber library.
    """

    try:
        import pdfplumber 
    except ImportError:
        raise ImportError("pdfplumber library is not installed. Please install it using 'pip install pdfplumber'.")
    
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f" The file {pdf_path} does not exist.")
    
    full_text : list[str] = []

    with pdfplumber.open(str(pdf_path)) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text and page_text.strip():
                full_text.append(page_text)
            else:
                logger.warning(f"Page {page_num} of {pdf_path} is empty or contains only whitespace.")
    
    extracted = "\n".join(full_text).strip()

    if not extracted:
        raise ValueError(
            f"No text could be extracted from {pdf_path}." 
            "The file may be empty or contain only non-text elements."
        )
    logger.info(f"Extracted text from {pdf_path} using pdfplumber.")
    return extracted 


def parse_resume(pdf_path : str, preferred_parser: str = "pymupdf") -> str:
    """
    Main function to parse a resume PDF file and extract text using the preferred parser.
    """

    parsers = {
        "pymupdf" : extract_text_pymupdf,
        "pdfplumber" : extracted_text_pdfplumber
    }

    order = (
        ["pymupdf", "pdfplumber"]
        if preferred_parser == "pymupdf"
        else ["pdfplumber", "pymupdf"]
    )

    last_error: Optional[Exception] = None

    for parser_name in order:
        try:
            logger.info(f"Attempting to extract text from {pdf_path} using {parser_name}.")
            return parsers[parser_name](pdf_path)
        except (ImportError, FileNotFoundError, ValueError) as e:
            logger.warning(f"Failed to extract text from {pdf_path} using {parser_name}: {e}")

            last_error = e
        except FileNotFoundError:
            raise 
    raise RuntimeError(
        f"Failed to extract text from {pdf_path} using both parsers. Last error: {last_error}")

   