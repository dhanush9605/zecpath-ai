"""Supervisor Proof Runner for Day 6 - Job Description Parsing System.

Executes end-to-end parsing across all employer job descriptions:
1. Runs JobDescriptionParser on all documents in data/raw/job_descriptions/.
2. Persists structured JSON profiles conforming to schema into data/structured/job_descriptions/.
3. Validates each generated JSON against canonical draft 2020-12 schema.
4. Runs pytest test suite for Day 6 and captures test output.
5. Generates logs/day6_test_results.log audit report.
6. Prints a clean executive summary table for supervisor review.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

from jsonschema import Draft202012Validator

# Ensure repository root is on sys.path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from parsers import JobDescriptionParser


def run_day6_verification() -> bool:
    """Run full Day 6 JD parsing pipeline, automated tests, and produce proof logs."""
    raw_jds_dir = repo_root / "data" / "raw" / "job_descriptions"
    structured_jds_dir = repo_root / "data" / "structured" / "job_descriptions"
    schema_path = repo_root / "data" / "schemas" / "job_description_schema.json"
    logs_dir = repo_root / "logs"

    structured_jds_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / "day6_test_results.log"
    log_lines = []

    def log(msg: str = "") -> None:
        print(msg)
        log_lines.append(msg)

    log("=" * 96)
    log("       ZECPATH AI -- DAY 6 JOB DESCRIPTION PARSING SYSTEM PROOF RUNNER")
    log("=" * 96)
    log(f"Execution Timestamp: {datetime.now(UTC).isoformat()}")
    log(f"Environment: Python {sys.version.split()[0]} on {sys.platform}")
    log("-" * 96)

    # Load canonical schema
    if not schema_path.exists():
        log(f"[ERROR] Schema file missing: {schema_path}")
        return False

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    parser = JobDescriptionParser()
    raw_files = sorted(list(raw_jds_dir.glob("*.txt")))

    if not raw_files:
        log("[ERROR] No job description files found in data/raw/job_descriptions/.")
        return False

    log("\n" + "-" * 96)
    log(" PART 1: JOB DESCRIPTION PARSING, TAXONOMY RESOLUTION & SCHEMA VALIDATION")
    log("-" * 96)
    header = (
        f"{'Requisition File':<26} | "
        f"{'Role Type':<13} | "
        f"{'Seniority':<9} | "
        f"{'Min Exp':<7} | "
        f"{'Skills':<6} | "
        f"{'Salary Range (USD)':<21} | "
        f"{'Schema'}"
    )
    log(header)
    log("-" * 96)

    parsed_count = 0
    all_success = True

    for raw_file in raw_files:
        try:
            json_path, profile = parser.parse_and_save(raw_file, structured_jds_dir)
            parsed_count += 1

            # Validate against canonical schema
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            errors = list(validator.iter_errors(payload))
            schema_ok = len(errors) == 0

            if not schema_ok:
                all_success = False
                schema_status = f"[FAIL: {len(errors)} errs]"
            else:
                schema_status = "[VALID]"

            salary_str = (
                f"${int(profile.salary_range.min_amount):,} - ${int(profile.salary_range.max_amount):,}"
                if profile.salary_range
                else "Not Disclosed"
            )

            row = (
                f"{raw_file.name[:25]:<26} | "
                f"{profile.role_type.value:<13} | "
                f"{profile.seniority_level.value:<9} | "
                f"{profile.requirements.minimum_experience_years:>4.1f} yrs | "
                f"{len(profile.requirements.required_skills):>2} req | "
                f"{salary_str:<21} | "
                f"{schema_status}"
            )
            log(row)
        except Exception as e:
            all_success = False
            log(f"{raw_file.name[:25]:<26} | {'ERROR':<13} | {'-':<9} | {'-':<7} | {'-':<6} | {'-':<21} | [FAILED: {e}]")

    log("-" * 96)
    log(f"Total job descriptions processed: {parsed_count} / {len(raw_files)}")
    log(f"Structured output directory: {structured_jds_dir}")

    # Part 2: Execute automated test suite
    log("\n" + "-" * 96)
    log(" PART 2: AUTOMATED PYTEST SUITE EXECUTION (tests/test_jd_parser.py)")
    log("-" * 96)

    pytest_cmd = [sys.executable, "-m", "pytest", "tests/test_jd_parser.py", "-v"]
    res = subprocess.run(pytest_cmd, cwd=str(repo_root), capture_output=True, text=True)

    log(res.stdout.strip())
    if res.stderr:
        log(res.stderr.strip())

    tests_passed = (res.returncode == 0)

    log("\n" + "=" * 96)
    if all_success and tests_passed:
        log("[SUCCESS] DAY 6 VERIFICATION PASSED 100%!")
        log("1. JobDescriptionParser parsed all requisitions into typed Pydantic models.")
        log("2. Synonym and taxonomy engine resolved canonical skills, seniorities, and roles.")
        log("3. Experience thresholds, salary brackets, and education credentials successfully extracted.")
        log("4. 100% of generated structured JDs passed JSON Schema draft 2020-12 validation.")
        log(f"5. Audit log written to: {log_file}")
    else:
        log("[FAIL] Day 6 verification completed with errors.")
    log("=" * 96)

    # Persist log file
    log_file.write_text("\n".join(log_lines), encoding="utf-8")
    return all_success and tests_passed


if __name__ == "__main__":
    success = run_day6_verification()
    sys.exit(0 if success else 1)
