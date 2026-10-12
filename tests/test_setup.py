"""Setup and sanity tests for Zecpath AI repository environment (Day 3).

Verifies module discoverability, logging initialization, file-writing capabilities,
and core repository structural integrity without external network or database dependencies.
"""

from __future__ import annotations

import importlib
import logging
from pathlib import Path

from utils.logger import get_logger, setup_logger


def test_core_module_imports() -> None:
    """Verify that all planned architectural modules can be imported successfully."""
    expected_modules = [
        "parsers",
        "ats_engine",
        "screening_ai",
        "interview_ai",
        "scoring",
        "utils",
    ]

    for module_name in expected_modules:
        mod = importlib.import_module(module_name)
        assert mod is not None, f"Module '{module_name}' could not be loaded."
        assert hasattr(mod, "__file__"), f"Module '{module_name}' missing __file__ attribute."


def test_logger_setup_and_file_writing(tmp_path: Path) -> None:
    """Verify that setup_logger initializes properly and persists log messages to disk."""
    test_log_file = tmp_path / "test_run.log"
    logger_name = "test_setup_runner"

    logger = setup_logger(
        name=logger_name,
        log_file=test_log_file,
        level=logging.INFO,
        console=False,
    )

    assert logger is not None
    assert logger.level == logging.INFO

    test_message = "Initialization sanity check passed."
    logger.info(test_message)

    # Flush handlers to ensure file content is synced
    for handler in logger.handlers:
        handler.flush()

    assert test_log_file.exists(), "Log file was not created on disk."
    content = test_log_file.read_text(encoding="utf-8")
    assert test_message in content
    assert "INFO" in content
    assert logger_name in content


def test_logger_prevents_duplicate_handlers(tmp_path: Path) -> None:
    """Verify that re-invoking setup_logger on an existing logger does not add handlers."""
    logger_name = "test_duplicate_preventer"
    test_log_file = tmp_path / "test_dedup.log"

    logger_first = setup_logger(name=logger_name, log_file=test_log_file, console=True)
    initial_handler_count = len(logger_first.handlers)

    logger_second = setup_logger(name=logger_name, log_file=test_log_file, console=True)
    second_handler_count = len(logger_second.handlers)

    assert initial_handler_count == second_handler_count, "Duplicate handlers were added."


def test_logger_sensitive_data_redaction(tmp_path: Path) -> None:
    """Verify that credentials and candidate PII are redacted from log entries."""
    test_log_file = tmp_path / "test_redaction.log"
    logger_name = "test_security_redactor"

    logger = setup_logger(
        name=logger_name,
        log_file=test_log_file,
        level=logging.INFO,
        console=False,
    )

    leak_candidate_msg = "Candidate email is candidate.test@example.com with api_key=topsecret123"
    logger.info(leak_candidate_msg)

    for handler in logger.handlers:
        handler.flush()

    content = test_log_file.read_text(encoding="utf-8")
    assert "topsecret123" not in content, "API secret leaked into log file!"
    assert "candidate.test@example.com" not in content, "Candidate email leaked into log file!"
    assert "[REDACTED]" in content
    assert "[REDACTED_EMAIL]" in content


def test_get_logger_convenience_function() -> None:
    """Verify that get_logger returns an operable logger instance with default settings."""
    logger = get_logger("zecpath_convenience_test")
    assert logger is not None
    assert len(logger.handlers) > 0


def test_required_repository_structure() -> None:
    """Verify presence of all required root files and directories for Day 3."""
    repo_root = Path(__file__).resolve().parent.parent

    expected_files = [
        repo_root / ".gitignore",
        repo_root / ".env.example",
        repo_root / "requirements.txt",
        repo_root / "data" / ".gitkeep",
    ]

    for file_path in expected_files:
        assert file_path.exists(), f"Required project file '{file_path.name}' is missing."
