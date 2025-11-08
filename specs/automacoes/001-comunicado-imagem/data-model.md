# Modelo de Dados: Automação de Comunicados em Imagem

**Feature**: automacoes/001-comunicado-imagem
**Data**: 2025-11-08
**Status**: Design da Fase 1

---

## Entidades Principais

### 1. Comunicado

**Descrição**: Representa um comunicado oficial com elementos fixos e variáveis

**Campos**:
- `origem`: string - Fonte do comunicado (ex: "EXPANSÃO")
- `evento`: string - Tipo de evento/acontecimento (ex: "CONCLUSÃO DE ESTÁGIO")
- `nome_integrante`: string - Nome do colete com número (ex: "XANDECO (183)")
- `resultado`: string - Resultado do evento (ex: "SEM APROVEITAMENTO:")
- `localizacao`: string - Onde o integrante está (ex: "EXPANSÃO REGIONAL")
- `grau`: string - Grau do colete (ex: "GRAU V")
- `data`: string - Data do comunicado (formato: "DD/MM/AAAA")

**Elementos Fixos** (não são campos, são constantes):
- Título: "COMUNICADO"
- Rodapé: "COMANDO MUNDIAL", "COMUNICADO INTERNO", "PROIBIDA A DIVULGAÇÃO EM QUALQUER REDE SOCIAL"

**Regras de Validação**:
- Todos os campos são obrigatórios (não podem ser vazio ou null)
- `data` deve seguir formato brasileiro "DD/MM/AAAA"
- `nome_integrante` deve conter o padrão "NOME (NÚMERO)"
- Todos os campos suportam UTF-8 completo (caracteres portugueses)
- Comprimento máximo de cada campo: 200 caracteres

**Relacionamentos**:
- 1 Comunicado contém 1 Integrante (informações extraídas dos campos)

---

### 2. Integrante

**Descrição**: Entidade derivada que representa um membro do clube

**Campos Derivados**:
- `nome_colete`: string - Extraído de `nome_integrante`, parte antes do parênteses (ex: "XANDECO")
- `numero`: integer - Extraído de `nome_integrante`, número dentro do parênteses (ex: 183)
- `grau`: string - Copiado diretamente do campo `grau` do Comunicado
- `localizacao`: string - Copiado diretamente do campo `localizacao` do Comunicado

**Uso**: Utilizado para gerar o nome do arquivo de saída (formato: `YYYYMMDD_NOMECOLETE.jpeg`)

**Exemplo**:
```
nome_integrante: "XANDECO (183)"
→ nome_colete: "XANDECO"
→ numero: 183

Arquivo gerado: "20251108_XANDECO.jpeg"
```

---

### 3. Template Visual

**Descrição**: Define o layout, cores e posicionamento dos elementos na imagem

**Propriedades**:
- `largura`: 1542 pixels
- `altura`: 1600 pixels
- `formato`: JPEG
- `qualidade_jpeg`: 90 (0-100)

**Elementos Visuais**:

| Elemento | Cor | Fonte | Tamanho | Posição |
|----------|-----|-------|---------|---------|
| "COMUNICADO" | Amarelo (#FFD700) | DejaVu Sans Bold | 120px | Topo centralizado |
| Origem | Branco (#FFFFFF) | DejaVu Sans Bold | 90px | Abaixo do título |
| Evento | Amarelo (#FFD700) | DejaVu Sans Bold | 100px | Centro superior |
| Nome Integrante | Branco (#FFFFFF) | DejaVu Sans Regular | 70px | Centro |
| Resultado | Amarelo (#FFD700) | DejaVu Sans Bold | 90px | Centro inferior |
| Localização | Amarelo (#FFD700) | DejaVu Sans Bold | 80px | Mesma linha do resultado |
| Grau | Amarelo (#FFD700) | DejaVu Sans Bold | 80px | Mesma linha do resultado |
| Data | Branco (#FFFFFF) | DejaVu Sans Regular | 70px | Base da imagem |
| Rodapé (3 linhas) | Branco (#FFFFFF) | DejaVu Sans Regular | 50px | Rodapé |

**Comportamento Dinâmico**:
- Se qualquer campo exceder o espaço disponível → reduzir fonte automaticamente
- Tamanho mínimo de fonte: 30px (garantir legibilidade)
- Algoritmo de ajuste: decrementar 2px por iteração até caber

**Background**:
- Fundo escuro (preto ou dark gray)
- Marca d'água decorativa (logo do clube em opacidade reduzida)

---

## Fluxo de Dados

```
API Request (JSON)
    ↓
Validação Pydantic (ComunicadoRequest)
    ↓
Extração de Integrante (nome_colete, numero)
    ↓
Geração de Imagem (Pillow + Template)
    ↓
Salvar JPEG (YYYYMMDD_NOMECOLETE.jpeg)
    ↓
API Response (file_path)
```

---

## Exemplos de Dados

### Exemplo 1: Comunicado Completo

```json
{
  "origem": "EXPANSÃO",
  "evento": "CONCLUSÃO DE ESTÁGIO",
  "nome_integrante": "XANDECO (183)",
  "resultado": "SEM APROVEITAMENTO:",
  "localizacao": "EXPANSÃO REGIONAL",
  "grau": "GRAU V",
  "data": "04/11/2025"
}
```

**Saída**:
- Arquivo: `20251104_XANDECO.jpeg`
- Integrante derivado: `{nome_colete: "XANDECO", numero: 183}`

---

### Exemplo 2: Nome com Caracteres UTF-8

```json
{
  "origem": "EXPANSÃO",
  "evento": "PROMOÇÃO DE GRAU",
  "nome_integrante": "JOSÉ DA CONCEIÇÃO (245)",
  "resultado": "APROVADO:",
  "localizacao": "EXPANSÃO NACIONAL",
  "grau": "GRAU III",
  "data": "15/12/2025"
}
```

**Saída**:
- Arquivo: `20251215_JOSEDACONCEICAO.jpeg` (normalizado para nome de arquivo)
- UTF-8 preservado na imagem renderizada: "JOSÉ DA CONCEIÇÃO"

---

## Estados e Transições

### Estado do Comunicado

```
┌──────────┐
│  Criado  │ (JSON recebido)
└────┬─────┘
     │
     ▼ Validação
┌──────────┐
│ Validado │ (todos os campos presentes e corretos)
└────┬─────┘
     │
     ▼ Geração
┌──────────┐
│  Gerado  │ (imagem JPEG salva com sucesso)
└──────────┘
```

**Transições de Erro**:
- `Criado → Erro de Validação`: Campo faltando ou formato inválido
- `Validado → Erro de Geração`: Falha ao renderizar/salvar imagem

---

## Regras de Negócio

### RN-001: Formato de Data
- **Regra**: Data deve ser no formato brasileiro "DD/MM/AAAA"
- **Validação**: Regex `^\d{2}/\d{2}/\d{4}$`
- **Erro**: HTTP 400 com mensagem "Data inválida. Formato esperado: DD/MM/AAAA"

### RN-002: Padrão de Nome de Integrante
- **Regra**: Nome deve conter padrão "NOME (NÚMERO)"
- **Validação**: Regex `^.+\s\(\d+\)$`
- **Erro**: HTTP 400 com mensagem "Nome inválido. Formato esperado: NOME (NÚMERO)"

### RN-003: Nome de Arquivo
- **Regra**: Nome do arquivo é `YYYYMMDD_NOMECOLETE.jpeg`
- **Extração**:
  - Data: Converter "DD/MM/AAAA" → "YYYYMMDD"
  - Nome: Extrair tudo antes de "(" e remover espaços
- **Normalização**: Remover acentos do nome do arquivo (manter UTF-8 na imagem)

### RN-004: Ajuste de Fonte Dinâmico
- **Regra**: Se texto exceder espaço, reduzir fonte até caber (mínimo 30px)
- **Algoritmo**:
  1. Começar com tamanho padrão
  2. Medir texto com `font.getbbox()`
  3. Se exceder → reduzir 2px
  4. Repetir até caber ou atingir mínimo
- **Erro**: Se atingir mínimo e ainda não caber → HTTP 400 "Texto muito longo"

### RN-005: Unicidade de Arquivo
- **Regra**: Se arquivo já existir, sobrescrever (comunicados são idempotentes)
- **Comportamento**: Mesmo comunicado gerado 2x → mesmo arquivo, conteúdo idêntico

---

## Constraints de Performance

| Métrica | Limite | Medição |
|---------|--------|---------|
| Tempo de geração | <10 segundos | Timer em API handler |
| Tamanho do arquivo JPEG | 200-500 KB | Qualidade 90, otimizado |
| Memória RAM | <100 MB | Pillow mantém imagem em memória |
| Taxa de sucesso | >99% | Monitorar logs de erro |

---

## Dependências de Dados

**Inputs Externos**:
- Template de imagem base (`automacoes/comunicado_imagem/templates/base_template.png`)
- Fontes TrueType (`automacoes/comunicado_imagem/templates/fonts/DejaVuSans-Bold.ttf`)

**Outputs**:
- Arquivo JPEG em diretório temporário (`automacoes/outputs/YYYYMMDD_NOME.jpeg`)
- Resposta JSON com `file_path`

**Sem Persistência**:
- Dados não são salvos em banco de dados
- Arquivos são temporários (podem ser movidos/deletados pelo consumidor da API)

