---
description: "Task list for 001-setup-venv feature implementation"
---

# Tasks: Setup de Ambiente Virtual Python

**Input**: Design documents from `/specs/001-setup-venv/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Tests**: Not requested for this feature - setup/infrastructure tooling does not require unit/integration tests. Manual validation per task applies.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Path Conventions

- **Root**: Project repository root where `README.md`, `requirements.txt` reside
- **Scripts**: `scripts/validate-python.sh` (Unix) and `scripts/validate-python.bat` (Windows)
- **Docs**: `docs/SETUP.md` for detailed troubleshooting
- **Config**: `.env.example`, `.gitignore` at root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure. Create all shared files needed by all user stories.

- [x] T001 Create project structure: create `docs/` and `scripts/` directories (repository root)
- [x] T002 [P] Create `scripts/validate-python.sh` (bash script) to validate Python 3.11+ for Linux/macOS
- [x] T003 [P] Create `scripts/validate-python.bat` (batch script) to validate Python 3.11+ for Windows
- [x] T004 Create `requirements.txt` (repository root) with 4 pinned dependencies: pandas==2.1.*, psycopg2==2.9.*, python-dotenv==1.0.*, requests==2.31.*
- [x] T005 [P] Create `.env.example` (repository root) with 4 required variables: DB_HOST, DB_USER, DB_PASSWORD, API_TOKEN (no secrets, templates only)
- [x] T006 Update `.gitignore` (repository root) to protect: `.env` (credentials), `expansao/` (virtual environment), standard Python ignores

**Checkpoint**: All shared infrastructure files created. Ready to proceed with user story implementation.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core documentation that MUST be complete before ANY user story can be tested

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create `docs/SETUP.md` (detailed guide) with sections:
  - Overview of all 3 platforms (Windows, macOS, Linux)
  - Python 3.11+ installation guide per OS with links
  - PostgreSQL installation and verification per OS
  - Virtual environment creation and activation (3 variants)
  - pip troubleshooting (permissions, offline, version conflicts)
  - Credential (.env) validation checklist
  - Common error messages and solutions per OS

- [x] T008 Update `README.md` (repository root) with new "🚀 Quick Setup" section containing:
  - Prerequisites (Python 3.11, PostgreSQL)
  - 3 separate command blocks (Windows CMD/PowerShell, macOS, Linux)
  - Exact commands for: validate-python script, create venv, activate venv, pip install, .env copy, .env edit
  - Quick troubleshooting (3-5 common issues)
  - Reference to docs/SETUP.md for detailed help
  - Estimated time: ~10 minutes

**Checkpoint**: Foundation complete - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Criar e Ativar Ambiente Virtual (Priority: P1) 🎯 MVP

**Goal**: Developers can create and activate isolated Python 3.11 environment named `expansao`

**Independent Test**:
- Can create venv via `python -m venv expansao`
- Can activate via `source expansao/bin/activate` (Unix) or `expansao\Scripts\activate.bat` (Windows)
- Prompt changes indicating active environment
- `python --version` shows 3.11.x

### Implementation for User Story 1

- [ ] T009 [US1] Implement validate-python.sh (scripts/validate-python.sh):
  - Check for `python3 --version`
  - Compare against minimum 3.11
  - Return clear error if version < 3.11 with installation link
  - Exit code 0 on success, non-zero on failure

- [ ] T010 [US1] Implement validate-python.bat (scripts/validate-python.bat):
  - Check for `python --version`
  - Compare against minimum 3.11
  - Return clear error if version < 3.11 with installation link
  - Exit code 0 on success, 1 on failure

- [ ] T011 [US1] Update README.md Setup section - venv creation subsection:
  - Exact command: `python -m venv expansao` (works identically on all 3 OS)
  - Explain what venv folder contains (bin/, lib/, etc.)
  - Show folder structure created

- [ ] T012 [US1] Update README.md Setup section - activation subsection:
  - Linux/macOS command: `source expansao/bin/activate`
  - Windows CMD command: `expansao\Scripts\activate.bat`
  - Windows PowerShell command: `& "expansao\Scripts\Activate.ps1"`
  - What to expect: prompt changes to show `(expansao)`

- [ ] T013 [US1] Document in docs/SETUP.md - venv section:
  - Screenshots or examples of each OS after activation
  - How to deactivate: `deactivate` command
  - How to delete venv if corrupted: `rm -rf expansao` (Unix) or `rmdir /s expansao` (Windows)
  - Difference between venv and system Python

**Checkpoint**: User Story 1 complete - developers can create + activate venv independently

---

## Phase 4: User Story 2 - Instalar Dependências com Pinned Versions (Priority: P1)

**Goal**: All required packages installed with exact versions for reproducible environment

**Independent Test**:
- `pip install -r requirements.txt` completes without errors
- `pip list` shows: pandas 2.1.x, psycopg2 2.9.x, python-dotenv 1.0.x, requests 2.31.x
- `python -c "import pandas, psycopg2, dotenv, requests; print('OK')"` prints OK

### Implementation for User Story 2

- [ ] T014 [US1] Create requirements.txt (repository root) with exact format:
  ```
  pandas==2.1.*
  psycopg2==2.9.*
  python-dotenv==1.0.*
  requests==2.31.*
  ```
  - Each line: `package==version` (no spaces)
  - Comments above each line explaining purpose
  - Keep file minimal (4 packages only)

- [ ] T015 [US2] Update README.md Setup section - pip install subsection:
  - Command: `pip install -r requirements.txt`
  - Explain what pip does (installs packages to venv, not system)
  - Expected output: "Successfully installed pandas-2.1.x psycopg2-2.9.x..."
  - Estimated time: 2-3 minutes

- [ ] T016 [US2] Document in docs/SETUP.md - dependencies section:
  - What each package does:
    - pandas: Data manipulation for ETL
    - psycopg2: PostgreSQL connection driver
    - python-dotenv: Load .env environment variables
    - requests: HTTP client for APIs
  - How to add new dependencies: edit requirements.txt, run pip install again
  - How to fix "conflicting dependencies" error (with 3 common solutions)
  - How to check installed versions: `pip list`

- [ ] T017 [US2] Add validation script reference in README.md:
  - Recommend running `scripts/validate-python.sh` or `.bat` BEFORE `pip install`
  - This prevents "Python version too old" errors from appearing during install

**Checkpoint**: User Stories 1 & 2 complete - venv created, dependencies installed

---

## Phase 5: User Story 3 - Configurar Arquivo .env para Credenciais (Priority: P1)

**Goal**: Developer has secure local .env file with required 4 variables, protected from git

**Independent Test**:
- `.env` file exists locally (not in git)
- `cat .env` (or `type .env` on Windows) shows DB_HOST, DB_USER, DB_PASSWORD, API_TOKEN
- `git status | grep .env` returns empty (proof .env is ignored)
- `python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('DB_HOST'))"` prints value (proof vars readable)

### Implementation for User Story 3

- [ ] T018 [P] [US3] Create `.env.example` (repository root) with exact format:
  ```
  # PostgreSQL Connection (REQUIRED)
  DB_HOST=localhost
  DB_USER=your_username
  DB_PASSWORD=your_password

  # External APIs (REQUIRED)
  API_TOKEN=your_token_here
  ```
  - Comments explain each variable
  - No actual secrets (all template values)
  - Format: `VAR_NAME=value` (no spaces around =)

- [ ] T019 [P] [US3] Update `.gitignore` (repository root) to include:
  - `.env` (must never be versioned - credentials)
  - `expansao/` (virtual environment - local only)
  - Standard Python: `__pycache__/`, `*.pyc`, `*.pyo`, `.pytest_cache/`, etc.
  - Verify: `git status` should not show .env or expansao/

- [ ] T020 [US3] Update README.md Setup section - .env subsection:
  - Command: `cp .env.example .env` (Unix) or `copy .env.example .env` (Windows)
  - Instruction: "Edit .env with your PostgreSQL credentials and API token"
  - Command: `nano .env` (Unix) or `notepad .env` (Windows)
  - Warning: "Never commit .env to git - it contains passwords!"
  - Show example of filled .env (with fake but realistic values)

- [ ] T021 [US3] Document in docs/SETUP.md - .env section:
  - Full explanation of each 4 variables:
    - DB_HOST: PostgreSQL server address (e.g., localhost, db.company.com)
    - DB_USER: PostgreSQL username (e.g., developer_name, app_user)
    - DB_PASSWORD: PostgreSQL password (🔴 SENSITIVE - never log this)
    - API_TOKEN: External API key/token (🔴 SENSITIVE - never log this)
  - How to verify .env works: `python -c "from dotenv import load_dotenv..."` test
  - Common issues:
    - ".env not found" → copy .env.example first
    - "Variable returns None" → check spelling in .env
    - "Permission denied editing .env" → use proper editor or sudo

- [ ] T022 [US3] Create security validation in docs/SETUP.md:
  - Section "Security Checklist":
    - ✅ .env is in .gitignore
    - ✅ .env is NOT committed (verify: git log --all -- .env should be empty)
    - ✅ .env.example in repo has NO secrets
    - ✅ Python code uses `load_dotenv()` before accessing credentials

**Checkpoint**: User Stories 1, 2, 3 complete - environment setup ready for database testing

---

## Phase 6: User Story 4 - Testar Conexão com PostgreSQL (Priority: P2)

**Goal**: Developer can verify PostgreSQL connectivity before starting ETL development

**Independent Test**:
- PostgreSQL service is running
- Script `python scripts/test-connection.py` (to be created in Phase 2 Polish) succeeds with "Connection OK"
- Or manual test: `python -c "import psycopg2; conn = psycopg2.connect(host='localhost', user='...', password='...', database='postgres'); print('OK'); conn.close()"`

### Implementation for User Story 4

- [x] T023 [US4] Create `scripts/test-postgres-connection.py` (Python script):
  - Imports: psycopg2, os, dotenv
  - Loads .env via `load_dotenv()`
  - Tries to connect using DB_HOST, DB_USER, DB_PASSWORD from .env
  - On success: prints "✓ PostgreSQL connection OK" + connection details
  - On failure: prints clear error message (host not found, password wrong, etc.)
  - Returns exit code 0 on success, 1 on failure

- [ ] T024 [US4] Update README.md Setup section - PostgreSQL test subsection:
  - Command: `python scripts/test-postgres-connection.py`
  - What to expect: "✓ PostgreSQL connection OK" message
  - If fails: Reference docs/SETUP.md "Troubleshooting PostgreSQL Connection"

- [ ] T025 [US4] Document in docs/SETUP.md - PostgreSQL connection section:
  - How to install PostgreSQL per OS (with links):
    - macOS: `brew install postgresql@14` + `brew services start postgresql@14`
    - Linux: `apt-get install postgresql` + `sudo systemctl start postgresql`
    - Windows: Download from postgresql.org, run installer
  - How to verify PostgreSQL is running:
    - macOS: `brew services list | grep postgres`
    - Linux: `sudo systemctl status postgresql`
    - Windows: Check Services app
  - How to create user/database (if needed):
    - `createuser -P your_username` (macOS/Linux)
    - SQL script on Windows
  - Common PostgreSQL errors and fixes:
    - "could not connect to server" → PostgreSQL not running
    - "password authentication failed" → wrong password in .env
    - "FATAL: database 'X' does not exist" → create database first
    - "permission denied" → check PostgreSQL user permissions

**Checkpoint**: All User Stories complete - environment fully ready for ETL development

---

## Phase 7: User Story 5 - Documentação Completa no README (Priority: P1)

**Goal**: Complete README with clear setup instructions for all 3 platforms + troubleshooting

**Independent Test**:
- README.md has "Setup" section with subsections: Prerequisites, Quick Setup (3 OS variants), Validation, Troubleshooting
- New developer can follow README alone and complete setup successfully
- All commands are copy-paste ready (no placeholders)
- Links to PostgreSQL, Python downloads are present

### Implementation for User Story 5

- [ ] T026 [US5] Complete README.md "Setup" section structure:
  - **Prerequisites**: List Python 3.11+, PostgreSQL, pip
  - **Quick Setup**: 3 separate command blocks (Windows, macOS, Linux)
  - **Validation Checklist**: 6-8 checkboxes (venv created, activated, deps installed, .env exists, .env ignored, vars readable)
  - **Quick Troubleshooting**: 5 common issues with solutions
  - **What's Next**: Reference to docs/SETUP.md, next steps

- [ ] T027 [US5] Add links to external resources in README.md:
  - Python 3.11 download: https://www.python.org/downloads/
  - PostgreSQL: https://www.postgresql.org/download/
  - Virtual environments: https://docs.python.org/3/tutorial/venv.html
  - python-dotenv: https://github.com/theskumar/python-dotenv

- [ ] T028 [US5] Format README.md Setup section for readability:
  - Use clear headings (##, ###)
  - Use code blocks with language tags (```bash, ```batch, ```python)
  - Use emoji for visual clarity (🚀, ✅, ❌, ⚠️)
  - Keep lines under 100 chars where possible
  - Add horizontal separators between sections

- [ ] T029 [US5] Create summary table in README.md showing:
  - | Step | Command | Expected Output | Time |
  - 1. Validate Python | `scripts/validate-python.sh` | "Python 3.11.x detected" | <1min |
  - 2. Create venv | `python -m venv expansao` | Folder created | <1min |
  - ... etc for all 7 steps
  - Total estimated time: ~10 minutes

**Checkpoint**: User Story 5 complete - README fully documents setup for all platforms

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validations, testing, and documentation completeness

- [ ] T030 [P] Validate all file paths in README.md and docs/SETUP.md:
  - Run grep to find any hardcoded example paths that don't exist
  - Verify all scripts are referenced with correct paths: `scripts/validate-python.sh`, `scripts/validate-python.bat`
  - Verify all docs are referenced: `docs/SETUP.md`

- [ ] T031 [P] Test validate-python.sh on actual macOS/Linux machine:
  - With Python 3.11 installed: script should return success
  - With Python 3.9 installed: script should return clear error
  - Verify exit codes (0 = success, 1 = error)

- [ ] T032 [P] Test validate-python.bat on actual Windows machine:
  - With Python 3.11 installed: script should return success
  - With Python 3.8 installed: script should return clear error
  - Verify exit codes (0 = success, 1 = error)

- [ ] T033 [P] Test requirements.txt on each OS:
  - Linux: `pip install -r requirements.txt` should complete without errors
  - macOS: Same test
  - Windows: Same test
  - Verify exact versions installed: `pip show pandas | grep Version`

- [ ] T034 [P] Test .env.example → .env workflow:
  - `cp .env.example .env` (Unix) or `copy .env.example .env` (Windows)
  - Verify .env is created
  - Verify .gitignore protects it: `git status | grep .env` returns empty
  - Verify variables are readable: Load in Python and print each

- [ ] T035 Manual test: New developer setup (final validation):
  - Have someone not involved in project follow README alone
  - Time them (should be <10 minutes)
  - Collect feedback on unclear sections
  - Update README/docs based on feedback
  - Document success: "✅ Setup completed in X minutes"

- [ ] T036 Verify all .gitignore rules work:
  - Create test `.env` with fake credentials
  - Run `git add .env` - should fail or warn
  - Verify `git status` does not show .env
  - Verify `git status` does not show `expansao/`
  - Clean up test files

- [ ] T037 Final documentation review:
  - README.md: Clear, complete, no TODOs
  - docs/SETUP.md: Covers all 3 OS + all common errors
  - requirements.txt: Comments explain each package
  - .env.example: Template values realistic, comments clear
  - scripts/validate-python.sh: Executable (chmod +x), clear output
  - scripts/validate-python.bat: Runnable on Windows CMD, clear output

- [ ] T038 Create TROUBLESHOOTING summary in docs/SETUP.md appendix:
  - Quick reference table: Issue → Root Cause → Solution
  - Links to detailed sections for each issue
  - Examples of actual error messages + fixes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately ✅
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories ✅
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - **US1** (venv creation): No dependencies on other stories
  - **US2** (dependencies): Can start after US1 (or parallel if separate tasks)
  - **US3** (.env config): No dependencies on US2
  - **US4** (PostgreSQL test): Depends on US3 (needs .env) and US2 (needs python-dotenv installed)
  - **US5** (README docs): No dependencies on other stories (can run parallel)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundation: README + docs/SETUP.md)
    ↓
    ├─→ US1 (venv) ────────────┐
    │                           │
    ├─→ US2 (pip install) ──────┼──→ US4 (PostgreSQL test)
    │      ↑                    │
    │      └────────────────────┘
    │
    ├─→ US3 (.env config) ──────┐
    │                           │
    └─→ US5 (README) ───────────┴──→ Polish Phase
```

### Within Each User Story

- Setup files are created first (scripts, templates)
- README sections added
- Detailed documentation in docs/SETUP.md
- Each user story independently testable by end of its phase

### Parallel Opportunities

**Phase 1 (Setup) - T002 & T003 can run in parallel**:
- Task: "Create validate-python.sh"
- Task: "Create validate-python.bat"
- (Different files, no dependencies)

**Phase 1 (Setup) - T004 & T005 can run in parallel**:
- Task: "Create requirements.txt"
- Task: "Create .env.example"
- (Different files, no dependencies)

**Phase 3-5 (User Stories) - Can run in parallel**:
- US1 (venv creation) + US3 (.env config) + US5 (README docs) can proceed in parallel
- US2 (pip install) can start after US1
- US4 (PostgreSQL test) depends on US2 + US3, but can start once those are done

**Phase 7 (Testing) - T031, T032, T033, T034, T036 can run in parallel**:
- Each OS test (Windows, macOS, Linux) is independent
- Requirements.txt test is independent
- .env workflow test is independent
- gitignore validation is independent

---

## Parallel Example: Full Feature

**Estimated Timeline: 2-3 hours (1 developer)**

```
Time | Phase 1 (Shared) | US1 (P1)    | US2 (P1)    | US3 (P1)    | US5 (P1)    | Polish
-----|------------------|-------------|-------------|-------------|-------------|--------
 0h  | T001             |             |             |             |             |
     | T002, T003 [P]   |             |             |             |             |
     | T004, T005 [P]   |             |             |             |             |
     | T006             |             |             |             |             |
-----|------------------|-------------|-------------|-------------|-------------|--------
 30m |                  | T009, T010  | T014        | T018, T019  | T026        |
     |                  | T011, T012  | T015, T016  | T020        | T027, T028  |
     |                  | T013        | T017        | T021, T022  | T029        |
-----|------------------|-------------|-------------|-------------|-------------|--------
 1h5m| Phase 1 DONE     | US1 DONE    | US2 DONE    | US3 DONE    | US5 DONE    |
     |                  |             |             |             |             |
     |                  |             |             | T023        |             |
     |                  |             |             | T024, T025  |             |
-----|------------------|-------------|-------------|-------------|-------------|--------
 1h45m                                            | US4 DONE    |             |
-----|------------------|-------------|-------------|-------------|-------------|--------
 2h  |                  |             |             |             |             | Polish
     |                  |             |             |             |             | T030-T038
-----|------------------|-------------|-------------|-------------|-------------|--------
 3h  |                  |             |             |             |             | ✅ DONE
```

---

## Parallel Team Strategy

**With 3 developers**:

1. **Developer A**: US1 (venv creation) + US2 (pip install)
2. **Developer B**: US3 (.env config) + US4 (PostgreSQL test)
3. **Developer C**: US5 (README & docs) + Phase 1 (Shared setup)
4. **All together**: Phase 2 (Foundation) + Phase 7 (Polish & testing)

Timeline: ~2 hours parallel, then 30 min polish.

---

## Implementation Strategy

### MVP First (Minimum Viable Setup)

**Goal**: New developer can complete basic setup in ~10 minutes

1. ✅ Complete Phase 1: Setup (shared files)
2. ✅ Complete Phase 2: Foundation (README + docs)
3. ✅ Complete US1: Create venv
4. ✅ Complete US2: Install dependencies
5. ✅ Complete US3: .env configuration
6. **STOP and VALIDATE**: Test venv creation + pip install + .env loading manually
7. Deploy/Document this MVP state

### Incremental Delivery

1. Phase 1 + 2 (foundation) → Team can proceed with any story
2. Add US1 (venv) → Test venv creation independently
3. Add US2 (pip install) → Test dependencies independently
4. Add US3 (.env) → Test credential loading independently
5. Add US4 (PostgreSQL test) → Test database connectivity independently
6. Add US5 (README) → Test documentation completeness independently
7. Phase 7 (Polish) → Final validation across all platforms

Each story adds value without breaking previous stories.

---

## Notes

- **[P] tasks** = Different files, no dependencies on incomplete tasks
- **[Story] label** = Maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Setup files (requirements.txt, .env.example) are "Foundational" - affect all stories
- Documentation (README, docs/SETUP.md) should be created early and refined per story
- Test on actual hardware (3 OS minimum) before declaring complete

---

## Task Summary

| Phase | Count | Purpose |
|-------|-------|---------|
| Phase 1 (Setup) | 6 | Shared infrastructure |
| Phase 2 (Foundation) | 2 | Blocking prerequisites |
| Phase 3 (US1 - venv) | 5 | Virtual environment creation |
| Phase 4 (US2 - pip) | 4 | Dependency installation |
| Phase 5 (US3 - .env) | 5 | Credentials configuration |
| Phase 6 (US4 - PostgreSQL) | 3 | Database connectivity test |
| Phase 7 (US5 - README) | 5 | Documentation completeness |
| Phase 8 (Polish) | 9 | Testing & validation |
| **TOTAL** | **38 tasks** | Ready for implementation |

---

✅ **ALL TASKS READY FOR EXECUTION**

Start with Phase 1, proceed through phases sequentially, or parallelize within phase constraints documented above.
