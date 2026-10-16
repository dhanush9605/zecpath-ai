"""Candidate profile data model for Zecpath AI (Day 4).

Represents the standardized, structured entity for resume extraction, screening evaluation,
and applicant tracking matching.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from parsers.models.entities import (
    CertificationObject,
    EducationObject,
    ExperienceObject,
    LanguageProficiencyObject,
    LocationObject,
    ProjectObject,
    SkillObject,
)


class ContactInfo(BaseModel):
    """Personal and digital contact information of the candidate."""

    full_name: str = Field(..., min_length=1, description="Candidate legal or preferred name")
    email: str = Field(
        ..., pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", description="Standardized email address"
    )
    phone: str | None = Field(default=None, description="Contact phone number with country code")
    location: LocationObject | None = Field(
        default=None, description="Current residence or base location"
    )
    linkedin_url: str | None = Field(default=None, description="LinkedIn profile URL")
    github_url: str | None = Field(default=None, description="GitHub or code repository URL")
    portfolio_url: str | None = Field(
        default=None, description="Personal website or portfolio URL"
    )


class CandidateMetadata(BaseModel):
    """Extraction provenance and processing audit metadata."""

    source_file_name: str = Field(..., description="Original resume document file name")
    parser_version: str = Field(default="0.1.0", description="Parser engine semantic version")
    extracted_at: str = Field(..., description="ISO 8601 extraction timestamp")
    confidence_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Aggregate extraction confidence score (0.0 to 1.0)",
    )


class CandidateProfile(BaseModel):
    """Comprehensive, normalized AI candidate profile entity."""

    candidate_id: str = Field(..., min_length=1, description="Unique candidate identifier or UUID")
    contact_info: ContactInfo = Field(..., description="Contact and personal information")
    headline: str | None = Field(default=None, description="Professional headline or tagline")
    professional_summary: str = Field(
        default="", description="Executive summary of background, competencies, and achievements"
    )
    target_role: str | None = Field(default=None, description="Desired target job title or role")
    domain: str = Field(
        ..., description="Primary industry domain (e.g. Backend, Data Science, HR, Finance)"
    )
    total_experience_years: float = Field(
        default=0.0,
        ge=0.0,
        description="Calculated total cumulative professional experience in years",
    )
    skills: list[SkillObject] = Field(
        default_factory=list, description="Extracted and normalized skills"
    )
    experience: list[ExperienceObject] = Field(
        default_factory=list, description="Chronological work history records"
    )
    education: list[EducationObject] = Field(
        default_factory=list, description="Formal academic credentials"
    )
    certifications: list[CertificationObject] = Field(
        default_factory=list, description="Professional certifications and credentials"
    )
    projects: list[ProjectObject] = Field(
        default_factory=list, description="Notable projects and case studies"
    )
    languages: list[LanguageProficiencyObject] = Field(
        default_factory=list, description="Spoken and written language proficiencies"
    )
    metadata: CandidateMetadata | None = Field(
        default=None, description="Extraction provenance and audit metadata"
    )
