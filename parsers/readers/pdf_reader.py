"""PDF resume reader using pypdf for layout-aware text extraction (Day 5)."""

from __future__ import annotations

import io
from pathlib import Path
from typing import BinaryIO

from pypdf import PdfReader
from pypdf.errors import EmptyFileError, PdfReadError

from parsers.readers.base import BaseDocumentReader


class PDFReader(BaseDocumentReader):
    """Robust PDF document text reader with multi-page and layout support."""

    def read(self, source: str | Path | BinaryIO) -> tuple[str, dict]:
        """Extract text from a PDF file path or file-like binary stream.

        Returns:
            (raw_text, metadata_dict)
        """
        stream: BinaryIO
        close_stream = False
        source_name = "stream"

        if isinstance(source, (str, Path)):
            path = Path(source)
            if not path.exists():
                raise FileNotFoundError(f"PDF document not found: {path}")
            if path.stat().st_size == 0:
                raise EmptyFileError(f"PDF document is empty (0 bytes): {path}")
            stream = open(path, "rb")
            close_stream = True
            source_name = path.name
        elif isinstance(source, bytes):
            stream = io.BytesIO(source)
        else:
            stream = source

        try:
            reader = PdfReader(stream)

            if reader.is_encrypted:
                try:
                    # Attempt empty password decryption
                    reader.decrypt("")
                except Exception as dec_err:
                    raise PermissionError(f"PDF document is password protected: {dec_err}") from dec_err

            page_texts: list[str] = []
            page_count = len(reader.pages)

            for _page_idx, page in enumerate(reader.pages):
                try:
                    # Try layout-aware extraction first
                    text = page.extract_text(extraction_mode="layout")
                except Exception:
                    # Fallback to standard text extraction
                    text = page.extract_text() or ""

                if text:
                    page_texts.append(text)

            raw_text = "\n\n".join(page_texts)

            doc_info = {}
            if reader.metadata:
                for k, v in reader.metadata.items():
                    clean_k = k.lstrip("/")
                    if v and isinstance(v, str):
                        doc_info[clean_k] = v

            metadata = {
                "format": "PDF",
                "source": source_name,
                "page_count": page_count,
                "extracted_pages": len(page_texts),
                "pdf_metadata": doc_info,
            }

            return raw_text, metadata

        except PdfReadError as err:
            raise ValueError(f"Corrupted or invalid PDF structure: {err}") from err
        finally:
            if close_stream:
                stream.close()
