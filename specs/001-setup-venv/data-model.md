# Data Model: Setup de Ambiente Virtual Python

**Phase**: Phase 1 (Design & Data Model)
**Date**: 2025-11-07
**Feature**: 001-setup-venv

---

## Overview

This feature is **infrastructure/setup only** - NOT a data-driven application. There is no persistent database model. Instead, this document describes the **configuration entities** and **environment state** that developers manage locally.

---

## Configuration Entities

### 1. Python Environment Config

**Purpose**: Represents the state of a developer's isolated Python environment

**Location**: Local filesystem - `./expansao/` directory

**Fields**:
- `python_version` (string, required): "3.11.x" - verified by validate-python.sh/.bat
- `venv_path` (string, required): "./expansao" - standard location
- `activation_state` (enum): "active", "inactive" - tracked in shell session
- `created_date` (datetime, implicit): When `python -m venv expansao` was run

**Validation Rules**:
- ✅ `python_version` MUST be ≥ 3.11
- ✅ `venv_path` MUST exist as directory after creation
- ✅ `venv_path` is LOCAL ONLY - never in git (protected by .gitignore)

**Lifecycle**:
1. **Initial**: Does not exist
2. **Create**: `python -m venv expansao` command
3. **Active**: Developer runs `source expansao/bin/activate` (Unix) or `expansao\Scripts\activate.bat` (Windows)
4. **In Use**: Dependencies installed via `pip install -r requirements.txt`
5. **Cleanup** (optional): `rm -rf expansao` to reset

---

### 2. Dependencies Configuration

**Purpose**: Specification of Python packages required for the project

**Location**: `requirements.txt` (text file, root of repo)

**Fields**:
- `package_name` (string): e.g., "pandas"
- `version_constraint` (string): e.g., "==2.1.*" or "==2.9.4"
- `description` (comment): Purpose of the package

**Format Example**:
```
pandas==2.1.*                   # Data manipulation for ETL
psycopg2==2.9.*                # PostgreSQL driver
python-dotenv==1.0.*           # Load .env environment variables
requests==2.31.*               # HTTP client for APIs
```

**Validation Rules**:
- ✅ ALL packages must have version constraints (no floating versions like `pandas>=2.0`)
- ✅ Pandas uses minor-pinning (`==2.1.*`), others exact (`==X.Y.Z`)
- ✅ No duplicate packages
- ✅ Each package must be pip-installable

**Lifecycle**:
1. **Created**: During Phase 2 (Task execution)
2. **Updated**: When new dependencies needed (via PR review)
3. **Locked**: After `pip install -r requirements.txt`, actual installed versions saved (optional future: requirements-lock.txt)

---

### 3. Environment Secrets Config

**Purpose**: Sensitive configuration variables (credentials, API tokens) stored locally

**Location**: `.env` file (local only, never in git)

**Template Location**: `.env.example` (in repo, no secrets)

**Fields** (4 mandatory):

| Variable | Type | Example | Sensitivity | Notes |
|----------|------|---------|-------------|-------|
| `DB_HOST` | string | `localhost` | Low | PostgreSQL server address |
| `DB_USER` | string | `developer` | Medium | PostgreSQL username |
| `DB_PASSWORD` | string | `secret_here` | 🔴 HIGH | PostgreSQL password - NEVER in git |
| `API_TOKEN` | string | `token_xyz` | 🔴 HIGH | External API authentication - NEVER in git |

**Validation Rules**:
- ✅ `.env` file is listed in `.gitignore` - never versioned
- ✅ `.env.example` exists in repo - shows REQUIRED variables without secrets
- ✅ All 4 variables are required (scripts should validate presence)
- ✅ `.env` is read by `python-dotenv` library at runtime

**Example .env.example**:
```
# PostgreSQL Connection
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password

# External APIs
API_TOKEN=your_token_here
```

**Example .env** (local, NOT versioned):
```
DB_HOST=db.internal.company.com
DB_USER=developer_name
DB_PASSWORD=my_secure_password_12345
API_TOKEN=sk-abc123xyz789
```

**Lifecycle**:
1. **Template**: `.env.example` created in Phase 2
2. **Local Copy**: Developer runs `cp .env.example .env` (or Windows equivalent)
3. **Populate**: Developer fills in real values (DB credentials, API tokens)
4. **Usage**: Python code loads via `from dotenv import load_dotenv; load_dotenv()` then `os.getenv('DB_HOST')`
5. **Protection**: Never committed; CI/CD injects secrets via other means (env vars, secrets manager)

---

### 4. Validation Scripts Config

**Purpose**: Configuration for platform-specific Python version checks

**Location**: `scripts/validate-python.sh` (Unix) and `scripts/validate-python.bat` (Windows)

**Execution**:
- **Unix** (Linux/macOS): `bash scripts/validate-python.sh`
- **Windows**: `scripts\validate-python.bat` or `call scripts\validate-python.bat`

**Output**:
- ✅ Success: "Python 3.11.x detected. Ready to proceed with pip install."
- ❌ Failure: "ERROR: Python 3.8.x found. Project requires Python 3.11+. Install from python.org and try again."

**Validation Rules**:
- ✅ Script MUST detect installed Python version
- ✅ Script MUST compare against minimum version 3.11
- ✅ Script MUST exit with code 0 on success, non-zero on failure
- ✅ Error message must be clear and actionable

**Lifecycle**:
1. **Created**: Phase 2
2. **Run**: Before `pip install -r requirements.txt`
3. **Results**: Pass → proceed; Fail → user fixes Python version

---

## No Database Schema

This feature does NOT create a database or schema. PostgreSQL connection is **tested** (User Story 4) but setup is NOT included (deferred to separate feature).

Developers are assumed to have PostgreSQL already installed and running with credentials known.

---

## State Diagram: Developer Setup Journey

```
┌─────────────────┐
│   Start: No     │
│   venv exists   │
└────────┬────────┘
         │
         ├─→ Run: python -m venv expansao
         │   [Creates: expansao/ directory]
         │
         ├─→ Run: source expansao/bin/activate (Unix)
         │   or:  expansao\Scripts\activate.bat (Windows)
         │   [State: "active"]
         │
         ├─→ Run: bash scripts/validate-python.sh
         │   [Checks: Python ≥ 3.11]
         │   [Result: PASS/FAIL]
         │
         ├─→ If FAIL: Install Python 3.11, retry script
         │
         ├─→ If PASS: Run pip install -r requirements.txt
         │   [Installs: pandas, psycopg2, python-dotenv, requests]
         │
         ├─→ Copy: cp .env.example .env
         │   [Creates: local .env with template]
         │
         ├─→ Edit: nano .env (or your editor)
         │   [Populate: DB credentials, API tokens]
         │
         ├─→ Verify: python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('DB_HOST'))"
         │   [Checks: env vars are readable]
         │
         └─→ Ready: Environment setup complete!
            Can now run ETL scripts, test DB connection, etc.
```

---

## Configuration Summary Table

| Entity | Location | Mutable | Versioned | Validation |
|--------|----------|---------|-----------|-----------|
| **Python Environment** | ./expansao/ | No (recreate if needed) | ❌ .gitignore | validate-python.sh/.bat |
| **Dependencies** | requirements.txt | Yes (via PR) | ✅ Git | pip check, pip compile |
| **Secrets** | .env (local) | Yes (manual edit) | ❌ .gitignore | Must exist + readable |
| **Validation Scripts** | scripts/*.sh/.bat | Rarely | ✅ Git | Executable + error codes |
| **Template Secrets** | .env.example | Yes (via PR) | ✅ Git | No real secrets |

---

## Notes for Implementation (Phase 2)

1. **requirements.txt** - Start with 4 core packages, can be extended later
2. **.env.example** - Document REQUIRED vs optional variables (all 4 are required initially)
3. **validate-python.sh** - Bash script checking `python3 --version` against 3.11
4. **validate-python.bat** - Batch script checking `python --version` against 3.11
5. **README Setup Section** - Clear instructions per OS with exact command sequences
6. **docs/SETUP.md** - Troubleshooting per OS (Python install, PostgreSQL issues, etc.)

---

✅ **PHASE 1 DATA MODEL COMPLETE**
