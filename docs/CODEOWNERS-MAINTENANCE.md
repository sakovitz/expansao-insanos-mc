# Guia de Manutenção: Arquivo CODEOWNERS

## Propósito

Este guia descreve como manter e atualizar o arquivo `CODEOWNERS` conforme a equipe e responsabilidades evoluem.

## Quando Modificar CODEOWNERS

Modifique o arquivo CODEOWNERS quando:

1. **Novo proprietário**: Alguém assume liderança técnica
2. **Proprietário sai**: Um proprietário sai do projeto ou equipe
3. **Mudança de escopo**: Diferentes áreas do código têm proprietários diferentes
4. **Reorganização**: Estrutura de equipe muda

## Como Adicionar um Novo Proprietário

### Passo 1: Criar Issue de Discussão

Crie uma issue no repositório documentando:

```markdown
## Título
Adicionar @novo-usuario como proprietário de código

## Razão
[Explique por que novo proprietário é necessário]

## Responsabilidades
[Descreva qual será a responsabilidade do novo proprietário]

## Discussão
[Deixe aberto para feedback por 1 semana]
```

### Passo 2: Obter Consenso

- Notifique proprietários atuais (@sakovitz, @jonasplima)
- Deixe aberto para feedback da equipe por 1 semana
- Resolve quando houver acordo

### Passo 3: Atualizar CODEOWNERS

Edit `CODEOWNERS` na raiz:

**Antes:**
```
*  @sakovitz @jonasplima
```

**Depois:**
```
*  @sakovitz @jonasplima @novo-usuario
```

### Passo 4: Confirmar Mudança

Crie uma PR com:

```markdown
## Título
feat: add @novo-usuario as code owner

## Descrição
Adiciona @novo-usuario como proprietário de código compartilhado.

Fecha #[issue-number]

## Razão
[Cópia da issue de discussão]

## Validação
- [x] @novo-usuario confirmou aceitação
- [x] @sakovitz e @jonasplima concordam
- [x] Discussão durou 1+ semana
```

### Passo 5: Merge

Uma vez aprovada pelos proprietários atuais, pode ser mesclada.

### Passo 6: Documentar

Atualize `docs/CODEOWNERS-POLICY.md` com novo proprietário na seção "Proprietários Atuais".

## Como Remover um Proprietário

### Passo 1: Notificar

Notifique o proprietário com antecedência:
- Por que está sendo removido
- Timeline
- Plano de transição

### Passo 2: Discutir

Abra uma issue pública (se apropriado) ou converse com liderança sobre:
- Razão da remoção
- Impacto na equipe
- Plano de cobertura

### Passo 3: Transição

Antes de remover:
- Redir responsabilidades para proprietário substituto
- Garantir que nenhuma ação pendente fica para trás
- Documentar qualquer conhecimento crítico

### Passo 4: Atualizar CODEOWNERS

**Antes:**
```
*  @sakovitz @jonasplima @usuario-saindo
```

**Depois:**
```
*  @sakovitz @jonasplima
```

### Passo 5: PR e Merge

Crie PR documentando a mudança:

```markdown
## Título
refactor: remove @usuario-saindo as code owner

## Razão
[Breve explicação]

## Transição
[Como responsabilidades foram redirecionadas]
```

## Propriedade por Área (Futuro)

Se o projeto cresce, pode ser necessário ter proprietários diferentes por área:

### Exemplo: Múltiplos Proprietários por Pasta

```
# Proprietários padrão para tudo
*  @sakovitz @jonasplima

# Proprietários específicos por área
pipelines/  @owner-pipelines @sakovitz
ia/  @owner-ia @jonasplima
automacoes/  @owner-automacoes @sakovitz
```

### Como Implementar

1. Discuta com equipe sobre necessidade
2. Identifique proprietários para cada área
3. Atualize CODEOWNERS com padrões específicos
4. Documente em `CODEOWNERS-POLICY.md`
5. Notifique equipe sobre nova estrutura

## Sintaxe de Referência

### Padrões Válidos

```
# Todos os arquivos
*  @owner

# Pasta específica
pipelines/  @owner

# Arquivo específico
README.md  @owner

# Múltiplos proprietários
pipelines/  @owner1 @owner2 @owner3

# Equipe GitHub
frontend/  @organization/frontend-team

# Combinação
*  @sakovitz @jonasplima         # Default para tudo
src/  @dev-team                  # Equipe específica
docs/  @documentation-owner      # Um proprietário
```

### Caracteres Especiais

```
# Comentários começam com #
# Linhas em branco são ignoradas
# Proprietários devem ter @ antes do nome
# Use espaço para separar múltiplos proprietários
```

## Validação

### Antes de fazer commit

1. Verif ique sintaxe:
   ```bash
   # Não há validação automatizada, mas procure por:
   # - Linhas sem @ (typos?)
   # - Espaçamento estranho
   # - Nomes de usuário corretos
   ```

2. Teste localmente:
   ```bash
   cat CODEOWNERS  # Verifique formatação
   ```

3. Verifique que todos os proprietários existem:
   ```bash
   # Visite: https://github.com/[proprietario]
   # Confirme que perfil é público e acessível
   ```

### Após Merge

GitHub automaticamente valida CODEOWNERS. Se houver erros:

1. Visite Settings > Branches > Status checks
2. Procure por "CODEOWNERS" ou "Code owner"
3. Se erro: Corrija e faça commit novo

## Cronograma de Revisão

### Mensal
- Revisar propriedades ativas
- Verificar que nenhum proprietário está inativo

### Trimestral
- Revisar carga de trabalho dos proprietários
- Considerar se divisão por área é necessária

### Semestral
- Reunião formal com proprietários
- Discutir mudanças estruturais se necessárias
- Atualizar política se apropriado

## Contato

Para perguntas sobre manutenção do CODEOWNERS:

- Abra uma issue com tag `codeowners`
- Comente em PR relacionada
- Fale diretamente com @sakovitz ou @jonasplima

## Histórico de Mudanças

| Data | Mudança | Proprietário |
|------|---------|------------|
| 2025-11-13 | Criação inicial | Feature 002-codeowners-setup |
| | | |

---

**Última Atualização**: 2025-11-13
**Próxima Revisão**: 2025-12-13
