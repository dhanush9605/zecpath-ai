"""Base document reader interface for Zecpath AI resume extraction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO


class BaseDocumentReader(ABC):
    """Abstract base class for document readers (PDF, DOCX, TXT)."""

    @abstractmethod
    def read(self, source: str | Path | BinaryIO) -> tuple[str, dict]:
        """Extract raw text and reader metadata from the document source.

        Args:
            source: File path (str or Path) or binary file stream.

        Returns:
            tuple[str, dict]: (extracted_raw_text, reader_metadata)
        """
        pass
