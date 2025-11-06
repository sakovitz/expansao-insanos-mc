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

Esta constituição é a autoridade máxima para práticas de desenvolvimento. Desvios requerem:
- Documentação com justificativa
- Aprovação do líder técnico
- Prazo definido para revisão
- Registro como dívida técnica

Alterações na constituição exigem:
1. Proposta formal
2. Período de discussão (mínimo 1 semana)
3. Aprovação unânime dos líderes
4. Atualização da documentação
5. Notificação da equipe

🧩 Filosofia do Projeto:
Cada pipeline é um motor, cada script é uma engrenagem — juntos impulsionam a expansão do clube.
Código limpo, bem documentado e seguro é a base para evoluir com confiança e respeito à irmandade.

**Versão**: 1.0.0 | **Ratificada**: 2024-01-17 | **Última Alteração**: 2024-01-17
