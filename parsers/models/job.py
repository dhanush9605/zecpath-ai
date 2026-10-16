"""Job description and profile data model for Zecpath AI (Day 4).

Represents the standardized, structured entity for job specifications, screening requirements,
and candidate matching scoring.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from parsers.models.entities import (
    DegreeLevel,
    EmploymentType,
    LocationObject,
    RoleType,
    SeniorityLevel,
    SkillObject,
    WorkplaceType,
)


class PayPeriod(StrEnum):
    """Frequency of compensation calculation."""

    ANNUAL = "ANNUAL"
    MONTHLY = "MONTHLY"
    HOURLY = "HOURLY"


class SalaryRange(BaseModel):
    """Structured compensation and remuneration bracket."""

    currency: str = Field(default="USD", description="Currency ISO 4217 code (e.g. USD, EUR, INR)")
    min_amount: float | None = Field(default=None, ge=0.0, description="Minimum base salary")
    max_amount: float | None = Field(default=None, ge=0.0, description="Maximum base salary")
    pay_period: PayPeriod = Field(default=PayPeriod.ANNUAL, description="Pay frequency period")


class JobRequirements(BaseModel):
    """Categorized screening requirements for the vacancy."""

    minimum_experience_years: float = Field(
        default=0.0, ge=0.0, description="Minimum mandatory years of professional experience"
    )
    required_skills: list[SkillObject] = Field(
        default_factory=list, description="Mandatory skills required for ATS qualification"
    )
    preferred_skills: list[SkillObject] = Field(
        default_factory=list, description="Nice-to-have supplementary skills"
    )
    minimum_education_level: DegreeLevel = Field(
        default=DegreeLevel.BACHELOR, description="Baseline academic qualification requirement"
    )
    required_certifications: list[str] = Field(
        default_factory=list, description="Mandatory certifications or active licenses"
    )


class JobProfile(BaseModel):
    """Standardized AI job profile entity."""

    job_id: str = Field(..., min_length=1, description="Unique job requisition identifier")
    title: str = Field(..., min_length=1, description="Official job title")
    company_name: str = Field(..., min_length=1, description="Hiring organization name")
    department: str = Field(default="General", description="Department or business unit")
    role_type: RoleType = Field(
        default=RoleType.TECHNICAL, description="Technical vs non-technical role type"
    )
    seniority_level: SeniorityLevel = Field(
        default=SeniorityLevel.MID, description="Requisite seniority bracket"
    )
    employment_type: EmploymentType = Field(
        default=EmploymentType.FULL_TIME, description="Engagement type"
    )
    workplace_type: WorkplaceType = Field(
        default=WorkplaceType.HYBRID, description="Work arrangement"
    )
    location: LocationObject | None = Field(
        default=None, description="Office or territory location"
    )
    salary_range: SalaryRange | None = Field(default=None, description="Compensation range")
    summary: str = Field(default="", description="Executive overview of the role and mission")
    responsibilities: list[str] = Field(
        default_factory=list, description="Core responsibilities and duties"
    )
    requirements: JobRequirements = Field(
        ..., description="Screening qualifications and requirements"
    )
    benefits: list[str] = Field(default_factory=list, description="Perks and benefits offered")
    created_at: str = Field(..., description="ISO 8601 posting creation date")
    is_active: bool = Field(default=True, description="Whether position is currently open")
