"""Document readers package for Zecpath AI resume extraction engine."""

from parsers.readers.base import BaseDocumentReader
from parsers.readers.docx_reader import DOCXReader
from parsers.readers.pdf_reader import PDFReader

__all__ = ["BaseDocumentReader", "DOCXReader", "PDFReader"]
