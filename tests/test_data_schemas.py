"""Test suite for Day 4 - Data Understanding & Structuring.

Validates that all sample resumes and job descriptions conform strictly to:
1. Standard JSON Schema definitions (data/schemas/*.json).
2. Pydantic AI data models (CandidateProfile, JobProfile, SkillObject, ExperienceObject).
3. Edge case constraints and validation rules.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from parsers.models import (
    CandidateProfile,
    ContactInfo,
    ExperienceObject,
    JobProfile,
    RoleType,
    SkillObject,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
RESUME_SCHEMA_PATH = REPO_ROOT / "data" / "schemas" / "resume_schema.json"
JD_SCHEMA_PATH = REPO_ROOT / "data" / "schemas" / "job_description_schema.json"
STRUCTURED_RESUMES_DIR = REPO_ROOT / "data" / "structured" / "resumes"
STRUCTURED_JDS_DIR = REPO_ROOT / "data" / "structured" / "job_descriptions"
RAW_RESUMES_DIR = REPO_ROOT / "data" / "raw" / "resumes"
RAW_JDS_DIR = REPO_ROOT / "data" / "raw" / "job_descriptions"


@pytest.fixture(scope="session")
def resume_schema() -> dict:
    """Load canonical resume JSON schema."""
    assert RESUME_SCHEMA_PATH.exists(), "resume_schema.json does not exist."
    content = json.loads(RESUME_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(content)
    return content


@pytest.fixture(scope="session")
def jd_schema() -> dict:
    """Load canonical job description JSON schema."""
    assert JD_SCHEMA_PATH.exists(), "job_description_schema.json does not exist."
    content = json.loads(JD_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(content)
    return content


def test_resume_schema_structure(resume_schema: dict) -> None:
    """Verify resume schema has core properties and required keys."""
    assert resume_schema.get("title") == "ZecpathResumeSchema"
    properties = resume_schema.get("properties", {})
    required_keys = ["candidate_id", "contact_info", "domain", "skills", "experience", "education"]
    for key in required_keys:
        assert key in properties, f"Missing '{key}' in resume schema properties."


def test_jd_schema_structure(jd_schema: dict) -> None:
    """Verify job description schema has core properties and required keys."""
    assert jd_schema.get("title") == "ZecpathJobDescriptionSchema"
    properties = jd_schema.get("properties", {})
    required_keys = ["job_id", "title", "company_name", "role_type", "requirements"]
    for key in required_keys:
        assert key in properties, f"Missing '{key}' in JD schema properties."


def test_ten_sample_resumes_exist() -> None:
    """Verify at least 10 resumes exist in raw and structured directories."""
    raw_files = list(RAW_RESUMES_DIR.glob("*.txt"))
    structured_files = list(STRUCTURED_RESUMES_DIR.glob("*.json"))

    assert len(raw_files) >= 10, f"Expected >= 10 raw resumes, found {len(raw_files)}"
    assert len(structured_files) >= 10, (
        f"Expected >= 10 structured resumes, found {len(structured_files)}"
    )


def test_job_descriptions_exist() -> None:
    """Verify technical and non-technical JDs exist in raw and structured directories."""
    raw_files = list(RAW_JDS_DIR.glob("*.txt"))
    structured_files = list(STRUCTURED_JDS_DIR.glob("*.json"))

    assert len(raw_files) >= 4, f"Expected >= 4 raw JDs, found {len(raw_files)}"
    assert len(structured_files) >= 4, (
        f"Expected >= 4 structured JDs, found {len(structured_files)}"
    )


def test_all_structured_resumes_validate_against_json_schema(resume_schema: dict) -> None:
    """Validate every structured resume JSON against the draft 2020-12 schema."""
    validator = Draft202012Validator(resume_schema)
    json_files = list(STRUCTURED_RESUMES_DIR.glob("*.json"))

    for json_file in json_files:
        payload = json.loads(json_file.read_text(encoding="utf-8"))
        errors = list(validator.iter_errors(payload))
        assert len(errors) == 0, (
            f"Schema validation failed for {json_file.name}: {[e.message for e in errors]}"
        )


def test_all_structured_jds_validate_against_json_schema(jd_schema: dict) -> None:
    """Validate every structured JD JSON against the draft 2020-12 schema."""
    validator = Draft202012Validator(jd_schema)
    json_files = list(STRUCTURED_JDS_DIR.glob("*.json"))

    for json_file in json_files:
        payload = json.loads(json_file.read_text(encoding="utf-8"))
        errors = list(validator.iter_errors(payload))
        assert len(errors) == 0, (
            f"Schema validation failed for {json_file.name}: {[e.message for e in errors]}"
        )


def test_all_resumes_pydantic_roundtrip() -> None:
    """Verify all resume JSON instances parse into CandidateProfile and serialize back."""
    json_files = list(STRUCTURED_RESUMES_DIR.glob("*.json"))
    for json_file in json_files:
        raw_json = json_file.read_text(encoding="utf-8")
        profile = CandidateProfile.model_validate_json(raw_json)
        assert profile.candidate_id is not None
        assert profile.contact_info.email is not None
        assert len(profile.skills) > 0
        assert len(profile.experience) > 0

        # Roundtrip check
        dumped = profile.model_dump_json()
        reloaded = CandidateProfile.model_validate_json(dumped)
        assert profile.candidate_id == reloaded.candidate_id


def test_all_jds_pydantic_roundtrip() -> None:
    """Verify all JD JSON instances parse into JobProfile and serialize back."""
    json_files = list(STRUCTURED_JDS_DIR.glob("*.json"))
    for json_file in json_files:
        raw_json = json_file.read_text(encoding="utf-8")
        job = JobProfile.model_validate_json(raw_json)
        assert job.job_id is not None
        assert job.role_type in [RoleType.TECHNICAL, RoleType.NON_TECHNICAL, RoleType.HYBRID]
        assert len(job.requirements.required_skills) > 0

        # Roundtrip check
        dumped = job.model_dump_json()
        reloaded = JobProfile.model_validate_json(dumped)
        assert job.job_id == reloaded.job_id


def test_candidate_profile_validation_rejects_invalid_data() -> None:
    """Verify Pydantic models reject invalid inputs with ValidationError."""
    # 1. Invalid email
    with pytest.raises(ValidationError):
        ContactInfo(full_name="Test User", email="not-an-email")

    # 2. Negative experience years
    with pytest.raises(ValidationError):
        SkillObject(name="Python", years_of_experience=-2.0)

    # 3. Invalid date pattern
    with pytest.raises(ValidationError):
        ExperienceObject(
            company_name="Test Corp", designation="Engineer", start_date="invalid-date-format"
        )


def test_domain_diversity_across_resumes() -> None:
    """Verify that the 10 resumes represent distinct technical and non-technical domains."""
    json_files = list(STRUCTURED_RESUMES_DIR.glob("*.json"))
    domains = set()
    for json_file in json_files:
        profile = CandidateProfile.model_validate_json(json_file.read_text(encoding="utf-8"))
        domains.add(profile.domain)

    # We expect 10 distinct domains
    assert len(domains) >= 10, f"Expected 10 distinct domains, found {len(domains)}: {domains}"
