"""Automated test suite for Day 5 - Resume Text Extraction Engine.

Tests PDF, DOCX, and TXT readers, unicode cleaning, bullet normalization,
heading detection, whitespace cleanup, and end-to-end extraction persistence.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from parsers import (
    DOCXReader,
    PDFReader,
    ResumeExtractor,
    clean_resume_text,
)
from parsers.cleaner import (
    clean_whitespace,
    fix_hyphenated_line_breaks,
    normalize_bullets,
    normalize_section_headings,
    normalize_unicode,
    remove_unprintable_artifacts,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_RESUMES_DIR = REPO_ROOT / "data" / "raw" / "resumes"
SAMPLE_DOCX = RAW_RESUMES_DIR / "resume_01_backend.docx"
SAMPLE_PDF = RAW_RESUMES_DIR / "resume_02_frontend.pdf"


def test_pdf_reader_extracts_text_and_metadata() -> None:
    """Verify PDFReader extracts text and page metadata from a real PDF file."""
    assert SAMPLE_PDF.exists(), f"Sample PDF missing: {SAMPLE_PDF}"
    reader = PDFReader()
    text, meta = reader.read(SAMPLE_PDF)

    assert len(text) > 50
    assert "PRIYA SHARMA" in text
    assert meta["format"] == "PDF"
    assert meta["page_count"] >= 1


def test_docx_reader_extracts_paragraphs_and_tables() -> None:
    """Verify DOCXReader extracts paragraphs and embedded table rows."""
    assert SAMPLE_DOCX.exists(), f"Sample DOCX missing: {SAMPLE_DOCX}"
    reader = DOCXReader()
    text, meta = reader.read(SAMPLE_DOCX)

    assert len(text) > 50
    assert "ALEX CHEN" in text
    assert "Go, Python, SQL" in text  # Extracted from table cell
    assert meta["format"] == "DOCX"
    assert meta["table_count"] >= 1


def test_unicode_and_ligature_normalization() -> None:
    """Verify ligatures and typographic quotes/dashes are normalized to standard ASCII equivalents."""
    messy_text = "Experienced in \ufb01ntech and \ufb02ow design with \u201csmart\u201d quotes \u2014 and dashes."
    cleaned = normalize_unicode(messy_text)

    assert "fintech" in cleaned
    assert "flow" in cleaned
    assert '"smart"' in cleaned
    assert " - " in cleaned


def test_remove_unprintable_artifacts() -> None:
    """Verify non-printable control characters are removed while preserving newlines."""
    dirty_text = "Hello\x00\x08World\x0b!\nLine 2\x1f."
    cleaned = remove_unprintable_artifacts(dirty_text)

    assert cleaned == "HelloWorld!\nLine 2."


def test_fix_hyphenated_line_breaks() -> None:
    """Verify words split across line breaks by hyphens are rejoined correctly."""
    split_text = "Designed high-throughput distri-\nbuted micro-\nservices."
    fixed = fix_hyphenated_line_breaks(split_text)

    assert "distributed" in fixed
    assert "microservices" in fixed


def test_bullet_normalization() -> None:
    """Verify diverse bullet symbols are standardized to a canonical bullet marker ('• ')."""
    multi_bullet_text = """
- First bullet item
* Second bullet item
▪ Third bullet item
► Fourth bullet item
o Fifth bullet item
"""
    normalized = normalize_bullets(multi_bullet_text)
    lines = [line.strip() for line in normalized.strip().splitlines()]

    for line in lines:
        assert line.startswith("• "), f"Line failed bullet normalization: '{line}'"


def test_section_heading_normalization() -> None:
    """Verify informal section headings are detected and mapped to uppercase canonical headers."""
    resume_with_headings = """
John Doe
Software Engineer

== Summary ==
Passionate backend engineer.

Work Experience:
Lead developer at TechCorp.

Key Skills:
Python, Docker, SQL.

Academic Background:
B.S. in Computer Science.
"""
    transformed, detected = normalize_section_headings(resume_with_headings)

    assert "PROFESSIONAL SUMMARY" in detected
    assert "WORK EXPERIENCE" in detected
    assert "TECHNICAL SKILLS" in detected
    assert "EDUCATION" in detected
    assert "PROFESSIONAL SUMMARY" in transformed


def test_clean_whitespace() -> None:
    """Verify multi-spaces, trailing spaces, and excessive blank lines are cleaned."""
    spaced_text = "Name:   Jane Doe    \n\n\n\nRole:   Engineer    "
    cleaned = clean_whitespace(spaced_text)

    assert "Jane Doe" in cleaned
    assert "\n\n\n" not in cleaned
    assert cleaned == "Name:  Jane Doe\n\nRole:  Engineer"


def test_full_cleaning_pipeline_statistics() -> None:
    """Verify clean_resume_text returns clean text and accurate extraction statistics."""
    sample_text = """
Dr. Alan Turing
Summary
• Father of theoretical computer science.
Skills:
- Cryptanalysis, Logic, Algorithms.
"""
    cleaned, stats = clean_resume_text(sample_text)

    assert len(cleaned) > 0
    assert stats["word_count"] > 5
    assert len(stats["detected_sections"]) >= 2
    assert "PROFESSIONAL SUMMARY" in stats["detected_sections"]
    assert "TECHNICAL SKILLS" in stats["detected_sections"]


def test_resume_extractor_end_to_end_on_pdf() -> None:
    """Verify ResumeExtractor on PDF returns complete ExtractionResult."""
    extractor = ResumeExtractor()
    result = extractor.extract_file(SAMPLE_PDF)

    assert result.file_name == SAMPLE_PDF.name
    assert result.file_type == "PDF"
    assert len(result.cleaned_text) > 0
    assert result.word_count > 20
    assert "PRIYA SHARMA" in result.cleaned_text
    assert len(result.detected_sections) >= 3


def test_resume_extractor_extract_and_save(tmp_path: Path) -> None:
    """Verify extract_and_save writes both .txt and .json files to destination directory."""
    extractor = ResumeExtractor()
    txt_path, json_path, result = extractor.extract_and_save(SAMPLE_DOCX, output_dir=tmp_path)

    assert txt_path.exists()
    assert json_path.exists()
    assert txt_path.suffix == ".txt"
    assert json_path.suffix == ".json"

    # Verify content was saved
    saved_text = txt_path.read_text(encoding="utf-8")
    assert "ALEX CHEN" in saved_text
    assert result.word_count > 50


def test_extractor_rejects_missing_and_invalid_files(tmp_path: Path) -> None:
    """Verify extractor raises proper exceptions on missing or unsupported files."""
    extractor = ResumeExtractor()

    # 1. Missing file
    with pytest.raises(FileNotFoundError):
        extractor.extract_file(tmp_path / "non_existent.pdf")

    # 2. Unsupported extension
    invalid_file = tmp_path / "resume.xyz"
    invalid_file.write_text("Hello World", encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported resume file format"):
        extractor.extract_file(invalid_file)
