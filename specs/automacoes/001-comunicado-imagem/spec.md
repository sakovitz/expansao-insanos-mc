# Feature Specification: Automação de Geração de Comunicados em Imagem

**Feature Branch**: `automacoes/001-comunicado-imagem`
**Created**: 2025-11-08
**Status**: Draft
**Input**: User description: "Eu quero criar a estrutura de pastas do projeto seguindo o padrão definido dentro do README.md na raiz do projeto. Também quero que na pasta de seja criado dentro da pasta de automações uma automação que trabalhará com imagens. A ideia é utilizar o modelo da imagem abaixo, onde a palavra 'COMUNICADO' esteja fixa, porém, as outras variáveis mudem de acordo com a necessidade."

## Clarifications

### Session 2025-11-08

- Q: When the automation receives invalid or incomplete data (e.g., missing required field, invalid date format), how should it respond? → A: Fail immediately with error message specifying which field is invalid
- Q: When a member name is too long to fit in the allocated template space, how should the system handle it? → A: Automatically reduce font size to fit all text
- Q: How should the system handle special characters and accents in variable fields (names, locations, etc.)? → A: Support full Portuguese character set (UTF-8 encoding)
- Q: What is the primary intended use for the generated images given the 1542x1600 JPEG format? → A: Digital viewing only (web, mobile, messaging apps)
- Q: How should users invoke the image generation automation? → A: API call would be the best

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Criação da Estrutura de Pastas (Priority: P1)

Um administrador do sistema precisa organizar o projeto seguindo o padrão definido no README.md, criando as pastas principais: pipelines, ia, automacoes, data, e docs. Esta estrutura permite que diferentes tipos de trabalho sejam organizados de forma clara e escalável.

**Why this priority**: É a base fundamental para todo o projeto. Sem a estrutura correta, não é possível organizar os demais componentes de forma adequada.

**Independent Test**: Pode ser totalmente testado verificando se todas as pastas definidas no README.md foram criadas na raiz do projeto e estão acessíveis.

**Acceptance Scenarios**:

1. **Given** o projeto está na raiz sem estrutura de pastas, **When** a estrutura é criada, **Then** as pastas pipelines/, ia/, automacoes/, data/, e docs/ devem existir
2. **Given** a estrutura foi criada, **When** um usuário navega até a pasta automacoes/, **Then** ela deve estar acessível e vazia aguardando automações

---

### User Story 2 - Geração de Comunicado com Dados Variáveis (Priority: P2)

Um membro da área de Expansão precisa gerar um comunicado visual padronizado informando sobre conclusão de estágio de um integrante. O usuário faz uma chamada de API fornecendo os dados variáveis (origem, evento, nome do colete, resultado, localização, grau e data) e o sistema gera automaticamente uma imagem formatada seguindo o template padrão, retornando o caminho do arquivo.

**Why this priority**: É a funcionalidade principal da automação. Permite criar comunicados visuais de forma rápida e padronizada, economizando tempo e garantindo consistência visual.

**Independent Test**: Pode ser testado fornecendo um conjunto de dados de entrada (ex: origem="EXPANSÃO", evento="CONCLUSÃO DE ESTÁGIO", nome="XANDECO (183)") e verificando se a imagem gerada contém todos os elementos visuais corretos no template.

**Acceptance Scenarios**:

1. **Given** dados válidos do integrante, **When** uma chamada de API é feita com esses dados, **Then** a API deve retornar o caminho de uma imagem gerada com o texto "COMUNICADO" fixo no topo
2. **Given** dados do comunicado (origem, evento, nome, resultado, localização, grau, data), **When** enviados via API, **Then** todos os campos variáveis devem aparecer formatados corretamente nas posições definidas pelo template
3. **Given** uma chamada de API bem-sucedida, **When** a imagem retornada é visualizada, **Then** deve seguir o estilo visual do template (fundo escuro, textos em amarelo e branco, logo marca d'água)

---

### User Story 3 - Manutenção de Elementos Fixos do Template (Priority: P3)

O sistema deve manter automaticamente todos os elementos fixos do template em cada comunicado gerado: o título "COMUNICADO", rodapé "COMANDO MUNDIAL", aviso "COMUNICADO INTERNO", e texto de proibição de divulgação em redes sociais. Estes elementos garantem a identidade visual e as políticas de divulgação.

**Why this priority**: Garante consistência e conformidade com as políticas de comunicação interna. Embora importante, é uma funcionalidade que suporta as anteriores.

**Independent Test**: Pode ser testado gerando múltiplos comunicados com dados diferentes e verificando que todos os elementos fixos aparecem idênticos em todas as imagens.

**Acceptance Scenarios**:

1. **Given** qualquer conjunto de dados variáveis, **When** a imagem é gerada, **Then** deve conter "COMUNICADO" em amarelo no topo
2. **Given** uma imagem gerada, **When** verificado o rodapé, **Then** deve mostrar "COMANDO MUNDIAL", "COMUNICADO INTERNO" e "PROIBIDA A DIVULGAÇÃO EM QUALQUER REDE SOCIAL"
3. **Given** múltiplas execuções da automação, **When** comparados os elementos fixos, **Then** devem ser idênticos em posição, cor e formatação

---

### Edge Cases

- **Resolved**: Nome de integrante muito longo → Sistema reduz automaticamente o tamanho da fonte para ajustar todo o texto no espaço disponível
- **Resolved**: Caracteres especiais ou acentuação → Sistema suporta conjunto completo de caracteres portugueses (UTF-8) incluindo á, ã, ç, õ, etc.
- **Resolved**: Data fornecida em formato inválido → Sistema falha com mensagem específica indicando formato esperado (DD/MM/AAAA)
- **Resolved**: Resolução adequada → 1542x1600 JPEG otimizado para visualização digital (web, mobile, messaging apps), não para impressão
- **Resolved**: Campo variável vazio ou ausente → Sistema falha com mensagem específica indicando qual campo está faltando

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Sistema DEVE criar a estrutura de pastas conforme definida no README.md (pipelines/, ia/, automacoes/, data/, docs/)
- **FR-002**: Sistema DEVE criar uma automação na pasta automacoes/ que gera imagens de comunicados acessível via API
- **FR-003**: API DEVE aceitar como entrada os seguintes dados variáveis: origem do comunicado, tipo de evento, nome e número do colete, resultado, localização, grau do integrante, e data
- **FR-003a**: Sistema DEVE suportar codificação UTF-8 completa para caracteres portugueses (incluindo á, ã, â, à, ç, é, ê, í, ó, õ, ô, ú) em todos os campos variáveis
- **FR-004**: Imagem gerada DEVE conter o texto "COMUNICADO" fixo no topo em formato destacado
- **FR-005**: Imagem gerada DEVE posicionar os dados variáveis nas seguintes seções (em ordem): origem (fonte do comunicado), evento (título do acontecimento), nome do integrante com número, resultado com localização e grau, data
- **FR-005a**: Sistema DEVE ajustar automaticamente o tamanho da fonte de campos variáveis longos para garantir que todo o texto caiba no espaço alocado do template, mantendo a legibilidade
- **FR-006**: Imagem gerada DEVE incluir elementos fixos no rodapé: "COMANDO MUNDIAL", "COMUNICADO INTERNO", "PROIBIDA A DIVULGAÇÃO EM QUALQUER REDE SOCIAL"
- **FR-007**: Imagem DEVE seguir o estilo visual do template: fundo escuro com marca d'água, textos em amarelo para destaques (COMUNICADO, evento, resultado/localização/grau) e branco para demais informações
- **FR-008**: Sistema DEVE validar que todos os campos obrigatórios foram fornecidos antes de gerar a imagem, falhando imediatamente com mensagem de erro que especifica qual campo está inválido ou ausente
- **FR-009**: Sistema DEVE gerar imagens no formato JPEG com resolução de 1542x1600 pixels
- **FR-010**: Sistema DEVE salvar as imagens geradas como arquivo temporário e retornar o caminho via resposta da API, com nome no formato "YYYYMMDD_INTEGRANTE.jpeg" (exemplo: "20251108_XANDECO.jpeg")
- **FR-011**: API DEVE retornar código de status HTTP apropriado e mensagem de erro detalhada quando a validação falhar

### Key Entities

- **Comunicado**: Representa um comunicado oficial contendo campos fixos (título, rodapé, avisos) e campos variáveis (origem, evento, integrante, resultado, data)
- **Integrante**: Entidade que contém nome do colete, número identificador, grau, e localização atual
- **Template Visual**: Define o layout, cores, fontes e posicionamento dos elementos na imagem final

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Estrutura de pastas do projeto é criada em menos de 5 segundos e reflete exatamente o padrão do README.md
- **SC-002**: Usuário consegue gerar um comunicado visual completo através de chamada de API fornecendo os dados variáveis, com resposta em menos de 10 segundos
- **SC-003**: 100% dos comunicados gerados contêm todos os elementos fixos (COMUNICADO, rodapé, avisos) em formato idêntico
- **SC-004**: Imagens geradas são visualmente legíveis e mantêm a identidade visual do template original (cores, layout, marca d'água)
- **SC-005**: Sistema processa e valida os dados de entrada antes da geração, rejeitando entradas inválidas com mensagem clara sobre o problema

## Assumptions

- O template visual (cores, fontes, layout) está definido pela imagem de referência fornecida
- A API será utilizada por membros da área de Expansão ou sistemas integrados que têm conhecimento dos dados necessários
- A API será RESTful e seguirá convenções HTTP padrão para sucesso (200) e erro (400, 500)
- Formato de data de entrada padrão brasileiro (DD/MM/AAAA) baseado no exemplo "04/11/2025"
- Formato de data no nome do arquivo é YYYYMMDD (exemplo: 20251108)
- Nome do integrante no arquivo usa apenas o apelido do colete sem número (exemplo: "XANDECO" de "XANDECO (183)")
- Resolução de 1542x1600 pixels em formato JPEG é otimizada para visualização digital (web, mobile, messaging apps) e não é destinada para impressão de alta qualidade
- A marca d'água de fundo é um elemento decorativo e não precisa ser dinâmica
- Campos de texto em amarelo indicam informações de destaque/variáveis: COMUNICADO (fixo mas destacado), origem, evento, resultado/localização/grau
- Campos de texto em branco indicam informações complementares: nome do integrante, rodapé, avisos
- Arquivo temporário gerado pode ser movido/copiado pelo sistema chamador para destino final desejado

## Dependencies

- Biblioteca de manipulação de imagens compatível com Python 3.11
- Acesso ao sistema de arquivos para criar estrutura de pastas
- Template base ou especificações de design (fontes, cores exatas, dimensões) para reproduzir o layout visual
