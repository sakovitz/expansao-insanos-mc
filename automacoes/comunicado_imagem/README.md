# Automação de Geração de Comunicados em Imagem

**Versão**: 1.0.0
**Feature**: automacoes/001-comunicado-imagem
**Status**: ✅ Implementado e testado (27/27 testes passando)

---

## 📋 Visão Geral

API REST que gera comunicados visuais padronizados para a área de Expansão do Insanos MC.

**Características principais**:
- ✅ Geração de imagens JPEG 1542x1600 pixels
- ✅ Suporte completo a caracteres UTF-8 portugueses (á, ã, ç, õ, etc.)
- ✅ Validação automática de dados de entrada
- ✅ Ajuste dinâmico de tamanho de fonte
- ✅ Tempo de resposta < 10 segundos (média: 0.5-2 segundos)
- ✅ Documentação OpenAPI/Swagger automática

---

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11+
- Ambiente virtual `expansao` ativado

### Instalação

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Baixar fontes DejaVu Sans
python download_fonts.py

# 3. Adicionar imagem de template (fornecida pelo usuário)
# Colocar em: automacoes/comunicado_imagem/templates/base_template.png
```

### Iniciar Servidor

```bash
# Desenvolvimento (com hot-reload)
uvicorn automacoes.comunicado_imagem.api:app --reload --host 0.0.0.0 --port 8000

# Acessar documentação interativa
# http://localhost:8000/docs
```

### Exemplo de Uso

**Request**:
```bash
curl -X POST http://localhost:8000/gerar-comunicado \
  -H "Content-Type: application/json" \
  -d '{
    "origem": "EXPANSÃO",
    "evento": "CONCLUSÃO DE ESTÁGIO",
    "nome_integrante": "XANDECO (183)",
    "resultado": "SEM APROVEITAMENTO:",
    "localizacao": "EXPANSÃO REGIONAL",
    "grau": "GRAU V",
    "data": "04/11/2025"
  }'
```

**Response**:
```json
{
  "success": true,
  "file_path": "automacoes/outputs/20251104_XANDECO.jpeg",
  "generation_time_ms": 507.77
}
```

---

## 📁 Estrutura do Projeto

```
automacoes/comunicado_imagem/
├── __init__.py              # Módulo principal
├── api.py                   # FastAPI application (endpoint REST)
├── generator.py             # Lógica de geração de imagem (Pillow)
├── validator.py             # Validação customizada de dados
├── models.py                # Modelos Pydantic (request/response)
├── templates/
│   ├── base_template.png    # Imagem de fundo (fornecida pelo usuário)
│   └── fonts/
│       ├── DejaVuSans-Bold.ttf
│       └── DejaVuSans.ttf
└── README.md                # Este arquivo

automacoes/outputs/          # Imagens geradas (temporárias)
└── YYYYMMDD_INTEGRANTE.jpeg

tests/
├── unit/
│   ├── test_validator.py    # Testes de validação
│   └── test_generator.py    # Testes de geração
└── integration/
    └── test_api_integration.py  # Testes end-to-end da API
```

---

## 🧪 Testes

```bash
# Executar todos os testes
pytest tests/ -v

# Executar apenas testes unitários
pytest tests/unit/ -v

# Executar apenas testes de integração
pytest tests/integration/ -v

# Testes com cobertura
pytest tests/ --cov=automacoes.comunicado_imagem
```

**Status atual**: ✅ 27/27 testes passando

---

## 📖 API Endpoints

### `POST /gerar-comunicado`

Gera imagem de comunicado.

**Body** (JSON):
```json
{
  "origem": "string",           // Ex: "EXPANSÃO"
  "evento": "string",           // Ex: "CONCLUSÃO DE ESTÁGIO"
  "nome_integrante": "string",  // Ex: "XANDECO (183)" - Formato: NOME (NÚMERO)
  "resultado": "string",        // Ex: "SEM APROVEITAMENTO:"
  "localizacao": "string",      // Ex: "EXPANSÃO REGIONAL"
  "grau": "string",             // Ex: "GRAU V"
  "data": "string"              // Ex: "04/11/2025" - Formato: DD/MM/AAAA
}
```

**Validações**:
- Todos os campos obrigatórios
- `data`: formato DD/MM/AAAA
- `nome_integrante`: formato NOME (NÚMERO)
- Comprimento máximo: 200 caracteres por campo

**Response** (200):
```json
{
  "success": true,
  "file_path": "automacoes/outputs/20251104_XANDECO.jpeg",
  "generation_time_ms": 507.77
}
```

**Erros**:
- `400`: Validação falhou (campo inválido)
- `422`: Campo obrigatório faltando
- `500`: Erro interno (fonte não encontrada, etc.)

### `GET /health`

Health check.

**Response** (200):
```json
{
  "status": "healthy",
  "service": "comunicado-api"
}
```

### `GET /`

Informações da API.

---

## 🎨 Template Visual

A imagem gerada possui:

**Dimensões**: 1542x1600 pixels
**Formato**: JPEG (qualidade 90)
**Tamanho**: ~200-500 KB

**Elementos fixos**:
- Título: "COMUNICADO" (amarelo #FFD700, 120px, bold)
- Rodapé: "COMANDO MUNDIAL" / "COMUNICADO INTERNO" / "PROIBIDA A DIVULGAÇÃO..."

**Elementos variáveis** (posicionados automaticamente):
- Origem (branco, 90px, bold)
- Evento (amarelo, 100px, bold)
- Nome Integrante (branco, 70px, regular)
- Resultado (amarelo, 90px, bold)
- Localização (amarelo, 80px, bold)
- Grau (amarelo, 80px, bold)
- Data (branco, 70px, regular)

**Ajuste automático**: Se o texto for muito longo, a fonte é reduzida automaticamente (mínimo: 30px)

---

## 🔧 Troubleshooting

### Erro: "Fonte não encontrada"

**Causa**: Arquivos TTF não estão no diretório correto.

**Solução**:
```bash
python download_fonts.py
```

Ou baixar manualmente de https://sourceforge.net/projects/dejavu/ e colocar em `automacoes/comunicado_imagem/templates/fonts/`

### Erro: "Template não encontrado"

**Causa**: Imagem de fundo não foi adicionada.

**Solução**: O usuário deve fornecer a imagem de template e salvá-la em:
```
automacoes/comunicado_imagem/templates/base_template.png
```

Se não fornecida, o sistema cria uma imagem com fundo escuro (#1a1a1a).

### Performance: API demora muito

**Diagnóstico**: Verificar logs para identificar gargalo:
```
INFO: Carregando template: 234ms
INFO: Renderizando texto: 1523ms
INFO: Salvando JPEG: 66ms
```

**Possíveis causas**:
- Template muito grande (redimensionar para 1542x1600)
- Disco lento (mover outputs/ para SSD)

---

## 📚 Documentação Completa

- **Especificação**: [specs/automacoes/001-comunicado-imagem/spec.md](../../specs/automacoes/001-comunicado-imagem/spec.md)
- **Plano de Implementação**: [specs/automacoes/001-comunicado-imagem/plan.md](../../specs/automacoes/001-comunicado-imagem/plan.md)
- **Pesquisa Técnica**: [specs/automacoes/001-comunicado-imagem/research.md](../../specs/automacoes/001-comunicado-imagem/research.md)
- **Modelo de Dados**: [specs/automacoes/001-comunicado-imagem/data-model.md](../../specs/automacoes/001-comunicado-imagem/data-model.md)
- **Quickstart**: [specs/automacoes/001-comunicado-imagem/quickstart.md](../../specs/automacoes/001-comunicado-imagem/quickstart.md)
- **Contrato API**: [specs/automacoes/001-comunicado-imagem/contracts/api-spec.yaml](../../specs/automacoes/001-comunicado-imagem/contracts/api-spec.yaml)

---

## 🛠️ Tecnologias

- **Python 3.11**
- **FastAPI 0.115.x** - Framework de API REST
- **Uvicorn 0.32.x** - Servidor ASGI
- **Pydantic 2.9.x** - Validação de dados
- **Pillow 12.0.0** - Manipulação de imagens
- **DejaVu Sans** - Fonte TrueType com suporte UTF-8
- **pytest 9.0.0** - Framework de testes

---

## 📄 Licença

Propriedade de **Insanos MC - Área de Expansão**

---

## 🤝 Contribuindo

1. Criar branch no padrão: `automacoes/NNN-feature-name`
2. Implementar feature seguindo `specs/`
3. Adicionar testes em `tests/`
4. Garantir 100% dos testes passando
5. Atualizar documentação
6. Criar Pull Request

---

## 📞 Suporte

Para dúvidas ou problemas, consultar:
- Documentação completa em `specs/automacoes/001-comunicado-imagem/`
- Logs da API para diagnóstico
- Testes de integração para exemplos de uso
