"""Parsers module for Zecpath AI.

Responsible for extracting structured information from candidate resumes,
CVs, portfolios, and job descriptions (PDF, DOCX, TXT formats).
"""

from parsers.cleaner import clean_resume_text
from parsers.extractor import ExtractionResult, ResumeExtractor
from parsers.jd_parser import JobDescriptionParser
from parsers.readers import DOCXReader, PDFReader

__version__ = "0.1.0"

__all__ = [
    "DOCXReader",
    "ExtractionResult",
    "JobDescriptionParser",
    "PDFReader",
    "ResumeExtractor",
    "clean_resume_text",
]
