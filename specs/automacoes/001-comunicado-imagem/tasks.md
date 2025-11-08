# Tasks: Automação de Geração de Comunicados em Imagem

**Input**: Design documents from `/specs/automacoes/001-comunicado-imagem/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-spec.yaml

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: Repository root with `automacoes/`, `tests/`, `docs/`
- Paths shown below follow the structure defined in plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Install Python dependencies in requirements.txt: Pillow>=10.4.0, fastapi==0.115.*, uvicorn[standard]==0.32.*, pydantic==2.9.*
- [ ] T002 Download DejaVu Sans fonts (DejaVuSans-Bold.ttf, DejaVuSans.ttf) from https://sourceforge.net/projects/dejavu/
- [ ] T003 Create base directory structure: automacoes/, automacoes/outputs/, tests/, tests/contract/, tests/integration/, tests/unit/, docs/runbooks/

---

## Phase 2: User Story 1 - Criação da Estrutura de Pastas (Priority: P1)

**Goal**: Criar estrutura de pastas do projeto seguindo padrão definido no README.md (pipelines/, ia/, automacoes/, data/, docs/)

**Independent Test**: Verificar se todas as pastas definidas no README.md foram criadas na raiz do projeto e estão acessíveis

### Implementation for User Story 1

- [ ] T004 [US1] Create root directory structure in project root: pipelines/, ia/, automacoes/, data/, docs/
- [ ] T005 [US1] Create automacoes/comunicado_imagem/ package structure with __init__.py
- [ ] T006 [US1] Create automacoes/comunicado_imagem/templates/ directory for base_template.png and fonts/
- [ ] T007 [US1] Copy DejaVuSans-Bold.ttf and DejaVuSans.ttf to automacoes/comunicado_imagem/templates/fonts/
- [ ] T008 [US1] Validate all directories exist and are accessible via Python os.path.exists()

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - all required directories should exist and be accessible

---

## Phase 3: User Story 2 - Geração de Comunicado com Dados Variáveis (Priority: P2)

**Goal**: API REST que aceita dados de integrantes via POST e gera imagem JPEG 1542x1600 com elementos variáveis, retornando file_path em <10s

**Independent Test**: Fornecer dados de entrada (origem="EXPANSÃO", evento="CONCLUSÃO DE ESTÁGIO", nome_integrante="XANDECO (183)") via POST /gerar-comunicado e verificar se imagem gerada contém todos os textos nas posições corretas

### Implementation for User Story 2

- [ ] T009 [P] [US2] Create Pydantic models in automacoes/comunicado_imagem/models.py: ComunicadoRequest with 7 fields (origem, evento, nome_integrante, resultado, localizacao, grau, data), ComunicadoResponse with success/file_path/generation_time_ms
- [ ] T010 [P] [US2] Create validation logic in automacoes/comunicado_imagem/validator.py: validate_date_format (regex ^\d{2}/\d{2}/\d{4}$), validate_nome_integrante (regex ^.+\s\(\d+\)$), extract_integrante_info (parse nome_colete and numero)
- [ ] T011 [US2] Create image generator core in automacoes/comunicado_imagem/generator.py: load_template(), create_base_image(1542x1600), load_fonts(DejaVuSans-Bold.ttf)
- [ ] T012 [US2] Implement text rendering with UTF-8 support in automacoes/comunicado_imagem/generator.py: render_text_centered(), render_text_with_color (yellow #FFD700, white #FFFFFF), handle Portuguese characters (á, ã, ç, õ)
- [ ] T013 [US2] Implement dynamic font sizing in automacoes/comunicado_imagem/generator.py: calculate_text_bbox(), adjust_font_size_to_fit (decrement 2px per iteration, min 30px), fail if text too long
- [ ] T014 [US2] Implement JPEG save with optimization in automacoes/comunicado_imagem/generator.py: save_jpeg(quality=90, optimize=True), generate_filename (format: YYYYMMDD_NOMECOLETE.jpeg)
- [ ] T015 [US2] Create FastAPI application in automacoes/comunicado_imagem/api.py: app instance, @app.post("/gerar-comunicado") endpoint with ComunicadoRequest/ComunicadoResponse models
- [ ] T016 [US2] Implement API endpoint handler in automacoes/comunicado_imagem/api.py: validate request via Pydantic, call generator.gerar_comunicado(), measure generation_time_ms, return file_path
- [ ] T017 [US2] Add error handling in automacoes/comunicado_imagem/api.py: HTTP 400 for validation errors with specific field messages, HTTP 500 for generation errors, structured logging (INFO, WARNING, ERROR)
- [ ] T018 [US2] Add health check endpoint in automacoes/comunicado_imagem/api.py: @app.get("/health") returning status="healthy", service="comunicado-api"
- [ ] T019 [US2] Integration test: Start uvicorn server, POST request with valid data, verify 200 response, verify file exists at returned path, verify image contains all variable texts (origem, evento, nome_integrante, resultado, localizacao, grau, data)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - API should accept POST requests and generate valid JPEG images with variable data

---

## Phase 4: User Story 3 - Manutenção de Elementos Fixos do Template (Priority: P3)

**Goal**: Garantir que todos os elementos fixos (título "COMUNICADO", rodapé "COMANDO MUNDIAL", avisos) aparecem idênticos em todas as imagens geradas

**Independent Test**: Gerar múltiplos comunicados com dados diferentes e verificar que todos os elementos fixos aparecem idênticos em todas as imagens (mesma posição, cor, fonte)

### Implementation for User Story 3

- [ ] T020 [US3] Define fixed template constants in automacoes/comunicado_imagem/generator.py: TITLE="COMUNICADO", FOOTER_LINE1="COMANDO MUNDIAL", FOOTER_LINE2="COMUNICADO INTERNO", FOOTER_LINE3="PROIBIDA A DIVULGAÇÃO EM QUALQUER REDE SOCIAL"
- [ ] T021 [US3] Implement fixed element rendering in automacoes/comunicado_imagem/generator.py: render_title_comunicado (yellow #FFD700, 120px, top centered), render_footer_lines (white #FFFFFF, 50px, bottom aligned)
- [ ] T022 [US3] Ensure fixed elements are rendered in every gerar_comunicado() call in automacoes/comunicado_imagem/generator.py: call render_title_comunicado() before variable data, call render_footer_lines() after variable data
- [ ] T023 [US3] Validation test: Generate 3 different comunicados, extract fixed element positions via PIL, verify identical coordinates, colors, and font sizes across all images

**Checkpoint**: All user stories should now be independently functional - every generated image contains identical fixed elements regardless of variable data

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T024 [P] Create runbook documentation in docs/runbooks/comunicado-imagem-api.md: API usage examples, troubleshooting common errors, performance diagnostics
- [ ] T025 [P] Add comprehensive docstrings (Google style) to all functions in automacoes/comunicado_imagem/*.py modules
- [ ] T026 [P] Configure structured logging in automacoes/comunicado_imagem/api.py: log level INFO, format with timestamp and level, log requests/responses/errors
- [ ] T027 Validate quickstart.md instructions: Follow all setup steps, start uvicorn server, test all curl examples, verify all responses match documentation
- [ ] T028 Update CLAUDE.md with new technologies and commands: Add Pillow, FastAPI, Uvicorn to active technologies, add command to start API server (uvicorn automacoes.comunicado_imagem.api:app)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **User Story 1 (Phase 2)**: Depends on Setup completion - creates directory structure
- **User Story 2 (Phase 3)**: Depends on User Story 1 completion - requires directories and fonts from US1
- **User Story 3 (Phase 4)**: Depends on User Story 2 completion - extends generator.py created in US2
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup - No dependencies on other stories
- **User Story 2 (P2)**: Depends on User Story 1 (needs directory structure and fonts) - Independently testable via API calls
- **User Story 3 (P3)**: Depends on User Story 2 (extends generator.py) - Independently testable by comparing multiple generated images

### Within Each User Story

#### User Story 1 (Estrutura de Pastas)
- T004 (create directories) → T005 (create package) → T006 (create templates dir) → T007 (copy fonts) → T008 (validate)
- All directory creation tasks must complete before validation

#### User Story 2 (Geração de Comunicados)
- T009 (models) and T010 (validator) can run in parallel [P]
- T011 (generator core) depends on T007 (fonts available)
- T012 (text rendering) depends on T011 (generator core)
- T013 (font sizing) depends on T012 (text rendering)
- T014 (JPEG save) depends on T013 (complete image)
- T015 (FastAPI app) and T016 (endpoint handler) depend on T009 (models) and T014 (complete generator)
- T017 (error handling) depends on T016 (endpoint exists)
- T018 (health check) can be parallel with T017 [P-style]
- T019 (integration test) depends on ALL previous tasks in US2

#### User Story 3 (Elementos Fixos)
- T020 (constants) → T021 (rendering) → T022 (integration) → T023 (validation)
- Sequential flow to ensure fixed elements are properly integrated

### Parallel Opportunities

- **Phase 1**: T002 (download fonts) can happen in parallel with T001 (install deps) and T003 (create dirs)
- **User Story 2**: T009 (models) and T010 (validator) are independent, can run in parallel
- **Polish Phase**: T024 (runbook), T025 (docstrings), T026 (logging) can all run in parallel as they touch different aspects

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: User Story 1
3. **STOP and VALIDATE**: Verify all directories exist via os.path.exists()
4. Directories ready for automation code

### Incremental Delivery

1. Complete Setup + User Story 1 → Directory structure ready
2. Add User Story 2 → Test independently via API → **MVP: Working API that generates images**
3. Add User Story 3 → Test independently by comparing images → **Complete: All elements fixed and consistent**
4. Add Polish → Documentation and logging complete

### Sequential Execution (Recommended)

Given dependencies between user stories:

1. **Week 1**: Phase 1 (Setup) + Phase 2 (US1) → Directories ready
2. **Week 2**: Phase 3 (US2) → API + image generation working
3. **Week 3**: Phase 4 (US3) → Fixed elements guaranteed
4. **Week 4**: Phase 5 (Polish) → Documentation and refinements

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- US1 creates infrastructure, US2 builds core functionality, US3 adds consistency guarantees
- Commit after each task or logical group (e.g., after completing all models)
- Stop at any checkpoint to validate story independently
- No tests were requested in spec.md, so no test tasks included (except integration validation)
- File paths use Windows style (backslashes) based on environment: `C:\Users\jonas\github\expansao-insanos-mc\`
- Follow quickstart.md for setup validation and API testing procedures
