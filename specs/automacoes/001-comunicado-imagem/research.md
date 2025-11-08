# Documento de Pesquisa: Automação de Geração de Comunicados em Imagem

**Data**: 2025-11-08
**Feature**: automacoes/001-comunicado-imagem
**Objetivo**: Resolver questões técnicas e selecionar tecnologias para implementação

---

## Decisões Técnicas

### 1. Biblioteca de Manipulação de Imagens

**Decisão**: **Pillow >= 10.4.0**

**Rationale**:
- **Suporte UTF-8 Completo**: Funciona nativamente com caracteres portugueses (á, ã, ç, õ) sem necessidade de bibliotecas adicionais
- **Performance Superior**: Gera imagens em <2 segundos, muito abaixo do requisito de <10s
- **Facilidade de Uso**: API intuitiva com `ImageDraw.text()` e `ImageFont.truetype()` para renderização
- **Maturidade**: Fork oficial do PIL com 12+ anos de desenvolvimento ativo, releases trimestrais
- **Zero Dependências Externas**: Instalação via pip sem necessidade de binários externos (diferente de Wand/ImageMagick)
- **Python 3.11 Nativo**: Suporte oficial desde versão 9.3.0

**Alternativas Consideradas**:
- **Wand (ImageMagick binding)**: ❌ Rejeitada - Requer ImageMagick binary externo, complexidade desnecessária
- **pyvips (libvips binding)**: ❌ Rejeitada - Overkill para caso de uso, requer libvips binary, API menos intuitiva
- **OpenCV (cv2)**: ❌ Rejeitada - Focado em computer vision, suporte UTF-8 limitado e complicado
- **Pillow-SIMD**: ⚠️ Alternativa futura opcional se houver necessidade de otimização adicional (4-6x mais rápido)

**Considerações Especiais**:
- **Fontes TrueType Obrigatórias**: Necessário incluir arquivo `.ttf` no projeto
- **Fonte Recomendada**: DejaVu Sans (suporte completo a português, licença livre)
- **Estrutura**: `automacoes/comunicado_imagem/templates/fonts/DejaVuSans-Bold.ttf`
- **Text Wrapping**: Não é automático - requer implementação manual com `font.getlength()`
- **JPEG Quality**: Recomendado 85-95 para balanço qualidade vs tamanho

---

### 2. Framework de API REST

**Decisão**: **FastAPI 0.115.x + Uvicorn 0.32.x**

**Rationale**:
- **Validação Built-in**: Pydantic V2 integrado, validação automática via Python type hints
- **Performance**: 30%+ mais rápido que Flask, ASGI nativo, ideal para I/O-bound workloads
- **Simplicidade**: API completa em arquivo único, zero boilerplate
- **Auto-documentação**: Swagger UI e ReDoc gerados automaticamente
- **HTTP Status Codes**: Retorna 422 automaticamente para erros de validação, 200 para sucesso
- **Logging Estruturado**: Integração nativa com Python `logging` stdlib, middleware support

**Alternativas Consideradas**:
- **Flask**: ❌ Rejeitada - Sem validação built-in (precisa Marshmallow), 30% mais lento, mais código
- **Django REST Framework**: ❌ Rejeitada - Overkill (ORM, admin, auth não necessários), 10+ dependências
- **Falcon**: ❌ Rejeitada - Sem validação built-in, minimalista demais, menos recursos
- **Bottle**: ❌ Rejeitada - Sem async nativo, validação manual, menos ativo

**Estrutura Recomendada**:
- **Início**: Single-file em `automacoes/comunicado_imagem/api.py`
- **Futuro**: Modular se crescer (separar models.py, generator.py, validator.py)

**Dependências**:
```
fastapi==0.115.*
uvicorn[standard]==0.32.*
pydantic==2.9.*
```

---

## Implementações de Referência

### Exemplo: Geração de Imagem com UTF-8

```python
from PIL import Image, ImageDraw, ImageFont

def gerar_comunicado(texto: str, output_path: str):
    # Carregar fundo
    img = Image.open("templates/fundo.png").convert('RGB')
    img = img.resize((1542, 1600), Image.Resampling.LANCZOS)

    # Configurar fonte (OBRIGATÓRIO para UTF-8)
    fonte = ImageFont.truetype("fonts/DejaVuSans-Bold.ttf", 80)
    draw = ImageDraw.Draw(img)

    # Desenhar texto centralizado
    bbox = draw.textbbox((0, 0), texto, font=fonte)
    x = (1542 - (bbox[2] - bbox[0])) // 2
    y = (1600 - (bbox[3] - bbox[1])) // 2

    # Texto com sombra para legibilidade
    draw.text((x+3, y+3), texto, font=fonte, fill=(0,0,0))
    draw.text((x, y), texto, font=fonte, fill=(255,255,255))

    # Salvar JPEG
    img.save(output_path, 'JPEG', quality=90, optimize=True)
```

### Exemplo: Endpoint FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

app = FastAPI(title="Comunicado API")
logger = logging.getLogger(__name__)

class ComunicadoRequest(BaseModel):
    origem: str
    evento: str
    nome: str
    resultado: str
    localizacao: str
    grau: str
    data: str

@app.post("/gerar-comunicado")
async def gerar_comunicado(req: ComunicadoRequest):
    try:
        logger.info(f"Gerando comunicado para {req.nome}")
        # Chamar gerador de imagem
        file_path = f"outputs/{req.data.replace('/','')}_{req.nome}.jpeg"
        return {"success": True, "file_path": file_path}
    except Exception as e:
        logger.error(f"Erro: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Próximos Passos

### Fase 1: Design & Contratos

1. **Data Model**: Definir modelos Pydantic para Comunicado e Integrante
2. **API Contract**: Especificação OpenAPI para POST `/gerar-comunicado`
3. **Quickstart**: Guia de setup e uso da API

### Dependências a Adicionar

```bash
# requirements.txt
Pillow>=10.4.0,<13.0.0
fastapi==0.115.*
uvicorn[standard]==0.32.*
pydantic==2.9.*
```

### Recursos Externos Necessários

- Fonte DejaVu Sans (download: https://sourceforge.net/projects/dejavu/)
- Template de imagem base (fundo escuro com marca d'água)
- Especificação de cores exatas (amarelo, branco, preto)

---

## Validação de Requisitos

| Requisito | Tecnologia | Status |
|-----------|-----------|--------|
| Python 3.11 | Pillow + FastAPI | ✅ Suportado |
| UTF-8 português | Pillow + DejaVu Sans | ✅ Completo |
| JPEG 1542x1600 | Pillow | ✅ Configurável |
| API REST | FastAPI | ✅ Nativo |
| Validação entrada | Pydantic | ✅ Automática |
| <10s resposta | Pillow + FastAPI | ✅ <2s estimado |
| HTTP status codes | FastAPI | ✅ Automático |
| Logging estruturado | FastAPI middleware | ✅ Built-in |
| Ajuste de fonte | Pillow custom logic | ✅ Manual |

**Conclusão**: Todas as tecnologias selecionadas atendem aos requisitos da especificação.

