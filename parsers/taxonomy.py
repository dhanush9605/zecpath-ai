"""Taxonomy, skill synonym resolution, and role classification rules for Zecpath AI (Day 6).

Provides dictionary registries and heuristic mapping for:
1. Skill synonyms (e.g. 'Golang' -> 'Go', 'K8s' -> 'Kubernetes').
2. Skill categories and default proficiencies.
3. Seniority level hierarchies and keyword patterns.
4. Role type classification (TECHNICAL, NON_TECHNICAL, HYBRID).
5. Education degree level detection patterns.
"""

from __future__ import annotations

import re
from typing import NamedTuple

from parsers.models.entities import (
    DegreeLevel,
    RoleType,
    SeniorityLevel,
    SkillCategory,
    SkillProficiency,
)


class CanonicalSkill(NamedTuple):
    """Metadata definition for a canonical skill."""
    canonical_name: str
    category: SkillCategory
    default_proficiency: SkillProficiency
    synonyms: list[str]


# Comprehensive Skill Synonym & Taxonomy Registry
SKILL_TAXONOMY: list[CanonicalSkill] = [
    # Technical Programming Languages & Runtimes
    CanonicalSkill("Go", SkillCategory.TECHNICAL, SkillProficiency.ADVANCED, ["golang", "go language", "go lang"]),
    CanonicalSkill("Python", SkillCategory.TECHNICAL, SkillProficiency.ADVANCED, ["python3", "python 3", "py"]),
    CanonicalSkill("TypeScript", SkillCategory.TECHNICAL, SkillProficiency.ADVANCED, ["ts", "typescript"]),
    CanonicalSkill("JavaScript", SkillCategory.TECHNICAL, SkillProficiency.ADVANCED, ["js", "javascript", "ecmascript", "es6", "esnext"]),
    CanonicalSkill("C++", SkillCategory.TECHNICAL, SkillProficiency.ADVANCED, ["cpp", "c plus plus"]),
    CanonicalSkill("SQL", SkillCategory.TECHNICAL, SkillProficiency.ADVANCED, ["structured query language", "ansi sql"]),

    # Frameworks & Libraries
    CanonicalSkill("React", SkillCategory.FRAMEWORK, SkillProficiency.EXPERT, ["reactjs", "react.js", "react js"]),
    CanonicalSkill("Next.js", SkillCategory.FRAMEWORK, SkillProficiency.ADVANCED, ["nextjs", "next.js", "next js"]),
    CanonicalSkill("PyTorch", SkillCategory.FRAMEWORK, SkillProficiency.EXPERT, ["pytorch", "torch"]),
    CanonicalSkill("TensorFlow", SkillCategory.FRAMEWORK, SkillProficiency.ADVANCED, ["tensorflow", "tf"]),
    CanonicalSkill("FastAPI", SkillCategory.FRAMEWORK, SkillProficiency.ADVANCED, ["fastapi", "fast-api"]),
    CanonicalSkill("gRPC", SkillCategory.FRAMEWORK, SkillProficiency.ADVANCED, ["grpc", "grpc microservices"]),

    # Databases & Stores
    CanonicalSkill("PostgreSQL", SkillCategory.DATABASE, SkillProficiency.ADVANCED, ["postgres", "postgresql", "psql"]),
    CanonicalSkill("Redis", SkillCategory.DATABASE, SkillProficiency.ADVANCED, ["redis cache", "redis cluster"]),
    CanonicalSkill("MongoDB", SkillCategory.DATABASE, SkillProficiency.INTERMEDIATE, ["mongo", "mongodb"]),
    CanonicalSkill("Vector Databases", SkillCategory.DATABASE, SkillProficiency.ADVANCED, ["vector db", "vector databases", "pinecone", "milvus", "qdrant", "weaviate"]),

    # Cloud, DevOps & Infrastructure
    CanonicalSkill("AWS", SkillCategory.CLOUD_DEVOPS, SkillProficiency.ADVANCED, ["amazon web services", "aws cloud", "aws"]),
    CanonicalSkill("Kubernetes", SkillCategory.CLOUD_DEVOPS, SkillProficiency.ADVANCED, ["k8s", "kubernetes", "kube", "k8s cluster"]),
    CanonicalSkill("Docker", SkillCategory.CLOUD_DEVOPS, SkillProficiency.ADVANCED, ["docker containers", "dockerfile", "containerization"]),
    CanonicalSkill("Terraform", SkillCategory.TOOL, SkillProficiency.ADVANCED, ["terraform", "tf", "hashicorp terraform"]),
    CanonicalSkill("Apache Kafka", SkillCategory.TOOL, SkillProficiency.ADVANCED, ["kafka", "apache kafka", "event streaming"]),

    # AI, ML & Data Science Domains
    CanonicalSkill("Distributed Systems", SkillCategory.TECHNICAL, SkillProficiency.ADVANCED, ["distributed systems", "distributed computing", "high-throughput systems"]),
    CanonicalSkill("Large Language Models (LLMs)", SkillCategory.TECHNICAL, SkillProficiency.ADVANCED, ["llm", "llms", "large language models", "foundation models"]),
    CanonicalSkill("Generative AI", SkillCategory.TECHNICAL, SkillProficiency.ADVANCED, ["genai", "gen ai", "generative ai"]),
    CanonicalSkill("Retrieval-Augmented Generation (RAG)", SkillCategory.TECHNICAL, SkillProficiency.ADVANCED, ["rag", "retrieval augmented generation"]),
    CanonicalSkill("MLOps", SkillCategory.CLOUD_DEVOPS, SkillProficiency.ADVANCED, ["mlops", "machine learning operations", "kubeflow", "mlflow"]),

    # Design & Product
    CanonicalSkill("Figma", SkillCategory.TOOL, SkillProficiency.EXPERT, ["figma", "figma tokens"]),
    CanonicalSkill("Design Systems", SkillCategory.DOMAIN, SkillProficiency.EXPERT, ["design systems", "design tokens", "component libraries"]),
    CanonicalSkill("User Research", SkillCategory.METHODOLOGY, SkillProficiency.ADVANCED, ["user research", "usability testing", "user testing"]),
    CanonicalSkill("Product Strategy", SkillCategory.DOMAIN, SkillProficiency.EXPERT, ["product strategy", "product roadmap", "prd"]),
    CanonicalSkill("Agile / Scrum", SkillCategory.METHODOLOGY, SkillProficiency.EXPERT, ["agile", "scrum", "sprint planning", "kanban"]),

    # HR & Non-Technical Operations
    CanonicalSkill(
        "Technical Recruiting",
        SkillCategory.DOMAIN,
        SkillProficiency.ADVANCED,
        [
            "technical recruiting",
            "tech hiring",
            "talent acquisition",
            "recruiting",
            "full-lifecycle recruiting",
            "full lifecycle recruiting",
            "recruiting experience",
            "talent partner",
        ],
    ),
    CanonicalSkill("Greenhouse ATS", SkillCategory.TOOL, SkillProficiency.ADVANCED, ["greenhouse", "greenhouse ats", "greenhouse.io", "ashby", "lever"]),
    CanonicalSkill("Candidate Sourcing & Outreach", SkillCategory.DOMAIN, SkillProficiency.ADVANCED, ["sourcing", "boolean search", "candidate outreach", "talent sourcing"]),
    CanonicalSkill("DEI Strategy", SkillCategory.DOMAIN, SkillProficiency.INTERMEDIATE, ["dei", "diversity recruiting", "diversity and inclusion"]),

    # Finance & Analytics
    CanonicalSkill("Financial Modeling", SkillCategory.TECHNICAL, SkillProficiency.EXPERT, ["financial modeling", "3-statement modeling", "dcf", "discounted cash flow", "financial valuation"]),
    CanonicalSkill("Corporate Budgeting & FP&A", SkillCategory.DOMAIN, SkillProficiency.EXPERT, ["fp&a", "financial planning and analysis", "corporate budgeting", "variance analysis"]),
    CanonicalSkill("Advanced Excel", SkillCategory.TOOL, SkillProficiency.EXPERT, ["excel", "advanced excel", "vba", "financial excel"]),
    CanonicalSkill("Power BI", SkillCategory.TOOL, SkillProficiency.ADVANCED, ["power bi", "powerbi", "tableau"]),
    CanonicalSkill("US GAAP", SkillCategory.DOMAIN, SkillProficiency.ADVANCED, ["gaap", "us gaap", "asc 606", "ifrs"]),

    # Growth & Marketing
    CanonicalSkill("Performance Marketing & Paid Ads", SkillCategory.TECHNICAL, SkillProficiency.EXPERT, ["paid ads", "google ads", "performance marketing", "sem"]),
    CanonicalSkill("Conversion Rate Optimization (CRO)", SkillCategory.METHODOLOGY, SkillProficiency.EXPERT, ["cro", "conversion rate optimization", "a/b testing"]),
    CanonicalSkill("Google Analytics 4 / GA4", SkillCategory.TOOL, SkillProficiency.ADVANCED, ["ga4", "google analytics 4", "google analytics"]),
]

# Fast lookup dictionary mapping lowercase synonym -> CanonicalSkill
SYNONYM_LOOKUP: dict[str, CanonicalSkill] = {}
for skill_def in SKILL_TAXONOMY:
    SYNONYM_LOOKUP[skill_def.canonical_name.lower()] = skill_def
    for synonym in skill_def.synonyms:
        SYNONYM_LOOKUP[synonym.lower()] = skill_def

# Seniority keyword matching table
SENIORITY_PATTERNS: list[tuple[re.Pattern, SeniorityLevel]] = [
    (re.compile(r"\b(vp|vice president|c-level|cxo|cto|cfo|chief)\b", re.IGNORECASE), SeniorityLevel.EXECUTIVE),
    (re.compile(r"\b(director|head of)\b", re.IGNORECASE), SeniorityLevel.DIRECTOR),
    (re.compile(r"\b(principal|staff|architect)\b", re.IGNORECASE), SeniorityLevel.PRINCIPAL),
    (re.compile(r"\b(lead|team lead|tech lead)\b", re.IGNORECASE), SeniorityLevel.LEAD),
    (re.compile(r"\b(senior|sr\.?)\b", re.IGNORECASE), SeniorityLevel.SENIOR),
    (re.compile(r"\b(junior|jr\.?|associate)\b", re.IGNORECASE), SeniorityLevel.JUNIOR),
    (re.compile(r"\b(intern|internship|trainee|entry)\b", re.IGNORECASE), SeniorityLevel.ENTRY),
]

# Degree level patterns
DEGREE_PATTERNS: list[tuple[re.Pattern, DegreeLevel]] = [
    (re.compile(r"\b(ph\.?d\.?|doctorate|doctoral)\b", re.IGNORECASE), DegreeLevel.DOCTORATE),
    (re.compile(r"\b(master'?s?|m\.?s\.?|m\.?tech|m\.?eng|mba)\b", re.IGNORECASE), DegreeLevel.MASTER),
    (re.compile(r"\b(bachelor'?s?|b\.?s\.?|b\.?tech|b\.?e\.?|b\.?a\.?|undergraduate)\b", re.IGNORECASE), DegreeLevel.BACHELOR),
    (re.compile(r"\b(associate'?s?)\b", re.IGNORECASE), DegreeLevel.ASSOCIATE),
    (re.compile(r"\b(high school|secondary)\b", re.IGNORECASE), DegreeLevel.HIGH_SCHOOL),
]

# Technical vs Non-Technical indicators
TECHNICAL_ROLE_KEYWORDS = {
    "software", "engineer", "developer", "backend", "frontend", "fullstack",
    "machine learning", "ai", "data scientist", "data engineer", "devops",
    "cloud", "architect", "systems", "security", "cybersecurity", "qa",
}

NON_TECHNICAL_ROLE_KEYWORDS = {
    "recruiter", "talent acquisition", "hr", "human resources", "finance",
    "financial analyst", "fp&a", "accountant", "marketing", "sales",
    "business development", "legal", "operations",
}


def resolve_skill_synonym(skill_name: str) -> CanonicalSkill | None:
    """Resolve a raw skill mention to its canonical skill object and taxonomy category."""
    clean = skill_name.strip().lower()
    return SYNONYM_LOOKUP.get(clean)


def detect_seniority(title: str, min_exp_years: float = 0.0) -> SeniorityLevel:
    """Infer seniority level from title keywords and experience thresholds."""
    for pattern, level in SENIORITY_PATTERNS:
        if pattern.search(title):
            return level

    # Experience-based fallback
    if min_exp_years >= 10.0:
        return SeniorityLevel.PRINCIPAL
    if min_exp_years >= 7.0:
        return SeniorityLevel.LEAD
    if min_exp_years >= 5.0:
        return SeniorityLevel.SENIOR
    if min_exp_years >= 3.0:
        return SeniorityLevel.MID
    if min_exp_years >= 1.0:
        return SeniorityLevel.JUNIOR
    return SeniorityLevel.MID


def detect_role_type(title: str) -> RoleType:
    """Classify role as TECHNICAL, NON_TECHNICAL, or HYBRID based on title terms."""
    title_lower = title.lower()
    has_tech = any(k in title_lower for k in TECHNICAL_ROLE_KEYWORDS)
    has_non_tech = any(k in title_lower for k in NON_TECHNICAL_ROLE_KEYWORDS)

    if has_tech and has_non_tech:
        return RoleType.HYBRID
    if has_tech:
        return RoleType.TECHNICAL
    if has_non_tech:
        return RoleType.NON_TECHNICAL

    # Hybrid roles like Product Manager
    if "product" in title_lower:
        return RoleType.HYBRID

    return RoleType.TECHNICAL


def detect_education_level(text: str) -> DegreeLevel:
    """Extract required education credential from text, defaulting to BACHELOR."""
    for pattern, level in DEGREE_PATTERNS:
        if pattern.search(text):
            return level
    return DegreeLevel.BACHELOR
