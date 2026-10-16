"""Export canonical JSON schemas for Resume (CandidateProfile) and Job Description (JobProfile).

Generates data/schemas/resume_schema.json and data/schemas/job_description_schema.json
from Pydantic v2 models.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure repository root is on sys.path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from parsers.models import CandidateProfile, JobProfile


def export_schemas() -> None:
    """Generate and persist standard JSON Schemas to data/schemas/."""
    schema_dir = Path(__file__).resolve().parent.parent / "data" / "schemas"
    schema_dir.mkdir(parents=True, exist_ok=True)

    # 1. Resume / Candidate Profile Schema
    resume_schema = CandidateProfile.model_json_schema()
    resume_schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    resume_schema["title"] = "ZecpathResumeSchema"
    resume_schema["description"] = (
        "Standardized AI-ready JSON schema for candidate profiles, resumes, and CV extraction."
    )

    resume_schema_path = schema_dir / "resume_schema.json"
    resume_schema_path.write_text(json.dumps(resume_schema, indent=2), encoding="utf-8")
    print(f"[OK] Exported: {resume_schema_path}")

    # 2. Job Description Schema
    job_schema = JobProfile.model_json_schema()
    job_schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    job_schema["title"] = "ZecpathJobDescriptionSchema"
    job_schema["description"] = (
        "Standardized AI-ready JSON schema for job descriptions, vacancy specifications, and matching criteria."
    )

    job_schema_path = schema_dir / "job_description_schema.json"
    job_schema_path.write_text(json.dumps(job_schema, indent=2), encoding="utf-8")
    print(f"[OK] Exported: {job_schema_path}")


if __name__ == "__main__":
    export_schemas()
