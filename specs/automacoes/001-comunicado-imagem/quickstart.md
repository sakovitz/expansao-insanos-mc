# Quickstart: API de Geração de Comunicados

**Feature**: automacoes/001-comunicado-imagem
**Data**: 2025-11-08
**Objetivo**: Guia rápido para setup e uso da API

---

## Pré-requisitos

- Python 3.11+ instalado
- Ambiente virtual "expansao" ativado
- Acesso ao repositório expansao-insanos-mc

---

## Setup Rápido (5 minutos)

### 1. Instalar Dependências

```bash
# Ativar ambiente virtual
cd c:\Users\jonas\github\expansao-insanos-mc
expansao\Scripts\activate

# Instalar bibliotecas
pip install fastapi==0.115.* uvicorn[standard]==0.32.* pydantic==2.9.* Pillow>=10.4.0
```

### 2. Baixar Fonte DejaVu Sans

**Opção A - Download Manual**:
1. Acesse: https://sourceforge.net/projects/dejavu/
2. Baixe `dejavu-fonts-ttf-2.37.zip`
3. Extraia `DejaVuSans-Bold.ttf` e `DejaVuSans.ttf`
4. Copie para `automacoes/comunicado_imagem/templates/fonts/`

**Opção B - Script Automatizado** (futuro):
```bash
python scripts/download-fonts.py
```

### 3. Preparar Template Base

Coloque a imagem de fundo em:
```
automacoes/comunicado_imagem/templates/base_template.png
```

---

## Iniciar o Servidor

```bash
# Rodar API (desenvolvimento com hot-reload)
uvicorn automacoes.comunicado_imagem.api:app --reload --host 0.0.0.0 --port 8000

# Output esperado:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete.
```

**Acessar documentação interativa**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Testar a API

### Opção 1: Swagger UI (Recomendado)

1. Abra http://localhost:8000/docs
2. Expanda `POST /gerar-comunicado`
3. Clique "Try it out"
4. Use o exemplo pré-populado ou edite os dados:

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

5. Clique "Execute"
6. Verifique a resposta em "Responses"

---

### Opção 2: cURL (Terminal)

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

**Resposta Esperada**:
```json
{
  "success": true,
  "file_path": "automacoes/outputs/20251104_XANDECO.jpeg",
  "generation_time_ms": 1823.45
}
```

---

### Opção 3: Python Requests

```python
import requests

url = "http://localhost:8000/gerar-comunicado"
data = {
    "origem": "EXPANSÃO",
    "evento": "PROMOÇÃO DE GRAU",
    "nome_integrante": "JOSÉ DA CONCEIÇÃO (245)",
    "resultado": "APROVADO:",
    "localizacao": "EXPANSÃO NACIONAL",
    "grau": "GRAU III",
    "data": "15/12/2025"
}

response = requests.post(url, json=data)
print(response.json())
# {'success': True, 'file_path': 'automacoes/outputs/20251215_JOSEDACONCEICAO.jpeg', ...}
```

---

## Estrutura de Arquivos

```
expansao-insanos-mc/
├── automacoes/
│   ├── comunicado_imagem/
│   │   ├── __init__.py
│   │   ├── api.py              ← Código principal da API
│   │   ├── generator.py        ← Lógica de geração de imagem
│   │   ├── validator.py        ← Validação customizada
│   │   ├── models.py           ← Pydantic models
│   │   └── templates/
│   │       ├── base_template.png   ← Template de fundo
│   │       └── fonts/
│   │           ├── DejaVuSans-Bold.ttf
│   │           └── DejaVuSans.ttf
│   └── outputs/                ← Imagens geradas (JPEG)
│       └── 20251104_XANDECO.jpeg
├── specs/
│   └── automacoes/
│       └── 001-comunicado-imagem/
│           ├── spec.md
│           ├── plan.md
│           ├── research.md
│           ├── data-model.md
│           ├── quickstart.md   ← Este arquivo
│           └── contracts/
│               └── api-spec.yaml
└── requirements.txt
```

---

## Exemplos de Uso

### Exemplo 1: Comunicado de Conclusão de Estágio

**Request**:
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

**Response**:
```json
{
  "success": true,
  "file_path": "automacoes/outputs/20251104_XANDECO.jpeg",
  "generation_time_ms": 1823.45
}
```

**Resultado**: Imagem salva em `automacoes/outputs/20251104_XANDECO.jpeg`

---

### Exemplo 2: Nome com Acentuação (UTF-8)

**Request**:
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

**Resultado**: Imagem renderiza corretamente "JOSÉ DA CONCEIÇÃO" com acentos preservados.

---

## Troubleshooting

### Erro: "Fonte não encontrada"

**Sintoma**:
```json
{"detail": "Erro ao gerar imagem: Fonte não encontrada"}
```

**Solução**:
1. Verifique se `DejaVuSans-Bold.ttf` está em `automacoes/comunicado_imagem/templates/fonts/`
2. Confirme permissões de leitura do arquivo

---

### Erro: "Data inválida. Formato esperado: DD/MM/AAAA"

**Sintoma**:
```json
{
  "detail": [
    {
      "loc": ["body", "data"],
      "msg": "Data inválida. Formato esperado: DD/MM/AAAA",
      "type": "value_error.str.regex"
    }
  ]
}
```

**Solução**:
Forneça data no formato brasileiro: `"04/11/2025"` (não `"2025-11-04"`)

---

### Erro: "Nome inválido. Formato esperado: NOME (NÚMERO)"

**Sintoma**:
```json
{
  "detail": [
    {
      "loc": ["body", "nome_integrante"],
      "msg": "Nome inválido. Formato esperado: NOME (NÚMERO)",
      "type": "value_error.str.regex"
    }
  ]
}
```

**Solução**:
Forneça nome com número entre parênteses: `"XANDECO (183)"` (não `"XANDECO 183"`)

---

### Performance: API demora >10 segundos

**Possíveis Causas**:
1. Imagem de template muito grande (redimensionar para 1542x1600)
2. Texto muito longo (causando iterações excessivas de ajuste de fonte)
3. Disco lento (SSD recomendado)

**Diagnóstico**:
Verifique logs para ver onde está o gargalo:
```bash
# Logs mostram tempo de cada etapa
INFO: Carregando template: 234ms
INFO: Renderizando texto: 1523ms
INFO: Salvando JPEG: 66ms
```

---

## Comandos Úteis

```bash
# Health check
curl http://localhost:8000/health

# Verificar logs em tempo real
tail -f logs/api.log  # (se configurado)

# Parar servidor (Ctrl+C no terminal)

# Limpar imagens antigas
rm automacoes/outputs/*.jpeg
```

---

## Próximos Passos

1. **Implementar código**: Seguir design de `data-model.md` e `api-spec.yaml`
2. **Criar testes**: `tests/test_api.py` e `tests/test_generator.py`
3. **Deploy**: Configurar servidor de produção (Gunicorn + Nginx)
4. **Monitoramento**: Adicionar métricas de performance e logs estruturados

---

## Documentação Completa

- **Especificação**: [spec.md](spec.md)
- **Plano de Implementação**: [plan.md](plan.md)
- **Pesquisa Técnica**: [research.md](research.md)
- **Modelo de Dados**: [data-model.md](data-model.md)
- **Contrato API**: [contracts/api-spec.yaml](contracts/api-spec.yaml)

**Dúvidas?** Consulte a documentação completa ou abra uma issue no GitHub.

