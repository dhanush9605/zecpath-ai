"""Reusable logging utility for Zecpath AI.

Provides structured console and file logging with automatic directory creation,
duplicate handler prevention, and sensitive data redaction to protect candidate PII
and application credentials.
"""

from __future__ import annotations

import logging
import re
import sys
from pathlib import Path

# Common patterns for sensitive information (tokens, keys, passwords, emails, phones)
_SENSITIVE_PATTERNS = [
    (
        re.compile(
            r"(?i)(password|passwd|secret|token|api[_-]?key|auth)\s*[:=]\s*['\"]?([^\s'\"]+)"
        ),
        r"\1=[REDACTED]",
    ),
    (
        re.compile(r"(?i)(bearer\s+)[a-zA-Z0-9_\-\.]+"),
        r"\1[REDACTED]",
    ),
    (
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"),
        r"[REDACTED_EMAIL]",
    ),
    (
        re.compile(r"\b\+?[0-9]{1,3}?[-.\s]?\(?[0-9]{2,4}\)?[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}\b"),
        r"[REDACTED_PHONE]",
    ),
]

DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_DIR = Path("logs")
DEFAULT_LOG_FILE = DEFAULT_LOG_DIR / "zecpath.log"


class SensitiveDataFilter(logging.Filter):
    """Filter that redacts passwords, tokens, API keys, and candidate PII from log messages."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            message = record.msg
            for pattern, replacement in _SENSITIVE_PATTERNS:
                message = pattern.sub(replacement, message)
            record.msg = message
        return True


def setup_logger(
    name: str = "zecpath",
    log_file: str | Path | None = DEFAULT_LOG_FILE,
    level: int | str = logging.INFO,
    console: bool = True,
) -> logging.Logger:
    """Configure and return a logger with console and/or file handlers.

    Parameters:
        name: Name of the logger, typically __name__ or service name.
        log_file: Path to destination log file. Set to None to disable file logging.
        level: Logging level (e.g., logging.INFO, logging.DEBUG, or 'INFO').
        console: Whether to attach stdout console logging handler.

    Returns:
        Configured logging.Logger instance.

    Raises:
        ValueError: If an invalid logging level is provided.
        OSError: If the log directory cannot be created.
    """
    logger = logging.getLogger(name)

    # Resolve log level if string is passed
    if isinstance(level, str):
        level_str = level.upper()
        if not hasattr(logging, level_str):
            raise ValueError(
                f"Invalid logging level: '{level}'. Expected DEBUG, INFO, WARNING, ERROR, CRITICAL."
            )
        numeric_level = getattr(logging, level_str)
    else:
        numeric_level = level

    logger.setLevel(numeric_level)

    # Avoid duplicate handlers if logger was previously initialized
    if logger.handlers:
        return logger

    formatter = logging.Formatter(fmt=DEFAULT_LOG_FORMAT, datefmt=DEFAULT_DATE_FORMAT)
    redaction_filter = SensitiveDataFilter()

    # 1. Console Handler (stdout)
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(redaction_filter)
        logger.addHandler(console_handler)

    # 2. File Handler
    if log_file is not None:
        file_path = Path(log_file)
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise OSError(f"Failed to create log directory '{file_path.parent}': {exc}") from exc

        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(redaction_filter)
        logger.addHandler(file_handler)

    # Prevent propagation to root logger to avoid duplicate console entries
    logger.propagate = False

    return logger


def get_logger(name: str = "zecpath") -> logging.Logger:
    """Retrieve an existing logger or create one with default settings if uninitialized.

    Parameters:
        name: Name of the logger (recommended to pass __name__ in modules).

    Returns:
        logging.Logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name=name)
    return logger
