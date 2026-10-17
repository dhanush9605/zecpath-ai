"""DOCX resume reader using python-docx with paragraph and table extraction (Day 5)."""

from __future__ import annotations

import io
from pathlib import Path
from typing import BinaryIO

import docx
from docx.opc.exceptions import PackageNotFoundError

from parsers.readers.base import BaseDocumentReader


class DOCXReader(BaseDocumentReader):
    """Robust DOCX document reader extracting flowing paragraphs and embedded tables."""

    def read(self, source: str | Path | BinaryIO) -> tuple[str, dict]:
        """Extract text from a DOCX file path or file-like binary stream.

        Returns:
            (raw_text, metadata_dict)
        """
        source_name = "stream"
        doc_stream: str | Path | BinaryIO

        if isinstance(source, (str, Path)):
            path = Path(source)
            if not path.exists():
                raise FileNotFoundError(f"DOCX document not found: {path}")
            if path.stat().st_size == 0:
                raise ValueError(f"DOCX document is empty (0 bytes): {path}")
            source_name = path.name
            doc_stream = str(path)
        elif isinstance(source, bytes):
            doc_stream = io.BytesIO(source)
        else:
            doc_stream = source

        try:
            document = docx.Document(doc_stream)

            extracted_blocks: list[str] = []
            para_count = 0
            table_count = 0

            # 1. Extract paragraphs
            for para in document.paragraphs:
                text = para.text.strip()
                if text:
                    para_count += 1
                    # Preserve heading context
                    if para.style and para.style.name and "Heading" in para.style.name:
                        extracted_blocks.append(f"\n{text}\n")
                    else:
                        extracted_blocks.append(text)

            # 2. Extract tables (resumes often format skills/experience in tables)
            for table in document.tables:
                table_count += 1
                table_rows: list[str] = []
                for row in table.rows:
                    cell_texts = [cell.text.strip().replace("\n", " ") for cell in row.cells]
                    # Filter empty duplicate merged cells
                    filtered = [c for c in cell_texts if c]
                    if filtered:
                        table_rows.append(" | ".join(filtered))

                if table_rows:
                    extracted_blocks.append("\n[TABLE]")
                    extracted_blocks.extend(table_rows)
                    extracted_blocks.append("[/TABLE]\n")

            raw_text = "\n".join(extracted_blocks)

            # Core document properties
            doc_info = {}
            if document.core_properties:
                props = document.core_properties
                if props.title:
                    doc_info["title"] = props.title
                if props.author:
                    doc_info["author"] = props.author
                if props.created:
                    doc_info["created"] = str(props.created)

            metadata = {
                "format": "DOCX",
                "source": source_name,
                "paragraph_count": para_count,
                "table_count": table_count,
                "docx_metadata": doc_info,
            }

            return raw_text, metadata

        except PackageNotFoundError as err:
            raise ValueError(f"Corrupted or invalid DOCX file: {err}") from err
