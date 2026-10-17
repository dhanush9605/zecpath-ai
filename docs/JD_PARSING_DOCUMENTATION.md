# Zecpath AI — Job Description Parsing System Documentation (Day 6)

**Document Version:** 1.0.0  
**Phase:** Day 6 — Job Description Parsing System  
**Status:** Implemented, Tested & Verified (100% Pass)  
**Author / Engineering Team:** Zecpath AI Engineering  
**Primary Deliverables:** `parsers/jd_parser.py`, `parsers/taxonomy.py`, `tests/test_jd_parser.py`, `scripts/verify_day6.py`, `data/structured/job_descriptions/*.json`

---

## 1. Executive Summary & Objective

In the automated recruitment lifecycle of **Zecpath AI**, matching candidates against job requisitions requires converting unstructured, human-written employer job descriptions into structured, AI-readable, and machine-actionable **Job Requirement Objects** (`JobProfile` and `JobRequirements`).

Human-written job postings exhibit significant variance:
- **Varying Section Semantics**: Sections may be titled `"About the Role"`, `"What You'll Do"`, `"Requirements"`, `"Basic Qualifications"`, or `"What We Offer"`.
- **Informal Experience Notations**: Phrases such as `"5+ years"`, `"minimum 6 yrs"`, or `"at least 3-5 years"`.
- **Skill Aliases & Synonyms**: Tools and languages are mentioned using slang, acronyms, or versions (e.g., `Golang` vs `Go`, `K8s` vs `Kubernetes`, `Postgres` vs `PostgreSQL`, `NextJS` vs `Next.js`).
- **Seniority & Role Ambiguity**: Titles like `"Staff ML Engineer"` imply specific architectural responsibilities and higher seniority than a standard `"Software Engineer"`.
- **Compensation Formatting**: Salary brackets appear as bullet points, ranges (`$165,000 - $210,000`), or shorthand (`$110k - $140k`).

The **Day 6 Job Description Parsing System** addresses these challenges by delivering a deterministic, rule-driven, taxonomy-backed parser that segments documents, normalizes text, maps synonyms, extracts requirements, and outputs validated, type-safe JSON compliant with Draft 2020-12 schema standards.

---

## 2. System Architecture & Extraction Pipeline

```
Unstructured JD Text / File
        │
        ▼
┌──────────────────────────────────────────────┐
│ 1. Text Normalization & Sanitization          │
│    - Unicode & Ligature Normalization        │
│    - Standardized ASCII Bullet Points        │
│    - Whitespace & Linebreak Consolidation    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ 2. Semantic Section Segmentation              │
│    - Header & Metadata Extraction             │
│    - Responsibilities Heuristics             │
│    - Requirements & Preferred Partitioning   │
│    - Compensation & Benefits Segregation     │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ 3. Taxonomy & Synonym Resolution Engine      │
│    - Canonical Skill Mapping (O(1) Lookup)    │
│    - Category & Default Proficiency Tagging  │
│    - Precompiled Regex Multi-Term Matching   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ 4. Attribute Inference & Extraction          │
│    - Role Type (Technical, Non-Tech, Hybrid) │
│    - Seniority Hierarchy Inference           │
│    - Minimum Experience Year Parser          │
│    - Degree Level Classifier                 │
│    - Annual Salary Range Bracket Parser      │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ 5. Structured Object & Validation            │
│    - Pydantic JobProfile & JobRequirements   │
│    - JSON Schema Draft 2020-12 Validation    │
│    - Disk Persistence (data/structured/jds/) │
└──────────────────────────────────────────────┘
```

---

## 3. Core Modules & Components

### 3.1 Taxonomy & Skill Resolution (`parsers/taxonomy.py`)

The taxonomy module provides a curated registry of skills, categories, synonyms, seniority patterns, and education heuristics.

#### Canonical Skill Definition
```python
class CanonicalSkill(NamedTuple):
    canonical_name: str
    category: SkillCategory
    default_proficiency: SkillProficiency
    synonyms: list[str]
```

#### Taxonomy Registry Coverage
The system indexes skills across 8 distinct categories:
- **Technical Languages**: `Go` (`golang`, `go language`), `Python` (`python3`, `py`), `TypeScript` (`ts`), `SQL`, `C++`.
- **Frameworks & Libraries**: `React` (`reactjs`, `react.js`), `Next.js` (`nextjs`), `PyTorch` (`torch`), `FastAPI`, `gRPC`.
- **Databases & Stores**: `PostgreSQL` (`postgres`, `psql`), `Redis`, `MongoDB`, `Vector Databases` (`pinecone`, `milvus`, `qdrant`).
- **Cloud & DevOps**: `AWS` (`amazon web services`), `Kubernetes` (`k8s`, `kube`), `Docker`, `Terraform`, `Apache Kafka`.
- **AI / ML Domains**: `Distributed Systems`, `Large Language Models (LLMs)`, `Generative AI`, `RAG`, `MLOps`.
- **Product & Design**: `Figma`, `Design Systems`, `User Research`, `Product Strategy`, `Agile / Scrum`.
- **Talent & HR Operations**: `Technical Recruiting` (`full-lifecycle recruiting`, `recruiting`, `talent acquisition`, `talent partner`), `Greenhouse ATS` (`ashby`, `lever`), `Candidate Sourcing`, `DEI Strategy`.
- **Finance & Corporate**: `Financial Modeling` (`3-statement modeling`, `dcf`), `Corporate Budgeting & FP&A`, `Advanced Excel`, `Power BI`, `US GAAP`.

#### Synonym Lookup Engine
The registry pre-computes an inverted index (`SYNONYM_LOOKUP: dict[str, CanonicalSkill]`) mapping lowercase synonym variants directly to their canonical definitions.

### 3.2 Role Classification & Seniority Heuristics

#### Role Type Classification
Roles are classified into three types based on title keyword analysis:
- **`RoleType.TECHNICAL`**: Keywords like `software`, `engineer`, `developer`, `backend`, `frontend`, `machine learning`, `systems`, `devops`, `architect`.
- **`RoleType.NON_TECHNICAL`**: Keywords like `recruiter`, `talent acquisition`, `hr`, `finance`, `fp&a`, `accountant`, `marketing`, `sales`.
- **`RoleType.HYBRID`**: Dual keyword matches (e.g., `Technical Product Manager`, `Technical Sourcer`, `Solutions Architect`).

#### Seniority Level Hierarchy
Seniority is inferred in priority order from title keywords, with a fallback to experience thresholds:
1. `EXECUTIVE`: `VP`, `Vice President`, `C-Level`, `CTO`, `CFO`, `Chief`
2. `DIRECTOR`: `Director`, `Head of`
3. `PRINCIPAL`: `Principal`, `Staff`, `Architect`
4. `LEAD`: `Lead`, `Team Lead`, `Tech Lead`
5. `SENIOR`: `Senior`, `Sr.`
6. `JUNIOR`: `Junior`, `Jr.`, `Associate`
7. `ENTRY`: `Intern`, `Internship`, `Trainee`, `Entry`
8. *Threshold Fallback*: >=10 yrs -> `PRINCIPAL`, >=7 yrs -> `LEAD`, >=5 yrs -> `SENIOR`, >=3 yrs -> `MID`, >=1 yr -> `JUNIOR`.

### 3.3 Experience & Salary Extraction Heuristics

#### Minimum Experience Years
Regular expressions extract numerical experience requirements from requirement blocks:
- `r"(\d+(?:\.\d+)?)\s*\+?\s*(?:-\s*\d+\s*)?(?:years|yrs)"`
- `r"(?:minimum|at least)\s*(\d+(?:\.\d+)?)\s*(?:years|yrs)?"`
Safeguards validate `0.5 <= val <= 30.0` before assigning `minimum_experience_years`.

#### Salary Range Parsing
Compensation ranges are extracted using regex supporting comma-formatted amounts and shorthand 'k' notation:
- `r"\$\s*(\d{1,3}(?:,\d{3})+|\d+k?)\s*(?:-|to)\s*\$\s*(\d{1,3}(?:,\d{3})+|\d+k?)"`
- Normalizes `$165,000 - $210,000` -> `min_amount: 165000.0`, `max_amount: 210000.0`.
- Benefits list filters out salary lines to prevent redundant metadata duplication.

---

## 4. Verification & Benchmarking Results

The parsing engine was verified against the repository's 4 diverse employer job requisitions. All 4 parsed files passed 100% strict JSON Schema Draft 2020-12 validation.

| Requisition File | Role Title | Role Type | Seniority | Min Exp | Required Skills | Salary Range (USD) | Schema Status |
|---|---|---|---|---|---|---|---|
| `jd_01_senior_backend.txt` | Senior Backend Distributed Systems Engineer | `TECHNICAL` | `SENIOR` | 5.0 yrs | 6 skills (`Go`, `Python`, `PostgreSQL`, `Kubernetes`, `Docker`, `Apache Kafka`) | $165,000 – $210,000 | **VALID** |
| `jd_02_ml_engineer.txt` | Staff Machine Learning & Generative AI Engineer | `TECHNICAL` | `PRINCIPAL` | 6.0 yrs | 3 skills (`PyTorch`, `Vector Databases`, `MLOps`) | $190,000 – $240,000 | **VALID** |
| `jd_03_talent_acquisition.txt` | Senior Talent Acquisition Partner | `NON_TECHNICAL` | `SENIOR` | 5.0 yrs | 3 skills (`Technical Recruiting`, `Greenhouse ATS`, `DEI Strategy`) | $110,000 – $140,000 | **VALID** |
| `jd_04_financial_analyst.txt` | Lead Financial Planning & Analysis (FP&A) Analyst | `NON_TECHNICAL` | `LEAD` | 5.0 yrs | 5 skills (`SQL`, `Financial Modeling`, `Corporate Budgeting & FP&A`, `Advanced Excel`, `Power BI`) | $135,000 – $165,000 | **VALID** |

### Test Suite Execution (`tests/test_jd_parser.py`)
- `test_skill_synonym_resolution`: **PASSED** (Verifies aliases like `Golang`, `k8s`, `Postgres`, `AWS Cloud`).
- `test_seniority_detection_heuristics`: **PASSED** (Verifies `Senior`, `Staff`, `Lead`, `Intern`, `VP`).
- `test_role_type_classification`: **PASSED** (Verifies `TECHNICAL`, `NON_TECHNICAL`, `HYBRID`).
- `test_education_level_detection`: **PASSED** (Verifies `DOCTORATE`, `MASTER`, `BACHELOR`).
- `test_parser_on_backend_job_description`: **PASSED** (Backend skills, experience, salary & schema).
- `test_parser_on_ai_ml_job_description`: **PASSED** (Staff ML role, education & schema).
- `test_parser_on_talent_acquisition_jd`: **PASSED** (HR domain skills & schema).
- `test_parser_on_financial_analyst_jd`: **PASSED** (Corporate finance modeling & schema).
- `test_parse_and_save_generates_json_file`: **PASSED** (Disk persistence and serialization).
- `test_parser_handles_missing_file`: **PASSED** (Error handling and FileNotFoundError).

**Overall Test Results:** 10 / 10 Day 6 tests passing; 38 / 38 repository tests passing.

---

## 5. Usage Guide & Python API

### 5.1 Parsing a Job Description File
```python
from pathlib import Path
from parsers import JobDescriptionParser

parser = JobDescriptionParser()

# Parse directly from raw text file
job_profile = parser.parse_file("data/raw/job_descriptions/jd_01_senior_backend.txt")

print(f"Title: {job_profile.title}")
print(f"Role Type: {job_profile.role_type.value}")
print(f"Seniority: {job_profile.seniority_level.value}")
print(f"Minimum Experience: {job_profile.requirements.minimum_experience_years} years")
print(f"Skills: {[s.name for s in job_profile.requirements.required_skills]}")
if job_profile.salary_range:
    print(f"Salary: ${job_profile.salary_range.min_amount:,.0f} - ${job_profile.salary_range.max_amount:,.0f}")
```

### 5.2 Parsing and Persisting Structured JSON
```python
# Saves structured JSON into output directory
json_path, profile = parser.parse_and_save(
    "data/raw/job_descriptions/jd_02_ml_engineer.txt",
    output_dir="data/structured/job_descriptions"
)
print(f"Persisted to: {json_path}")
```

### 5.3 Running the Supervisor Proof Script
```powershell
.\.venv\Scripts\python.exe scripts/verify_day6.py
```
This command runs end-to-end extraction, generates structured output files, runs the test suite, validates JSON schema compliance, and writes the audit log to `logs/day6_test_results.log`.
