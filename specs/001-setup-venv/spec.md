# Feature Specification: Setup de Ambiente Virtual Python

**Feature Branch**: `001-setup-venv`
**Created**: 2025-11-07
**Status**: Draft
**Input**: Definição de ambiente virtual com Python, venv, requirements.txt, .env, PostgreSQL, Pandas e documentação no README

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Criar e Ativar Ambiente Virtual (Priority: P1)

Um desenvolvedor recém-integrado ao time de Expansão precisa preparar seu ambiente local para começar a trabalhar nos scripts de ETL e automações. Ele deve ser capaz de criar um ambiente Python isolado seguindo um passo a passo claro no README.

**Why this priority**: Foundation essencial - sem o ambiente virtual configurado corretamente, nenhum desenvolvedor consegue começar. Bloqueia todas as outras atividades.

**Independent Test**: Pode ser testado independentemente executando os comandos no README e verificando que um novo venv foi criado com Python na versão correta, isolado do sistema.

**Acceptance Scenarios**:

1. **Given** um desenvolvedor com Python instalado localmente, **When** executa os comandos do README (ex: `python -m venv venv`), **Then** um ambiente virtual é criado na raiz do projeto
2. **Given** o ambiente virtual criado, **When** ativa-o (`source venv/bin/activate` ou `.venv\Scripts\activate`), **Then** o prompt muda indicando ativação e `python --version` mostra a versão esperada
3. **Given** um desenvolvedor novo, **When** lê a seção de setup do README, **Then** entende claramente qual versão Python usar, quais são os pré-requisitos e todos os passos necessários

---

### User Story 2 - Instalar Dependências com Pinned Versions (Priority: P1)

Depois de ativar o ambiente virtual, o desenvolvedor precisa instalar todas as bibliotecas necessárias (Pandas, PostgreSQL driver, etc.) com versões exatas para garantir consistência entre ambientes.

**Why this priority**: Crítico - sem as dependências corretas, os scripts não funcionam. Versões fixadas evitam conflitos entre devs e desvios entre ambientes.

**Independent Test**: Pode ser testado instalando as dependências de `requirements.txt` e verificando que todas as libs corretas estão instaladas com as versões exatas especificadas. Verificar com `pip list` que nenhuma dependência extra foi instalada.

**Acceptance Scenarios**:

1. **Given** um environment virtual ativado, **When** executa `pip install -r requirements.txt`, **Then** todas as dependências são instaladas com versões exatas (ex: `pandas==2.0.3`)
2. **Given** as dependências instaladas, **When** tenta importar bibliotecas chave (pandas, psycopg2, requests), **Then** todas importam sem erros
3. **Given** dois desenvolvedores em máquinas diferentes, **When** ambos instalam de `requirements.txt`, **Then** têm exatamente as mesmas versões de bibliotecas

---

### User Story 3 - Configurar Arquivo .env para Credenciais e Conexão ao BD (Priority: P1)

O desenvolvedor precisa criar um arquivo `.env` local para armazenar de forma segura as credenciais do banco PostgreSQL, tokens de API e outras variáveis sensíveis, sem expô-las no repositório.

**Why this priority**: Segurança - a Constituição exige proteção de credenciais. Sem .env, credenciais acabam no Git (risco crítico).

**Independent Test**: Pode ser testado criando um `.env.example` no repo (sem valores reais) e verificando que `.env` está no `.gitignore`. Validar que um desenvolvedor consegue copiar `.env.example` → `.env` e inserir suas credenciais locais.

**Acceptance Scenarios**:

1. **Given** um novo desenvolvedor sem arquivo `.env`, **When** executa `cp .env.example .env`, **Then** um arquivo `.env` é criado localmente
2. **Given** o arquivo `.env` criado, **When** ele preenche as variáveis (DB_HOST, DB_USER, DB_PASSWORD, API_TOKEN, etc.), **Then** os scripts conseguem ler essas variáveis via `os.getenv()`
3. **Given** um `.env` preenchido, **When** tenta fazer um git add, **Then** o arquivo `.env` é ignorado (protegido por `.gitignore`)

---

### User Story 4 - Testar Conexão com PostgreSQL (Priority: P2)

Um desenvolvedor quer verificar que sua conexão ao PostgreSQL está funcionando antes de iniciar o desenvolvimento de ETLs. Deve haver um script ou teste simples que valida a conexão.

**Why this priority**: Importância média - valida que infraestrutura está acessível, mas pode ser feito após setup básico.

**Independent Test**: Pode ser testado executando um script de validação que tenta conectar ao PostgreSQL usando credenciais do `.env` e retorna sucesso/falha.

**Acceptance Scenarios**:

1. **Given** variáveis de conexão definidas no `.env`, **When** executa script de teste de conexão, **Then** se PostgreSQL está acessível, retorna "Conexão OK"
2. **Given** credenciais inválidas no `.env`, **When** executa o script, **Then** retorna erro claro indicando qual credencial está incorreta

---

### User Story 5 - Documentação Completa no README (Priority: P1)

Todas as instruções de setup devem estar no README do projeto, incluindo: versão Python requerida, pré-requisitos do SO, passo a passo, troubleshooting.

**Why this priority**: Essencial - sem documentação clara, novos devs perdem horas em setup. Alinha com Princípio II (Documentação Mandatória) da Constituição.

**Independent Test**: Pode ser testado com um desenvolvedor novo seguindo APENAS o README para fazer setup - se conseguir, está bom.

**Acceptance Scenarios**:

1. **Given** um desenvolvedor novo com apenas o README, **When** segue os passos de setup, **Then** consegue criar e ativar venv sem dúvidas
2. **Given** um pré-requisito não instalado (ex: PostgreSQL não está rodando), **When** tenta executar script de teste, **Then** README tem seção de troubleshooting explicando o que fazer

---

### Edge Cases

- O que acontece se um desenvolvedor usa Python 3.8 quando o projeto requer 3.11+? (README deve deixar claro e script pode validar)
- E se PostgreSQL não está instalado ou não está rodando? (Erro claro, instruções de instalação no README)
- E se o `requirements.txt` tiver conflito de dependências? (pip install deve falhar com mensagem clara, README tem troubleshooting)
- E se `.env.example` não existe? (README explica como criar e quais variáveis são obrigatórias)

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: Sistema DEVE permitir criar um ambiente virtual Python isolado usando venv
- **FR-002**: Sistema DEVE suportar Python 3.11 como versão padrão requerida
- **FR-003**: Sistema DEVE instalar todas as dependências listadas em `requirements.txt` com versões exatas fixadas (ex: pandas==2.0.3, não pandas>=2.0)
- **FR-004**: Sistema DEVE incluir Pandas com versionamento minor fixado (ex: `pandas==2.1.*`) permitindo updates de patch automaticamente
- **FR-005**: Sistema DEVE incluir driver PostgreSQL (psycopg2 ou psycopg3) para conexão com banco de dados
- **FR-006**: Sistema DEVE suportar arquivo `.env` para armazenar variáveis sensíveis: DB_HOST, DB_USER, DB_PASSWORD, API_TOKEN
- **FR-007**: Sistema DEVE fornecer arquivo `.env.example` no repositório documentando as 4 variáveis obrigatórias (sem valores reais)
- **FR-008**: Sistema DEVE garantir que `.env` não é versionado (adicionado ao `.gitignore`)
- **FR-009**: Sistema DEVE fornecer script ou instrução clara para testar conexão com PostgreSQL
- **FR-010**: README DEVE incluir passo a passo exato de setup com comandos prontos para copiar/colar
- **FR-011**: README DEVE especificar qual versão Python é requerida e como instalar
- **FR-012**: README DEVE listar todos os pré-requisitos (PostgreSQL, Python, pip, ferramentas do SO)
- **FR-013**: README DEVE incluir script de validação que verifica se Python 3.11+ está instalado ANTES de executar `pip install`
- **FR-014**: README DEVE incluir seção "Troubleshooting Dependências" explicando causas comuns de conflitos e como resolvê-los
- **FR-015**: README DEVE incluir seção de troubleshooting para problemas comuns (PostgreSQL não rodando, version mismatch, etc)

### Key Entities

- **Environment Config**: Representa estado do ambiente virtual (versão Python, libs instaladas, variáveis ambiente ativas)
- **Dependency List**: Lista de bibliotecas com versões exatas fixadas (armazenada em `requirements.txt`)
- **Credentials Store**: Variáveis sensíveis armazenadas em `.env` (DB_HOST, DB_USER, DB_PASSWORD, API_TOKENS)

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Um novo desenvolvedor consegue completar setup do ambiente em menos de 10 minutos seguindo APENAS o README
- **SC-002**: 100% das dependências instaladas via `pip install -r requirements.txt` têm versões exatas (zero floating versions como pandas>=2.0)
- **SC-003**: Nenhuma credencial sensível está versionada no repositório (teste: grep -r password .git/ retorna 0 resultados)
- **SC-004**: Um desenvolvedor consegue importar Pandas, psycopg2, requests e fazer query simples no PostgreSQL sem erros
- **SC-005**: README cobre todas as plataformas (Windows, macOS, Linux) com instruções específicas
- **SC-006**: 100% dos pré-requisitos estão documentados e validáveis (via script check ou manual verification)
- **SC-007**: Novos desenvolvedores relatam >= 90% de sucesso na primeira tentativa de setup seguindo README
- **SC-008**: Script de validação de Python 3.11 fornecido no README detecta versão incorreta antes de `pip install`

## Clarifications

### Session 2025-11-07

- Q1: Validação de versão Python → A: Script de validação que checa `python --version` antes da instalação
- Q2: Conflitos de dependências → A: Seção "Troubleshooting Dependências" no README com causas comuns e resoluções
- Q3A: Estratégia de versionamento Pandas → A: Versão minor fixada (ex: `pandas==2.1.*`) permitindo patch updates automáticos
- Q3B: Variáveis obrigatórias .env → A: DB_HOST, DB_USER, DB_PASSWORD, API_TOKEN (confirmado)

## Assumptions

- Python 3.11 é a versão padrão requerida (estável, bom suporte de libraries, lançada 2022)
- PostgreSQL já está instalado em ambiente de desenvolvimento (setup do BD é outra feature)
- Desenvolvedores têm `pip` instalado (vem com Python 3.x)
- Projeto usará `venv` para ambientes virtuais (não conda ou pyenv)
- Pandas versionada como `pandas==2.1.*` (minor fixada, permitindo patch updates automáticos)
- Integração de APIs usará biblioteca `requests` (padrão HTTP em Python)
- Drivers PostgreSQL: psycopg2 ou psycopg3 (ambos compatíveis)
- `.env.example` documentará 4 variáveis obrigatórias: DB_HOST, DB_USER, DB_PASSWORD, API_TOKEN
- Script de validação Python será fornecido para detectar version mismatch antes de instalar deps
