# Política de Governança: Arquivo CODEOWNERS

## Propósito

Este documento define a política de governança para o arquivo CODEOWNERS do repositório expansao-insanos-mc. O CODEOWNERS é um mecanismo de controle de qualidade que garante que todas as pull requests sejam revisadas e aprovadas pelos proprietários designados de código antes da mesclagem.

## Proprietários Atuais

O seguinte(s) usuário(s) GitHub são designados como proprietários de código para **todo o repositório**:

- **@sakovitz** - Proprietário principal de código
- **@jonasplima** - Proprietário compartilhado de código

## Responsabilidades dos Proprietários

Como proprietário de código, você é responsável por:

1. **Code Review**: Revisar e validar todas as pull requests antes da aprovação
2. **Qualidade**: Garantir que o código atende aos padrões de qualidade definidos na constituição de engenharia
3. **Governança**: Manter-se informado sobre mudanças no repositório e políticas técnicas
4. **Orientação**: Fornecer feedback construtivo aos desenvolvedores

## Processo de Aprovação

### Fluxo Padrão de PR

1. Desenvolvedor cria um Pull Request (PR)
2. GitHub automaticamente adiciona @sakovitz e @jonasplima como revisores necessários
3. Pelo menos um proprietário deve revisar e aprovar
4. Após aprovação, o desenvolvedor pode mesclar a PR

### Tempo Esperado de Review

- **SLA de Resposta**: Máximo 1 semana para resposta inicial
- **Aprovação (Padrão)**: Dentro de 2 semanas para PRs padrão
- **Críticas/Hotfixes**: Dentro de 2 dias (se disponível)

## Modificações ao CODEOWNERS

Qualquer mudança ao arquivo CODEOWNERS deve seguir o processo abaixo:

### Processo de Alteração

1. **Proposta**: Criar issue ou PR com justificativa clara para a mudança
2. **Discussão**: Pelo menos 1 semana para feedback da equipe
3. **Aprovação**: Aprovação unânime dos líderes técnicos atuais
4. **Documentação**: Atualizar este arquivo com a mudança
5. **Confirmação**: Mesclar a PR com o novo arquivo CODEOWNERS

### Exemplos de Mudanças

- **Adicionar novo proprietário**: Quando nova pessoa assume liderança técnica
- **Remover proprietário**: Quando proprietário sai do projeto ou muda função
- **Propriedade por área**: Dividir responsabilidades por pasta/módulo (ex: `src/ @proprietario1`, `api/ @proprietario2`)

## Casos Especiais

### Auto-Aprovação

GitHub permite que proprietários de código aprovem suas próprias mudanças no arquivo CODEOWNERS. Isso é aceito quando:

- A mudança é claramente justificada (documentação, pequena correção)
- Outros proprietários foram notificados antes
- Revertibilidade é garantida (commits anteriores permanecem estáveis)

### Proprietários Ausentes

Se um proprietário não estiver disponível por período prolongado:

1. Notificar o outro proprietário com antecedência
2. Estabelecer cobertura temporária (segundo proprietário assume total)
3. Considerar adicionar proprietário auxiliar temporário
4. Comunicar à equipe

## Conformidade

### Auditoria

- **Mensal**: Revisar PRs aprovadas para garantir que seguem processo
- **Trimestral**: Verificar que proprietários estão ativos
- **Semestral**: Revisar necessidade de mudanças nos proprietários

### Escalation

Se proprietários não conseguem acompanhar:

1. Notificar liderança técnica/projeto
2. Considerar dividir propriedade por área
3. Adicionar proprietários adicionais se necessário
4. Revisar workload e prioridades

## Contato & Questionamentos

Para perguntas sobre este arquivo CODEOWNERS:

- Abrir uma issue no repositório com a tag `codeowners`
- Comentar diretamente em PRs com dúvidas
- Conversar diretamente com @sakovitz ou @jonasplima

## Histórico de Mudanças

| Data | Mudança | Responsável |
|------|---------|------------|
| 2025-11-13 | Criação inicial da política | Feature 002-codeowners-setup |
| | | |

---

**Versão**: 1.0
**Data de Criação**: 2025-11-13
**Próxima Revisão**: 2025-12-13 (1 mês)
