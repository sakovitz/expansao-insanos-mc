# Implementation Plan: Setup de Ambiente Virtual Python

**Branch**: `001-setup-venv` | **Date**: 2025-11-07 | **Spec**: `/specs/001-setup-venv/spec.md`
**Input**: Feature specification for environment virtualization setup with Python, venv, requirements.txt, .env, PostgreSQL, and Pandas

**Note**: This plan covers environment setup infrastructure - NOT application code development.

## Summary

Estabelecer um ambiente virtual isolado com Python 3.11 para o projeto Insanos MC Expansão, incluindo gerenciamento de dependências com versões fixadas (Pandas 2.1.*, drivers PostgreSQL), proteção de credenciais via .env, e documentação clara de setup para Windows, macOS, e Linux. Inclui scripts de validação e troubleshooting para evitar erros comuns de instalação.

## Technical Context

**Language/Version**: Python 3.11 (stable, good library support, released 2022)
**Primary Dependencies**: Pandas (==2.1.*), psycopg2/psycopg3 (PostgreSQL), python-dotenv (env loading), requests (HTTP API)
**Storage**: PostgreSQL (external, assumed installed - NOT included in this feature)
**Testing**: Manual testing (no unit tests needed for setup tooling)
**Target Platform**: Windows, macOS, Linux (multi-OS support required)
**Project Type**: CLI/Data Engineering (venv + requirements.txt model)
**Performance Goals**: Setup completes in <10 minutes on standard developer hardware
**Constraints**: Zero credentials in git repository (enforced via .gitignore), all deps have pinned versions
**Scale/Scope**: Single venv setup per developer machine, Pandas 2.1.* for ETL workloads

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Estrutura e Organização do Código**: Venv isolado (Princípio IV) alinha com "Ambiente isolado (venv/conda)"
✅ **Documentação Mandatória**: README com passo-a-passo claro (Princípio II) - runbooks detalhados com troubleshooting
✅ **Segurança e Logging (NÃO-NEGOCIÁVEL)**: .env para credenciais (Princípio III) - proteção obrigatória de DB_PASSWORD, API_TOKEN
✅ **Qualidade e Organização**: requirements.txt com dependências documentadas (Princípio IV) - versões cravadas exatamente

**GATE RESULT**: ✅ **PASSED** - Feature aligns with all 4 fundamental principles. No violations.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

Este é um feature de **setup/infraestrutura**, não código de aplicação. Estrutura mínima:

```text
.
├── README.md                    # ✅ Atualizar: add "Setup" section with:
│                                #    - Python 3.11 requirement
│                                #    - venv creation: python -m venv expansao (all OS)
│                                #    - Activation commands (per OS)
│                                #    - pip install -r requirements.txt
│                                #    - .env.example copy
│                                #    - validate-python.sh (Linux/macOS) + validate-python.bat (Windows)
│                                #    - Troubleshooting section
├── requirements.txt             # ✅ Criar: versões fixadas (pandas==2.1.*, psycopg2==2.9.*, python-dotenv==1.0.*, requests==2.31.*)
├── .env.example                 # ✅ Criar: template with DB_HOST, DB_USER, DB_PASSWORD, API_TOKEN
├── .gitignore                   # ✅ Atualizar: ensure .env + expansao/ ignored
├── scripts/
│   ├── validate-python.sh       # ✅ Criar: bash script to verify Python 3.11+ (Linux/macOS)
│   └── validate-python.bat      # ✅ Criar: batch script to verify Python 3.11+ (Windows)
├── docs/
│   └── SETUP.md                 # ✅ Criar: detailed setup guide per OS + troubleshooting
└── expansao/                    # Local only (in .gitignore) - NOT versioned
    └── [created after: python -m venv expansao]
```

**Structure Decision**: Infrastructure setup - apenas documentação + 5 arquivos de config (requirements.txt, .env.example, 2x validation scripts, .gitignore update) + README updates. Nenhum código de aplicação alterado.

## Complexity Tracking

✅ **NO VIOLATIONS** - Constitution gates all passed. Tracking table not needed.

---

## Phase 0: Research ✅ COMPLETE

**Deliverables**: `research.md`

**Decisions Made**:
1. ✅ venv folder name: `expansao` (project-specific naming)
2. ✅ Python validation: BOTH `validate-python.sh` (Linux/macOS) + `validate-python.bat` (Windows)
3. ✅ Pandas versioning: Minor-pinned (`==2.1.*`) for security patches
4. ✅ PostgreSQL driver: psycopg2 v2.9+
5. ✅ Environment loading: python-dotenv 1.0.*
6. ✅ HTTP client: requests 2.31.*
7. ✅ Multi-OS approach: Native scripts per platform (no shell compatibility hacks)
8. ✅ .env variables: 4 mandatory (DB_HOST, DB_USER, DB_PASSWORD, API_TOKEN)
9. ✅ Troubleshooting: 2-level (README + docs/SETUP.md)
10. ✅ requirements.txt: Minor-pinned Pandas + exact other versions

**No NEEDS CLARIFICATION markers remain** ✅

---

## Phase 1: Design ✅ COMPLETE

**Deliverables**:
- ✅ `research.md` - All technical decisions documented
- ✅ `data-model.md` - Configuration entities, state diagram, validation rules
- ✅ `contracts/env-contract.md` - .env file specification + test cases
- ✅ `quickstart.md` - Practical 10-minute setup guide for all 3 OSes

**Design Highlights**:
- Configuration entities: Python Environment Config, Dependencies Config, Secrets Config, Validation Scripts
- State lifecycle documented with clear transitions
- Cross-platform testing matrix (Windows / macOS / Linux)
- Security constraints on .env file (must never be versioned)
- Clear validation rules for all configuration

**Cross-Platform Validation**:
✅ Windows: `.bat` batch scripts for command-line compatibility
✅ macOS: `.sh` bash scripts for standard Unix environment
✅ Linux: `.sh` bash scripts for standard Unix environment

---

## Phase 2: Task Generation (Next Step)

**Will be generated by**: `/speckit.tasks` command

**Expected Deliverables**:
- tasks.md with action items:
  - Update README.md with Setup section
  - Create requirements.txt with 4 core dependencies
  - Create .env.example with 4 required variables
  - Create validate-python.sh (bash for Unix)
  - Create validate-python.bat (batch for Windows)
  - Create docs/SETUP.md with OS-specific troubleshooting
  - Update .gitignore to protect .env + expansao/
  - Test setup on Windows, macOS, Linux

---

## Implementation Strategy

### What Gets Built (Phase 2 Tasks):

```
Project Root Updates:
├── README.md                         [MODIFY] Add "Setup" section
├── requirements.txt                  [CREATE] 4 packages (pandas, psycopg2, python-dotenv, requests)
├── .env.example                      [CREATE] Template with 4 variables
├── .gitignore                        [MODIFY] Add .env + expansao/
├── scripts/validate-python.sh        [CREATE] Bash script for Unix
├── scripts/validate-python.bat       [CREATE] Batch script for Windows
└── docs/SETUP.md                     [CREATE] Detailed troubleshooting per OS

No Database Migration:
- PostgreSQL assumed to exist externally
- No schema changes in this feature

No Application Code:
- This is infrastructure setup only
- No src/, no classes, no business logic
```

### Success Criteria Verification (Phase 2):

All from spec.md Success Criteria section:
- ✅ SC-001: New dev completes setup in <10 minutes following README
- ✅ SC-002: 100% deps have exact/minor-pinned versions
- ✅ SC-003: Zero credentials in git (grep -r password .git/ returns 0)
- ✅ SC-004: Imports work (pandas, psycopg2, requests, python-dotenv)
- ✅ SC-005: README covers Windows, macOS, Linux
- ✅ SC-006: 100% prerequisites documented + validatable
- ✅ SC-007: ≥90% success on first attempt
- ✅ SC-008: validate-python.sh/.bat detects version before pip install

---

## Files Summary

### In Repo (Versioned):
- `specs/001-setup-venv/research.md` ✅
- `specs/001-setup-venv/plan.md` ✅ (this file)
- `specs/001-setup-venv/data-model.md` ✅
- `specs/001-setup-venv/contracts/env-contract.md` ✅
- `specs/001-setup-venv/quickstart.md` ✅
- `specs/001-setup-venv/checklists/requirements.md` ✅
- `specs/001-setup-venv/spec.md` ✅

### To Be Created in Phase 2:
- `README.md` (Setup section)
- `requirements.txt`
- `.env.example`
- `scripts/validate-python.sh`
- `scripts/validate-python.bat`
- `docs/SETUP.md`
- `.gitignore` (updated)

### Local Only (Not Versioned):
- `expansao/` (virtual environment - .gitignore)
- `.env` (credentials - .gitignore)

---

✅ **PHASE 0 & PHASE 1 COMPLETE** - Ready for Phase 2 Task Generation
