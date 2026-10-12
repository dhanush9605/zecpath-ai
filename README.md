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
