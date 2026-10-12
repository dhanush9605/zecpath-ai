# Zecpath AI — Hiring Platform

Zecpath AI is an intelligent hiring and talent evaluation platform designed to automate and standardize candidate screening, resume parsing, applicant tracking, and interactive technical interviews.

---

## 1. Project Purpose & Scope

The goal of Zecpath AI is to streamline the hiring lifecycle using specialized, decoupled AI components:
- Standardized document extraction for candidate resumes and job descriptions.
- Objective ATS keyword alignment and qualification checks.
- Structured screening and interactive conversational interview agents.
- Comprehensive, multi-dimensional candidate evaluation and ranking.

### Current Implementation Status (Day 3: Environment & Repository Setup)
- **Implemented (Day 3)**:
  - Repository directory structure and modular Python packages (`parsers`, `ats_engine`, `screening_ai`, `interview_ai`, `scoring`, `utils`).
  - Isolated virtual environment configuration (`.venv`).
  - Production-grade logging utility (`utils/logger.py`) supporting console and file logging, automatic directory provisioning, duplicate handler avoidance, and PII/credential redaction.
  - Automated setup and sanity test suite (`tests/test_setup.py`) using `pytest`.
  - Code formatting and linting setup with `ruff`.
  - Secure Git configuration excluding virtual environments, cache files, environment secrets, and sensitive candidate records.
- **Future Deliverables (Days 4+)**:
  - Implementation of individual AI engines (ATS matching, parser extractors, screening intelligence, interactive interview engines, and scoring algorithms).

---

## 2. Repository Structure

```text
zecpath-ai/
├── .env.example          # Environment variable template (copy to .env locally)
├── .gitignore             # Comprehensive Git exclusion rules
├── pyproject.toml         # Tool configurations for pytest and Ruff
├── requirements.txt       # Project dependencies (pytest, ruff)
├── README.md              # Project documentation and setup guide
├── data/                  # Data directory for sample schemas (candidate PII strictly excluded)
│   └── .gitkeep
├── parsers/               # Resume and job description document extraction
│   └── __init__.py
├── ats_engine/            # ATS keyword matching, qualification rules, and profile indexing
│   └── __init__.py
├── screening_ai/          # Candidate pre-screening and qualification assessment
│   └── __init__.py
├── interview_ai/          # Technical and behavioral conversational interview agents
│   └── __init__.py
├── scoring/               # Multi-stage evaluation score aggregation and ranking
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

1. **Clone or Navigate to the Workspace**:
   ```powershell
   cd c:\Users\dhanu\Downloads\Zescer\zecpath-ai
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

5. **Configure Environment Variables**:
   ```powershell
   Copy-Item .env.example .env
   ```

---

## 4. Running Tests & Quality Checks

### Run Automated Tests
Execute the setup and sanity test suite with `pytest`:
```powershell
pytest
```
For verbose output:
```powershell
pytest -v
```

### Run Linting and Code Quality (Ruff)
Check for code style, import sorting, and lint errors:
```powershell
ruff check .
```

To automatically apply fixes:
```powershell
ruff check --fix .
```

To verify code formatting:
```powershell
ruff format --check .
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
