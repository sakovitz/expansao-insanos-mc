# Plano de Implementação: Automação de Geração de Comunicados em Imagem

**Branch**: `automacoes/001-comunicado-imagem` | **Data**: 2025-11-08 | **Spec**: [spec.md](spec.md)
**Input**: Especificação da feature em `/specs/automacoes/001-comunicado-imagem/spec.md`

**Nota**: Este template é preenchido pelo comando `/speckit.plan`. Veja `.specify/templates/commands/plan.md` para o fluxo de execução.

## Resumo

Criar uma API REST de automação que gera comunicados visuais padronizados para a área de Expansão do Insanos MC. O sistema aceita dados de integrantes via chamadas de API e gera imagens JPEG de 1542x1600 pixels com elementos de marca fixos e informações variáveis do integrante. A API valida entradas, manipula caracteres portugueses UTF-8, ajusta tamanhos de fonte dinamicamente e retorna o caminho da imagem gerada em menos de 10 segundos.

## Contexto Técnico

**Linguagem/Versão**: Python 3.11 (já estabelecido no projeto)
**Dependências Principais**: Pillow 10.4.0+ (manipulação de imagens), FastAPI 0.115.x + Uvicorn 0.32.x (API REST)
**Armazenamento**: Sistema de arquivos para imagens temporárias
**Fontes Externas**: DejaVu Sans (TTF) para renderização UTF-8
**Testes**: pytest (segue padrão do projeto)
**Plataforma Alvo**: Servidor Linux/Windows (API web)
**Tipo de Projeto**: API Web (endpoint RESTful)
**Metas de Performance**: <10s tempo de resposta da API por geração de imagem
**Restrições**: Suporte UTF-8, qualidade de compressão JPEG vs tamanho de arquivo
**Escala/Escopo**: Endpoint único de API, ~7 campos variáveis, 1 template de imagem

## Verificação da Constituição

*GATE: Deve passar antes da Fase 0 de pesquisa. Reverificar após design da Fase 1.*

### ✅ Itens de Conformidade Obrigatória

| Princípio | Status | Evidência |
|-----------|--------|-----------|
| **Módulos com responsabilidade separada** | ✅ PASS | Plano inclui módulos separados: handler da API, gerador de imagem, validador |
| **Docstrings obrigatórias (Google/NumPy)** | ✅ PASS | Será aplicado em todos os módulos e funções |
| **Logs estruturados (INFO, WARNING, ERROR)** | ✅ PASS | API vai logar requisições, falhas de validação, sucesso/erros de geração |
| **Proteção de credenciais (.env)** | ✅ PASS | Nenhuma credencial necessária para geração de imagem; segue padrão .env existente |
| **Ambientes virtuais isolados** | ✅ PASS | Venv existente "expansao" já estabelecido (Python 3.11) |
| **Documentação em /docs** | ✅ PASS | Será criado runbook para uso da API e troubleshooting |
| **Code review obrigatório** | ✅ PASS | Processo padrão se aplica |

### 📋 Avaliação de Risco

**Risco Baixo**:
- Nenhum novo framework introduzido (usa stack Python 3.11 existente)
- Padrão REST API simples
- Responsabilidade única: geração de imagem
- Sem banco de dados ou gerenciamento de estado complexo

**Mitigação**:
- Escolha da biblioteca de imagem (Pillow) precisa de pesquisa para suporte a fontes UTF-8
- Qualidade de renderização de fonte precisa de validação na Fase 0

## Estrutura do Projeto

### Documentação (esta feature)

```text
specs/automacoes/001-comunicado-imagem/
├── spec.md              # Especificação da feature (completo)
├── plan.md              # Este arquivo (saída do comando /speckit.plan)
├── research.md          # Saída da Fase 0 (PENDENTE)
├── data-model.md        # Saída da Fase 1 (PENDENTE)
├── quickstart.md        # Saída da Fase 1 (PENDENTE)
├── contracts/           # Saída da Fase 1 (PENDENTE)
│   └── api-spec.yaml    # Especificação OpenAPI
└── tasks.md             # Saída da Fase 2 (comando /speckit.tasks - NÃO criado por /speckit.plan)
```

### Código Fonte (raiz do repositório)

```text
# Estrutura de projeto único (módulo de automação)
automacoes/
├── comunicado_imagem/
│   ├── __init__.py
│   ├── api.py              # Handler do endpoint FastAPI/Flask
│   ├── generator.py        # Lógica de geração de imagem
│   ├── validator.py        # Lógica de validação de entrada
│   ├── models.py           # Modelos de dados (Comunicado, Integrante)
│   └── templates/
│       ├── base_template.png  # Imagem de template base
│       └── fonts/             # Arquivos de fonte para renderização
│
├── outputs/                # Diretório de saída de imagem temporária
│
tests/
├── contract/
│   └── test_api_contract.py    # Validação de contrato da API
├── integration/
│   └── test_image_generation.py  # Testes de geração end-to-end
└── unit/
    ├── test_validator.py
    └── test_generator.py

docs/
└── runbooks/
    └── comunicado-imagem-api.md   # Guia de uso da API e troubleshooting
```

**Decisão de Estrutura**: Usando padrão "Projeto único" pois esta é uma automação autocontida dentro do diretório `automacoes/`. A automação será organizada como um pacote Python com clara separação entre tratamento de API, lógica de negócio (geração de imagem) e validação. Isso alinha com o requisito da constituição para módulos com responsabilidades separadas.

## Rastreamento de Complexidade

> **Nenhuma violação detectada - esta seção intencionalmente deixada vazia**

Todos os princípios da constituição estão sendo seguidos. O design é simples e focado, usando padrões existentes do projeto.

