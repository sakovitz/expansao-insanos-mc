# Research: Setup de Ambiente Virtual Python

**Phase**: Phase 0 (Research & Technical Decisions)
**Date**: 2025-11-07
**Feature**: 001-setup-venv

---

## 1. Virtual Environment Name

### Decision: `expansao` as Environment Folder Name

**Rationale**:
- Reflects project identity (Insanos MC Expansão)
- More descriptive than generic `venv`
- Consistent across all developer machines
- Aligns with project branding

**Activation Commands**:
- macOS/Linux: `source expansao/bin/activate`
- Windows: `expansao\Scripts\activate.bat`

**Implementation**: All docs and scripts reference `expansao` instead of `venv`

---

## 2. Versioning Strategy for Dependencies

### Decision: Minor-Pinned Versioning for Pandas (==2.1.*)

**Rationale**:
- Pandas 2.1.* provides security patches and bugfixes automatically
- Major version bumps (2.x → 3.x) are rare in Pandas and would be breaking
- Minor pinning balances stability (no surprise major changes) with maintenance (auto-patch)
- Aligns with production best practices for data engineering

**Alternatives Considered**:
- **Exact pinning** (e.g., pandas==2.1.4): Maximum control but requires manual updates for security patches ❌ More maintenance burden
- **Major pinning** (e.g., pandas==2.*): Flexible but risks breaking changes ❌ Not acceptable for ETL
- **No pinning** (e.g., pandas>=2.0): Unpredictable across environments ❌ Violates Constituição IV (versões cravadas)

**Implementation**: `requirements.txt` will list `pandas==2.1.*` instead of exact version

---

## 3. PostgreSQL Driver Choice

### Decision: psycopg2 as Primary with psycopg3 as Alternative

**Rationale**:
- psycopg2 (v2.9+): Mature, stable, widely used in Python ecosystem, excellent connection pooling
- psycopg3 (v3.1+): Async support, type hints, but newer - fewer examples/docs for beginners
- psycopg2 fits better with goal of "easy onboarding" for Engenheiros Iniciantes

**Alternatives Considered**:
- **SQLAlchemy ORM**: Over-engineered for simple connection setup ❌
- **asyncpg**: Async only, not needed for init setup ❌
- **pymysql**: Wrong database (we need PostgreSQL) ❌

**Implementation**: `requirements.txt` lists `psycopg2==2.9.*` with note "psycopg3==3.1.* available if async needed"

---

## 4. Environment Variable Loading

### Decision: python-dotenv Library

**Rationale**:
- `python-dotenv` is the standard for loading .env files in Python
- Simple API: `from dotenv import load_dotenv; os.getenv('VAR_NAME')`
- Used by nearly all Python projects (Flask, Django, FastAPI)
- Single file dependency (not heavy)

**Alternatives Considered**:
- **Manual os.environ parsing**: ❌ No .env file support, error-prone
- **python-decouple**: ❌ Over-featured, less community adoption than python-dotenv
- **environs**: ❌ Type casting adds complexity for setup phase

**Implementation**: `requirements.txt` lists `python-dotenv==1.0.*`

---

## 5. HTTP Client Library

### Decision: requests (Standard HTTP Library)

**Rationale**:
- `requests` is the de facto standard for HTTP in Python ("Requests: HTTP for Humans™")
- Used for API integrations mentioned in feature spec
- Simple, intuitive, excellent documentation
- Community consensus across all Python frameworks

**Alternatives Considered**:
- **urllib3**: ❌ Lower level, requires more code
- **httpx**: ❌ Newer, async-focused (not needed for init)
- **aiohttp**: ❌ Async only, overkill for API integration testing

**Implementation**: `requirements.txt` lists `requests==2.31.*`

---

## 6. Multi-OS Setup Support (Windows/macOS/Linux)

### Decision: Native Scripts for Each OS (validate-python.sh + validate-python.bat)

**Rationale**:
- venv creation is slightly different: `python -m venv expansao` (all OS) vs activate scripts
- Windows uses `expansao\Scripts\activate.bat` vs Unix `source expansao/bin/activate`
- Providing BOTH scripts removes ambiguity: each OS runs their native validation
- Cross-platform compatibility without compromise (no shell compatibility hacks)

**Scripts to Create**:
1. **validate-python.sh** (macOS/Linux):
   - Uses bash syntax
   - Checks `python3 --version` ≥ 3.11
   - Returns clear error if version < 3.11
   - Executable: `bash scripts/validate-python.sh`

2. **validate-python.bat** (Windows):
   - Uses batch/cmd syntax
   - Checks `python --version` ≥ 3.11
   - Returns clear error if version < 3.11
   - Executable: `scripts\validate-python.bat` or `call scripts\validate-python.bat`

**Implementation**:
- Both scripts in `scripts/` directory
- README documents each OS separately with correct script path
- Clear instructions: "Linux/macOS run this → Windows run that"

**Alternatives Considered**:
- **Single bash script**: ❌ Doesn't work natively on Windows (requires WSL/Git Bash)
- **Python cross-platform script**: ✅ Could work, but native scripts clearer for beginners
- **Docker**: ❌ Out of scope (infrastructure dependency too heavy)

---

## 7. .env.example Template Variables

### Decision: 4 Mandatory Variables (Clarification Session Confirmed)

**Variables**:
1. `DB_HOST` - PostgreSQL server hostname (e.g., localhost)
2. `DB_USER` - PostgreSQL username
3. `DB_PASSWORD` - PostgreSQL password (marked as sensitive)
4. `API_TOKEN` - Generic placeholder for external API tokens

**Rationale**:
- DB_HOST, DB_USER, DB_PASSWORD needed for PostgreSQL connectivity (User Story 4)
- API_TOKEN covers generic case for "Também fará conexões via API" requirement
- Exactly 4 variables keep setup simple but comprehensive
- All marked as "required" in .env.example comments

**Alternatives Considered**:
- **No template** (developers guess variables): ❌ Poor UX, error-prone
- **20+ variables**: ❌ Overkill for initial setup, confusing
- **Optional variables**: ❌ Lack of clarity defeats purpose

**Implementation**: `.env.example` created with 4 lines, all commented with descriptions

---

## 8. Troubleshooting Documentation

### Decision: Two-Level Approach (Clarification Session FR-014)

**Level 1**: README "Quick Troubleshooting" section (5-10 common issues)
- Python version mismatch
- PostgreSQL not running
- pip permission denied (macOS/Linux)
- Conflicting dependency versions

**Level 2**: `docs/SETUP.md` detailed guide (deep dives per issue)
- How to install Python 3.11 on each OS
- PostgreSQL setup guide (with links)
- Virtual environment corruption recovery
- .env validation checklist

**Rationale**:
- README keeps setup flow visible (not too long)
- docs/SETUP.md provides escape hatch for complex issues
- Aligns with Constituição II (Documentação Mandatória - runbooks detalhados)

**Implementation**:
- README: ~200 words of common fixes
- docs/SETUP.md: ~1000 words of comprehensive guide

---

## 9. .gitignore Updates

### Decision: Explicit `.env` Rule + Standard Ignores

**Rationale**:
- `.env` must NEVER be versioned (Constituição III - credential protection)
- `expansao/` folder (venv) must be ignored (local only)
- Standard Python ignores: `__pycache__`, `*.pyc`, `*.pyc`, etc.
- Explicit is better than implicit (PEP 20)

**Implementation**:
```gitignore
# Credentials
.env

# Virtual environments
expansao/
venv/
.venv/
env/

# Python
__pycache__/
*.pyc
*.pyo
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
```

---

## 10. Requirements.txt Exact Versions (Clarification + Spec)

### Decision: pandas==2.1.* with all other deps exactly pinned

**Core dependencies**:
```
pandas==2.1.*
psycopg2==2.9.*
python-dotenv==1.0.*
requests==2.31.*
```

**Rationale**:
- Pandas minor-pinned (clarification confirmed)
- Other libraries exact-pinned (common practice, avoids surprise upgrades)
- `pip install -r requirements.txt` produces IDENTICAL results across machines/OSes

**Alternatives Considered**:
- **All floating**: ❌ Violates FR-003 (exatas fixadas)
- **All exact**: ✅ Works but too strict; minor upgrades safe
- **Mixed approach**: ✅ Selected - minor for Pandas, exact for others

**Implementation**: `requirements.txt` created with 4 lines, ready for Phase 2 tasks

---

## Summary: All Phase 0 Decisions Complete

| Decision Area | Choice | Confidence |
|---------------|--------|-----------|
| venv Name | `expansao` folder | ✅ High |
| Python Validation | Both `.sh` and `.bat` scripts | ✅ High |
| Pandas Versioning | Minor-pinned (==2.1.*) | ✅ High |
| PostgreSQL Driver | psycopg2 v2.9+ | ✅ High |
| Env Loading | python-dotenv | ✅ High |
| HTTP Client | requests | ✅ High |
| Multi-OS Support | Native scripts per OS | ✅ High |
| .env Variables | 4 mandatory (DB_HOST, DB_USER, DB_PASSWORD, API_TOKEN) | ✅ High |
| Troubleshooting | 2-level (README + docs/SETUP.md) | ✅ High |
| requirements.txt | Minor-pinned Pandas + exact others | ✅ High |

✅ **PHASE 0 COMPLETE** - All research questions answered, ready for Phase 1 Design
