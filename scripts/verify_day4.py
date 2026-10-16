"""Supervisor Proof Runner for Day 4 - Data Understanding & Structuring.

Executes end-to-end verification of all multi-domain resumes and job descriptions:
1. Validates instances against canonical JSON Schemas.
2. Deserializes through Pydantic AI entities.
3. Outputs a formatted executive summary table for supervisor review.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure repository root is on sys.path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from jsonschema import Draft202012Validator

from parsers.models import CandidateProfile, JobProfile


def run_verification() -> bool:
    """Run full schema and data verification and print report."""
    base_data = repo_root / "data"
    resume_schema_file = base_data / "schemas" / "resume_schema.json"
    jd_schema_file = base_data / "schemas" / "job_description_schema.json"
    resumes_dir = base_data / "structured" / "resumes"
    jds_dir = base_data / "structured" / "job_descriptions"

    print("=" * 88)
    print("           ZECPATH AI -- DAY 4 DATA STRUCTURING VERIFICATION RUNNER")
    print("=" * 88)

    # 1. Load Schemas
    try:
        resume_schema = json.loads(resume_schema_file.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(resume_schema)
        resume_val = Draft202012Validator(resume_schema)

        jd_schema = json.loads(jd_schema_file.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(jd_schema)
        jd_val = Draft202012Validator(jd_schema)
        print("[OK] Canonical JSON Schemas loaded and verified (Draft 2020-12).")
    except Exception as exc:
        print(f"[ERROR] Schema loading failed: {exc}")
        return False

    all_passed = True

    # 2. Verify 10 Resumes
    print("\n" + "-" * 88)
    print(" PART 1: 10 MULTI-DOMAIN CANDIDATE RESUMES VERIFICATION")
    print("-" * 88)
    header = f"{'Domain':<30} | {'Candidate Name':<20} | {'Skills':<8} | {'Exp (Yrs)':<9} | {'Status'}"
    print(header)
    print("-" * 88)

    resume_files = sorted(resumes_dir.glob("*.json"))
    for file_path in resume_files:
        try:
            raw_data = json.loads(file_path.read_text(encoding="utf-8"))
            # Validate JSON Schema
            schema_errors = list(resume_val.iter_errors(raw_data))
            if schema_errors:
                raise ValueError(f"Schema errors: {schema_errors[0].message}")

            # Validate Pydantic Entity
            profile = CandidateProfile.model_validate(raw_data)
            status = "[VALID]"
            row = (
                f"{profile.domain[:29]:<30} | "
                f"{profile.contact_info.full_name[:19]:<20} | "
                f"{len(profile.skills):<8} | "
                f"{profile.total_experience_years:<9.1f} | "
                f"{status}"
            )
            print(row)
        except Exception as err:
            all_passed = False
            print(f"{file_path.name:<30} | {'ERROR':<20} | {'-':<8} | {'-':<9} | [FAILED: {err}]")

    # 3. Verify Job Descriptions
    print("\n" + "-" * 88)
    print(" PART 2: TECHNICAL & NON-TECHNICAL JOB DESCRIPTIONS VERIFICATION")
    print("-" * 88)
    jd_header = f"{'Job Title':<34} | {'Role Type':<14} | {'Req Skills':<10} | {'Min Exp':<8} | {'Status'}"
    print(jd_header)
    print("-" * 88)

    jd_files = sorted(jds_dir.glob("*.json"))
    for file_path in jd_files:
        try:
            raw_data = json.loads(file_path.read_text(encoding="utf-8"))
            schema_errors = list(jd_val.iter_errors(raw_data))
            if schema_errors:
                raise ValueError(f"Schema errors: {schema_errors[0].message}")

            job = JobProfile.model_validate(raw_data)
            status = "[VALID]"
            row = (
                f"{job.title[:33]:<34} | "
                f"{job.role_type.value:<14} | "
                f"{len(job.requirements.required_skills):<10} | "
                f"{job.requirements.minimum_experience_years:<8.1f} | "
                f"{status}"
            )
            print(row)
        except Exception as err:
            all_passed = False
            print(f"{file_path.name:<34} | {'ERROR':<14} | {'-':<10} | {'-':<8} | [FAILED: {err}]")

    print("=" * 88)
    if all_passed:
        print("[SUCCESS] All 10 Resumes and 4 Job Descriptions passed 100% schema validation!")
        print("Ready for supervisor presentation and AI screening ingestion.")
    else:
        print("[FAIL] One or more data instances failed verification.")
    print("=" * 88)

    return all_passed


if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
