# Guia de Code Review - Expansao Insanos MC

## Introdução

Este guia descreve o processo de code review (revisão de código) usado no projeto expansao-insanos-mc. Todos os pull requests (PRs) devem ser revisados e aprovados pelos proprietários de código antes de serem mesclados.

## Por que Code Review?

Code review garante:

- **Qualidade**: Múltiplos olhos verificam o código antes de entrar em produção
- **Consistência**: Código segue padrões e convenções definidas
- **Conhecimento Compartilhado**: Equipe aprende e entende as mudanças
- **Segurança**: Vulnerabilidades são identificadas e corrigidas
- **Governança**: Mudanças importantes são documentadas e rastreadas

## Proprietários de Código

O arquivo [`CODEOWNERS`](../CODEOWNERS) no repositório define quem são os proprietários de código:

- **@sakovitz** - Proprietário principal
- **@jonasplima** - Proprietário compartilhado

Ambos devem revisar PRs. **Pelo menos um deve aprovar** antes do merge.

## Fluxo de uma PR

### 1. Criação da PR

```
Developer -> Create PR -> GitHub
                           |
                           v
                    Add @sakovitz, @jonasplima as required reviewers
                           |
                           v
                    PR fica em estado "pending approval"
```

### 2. Processo de Review

**Para o Revisor (Proprietário):**

1. Recebe notificação de PR pendente
2. Abre a PR e lê:
   - Descrição da mudança
   - Diferenças de código
   - Discussão/comentários existentes
3. Revisa o código:
   - Verifica se segue constituição
   - Testa localmente se necessário
   - Identifica problemas ou melhorias
4. Comenta (se necessário) ou aprova
5. PR fica bloqueada até aprovação

**Para o Desenvolvedor:**

1. Vê comentários dos revisores
2. Faz ajustes se solicitado
3. Faz push das mudanças
4. Re-solicita review se necessário
5. Aguarda aprovação

### 3. Aprovação e Merge

```
Revisor aprova PR
       |
       v
GitHub habilita botão "Merge"
       |
       v
Developer clica "Merge"
       |
       v
PR é mesclada para main
```

## Expectativas de Review

### Tempo de Resposta

| Tipo de PR | SLA de Resposta | Aprovação Esperada |
|-----------|-----------------|-------------------|
| Padrão | 1 semana | Até 2 semanas |
| Crítica/Hotfix | 2 dias | Dentro de 2 dias |
| Documentação | 3 dias | Dentro de 1 semana |
| Experimental | 1 semana | Até 2 semanas |

### O que Revisor Procura

- ✅ Código segue convenções PEP8
- ✅ Funções/classes têm docstrings
- ✅ Lógica é clara e compreensível
- ✅ Não há código duplicado
- ✅ Testes estão inclusos (se aplicável)
- ✅ Sem hardcoding de valores/credenciais
- ✅ Mensagens de commit são descritivas
- ✅ Mudanças alinhadas com requisitos

## Boas Práticas para PRs

### Antes de Criar a PR

1. **Faça Push da Branch**
   ```bash
   git push origin seu-branch-name
   ```

2. **Descreva a PR Claramente**
   - Título: Breve e descritivo (ex: "Add user authentication")
   - Descrição: Por que, não apenas o quê
   - Referências: Link para issues ou tópicos relacionados

3. **Incluir Contexto**
   ```markdown
   ## Descripción
   Implements user authentication using JWT tokens

   ## Why
   Closes #123 - Users need secure login

   ## Validation
   - [ ] Manual testing done
   - [ ] Unit tests added
   - [ ] No breaking changes
   ```

### Mensagens de Commit Boas

✅ BOM:
```
feat: add JWT authentication module

Implements token-based authentication for user login.
Includes token generation, validation, and refresh logic.
Closes #123
```

❌ RUIM:
```
fix stuff
update code
changes
```

## Respondendo a Comentários

### Se Concordar com Sugestão

1. Faça a mudança sugerida
2. Faça um novo commit
3. Faça push da mudança
4. Comente: "Feito! Mudança implementada em [commit]"

### Se Discordar

1. Comente explicando seu ponto de vista
2. Se discordância permanecer, escalate para liderança
3. Sempre seja respeitoso e educado

### Pedindo Mais Tempo

Se precisar de tempo para fazer mudanças:

1. Comente na PR: "Vou fazer os ajustes até [data]"
2. Trabalhe nas mudanças
3. Faça push quando pronto
4. Solicite re-review

## Checklist para Criador de PR

Antes de submeter sua PR:

- [ ] Branch está atualizada com main?
- [ ] Todos os commits têm mensagens descritivas?
- [ ] Código segue PEP8 e convenções do projeto?
- [ ] Incluiu docstrings para funções/classes?
- [ ] Escreveu testes para novas funcionalidades?
- [ ] Testou manualmente as mudanças?
- [ ] Descrição da PR está clara?
- [ ] Sem código em debug ou comentado?
- [ ] Sem credenciais ou valores hardcoded?
- [ ] Descrição referencia issue(s) relacionada(s)?

## Checklist para Revisor

Ao revisar uma PR:

- [ ] Entendo o propósito da PR?
- [ ] Código segue convenções do projeto?
- [ ] Lógica está correta e clara?
- [ ] Há testes cobrindo as mudanças?
- [ ] Sem problemas de segurança óbvios?
- [ ] Nenhum código desnecessário ou duplicado?
- [ ] Mudanças são focadas (não inclui extra)?
- [ ] Documentação foi atualizada?

## Escalation e Conflitos

### Se PR está Bloqueada

1. Proprietário não respondeu em 1 semana?
2. Comente: "@sakovitz ou @jonasplima - PR aguardando revisão desde [data]"
3. Se ninguém responder em 2 dias: Contate liderança

### Se Desacordo com Revisor

1. Discuta respeitosamente nos comentários
2. Se não chegar a acordo: Marque tópico para retrospectiva
3. Liderança técnica pode tomar decisão final

## Referência

- [Arquivo CODEOWNERS](../CODEOWNERS)
- [Política de Governança](./CODEOWNERS-POLICY.md)
- [Constituição de Engenharia](./../.specify/memory/constitution.md)

## Dúvidas?

Se tiver dúvidas sobre o processo de review:

1. Pergunte em PR existente
2. Abra uma issue com tag `code-review`
3. Converse diretamente com @sakovitz ou @jonasplima
