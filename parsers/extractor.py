"""Unified Resume Text Extraction Engine for Zecpath AI (Day 5).

Coordinates PDF, DOCX, and TXT document reading, applies automated cleaning,
normalizes sections/bullets, and saves structured extraction results.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import BinaryIO

from pydantic import BaseModel, Field

from parsers.cleaner import clean_resume_text
from parsers.readers import DOCXReader, PDFReader


class ExtractionResult(BaseModel):
    """Complete extraction result model containing raw text, cleaned text, and metadata."""

    file_name: str = Field(..., description="Source document file name")
    file_type: str = Field(..., description="Document type: PDF, DOCX, or TXT")
    raw_text: str = Field(..., description="Raw text directly extracted from reader")
    cleaned_text: str = Field(..., description="Sanitized, normalized AI-ready text")
    detected_sections: list[str] = Field(default_factory=list, description="List of recognized standard resume sections")
    word_count: int = Field(default=0, description="Word count of cleaned text")
    character_count: int = Field(default=0, description="Character count of cleaned text")
    lines_count: int = Field(default=0, description="Line count of cleaned text")
    reader_metadata: dict = Field(default_factory=dict, description="Metadata from the document container")
    cleaning_stats: dict = Field(default_factory=dict, description="Statistics from cleaning pipeline")
    extracted_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="ISO 8601 UTC timestamp of extraction"
    )


class ResumeExtractor:
    """Production extraction engine for candidate resumes (PDF, DOCX, TXT)."""

    def __init__(self) -> None:
        self.pdf_reader = PDFReader()
        self.docx_reader = DOCXReader()

    def extract_file(self, file_path: str | Path) -> ExtractionResult:
        """Extract and clean resume text from a file path."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Resume file not found: {path}")

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            raw_text, meta = self.pdf_reader.read(path)
            file_type = "PDF"
        elif suffix in [".docx", ".doc"]:
            raw_text, meta = self.docx_reader.read(path)
            file_type = "DOCX"
        elif suffix in [".txt", ".md"]:
            raw_text = path.read_text(encoding="utf-8")
            meta = {"format": "TXT", "source": path.name}
            file_type = "TXT"
        else:
            raise ValueError(f"Unsupported resume file format '{suffix}'. Supported: .pdf, .docx, .txt")

        # Run text cleaning and normalization pipeline
        cleaned_text, stats = clean_resume_text(raw_text)

        return ExtractionResult(
            file_name=path.name,
            file_type=file_type,
            raw_text=raw_text,
            cleaned_text=cleaned_text,
            detected_sections=stats.get("detected_sections", []),
            word_count=stats.get("word_count", 0),
            character_count=len(cleaned_text),
            lines_count=stats.get("lines_count", 0),
            reader_metadata=meta,
            cleaning_stats=stats,
        )

    def extract_stream(
        self,
        stream: BinaryIO,
        file_name: str,
        file_type: str | None = None
    ) -> ExtractionResult:
        """Extract and clean resume text from an in-memory binary stream."""
        ext = file_type or Path(file_name).suffix.lower()
        if not ext.startswith("."):
            ext = f".{ext.lower()}"

        if ext == ".pdf":
            raw_text, meta = self.pdf_reader.read(stream)
            doc_type = "PDF"
        elif ext in [".docx", ".doc"]:
            raw_text, meta = self.docx_reader.read(stream)
            doc_type = "DOCX"
        elif ext in [".txt", ".md"]:
            raw_text = stream.read().decode("utf-8")
            meta = {"format": "TXT", "source": file_name}
            doc_type = "TXT"
        else:
            raise ValueError(f"Unsupported file format '{ext}'")

        cleaned_text, stats = clean_resume_text(raw_text)

        return ExtractionResult(
            file_name=file_name,
            file_type=doc_type,
            raw_text=raw_text,
            cleaned_text=cleaned_text,
            detected_sections=stats.get("detected_sections", []),
            word_count=stats.get("word_count", 0),
            character_count=len(cleaned_text),
            lines_count=stats.get("lines_count", 0),
            reader_metadata=meta,
            cleaning_stats=stats,
        )

    def extract_and_save(
        self,
        file_path: str | Path,
        output_dir: str | Path | None = None,
    ) -> tuple[Path, Path, ExtractionResult]:
        """Extract resume text and persist clean outputs as .txt and structured metadata as .json.

        Returns:
            tuple[Path, Path, ExtractionResult]: (txt_path, json_path, extraction_result)
        """
        path = Path(file_path)
        out_dir = Path(output_dir) if output_dir else path.parent.parent / "extracted"
        out_dir.mkdir(parents=True, exist_ok=True)

        result = self.extract_file(path)

        # 1. Save normalized clean text (.txt)
        txt_path = out_dir / f"{path.stem}_cleaned.txt"
        txt_path.write_text(result.cleaned_text, encoding="utf-8")

        # 2. Save structured extraction metadata (.json)
        json_path = out_dir / f"{path.stem}_extracted.json"
        json_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")

        return txt_path, json_path, result
