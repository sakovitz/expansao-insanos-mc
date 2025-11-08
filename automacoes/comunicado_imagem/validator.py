"""
Módulo de validação customizada para dados de comunicado.

Este módulo complementa as validações do Pydantic com regras de negócio específicas.
"""

import logging
from datetime import datetime
from .models import ComunicadoRequest

logger = logging.getLogger(__name__)


def validate_date_range(data_str: str) -> bool:
    """
    Valida se a data está em um range razoável (1900-2100).

    Args:
        data_str: Data no formato DD/MM/AAAA

    Returns:
        True se a data está no range válido

    Raises:
        ValueError: Se a data for inválida ou fora do range
    """
    try:
        dia, mes, ano = map(int, data_str.split('/'))

        # Validar ranges básicos
        if not (1 <= dia <= 31):
            raise ValueError(f"Dia inválido: {dia}. Deve estar entre 1 e 31")
        if not (1 <= mes <= 12):
            raise ValueError(f"Mês inválido: {mes}. Deve estar entre 1 e 12")
        if not (1900 <= ano <= 2100):
            raise ValueError(f"Ano inválido: {ano}. Deve estar entre 1900 e 2100")

        # Tentar criar objeto datetime para validação completa
        datetime(ano, mes, dia)

        logger.info(f"Data validada: {data_str}")
        return True

    except ValueError as e:
        logger.error(f"Erro ao validar data '{data_str}': {str(e)}")
        raise ValueError(f"Data inválida: {str(e)}")


def validate_text_length_for_rendering(text: str, max_chars: int = 100) -> bool:
    """
    Valida se o texto não é extremamente longo (verificação preliminar).

    Args:
        text: Texto a ser validado
        max_chars: Número máximo de caracteres permitido

    Returns:
        True se o texto está dentro do limite

    Raises:
        ValueError: Se o texto exceder o limite máximo
    """
    if len(text) > max_chars:
        raise ValueError(
            f"Texto muito longo ({len(text)} caracteres). "
            f"Máximo permitido: {max_chars} caracteres"
        )
    return True


def validate_comunicado_full(comunicado: ComunicadoRequest) -> bool:
    """
    Executa validação completa do comunicado com regras de negócio.

    Args:
        comunicado: Objeto ComunicadoRequest a ser validado

    Returns:
        True se todas as validações passarem

    Raises:
        ValueError: Se alguma validação falhar

    Example:
        >>> req = ComunicadoRequest(
        ...     origem="EXPANSÃO",
        ...     evento="CONCLUSÃO DE ESTÁGIO",
        ...     nome_integrante="XANDECO (183)",
        ...     resultado="SEM APROVEITAMENTO:",
        ...     localizacao="EXPANSÃO REGIONAL",
        ...     grau="GRAU V",
        ...     data="04/11/2025"
        ... )
        >>> validate_comunicado_full(req)
        True
    """
    logger.info(f"Validando comunicado para {comunicado.nome_integrante}")

    # Validar data
    validate_date_range(comunicado.data)

    # Validar comprimento dos campos para renderização
    validate_text_length_for_rendering(comunicado.origem, max_chars=100)
    validate_text_length_for_rendering(comunicado.evento, max_chars=100)
    validate_text_length_for_rendering(comunicado.nome_integrante, max_chars=100)
    validate_text_length_for_rendering(comunicado.resultado, max_chars=100)
    validate_text_length_for_rendering(comunicado.localizacao, max_chars=100)
    validate_text_length_for_rendering(comunicado.grau, max_chars=50)

    logger.info(f"Comunicado validado com sucesso: {comunicado.nome_integrante}")
    return True
