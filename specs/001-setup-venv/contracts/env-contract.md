# Contract: Environment Variables Configuration

**Feature**: 001-setup-venv
**Type**: Configuration Contract
**Date**: 2025-11-07

---

## Overview

This contract defines the interface between the developer's local environment (.env file) and Python scripts that need to access database credentials and API tokens.

---

## Contract Specification

### Input: .env File

**File Location**: Project root - `.env`

**Format**: Key=Value pairs (one per line)

**Required Variables**:

```env
DB_HOST=<postgresql_host>
DB_USER=<postgresql_username>
DB_PASSWORD=<postgresql_password>
API_TOKEN=<external_api_token>
```

| Variable | Type | Required | Default | Example | Notes |
|----------|------|----------|---------|---------|-------|
| `DB_HOST` | string | YES | None | `localhost` or `db.example.com` | PostgreSQL server hostname/IP |
| `DB_USER` | string | YES | None | `developer_name` or `app_user` | PostgreSQL username |
| `DB_PASSWORD` | string | YES | None | `my_secure_password` | PostgreSQL password (🔴 SENSITIVE) |
| `API_TOKEN` | string | YES | None | `sk-abc123xyz789` | External API authentication token (🔴 SENSITIVE) |

**Constraints**:
- ✅ All 4 variables are **REQUIRED** (empty values cause runtime errors)
- ✅ No spaces around `=` operator (parser is strict)
- ✅ Passwords may contain special characters (no escaping needed in quotes)
- ✅ No trailing whitespace after values
- ✅ Comments use `#` at start of line (inline comments not supported by python-dotenv)

**Example Valid .env**:
```env
# Database Configuration
DB_HOST=localhost
DB_USER=developer_01
DB_PASSWORD=P@ssw0rd!@#$%
API_TOKEN=ghp_abc123xyz789

# Note: This file is NOT versioned (in .gitignore)
```

---

### Output: Python Access Pattern

**Library**: `python-dotenv`

**Usage Pattern**:
```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
api_token = os.getenv('API_TOKEN')

# Validation (should not be None)
if not all([db_host, db_user, db_password, api_token]):
    raise ValueError("Missing required environment variables in .env")

# Use in PostgreSQL connection
import psycopg2
conn = psycopg2.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database="your_db"
)

# Use in API requests
import requests
headers = {"Authorization": f"Bearer {api_token}"}
response = requests.get("https://api.example.com/data", headers=headers)
```

---

### Test Cases

#### Test 1: Valid .env Present
```
GIVEN: .env file exists with all 4 variables populated
WHEN:  Python script imports and loads .env
THEN:  os.getenv() returns values for all variables (no None)
EXPECT: Script can establish DB connection + API calls work
```

#### Test 2: .env Missing
```
GIVEN: .env file does not exist (developer forgot cp .env.example .env)
WHEN:  Python script tries os.getenv('DB_HOST')
THEN:  Returns None (python-dotenv silently ignores missing file)
EXPECT: Script should validate and raise clear error "DB_HOST not found in .env"
```

#### Test 3: Variable Missing from .env
```
GIVEN: .env exists but DB_PASSWORD is missing
WHEN:  Python script tries os.getenv('DB_PASSWORD')
THEN:  Returns None
EXPECT: Script validation catches this and raises "Missing required: DB_PASSWORD"
```

#### Test 4: .env Visible in Git
```
GIVEN: Developer accidentally commits .env file
WHEN:  Git pre-commit checks run
THEN:  Should detect .env in staging area (if git hook exists)
EXPECT: Commit rejected with message "Remove .env - contains credentials"
```

#### Test 5: PostgreSQL Connection Failure
```
GIVEN: .env has invalid DB_HOST (server not running)
WHEN:  Script tries psycopg2.connect()
THEN:  ConnectionError is raised
EXPECT: Error message guides user to "start PostgreSQL service"
```

#### Test 6: Wrong Password
```
GIVEN: DB_PASSWORD in .env is incorrect
WHEN:  Script tries psycopg2.connect()
THEN:  OperationalError: "FATAL: password authentication failed"
EXPECT: Error message suggests "verify DB_PASSWORD in .env"
```

---

## Security Notes

🔴 **CRITICAL FIELDS**:
- `DB_PASSWORD` - Database password
- `API_TOKEN` - External API key/token

These MUST NEVER be:
- ✗ Committed to git repository
- ✗ Logged to stdout/stderr
- ✗ Sent in unencrypted HTTP requests
- ✗ Hardcoded in source files

**Protection Mechanism**:
1. `.env` is listed in `.gitignore`
2. `.env.example` is in repo without secrets (shows template only)
3. Developers copy `.env.example` → `.env` and populate with local values
4. CI/CD systems inject secrets via environment variables (not .env files)

---

## Implementation Notes (Phase 2)

1. **requirements.txt** must include `python-dotenv==1.0.*`
2. **validate-python.sh / .bat** should NOT check .env (it's created later)
3. **README Setup section** should guide: `cp .env.example .env`, then edit
4. **docs/SETUP.md** should include example safe editing (nano, vim, etc.)
5. **Future**: Add optional pre-commit hook to prevent .env commits

---

## Contract Status

✅ **APPROVED** - Ready for Phase 2 implementation

