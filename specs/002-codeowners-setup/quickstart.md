# Guia de Início Rápido: Arquivo CODEOWNERS

## O que é CODEOWNERS?

O arquivo `CODEOWNERS` é um arquivo de configuração especial do GitHub que especifica qual(is) pessoa(s) ou equipe(s) devem revisar pull requests em áreas específicas do repositório. É uma forma de aplicar governança automática de revisão de código.

## Localização

O arquivo deve estar localizado em um dos seguintes locais:
- `./CODEOWNERS` (raiz do repositório - **recomendado**)
- `./.github/CODEOWNERS`
- `./docs/CODEOWNERS`

Para este projeto, usamos: **`./CODEOWNERS`** (raiz do repositório)

## Sintaxe do CODEOWNERS

A sintaxe é simples:

```
[padrão de arquivo ou pasta]  [proprietário(s)]
```

Exemplos:

```
# Todos os arquivos
*  @sakovitz

# Pasta específica
src/  @sakovitz

# Arquivo específico
README.md  @sakovitz

# Múltiplos proprietários
api/  @sakovitz @outro-usuario

# Equipe do GitHub
frontend/  @organization/frontend-team
```

## Configuração para este Projeto

Para este projeto, @sakovitz é designado como proprietário de código para **todo o repositório**:

```
*  @sakovitz
```

Esta linha única indica que @sakovitz deve aprovar mudanças em qualquer arquivo do projeto.

## Como Funciona

1. **Quando uma PR é criada**: GitHub automaticamente revisa o arquivo CODEOWNERS
2. **Identifica arquivos modificados**: Determina qual(is) proprietário(s) deve(m) revisar
3. **Requer aprovação**: Marca @sakovitz como revisor necessário
4. **Bloqueia merge**: A PR não pode ser mesclada sem aprovação de @sakovitz
5. **Registra aprovação**: Quando aprovada, GitHub permite o merge

## Validação

Para verificar se o arquivo foi configurado corretamente:

1. **No repositório local**:
   ```bash
   # Listar o arquivo
   cat CODEOWNERS

   # Verificar sintaxe (o GitHub fará isso automaticamente)
   ```

2. **Na interface do GitHub**:
   - Crie uma PR de teste
   - Veja se @sakovitz aparece como revisor necessário
   - Verifique se o botão de merge fica desabilitado até aprovação

3. **Validações automáticas do GitHub**:
   - GitHub valida a sintaxe automaticamente
   - Se houver erros, aparecerão na interface de PR
   - Mensagens de erro indicam qual é o problema

## Casos de Uso

### Padrão Básico (Todo o repositório)
```
*  @sakovitz
```

### Padrão Avançado (Diferentes proprietários por área)
```
# Arquivo raiz
/CODEOWNERS  @sakovitz

# Documentação
/docs/  @sakovitz @documentação-team

# Código-fonte
/src/  @sakovitz

# Testes
/tests/  @sakovitz
```

## Boas Práticas

1. **Certifique-se de que o proprietário existe**: @sakovitz deve ser um usuário GitHub válido com acesso ao repositório
2. **Documente mudanças**: Se modificar CODEOWNERS, inclua em PR com justificativa
3. **Revise periodicamente**: Mantenha CODEOWNERS atualizado com mudanças de equipe
4. **Considere equipes**: Para múltiplos proprietários, use equipes do GitHub (@org/team-name)

## Referência

- [Documentação GitHub - CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Regras de padrão CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners#example-of-a-codeowners-file)

## Próximas Etapas

1. Criar arquivo `/CODEOWNERS` na raiz do repositório
2. Adicionar conteúdo: `* @sakovitz`
3. Confirmar no Git
4. Criar PR de teste para validar funcionamento
5. Documentar política de aprovação para a equipe
