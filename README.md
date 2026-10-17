# Zecpath AI — Hiring Platform

Zecpath AI is an intelligent hiring and talent evaluation platform designed to automate and standardize candidate screening, resume parsing, applicant tracking, and interactive technical interviews.

---

## 1. Project Purpose & Scope

The goal of Zecpath AI is to streamline the hiring lifecycle using specialized, decoupled AI components:
- Standardized document extraction for candidate resumes and job descriptions.
- Objective ATS keyword alignment and qualification checks.
- Structured screening and interactive conversational interview agents.
- Comprehensive, multi-dimensional candidate evaluation and ranking.

---

## 2. Repository Structure

```text
zecpath-ai/
├── .env.example          # Environment variable template
├── .gitignore             # Comprehensive Git exclusion rules
├── pyproject.toml         # Tool configurations for pytest and Ruff
├── requirements.txt       # Project dependencies (pytest, ruff)
├── README.md              # Project documentation and setup guide
├── data/                  # Data directory for sample schemas
│   └── .gitkeep
├── parsers/               # Resume and job description parsing
│   └── __init__.py
├── ats_engine/            # ATS keyword matching and qualification rules
│   └── __init__.py
├── screening_ai/          # Candidate screening and assessment
│   └── __init__.py
├── interview_ai/          # Technical and behavioral interview modules
│   └── __init__.py
├── scoring/               # Candidate scoring and evaluation
│   └── __init__.py
├── utils/                 # Shared utilities and helpers
│   ├── __init__.py
│   └── logger.py          # Centralized logging utility with PII sanitization
└── tests/                 # Automated test suite
    ├── __init__.py
    └── test_setup.py      # Environment and module sanity tests
```

---

## 3. Environment Setup & Installation

### Prerequisites
- Python 3.10+ (Developed and verified on Python 3.12)
- Git

### Windows PowerShell Setup Instructions

1. **Clone or Navigate to the Project Directory**:
   ```powershell
   cd path\to\zecpath-ai
   ```

2. **Create the Python Virtual Environment**:
   ```powershell
   python -m venv .venv
   ```

3. **Activate the Virtual Environment**:
   ```powershell
   # If script execution is restricted, run: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

4. **Upgrade Pip and Install Dependencies**:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

---

## 4. Running Tests & Quality Checks

### Run Automated Tests
Execute the setup and sanity test suite with `pytest`:
```powershell
python -m pytest
```
For verbose output:
```powershell
python -m pytest -v
```

### Run Linting and Code Quality (Ruff)
Check for code style, import sorting, and lint errors:
```powershell
python -m ruff check .
```

To automatically apply fixes:
```powershell
python -m ruff check --fix .
```

To verify code formatting:
```powershell
python -m ruff format --check .
```

---

## 5. Logging Configuration

The project uses a centralized logging utility located at `utils/logger.py`:

```python
from utils.logger import get_logger

# Module-level logger initialization
logger = get_logger(__name__)

logger.info("Service initialized successfully.")
logger.warning("Resource usage threshold warning.")
```

### Key Features:
- **Dual Outputs**: Emits logs simultaneously to standard output (`stdout`) and persistent file storage (`logs/zecpath.log`).
- **Automatic Directory Provisioning**: Creates `logs/` directory on demand without throwing missing path errors.
- **Handler Deduplication**: Prevents duplicate log messages if `setup_logger()` is called multiple times.
- **Data Protection & PII Redaction**: Built-in filter automatically masks API keys, bearer tokens, passwords, candidate emails, and phone numbers before writing to logs.

---

## 6. Development Conventions

1. **PEP 8 Compliance**: Follow standard Python conventions enforced by Ruff.
2. **Type Annotations**: Use Python type hints on all public function signatures.
3. **No Hardcoded Secrets**: Load secrets via environment variables. Never commit `.env` or credentials to version control.
4. **Data Protection**: Never commit real candidate resumes, personal contact info, or confidential company datasets to the repository.

---

## 7. Day 4 — Data Understanding & Structuring

Day 4 establishes the standard AI data schemas and entity models for unstructured resume extraction and job description matching.

### Key Deliverables:
- **Resume Schema**: `data/schemas/resume_schema.json` (Draft 2020-12)
- **Job Description Schema**: `data/schemas/job_description_schema.json` (Draft 2020-12)
- **AI Data Entity Design Document**: `docs/AI_DATA_ENTITY_DESIGN.md`
- **Pydantic AI Models**: `parsers/models/candidate.py`, `parsers/models/job.py`, `parsers/models/entities.py`
- **10 Multi-Domain Resumes**: `data/raw/resumes/` & `data/structured/resumes/`
- **4 Tech & Non-Tech JDs**: `data/raw/job_descriptions/` & `data/structured/job_descriptions/`

### Running the Supervisor Proof Script
To verify all 10 resumes and 4 job descriptions against schemas with formatted summary tables:
```powershell
python scripts/verify_day4.py
```

### Launching the Interactive Web Dashboard
To visually inspect resumes, raw text vs structured AI JSON, and test schema validation in your browser:
```powershell
python scripts/run_viewer.py
```
Open [http://localhost:8000](http://localhost:8000) in your web browser.

---

## 8. Day 5 — Resume Text Extraction Engine

Day 5 implements the modular document text extraction, unicode cleaning, bullet point standardization, section header normalization, and table extraction engine.

### Key Deliverables:
- **Resume Text Extraction Engine**: `parsers/extractor.py` (`ResumeExtractor`, `ExtractionResult`)
- **Cleaning & Normalization Pipeline**: `parsers/cleaner.py` (Unicode, ligatures, bullets, headers, whitespace)
- **Document Readers**: `parsers/readers/` (`PDFReader`, `DOCXReader`, `BaseDocumentReader`)
- **Sample PDF & DOCX Resumes**: `data/raw/resumes/` (`resume_01_backend.docx`, `resume_02_frontend.pdf`)
- **Cleaned Outputs & Metadata**: `data/extracted/` (`*_cleaned.txt` and `*_extracted.json`)
- **Test Result Logs**: `logs/day5_test_results.log`
- **Automated Test Suite**: `tests/test_extraction_engine.py` (12 tests passing, 28 total tests in repository)

### Running Day 5 Verification & Audit Logging
To extract all resumes (PDF, DOCX, TXT), verify normalization, and generate the supervisor audit log:
```powershell
python scripts/verify_day5.py
```

### Running Day 5 Extraction Tests
```powershell
python -m pytest tests/test_extraction_engine.py -v
```

---

## 9. Day 6 — Job Description Parsing System

Day 6 implements the automated Job Description Parsing System, converting unstructured employer job postings into structured, AI-readable `JobProfile` and `JobRequirements` objects conforming strictly to Draft 2020-12 schema standards.

### Key Deliverables:
- **Job Description Parser**: `parsers/jd_parser.py` (`JobDescriptionParser` with text cleaning, semantic section segmentation, experience parsing, and salary extraction)
- **Taxonomy & Synonym Resolution Engine**: `parsers/taxonomy.py` (`CanonicalSkill`, `SKILL_TAXONOMY`, `SYNONYM_LOOKUP`, `resolve_skill_synonym`, `detect_seniority`, `detect_role_type`, `detect_education_level`)
- **Structured JD Output Samples**: `data/structured/job_descriptions/` (`jd_01_senior_backend.json`, `jd_02_ml_engineer.json`, `jd_03_talent_acquisition.json`, `jd_04_financial_analyst.json`)
- **JD Parsing Architecture Documentation**: `docs/JD_PARSING_DOCUMENTATION.md`
- **Supervisor Proof Runner**: `scripts/verify_day6.py` (Parses all JDs, validates schema, prints summary table, runs pytest, generates proof log)
- **Verification Audit Report**: `logs/day6_test_results.log`
- **Automated Test Suite**: `tests/test_jd_parser.py` (10 tests passing; 38/38 total repository tests passing)

### Running Day 6 Verification & Audit Logging
To parse all job descriptions, validate schema compliance, run tests, and generate the supervisor audit log:
```powershell
python scripts/verify_day6.py
```

### Running Day 6 Automated Tests
```powershell
python -m pytest tests/test_jd_parser.py -v
```

### Running the Entire Repository Test Suite (38 Tests)
```powershell
python -m pytest -v
```
