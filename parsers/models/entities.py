"""Common entity models and enumeration types for Zecpath AI (Day 4).

Defines foundational atomic entities: SkillObject, ExperienceObject, EducationObject,
CertificationObject, ProjectObject, and LanguageProficiencyObject with strict Pydantic v2
validation, field descriptions, and JSON Schema generation support.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class SkillCategory(StrEnum):
    """Categorical classification of skills for AI screening and taxonomy mapping."""

    TECHNICAL = "TECHNICAL"
    FRAMEWORK = "FRAMEWORK"
    TOOL = "TOOL"
    DATABASE = "DATABASE"
    CLOUD_DEVOPS = "CLOUD_DEVOPS"
    SOFT = "SOFT"
    DOMAIN = "DOMAIN"
    LANGUAGE = "LANGUAGE"
    METHODOLOGY = "METHODOLOGY"


class SkillProficiency(StrEnum):
    """Normalized proficiency level for candidate skill matching."""

    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"
    UNSPECIFIED = "UNSPECIFIED"


class EmploymentType(StrEnum):
    """Standard employment arrangement types."""

    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    INTERNSHIP = "INTERNSHIP"
    FREELANCE = "FREELANCE"


class DegreeLevel(StrEnum):
    """Standard academic degree classifications."""

    HIGH_SCHOOL = "HIGH_SCHOOL"
    ASSOCIATE = "ASSOCIATE"
    BACHELOR = "BACHELOR"
    MASTER = "MASTER"
    DOCTORATE = "DOCTORATE"
    DIPLOMA = "DIPLOMA"
    CERTIFICATE = "CERTIFICATE"
    OTHER = "OTHER"


class WorkplaceType(StrEnum):
    """Work arrangement location model."""

    ONSITE = "ONSITE"
    REMOTE = "REMOTE"
    HYBRID = "HYBRID"


class SeniorityLevel(StrEnum):
    """Normalized seniority level hierarchy."""

    ENTRY = "ENTRY"
    JUNIOR = "JUNIOR"
    MID = "MID"
    SENIOR = "SENIOR"
    LEAD = "LEAD"
    PRINCIPAL = "PRINCIPAL"
    DIRECTOR = "DIRECTOR"
    EXECUTIVE = "EXECUTIVE"


class RoleType(StrEnum):
    """Job and role classification category."""

    TECHNICAL = "TECHNICAL"
    NON_TECHNICAL = "NON_TECHNICAL"
    HYBRID = "HYBRID"


class LocationObject(BaseModel):
    """Geographic location structure with remote flag."""

    city: str | None = Field(default=None, description="City name")
    state_or_province: str | None = Field(default=None, description="State, province, or region")
    country: str = Field(default="Unknown", description="Country name or ISO code")
    is_remote: bool = Field(default=False, description="Whether position/location is fully remote")


class SkillObject(BaseModel):
    """Standardized representation of a single skill entity."""

    name: str = Field(..., min_length=1, description="Standardized canonical skill name")
    category: SkillCategory = Field(
        default=SkillCategory.TECHNICAL, description="Skill taxonomy category"
    )
    proficiency: SkillProficiency = Field(
        default=SkillProficiency.UNSPECIFIED, description="Proficiency level assessed or claimed"
    )
    years_of_experience: float | None = Field(
        default=None, ge=0.0, description="Estimated or stated years of experience with this skill"
    )
    last_used_year: int | None = Field(
        default=None,
        ge=1970,
        description="The most recent calendar year the skill was actively applied",
    )
    verified: bool = Field(
        default=False,
        description="Whether skill was verified through assessment or validated portfolio",
    )


class ExperienceObject(BaseModel):
    """Granular work experience entry detailing employment tenure and accomplishments."""

    company_name: str = Field(..., min_length=1, description="Legal or common name of employer")
    designation: str = Field(..., min_length=1, description="Official job title as reported")
    standardized_title: str | None = Field(
        default=None, description="Standardized industry job title for canonical taxonomy mapping"
    )
    seniority: SeniorityLevel = Field(
        default=SeniorityLevel.MID, description="Calculated or matched seniority level"
    )
    employment_type: EmploymentType = Field(
        default=EmploymentType.FULL_TIME, description="Type of employment engagement"
    )
    location: LocationObject | None = Field(
        default=None, description="Geographic location of role"
    )
    start_date: str = Field(
        ..., pattern=r"^\d{4}(-\d{2})?$", description="Start date in ISO format YYYY or YYYY-MM"
    )
    end_date: str | None = Field(
        default=None,
        pattern=r"^\d{4}(-\d{2})?$",
        description="End date in ISO format YYYY or YYYY-MM (null if current)",
    )
    is_current: bool = Field(default=False, description="Flag indicating active ongoing tenure")
    duration_in_months: int | None = Field(
        default=None, ge=0, description="Calculated duration of tenure in calendar months"
    )
    description: str | None = Field(
        default="", description="Summary narrative of role context and team scope"
    )
    responsibilities: list[str] = Field(
        default_factory=list, description="List of primary functional duties"
    )
    achievements: list[str] = Field(
        default_factory=list,
        description="Measurable impact, achievements, and quantified metrics (STAR format)",
    )
    technologies_used: list[str] = Field(
        default_factory=list,
        description="Specific tools, languages, and technologies actively utilized in this role",
    )


class EducationObject(BaseModel):
    """Academic credential and formal degree structure."""

    institution_name: str = Field(..., min_length=1, description="College, university, or school")
    degree: str = Field(..., min_length=1, description="Degree title (e.g. Bachelor of Science)")
    degree_level: DegreeLevel = Field(
        default=DegreeLevel.BACHELOR, description="Standard degree classification"
    )
    field_of_study: str = Field(..., min_length=1, description="Major, discipline, or focus")
    start_year: int | None = Field(default=None, ge=1950, description="Matriculation year")
    end_year: int | None = Field(
        default=None, ge=1950, description="Graduation or completion year"
    )
    is_current: bool = Field(default=False, description="Whether study is currently in progress")
    grade_or_gpa: str | None = Field(
        default=None,
        description="Normalized grade, percentage, or GPA score (e.g. 3.8/4.0, First Class)",
    )


class CertificationObject(BaseModel):
    """Professional licenses, vendor certifications, and accredited credentials."""

    name: str = Field(..., min_length=1, description="Official credential title")
    issuing_organization: str = Field(
        ..., min_length=1, description="Certifying entity or institute"
    )
    issue_date: str | None = Field(
        default=None, pattern=r"^\d{4}(-\d{2})?$", description="Issue date (YYYY or YYYY-MM)"
    )
    expiry_date: str | None = Field(
        default=None,
        pattern=r"^\d{4}(-\d{2})?$",
        description="Expiration date (YYYY or YYYY-MM), null if lifetime",
    )
    credential_id: str | None = Field(
        default=None, description="Unique verification ID or serial code"
    )
    verification_url: str | None = Field(
        default=None, description="Public URL for credential verification"
    )


class ProjectObject(BaseModel):
    """Notable personal, open-source, or client project highlight."""

    title: str = Field(..., min_length=1, description="Project title")
    role: str | None = Field(default=None, description="Candidate role on project")
    description: str = Field(default="", description="High-level project scope and architecture")
    technologies: list[str] = Field(default_factory=list, description="Tech stack employed")
    outcomes: list[str] = Field(default_factory=list, description="Quantified outcomes or metrics")
    url: str | None = Field(default=None, description="Repository, live demo, or case study URL")


class LanguageProficiencyObject(BaseModel):
    """Spoken and written language competency."""

    language: str = Field(..., min_length=1, description="Language name")
    proficiency: str = Field(
        default="PROFICIENT",
        description="Fluency level (e.g. NATIVE, FLUENT, PROFESSIONAL_WORKING, CONVERSATIONAL)",
    )
