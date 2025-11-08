"""
API REST para geração de comunicados em imagem.

Este módulo fornece endpoints FastAPI para gerar comunicados visuais
padronizados com validação automática e resposta em <10 segundos.
"""

import logging
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ComunicadoRequest, ComunicadoResponse
from .validator import validate_comunicado_full
from .generator import ComunicadoGenerator

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="Comunicado Image Generation API",
    description="API REST para geração automática de comunicados visuais padronizados para a área de Expansão do Insanos MC.",
    version="1.0.0",
    contact={
        "name": "Área de Expansão - Insanos MC"
    }
)

# Configurar CORS (permitir chamadas de qualquer origem)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar gerador de comunicados
generator = ComunicadoGenerator()


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Verifica se a API está operacional.

    Returns:
        dict: Status da API

    Example:
        >>> GET /health
        {
            "status": "healthy",
            "service": "comunicado-api"
        }
    """
    logger.info("Health check requisitado")
    return {
        "status": "healthy",
        "service": "comunicado-api"
    }


@app.post("/gerar-comunicado", response_model=ComunicadoResponse)
async def gerar_comunicado(comunicado: ComunicadoRequest) -> ComunicadoResponse:
    """
    Gera uma imagem JPEG de comunicado com os dados fornecidos.

    Este endpoint:
    - Valida todos os campos obrigatórios
    - Gera imagem 1542x1600 JPEG
    - Salva com nome YYYYMMDD_INTEGRANTE.jpeg
    - Retorna caminho do arquivo gerado

    Args:
        comunicado: Dados do comunicado (origem, evento, nome, resultado, localização, grau, data)

    Returns:
        ComunicadoResponse: Resposta com sucesso, caminho do arquivo e tempo de geração

    Raises:
        HTTPException 400: Dados de entrada inválidos
        HTTPException 500: Erro interno ao gerar imagem

    Example:
        >>> POST /gerar-comunicado
        {
            "origem": "EXPANSÃO",
            "evento": "CONCLUSÃO DE ESTÁGIO",
            "nome_integrante": "XANDECO (183)",
            "resultado": "SEM APROVEITAMENTO:",
            "localizacao": "EXPANSÃO REGIONAL",
            "grau": "GRAU V",
            "data": "04/11/2025"
        }

        Response:
        {
            "success": true,
            "file_path": "automacoes/outputs/20251104_XANDECO.jpeg",
            "generation_time_ms": 1823.45
        }
    """
    start_time = time.time()

    logger.info(f"Recebida requisição para gerar comunicado: {comunicado.nome_integrante}")

    try:
        # Validação customizada (complementa validação Pydantic)
        validate_comunicado_full(comunicado)

        # Gerar imagem
        logger.info("Iniciando geração de imagem...")
        file_path = generator.generate_comunicado(comunicado)

        # Calcular tempo de geração
        generation_time_ms = (time.time() - start_time) * 1000

        logger.info(
            f"Comunicado gerado com sucesso em {generation_time_ms:.2f}ms: {file_path}"
        )

        return ComunicadoResponse(
            success=True,
            file_path=file_path,
            generation_time_ms=round(generation_time_ms, 2)
        )

    except ValueError as e:
        # Erro de validação
        logger.warning(f"Erro de validação: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except FileNotFoundError as e:
        # Erro de recurso não encontrado (fonte, template)
        logger.error(f"Erro de recurso não encontrado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar imagem: {str(e)}"
        )

    except Exception as e:
        # Erro genérico
        logger.error(f"Erro inesperado ao gerar comunicado: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao gerar comunicado: {str(e)}"
        )


@app.get("/")
async def root():
    """
    Endpoint raiz com informações da API.

    Returns:
        dict: Informações básicas da API
    """
    return {
        "service": "Comunicado Image Generation API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoint": "POST /gerar-comunicado"
    }
