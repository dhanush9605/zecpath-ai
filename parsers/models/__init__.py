"""Data models package for Zecpath AI parsing and structuring engine."""

from parsers.models.candidate import CandidateMetadata, CandidateProfile, ContactInfo
from parsers.models.entities import (
    CertificationObject,
    DegreeLevel,
    EducationObject,
    EmploymentType,
    ExperienceObject,
    LanguageProficiencyObject,
    LocationObject,
    ProjectObject,
    RoleType,
    SeniorityLevel,
    SkillCategory,
    SkillObject,
    SkillProficiency,
    WorkplaceType,
)
from parsers.models.job import JobProfile, JobRequirements, PayPeriod, SalaryRange

__all__ = [
    "CandidateMetadata",
    "CandidateProfile",
    "CertificationObject",
    "ContactInfo",
    "DegreeLevel",
    "EducationObject",
    "EmploymentType",
    "ExperienceObject",
    "JobProfile",
    "JobRequirements",
    "LanguageProficiencyObject",
    "LocationObject",
    "PayPeriod",
    "ProjectObject",
    "RoleType",
    "SalaryRange",
    "SeniorityLevel",
    "SkillCategory",
    "SkillObject",
    "SkillProficiency",
    "WorkplaceType",
]
