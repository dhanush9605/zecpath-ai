"""Supervisor Proof Runner for Day 5 - Resume Text Extraction Engine.

Executes end-to-end extraction across all candidate resumes (PDF, DOCX, TXT):
1. Runs ResumeExtractor on all documents in data/raw/resumes/.
2. Saves cleaned text and structured metadata into data/extracted/.
3. Runs pytest test suite and captures detailed output.
4. Generates logs/day5_test_results.log audit report.
5. Prints a clean executive summary table for supervisor review.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

# Ensure repository root is on sys.path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from parsers import ResumeExtractor


def run_day5_verification() -> bool:
    """Run full Day 5 extraction pipeline, automated tests, and produce proof logs."""
    raw_resumes_dir = repo_root / "data" / "raw" / "resumes"
    extracted_dir = repo_root / "data" / "extracted"
    logs_dir = repo_root / "logs"

    extracted_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / "day5_test_results.log"
    log_lines = []

    def log(msg: str = "") -> None:
        print(msg)
        log_lines.append(msg)

    log("=" * 88)
    log("       ZECPATH AI -- DAY 5 RESUME TEXT EXTRACTION ENGINE PROOF RUNNER")
    log("=" * 88)
    log(f"Execution Timestamp: {datetime.now(UTC).isoformat()}")
    log(f"Environment: Python {sys.version.split()[0]} on {sys.platform}")
    log("-" * 88)

    extractor = ResumeExtractor()
    doc_files = sorted(
        list(raw_resumes_dir.glob("*.pdf")) +
        list(raw_resumes_dir.glob("*.docx")) +
        list(raw_resumes_dir.glob("*.txt"))
    )

    if not doc_files:
        log("[ERROR] No resume files found in data/raw/resumes/.")
        return False

    log("\n" + "-" * 88)
    log(" PART 1: MULTI-FORMAT RESUME TEXT EXTRACTION & NORMALIZATION")
    log("-" * 88)
    header = f"{'Document Name':<28} | {'Type':<6} | {'Words':<7} | {'Lines':<6} | {'Sections':<10} | {'Status'}"
    log(header)
    log("-" * 88)

    extracted_count = 0
    all_success = True

    for doc_path in doc_files:
        try:
            txt_path, json_path, result = extractor.extract_and_save(doc_path, extracted_dir)
            extracted_count += 1
            sec_count = len(result.detected_sections)
            sec_str = f"{sec_count} detected"
            row = (
                f"{doc_path.name[:27]:<28} | "
                f"{result.file_type:<6} | "
                f"{result.word_count:<7} | "
                f"{result.lines_count:<6} | "
                f"{sec_str:<10} | "
                f"[SUCCESS]"
            )
            log(row)
        except Exception as e:
            all_success = False
            log(f"{doc_path.name[:27]:<28} | {'ERR':<6} | {'-':<7} | {'-':<6} | {'-':<10} | [FAILED: {e}]")

    log("-" * 88)
    log(f"Total documents processed: {extracted_count} / {len(doc_files)}")
    log(f"Cleaned text output directory: {extracted_dir}")

    # Part 2: Execute automated test suite
    log("\n" + "-" * 88)
    log(" PART 2: AUTOMATED PYTEST SUITE EXECUTION")
    log("-" * 88)

    pytest_cmd = [sys.executable, "-m", "pytest", "tests/test_extraction_engine.py", "-v"]
    res = subprocess.run(pytest_cmd, cwd=str(repo_root), capture_output=True, text=True)

    log(res.stdout.strip())
    if res.stderr:
        log(res.stderr.strip())

    tests_passed = (res.returncode == 0)

    log("\n" + "=" * 88)
    if all_success and tests_passed:
        log("[SUCCESS] DAY 5 VERIFICATION PASSED 100%!")
        log("1. Multi-format readers (PDF, DOCX, TXT) extracted with full table & layout support.")
        log("2. Cleaning pipeline normalized unicode, ligatures, bullet points, and section headings.")
        log("3. Cleaned text and extraction metadata persisted to data/extracted/.")
        log(f"4. Audit log written to: {log_file}")
    else:
        log("[FAIL] Verification completed with errors.")
    log("=" * 88)

    # Persist log file
    log_file.write_text("\n".join(log_lines), encoding="utf-8")
    return all_success and tests_passed


if __name__ == "__main__":
    success = run_day5_verification()
    sys.exit(0 if success else 1)
