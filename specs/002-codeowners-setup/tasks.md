---
description: "Lista de tarefas para implementação do arquivo CODEOWNERS"
---

# Tarefas: Configuração do CODEOWNERS

**Entrada**: Documentos de design de `/specs/002-codeowners-setup/`
**Pré-requisitos**: plan.md (obrigatório), spec.md (obrigatório para histórias de usuário)

**Testes**: Este é um arquivo de configuração simples. Não há testes automatizados - validação é feita manualmente via interface do GitHub.

**Organização**: Como esta é uma funcionalidade de configuração simples, as tarefas são organizadas por história de usuário para permitir implementação e testes independentes.

## Formato: `[ID] [P?] [Story] Descrição`

- **[P]**: Pode executar em paralelo (arquivos diferentes, sem dependências)
- **[Story]**: A qual história de usuário esta tarefa pertence (ex: US1, US2)
- Inclua caminhos exatos de arquivo nas descrições

## Convenções de Caminhos

- Arquivo de configuração: `/CODEOWNERS` (raiz do repositório)
- Documentação: `docs/`, `specs/`

---

## Fase 1: Setup (Infraestrutura Compartilhada)

**Propósito**: Inicialização do projeto e estrutura básica

- [x] T001 Criar estrutura base para feature 002-codeowners-setup (specs/002-codeowners-setup/)
- [x] T002 Revisar template de CODEOWNERS do GitHub e sintaxe esperada

---

## Fase 2: Fundacional (Pré-requisitos Bloqueantes)

**Propósito**: Configuração que deve estar completa ANTES de qualquer história de usuário

**⚠️ CRÍTICO**: Nenhum trabalho de história de usuário pode começar até que esta fase esteja completa

- [x] T003 Documentar política de governança de CODEOWNERS em docs/CODEOWNERS-POLICY.md
- [x] T004 Validar que @sakovitz e @jonasplima possuem contas GitHub válidas e acesso ao repositório

**Checkpoint**: Fundação pronta - implementação de histórias de usuário pode começar

---

## Fase 3: História de Usuário 1 - Gerente de Repositório Configura Requisitos de Aprovação de PR (Priority: P1) 🎯 MVP

**Objetivo**: Criar arquivo CODEOWNERS na raiz do repositório designando @sakovitz e @jonasplima como proprietários obrigatórios para todo o projeto

**Teste Independente**: Criar um arquivo CODEOWNERS e verificar que a interface de PR do GitHub o reconheça e aplique requisitos de aprovação dos proprietários especificados

### Implementação para História de Usuário 1

- [x] T005 [P] [US1] Criar arquivo `/CODEOWNERS` na raiz do repositório com conteúdo: `* @sakovitz @jonasplima`
- [x] T006 [US1] Confirmar arquivo CODEOWNERS no Git com mensagem descritiva
- [x] T007 [US1] Validar que GitHub reconhece o arquivo CODEOWNERS (nenhum erro na interface de PR)
- [x] T008 [US1] Criar PR de teste e verificar que @sakovitz e @jonasplima aparecem como revisores necessários
- [x] T009 [US1] Validar que botão de mesclagem fica desabilitado sem aprovação de proprietários

**Checkpoint**: Neste ponto, História de Usuário 1 deve estar totalmente funcional e testável independentemente

---

## Fase 4: História de Usuário 2 - Desenvolvedores Entendem Regras de Propriedade de Código (Priority: P2)

**Objetivo**: Garantir que desenvolvedores conseguem ver facilmente quem são os proprietários de código e entendem o processo de review

**Teste Independente**: Verificar que o arquivo CODEOWNERS é acessível e lista claramente os proprietários de código

### Implementação para História de Usuário 2

- [x] T010 [P] [US2] Criar documento `docs/CODE-REVIEW-GUIDE.md` explicando processo de aprovação
- [x] T011 [P] [US2] Adicionar referência ao CODEOWNERS no README.md do repositório
- [x] T012 [US2] Criar/atualizar quickstart com instruções sobre CODEOWNERS (specs/002-codeowners-setup/quickstart.md)
- [x] T013 [US2] Verificar que CODEOWNERS é visível para desenvolvedores via GitHub web interface

**Checkpoint**: Neste ponto, Histórias de Usuário 1 E 2 devem ambas funcionar independentemente

---

## Fase 5: Polish & Preocupações Transversais

**Propósito**: Melhorias que afetam múltiplas histórias de usuário

- [x] T014 [P] Adicionar comentários/documentação no arquivo CODEOWNERS se necessário
- [x] T015 [P] Validar sintaxe do CODEOWNERS contra documentação oficial do GitHub
- [x] T016 Documentar política de manutenção futura em docs/CODEOWNERS-MAINTENANCE.md (incluindo como adicionar/remover proprietários)
- [x] T017 Executar validação completa do quickstart conforme docs/CODEOWNERS/quickstart.md
- [x] T018 Revisar e confirmar que todas as histórias de usuário foram atendidas

---

## Dependências & Ordem de Execução

### Dependências de Fase

- **Setup (Fase 1)**: Sem dependências - pode começar imediatamente
- **Fundacional (Fase 2)**: Depende da conclusão do Setup - BLOQUEIA todas as histórias de usuário
- **Histórias de Usuário (Fase 3+)**: Todas dependem da conclusão da fase Fundacional
  - Histórias de usuário podem então prosseguir em paralelo (se tiver equipe)
  - Ou sequencialmente em ordem de prioridade (P1 → P2)
- **Polish (Fase Final)**: Depende das histórias de usuário desejadas estarem completas

### Dependências de História de Usuário

- **História de Usuário 1 (P1)**: Pode começar após Fundacional (Fase 2) - Sem dependências em outras histórias
- **História de Usuário 2 (P2)**: Pode começar após Fundacional (Fase 2) - Deve ser independentemente testável

### Dentro de Cada História de Usuário

- Implementação básica antes de documentação
- Validação manual antes de passagem para próxima fase
- Cada história completa antes de mover para próxima prioridade

### Oportunidades de Paralelismo

- Todas as tarefas de Setup marcadas [P] podem executar em paralelo
- Todas as tarefas Fundacionais marcadas [P] podem executar em paralelo (dentro da Fase 2)
- Uma vez que Fundacional esteja completa, todas as histórias de usuário podem começar em paralelo (se houver capacidade)
- Documentação de diferentes aspectos pode ser paralela

---

## Exemplo de Paralelismo: História de Usuário 1

```bash
# Tarefas que podem ser executadas em paralelo para US1:
Tarefa: T005 - Criar arquivo CODEOWNERS
Tarefa: T006 - Confirmar arquivo no Git
# (T007-T009 são sequenciais pois dependem de T006 estar completa)
```

---

## Estratégia de Implementação

### MVP Primeiro (Apenas História de Usuário 1)

1. Completar Fase 1: Setup
2. Completar Fase 2: Fundacional (CRÍTICO - bloqueia todas as histórias)
3. Completar Fase 3: História de Usuário 1
4. **PARAR e VALIDAR**: Testar História de Usuário 1 independentemente
5. Demonstrar/Deploy se pronto

### Entrega Incremental

1. Completar Setup + Fundacional → Fundação pronta
2. Adicionar História de Usuário 1 → Testar independentemente → Deploy/Demo (MVP!)
3. Adicionar História de Usuário 2 → Testar independentemente → Deploy/Demo
4. Cada história adiciona valor sem quebrar histórias anteriores

### Estratégia de Equipe Paralela

Com múltiplos desenvolvedores:

1. Equipe completa Setup + Fundacional juntos
2. Uma vez Fundacional completo:
   - Desenvolvedor A: História de Usuário 1
   - Desenvolvedor B: História de Usuário 2 (pode começar em paralelo)
3. Histórias completam e integram independentemente

---

## Notas

- [P] tarefas = arquivos diferentes, sem dependências
- [Story] label mapeia tarefa para história de usuário específica para rastreabilidade
- Cada história de usuário deve ser independentemente completável e testável
- Validação manual via GitHub interface é suficiente
- Confirme após cada tarefa ou grupo lógico
- Pare em qualquer checkpoint para validar história independentemente
- Evite: tarefas vagas, conflitos de mesmo arquivo, dependências cross-story que quebrem independência
