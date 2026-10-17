"""Automated test suite for Day 6 - Job Description Parsing System.

Verifies role extraction, experience thresholds, education levels, skill synonym
resolution, required vs preferred partitioning, and JSON schema compliance.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from parsers import JobDescriptionParser
from parsers.models.entities import (
    DegreeLevel,
    RoleType,
    SeniorityLevel,
    SkillCategory,
)
from parsers.taxonomy import (
    detect_education_level,
    detect_role_type,
    detect_seniority,
    resolve_skill_synonym,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_JDS_DIR = REPO_ROOT / "data" / "raw" / "job_descriptions"
JD_SCHEMA_PATH = REPO_ROOT / "data" / "schemas" / "job_description_schema.json"


@pytest.fixture(scope="session")
def jd_validator() -> Draft202012Validator:
    """Load canonical JD schema for validation checks."""
    assert JD_SCHEMA_PATH.exists(), "job_description_schema.json missing."
    schema = json.loads(JD_SCHEMA_PATH.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def test_skill_synonym_resolution() -> None:
    """Verify common skill aliases map to canonical names and taxonomy categories."""
    # Golang -> Go
    skill_go = resolve_skill_synonym("Golang")
    assert skill_go is not None
    assert skill_go.canonical_name == "Go"
    assert skill_go.category == SkillCategory.TECHNICAL

    # K8s -> Kubernetes
    skill_k8s = resolve_skill_synonym("k8s")
    assert skill_k8s is not None
    assert skill_k8s.canonical_name == "Kubernetes"
    assert skill_k8s.category == SkillCategory.CLOUD_DEVOPS

    # Postgres -> PostgreSQL
    skill_pg = resolve_skill_synonym("Postgres")
    assert skill_pg is not None
    assert skill_pg.canonical_name == "PostgreSQL"
    assert skill_pg.category == SkillCategory.DATABASE

    # ReactJS -> React
    skill_react = resolve_skill_synonym("reactjs")
    assert skill_react is not None
    assert skill_react.canonical_name == "React"

    # AWS Cloud -> AWS
    skill_aws = resolve_skill_synonym("AWS Cloud")
    assert skill_aws is not None
    assert skill_aws.canonical_name == "AWS"


def test_seniority_detection_heuristics() -> None:
    """Verify title keywords map to accurate SeniorityLevel hierarchy."""
    assert detect_seniority("Senior Backend Engineer") == SeniorityLevel.SENIOR
    assert detect_seniority("Staff Machine Learning Engineer") == SeniorityLevel.PRINCIPAL
    assert detect_seniority("Tech Lead / Engineering Manager") == SeniorityLevel.LEAD
    assert detect_seniority("Junior QA Tester") == SeniorityLevel.JUNIOR
    assert detect_seniority("Software Engineer Intern") == SeniorityLevel.ENTRY
    assert detect_seniority("VP of Technology") == SeniorityLevel.EXECUTIVE
    assert detect_seniority("Director of Product") == SeniorityLevel.DIRECTOR


def test_role_type_classification() -> None:
    """Verify technical vs non-technical vs hybrid classification."""
    assert detect_role_type("Senior Distributed Systems Backend Engineer") == RoleType.TECHNICAL
    assert detect_role_type("Staff Machine Learning Engineer") == RoleType.TECHNICAL
    assert detect_role_type("Senior Talent Acquisition Partner") == RoleType.NON_TECHNICAL
    assert detect_role_type("Lead FP&A Financial Analyst") == RoleType.NON_TECHNICAL
    assert detect_role_type("Technical Product Manager") == RoleType.HYBRID


def test_education_level_detection() -> None:
    """Verify extraction of minimum academic degree levels."""
    assert detect_education_level("Requires a Ph.D. in Computer Science") == DegreeLevel.DOCTORATE
    assert detect_education_level("Master's or Ph.D. preferred") == DegreeLevel.DOCTORATE
    assert detect_education_level("Requires Master of Science degree") == DegreeLevel.MASTER
    assert detect_education_level("Bachelor's degree in Engineering required") == DegreeLevel.BACHELOR


def test_parser_on_backend_job_description(jd_validator: Draft202012Validator) -> None:
    """Verify parser extracts technical backend JD accurately and passes schema validation."""
    backend_jd_file = RAW_JDS_DIR / "jd_01_senior_backend.txt"
    assert backend_jd_file.exists()

    parser = JobDescriptionParser()
    job = parser.parse_file(backend_jd_file)

    assert "Senior Backend" in job.title
    assert job.role_type == RoleType.TECHNICAL
    assert job.seniority_level == SeniorityLevel.SENIOR
    assert job.requirements.minimum_experience_years == 5.0
    assert len(job.requirements.required_skills) >= 3

    # Check skill resolution
    skill_names = [s.name for s in job.requirements.required_skills]
    assert "Go" in skill_names
    assert "PostgreSQL" in skill_names

    # Check salary extraction
    assert job.salary_range is not None
    assert job.salary_range.min_amount == 165000.0
    assert job.salary_range.max_amount == 210000.0

    # Validate against canonical JSON schema
    errors = list(jd_validator.iter_errors(job.model_dump(mode="json")))
    assert len(errors) == 0, f"Schema validation errors: {errors}"


def test_parser_on_ai_ml_job_description(jd_validator: Draft202012Validator) -> None:
    """Verify parser extracts ML & GenAI JD accurately."""
    ml_jd_file = RAW_JDS_DIR / "jd_02_ml_engineer.txt"
    assert ml_jd_file.exists()

    parser = JobDescriptionParser()
    job = parser.parse_file(ml_jd_file)

    assert "Staff" in job.title
    assert job.role_type == RoleType.TECHNICAL
    assert job.seniority_level == SeniorityLevel.PRINCIPAL
    assert job.requirements.minimum_experience_years == 6.0
    assert job.requirements.minimum_education_level in [DegreeLevel.MASTER, DegreeLevel.DOCTORATE]

    skill_names = [s.name for s in job.requirements.required_skills]
    assert "PyTorch" in skill_names

    errors = list(jd_validator.iter_errors(job.model_dump(mode="json")))
    assert len(errors) == 0


def test_parser_on_talent_acquisition_jd(jd_validator: Draft202012Validator) -> None:
    """Verify parser extracts non-technical HR / talent partner JD accurately."""
    talent_jd_file = RAW_JDS_DIR / "jd_03_talent_acquisition.txt"
    assert talent_jd_file.exists()

    parser = JobDescriptionParser()
    job = parser.parse_file(talent_jd_file)

    assert "Talent Acquisition" in job.title
    assert job.role_type == RoleType.NON_TECHNICAL
    assert job.requirements.minimum_experience_years == 5.0

    skill_names = [s.name for s in job.requirements.required_skills]
    assert "Technical Recruiting" in skill_names
    assert "Greenhouse ATS" in skill_names

    errors = list(jd_validator.iter_errors(job.model_dump(mode="json")))
    assert len(errors) == 0


def test_parser_on_financial_analyst_jd(jd_validator: Draft202012Validator) -> None:
    """Verify parser extracts non-technical finance / FP&A JD accurately."""
    finance_jd_file = RAW_JDS_DIR / "jd_04_financial_analyst.txt"
    assert finance_jd_file.exists()

    parser = JobDescriptionParser()
    job = parser.parse_file(finance_jd_file)

    assert "Financial" in job.title
    assert job.role_type == RoleType.NON_TECHNICAL
    assert job.requirements.minimum_experience_years == 5.0

    skill_names = [s.name for s in job.requirements.required_skills]
    assert "Financial Modeling" in skill_names
    assert "Advanced Excel" in skill_names

    errors = list(jd_validator.iter_errors(job.model_dump(mode="json")))
    assert len(errors) == 0


def test_parse_and_save_generates_json_file(tmp_path: Path) -> None:
    """Verify parse_and_save persists structured JSON file to output directory."""
    backend_jd_file = RAW_JDS_DIR / "jd_01_senior_backend.txt"
    parser = JobDescriptionParser()

    json_path, profile = parser.parse_and_save(backend_jd_file, output_dir=tmp_path)

    assert json_path.exists()
    assert json_path.suffix == ".json"

    saved_data = json.loads(json_path.read_text(encoding="utf-8"))
    assert saved_data["job_id"] == profile.job_id
    assert saved_data["title"] == profile.title


def test_parser_handles_missing_file() -> None:
    """Verify parser raises FileNotFoundError when given non-existent file path."""
    parser = JobDescriptionParser()
    with pytest.raises(FileNotFoundError):
        parser.parse_file("non_existent_requisition.txt")
