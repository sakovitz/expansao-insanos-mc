<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║                          SYNC IMPACT REPORT                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

VERSION CHANGE: 1.0.0 → 1.1.0 (MINOR version bump)
Reason: Added comprehensive governance structure with team roles, review cadence,
and decision-making authority. No principles removed or redefined.

NEW SECTIONS ADDED:
✅ Procedimentos de Emenda (formalized amendment process)
✅ Desvios & Exceções (deviation documentation requirements)
✅ Review Cadence & Compliance (governance timing - SEMESTRAL: Jan + Jul)
✅ Papéis & Responsabilidades (team roles: Líder Técnico, Engenheiro, Eng. Iniciante)
✅ Política de Versionamento (semantic versioning policy for constitution)
✅ Autoridade em Decisões (decision-making authority matrix)
✅ Escalation Path (conflict resolution escalation path)
✅ Glossário & Definições (terms used in governance)

MODIFIED SECTIONS:
→ Governança: Expanded from basic structure to comprehensive governance framework

DEPENDENT TEMPLATES IMPACT:
✅ .specify/templates/plan-template.md - NO CHANGES REQUIRED
   (Generic "Constitution Check" reference is compatible with new governance)
✅ .specify/templates/spec-template.md - NO CHANGES REQUIRED
   (No constitution-specific references)
✅ .specify/templates/tasks-template.md - NO CHANGES REQUIRED
   (No constitution-specific references)
✅ .specify/templates/checklist-template.md - NO CHANGES REQUIRED
   (Not constitution-dependent)

GOVERNANCE CALENDAR (IMPORTANT):
• Revisão Constitucional: Semestral (Janeiro e Julho)
• Auditoria de Conformidade:
  - Mensal: Documentação + Segurança
  - Trimestral: Análise de código
  - Anual: Revisão estratégica

METADATA UPDATES:
• Versão: 1.0.0 → 1.1.0
• Ratificada: 2024-01-17 (unchanged - original adoption date)
• Última Alteração: 2024-01-17 → 2025-11-07

FOLLOW-UP TODOS:
□ Communicate this update to the team (especially new review cadence)
□ Schedule first semestral review for July 2025
□ Document first governance audit checklist (monthly/trimestral/annual)
□ Ensure all deviations are tracked in issue tracker with technical debt label

NO BLOCKERS - Ready for deployment.
-->

# Constituição de Engenharia - Insanos MC - Área de Expansão

## Missão

Estabelecer os princípios técnicos e de qualidade que guiam o desenvolvimento de código, automações e inteligência artificial no projeto expansao-insanos-mc. Cada linha de código deve refletir o espírito do clube: disciplina, força e irmandade.

## Princípios Fundamentais

### I. Estrutura e Organização do Código
- Módulos com classes e funções separadas por responsabilidade
- Código executável isolado em `if __name__ == "__main__":`
- Convenções de nomenclatura PEP8:
  - snake_case para variáveis e funções
  - PascalCase para classes
  - UPPER_CASE para constantes
- Priorizar composição sobre duplicação

### II. Documentação Mandatória
- Docstrings obrigatórias (formato Google/NumPy) para funções, classes e módulos
- Documentação completa em `/docs` para cada módulo
- Runbooks detalhados com objetivos, parâmetros, instruções e troubleshooting
- Comentários focados no "porquê", não no "como"

### III. Segurança e Logging (NÃO-NEGOCIÁVEL)
- Logs estruturados com níveis (INFO, WARNING, ERROR, CRITICAL)
- Centralização de logs em módulo dedicado
- Proteção de credenciais:
  - Uso obrigatório de .env
  - Políticas de senha robustas
  - Integração com gestores de segredos

### IV. Qualidade e Organização
- Manter código organizado e legível
- Seguir padrões básicos de indentação
- Ambiente isolado (venv/conda)
- Dependências documentadas em requirements.txt/pyproject.toml

## Requisitos Técnicos

- Python como linguagem principal
- Ambientes virtuais isolados
- Documentação clara e organizada
- Monitoramento e logging centralizado

## Processo de Desenvolvimento

1. Documentação inicial
2. Revisão de design
3. Implementação
4. Code review por pelo menos um membro da equipe
5. Revisão de segurança
6. Aprovação para deploy

## Governança

Esta constituição é a autoridade máxima para práticas de desenvolvimento.

### Procedimentos de Emenda

Alterações na constituição exigem:
1. **Proposta formal**: Membro da equipe descreve mudança, razão e impacto
2. **Período de discussão**: Mínimo 1 semana em revisão
3. **Aprovação**: Unanimidade do(s) líder(es) técnico(s)
4. **Documentação**: Atualização de todos templates dependentes
5. **Notificação**: Comunicação formal à equipe

### Desvios & Exceções

Desvios da constituição requerem:
- Documentação justificada (por quê, por quanto tempo, alternativa considerada)
- Aprovação do líder técnico responsável
- Prazo definido para revisão
- Registro como dívida técnica em issue/ticket

### Review Cadence & Compliance

**Revisão Constitucional**:
- Semestral (Janeiro e Julho)
- Líder técnico agenda e convoca equipe
- Documentação de mudanças em relatório de auditoria

**Auditoria de Conformidade**:
- Mensal: Verificação de documentação (docstrings, runbooks)
- Mensal: Checklist de segurança (credenciais, logs, acesso)
- Trimestral: Análise de código (estrutura, PEP8, testes)
- Anual: Revisão estratégica (princípios ainda relevantes?)

### Papéis & Responsabilidades

#### Líder Técnico
- **Responsabilidade**: Guardião da constituição e padrões técnicos
- **Autoridade**: Aprovação de desvios, decisões em conflitos de design, priorização de conformidade
- **Revisão**: Valida PR em aspectos de conformidade com constituição, mentoring técnico
- **Governança**: Conduz revisão semestral e propõe emendas

#### Engenheiro
- **Responsabilidade**: Implementação conforme constituição, liderança técnica em pipelines/ia/automacoes
- **Autoridade**: Sugerir melhorias em princípios, decisões de design em features
- **Revisão**: Code review de pares, validação de docstrings/testes, mentoring de iniciantes
- **Governança**: Participa de discussões de proposta, feedback em retrospectivas

#### Engenheiro Iniciante
- **Responsabilidade**: Aprender estrutura e princípios, executar tarefas bem-definidas
- **Autoridade**: Questionar práticas em pair programming, sugerir melhorias em onboarding
- **Revisão**: Recebe mentoring de Engenheiros em conformidade, submete PR para revisão
- **Governança**: Feedback em retrospectivas, observa discussões de governança

### Política de Versionamento

```
MAJOR.MINOR.PATCH

- MAJOR: Remoção/redefinição de princípio (quebra backward compatibility)
- MINOR: Novo princípio/seção, expansão material de guidance
- PATCH: Clarificações, correções tipográficas, refinamento semântico

Exemplo:
  v1.0.0 → v1.1.0 (adicionou governance e team roles)
  v1.1.0 → v1.2.0 (expandiu "Security & Logging")
  v1.2.3 → v1.2.4 (corrigiu typo em documentação)
```

### Autoridade em Decisões

| Decisão | Autoridade | Processo |
|---------|-----------|----------|
| Code style/linting | Líder técnico | Ad-hoc com time feedback |
| Novo framework/lib | Líder técnico + equipe | Proposta + 1 semana discussão |
| Desvio constitucional | Líder técnico | Documentar com justificativa |
| Novo princípio | Todos | Unanimidade em revisão semestral |
| Emenda de princípio | Todos | Unanimidade em revisão semestral |
| Task de conformidade | Líder técnico + PO | Priorização em planning |

### Escalation Path

Se há desacordo sobre conformidade:
1. Desenvolvedores discutem 1-on-1
2. Se não resolvido → Líder técnico toma decisão
3. Se questiona decisão do líder → Revisão em retrospectiva/meeting
4. Se persiste → Agenda tópico para revisão semestral

### Glossário & Definições

- **Docstring obrigatória**: Formato Google/NumPy com tipo, descrição, exemplos
- **Structured logs**: Formato JSON com timestamp, level, module, message, context
- **Code review**: ≥1 aprovação antes de merge (não pode ser self-approve)
- **Runbook**: Documento com objetivo, pré-requisitos, step-by-step, troubleshooting

🧩 Filosofia do Projeto:
Cada pipeline é um motor, cada script é uma engrenagem — juntos impulsionam a expansão do clube.
Código limpo, bem documentado e seguro é a base para evoluir com confiança e respeito à irmandade.

**Versão**: 1.1.0 | **Ratificada**: 2024-01-17 | **Última Alteração**: 2025-11-07
