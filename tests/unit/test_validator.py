"""
Testes unitários para o módulo validator.

Testa as regras de validação customizadas para dados de comunicado.
"""

import pytest
from automacoes.comunicado_imagem.validator import (
    validate_date_range,
    validate_text_length_for_rendering,
    validate_comunicado_full
)
from automacoes.comunicado_imagem.models import ComunicadoRequest


class TestValidateDataRange:
    """Testes para validação de range de data."""

    def test_valid_date(self):
        """Testa data válida."""
        assert validate_date_range("04/11/2025") is True

    def test_invalid_day(self):
        """Testa dia inválido."""
        with pytest.raises(ValueError, match="Dia inválido"):
            validate_date_range("32/11/2025")

    def test_invalid_month(self):
        """Testa mês inválido."""
        with pytest.raises(ValueError, match="Mês inválido"):
            validate_date_range("04/13/2025")

    def test_invalid_year(self):
        """Testa ano inválido."""
        with pytest.raises(ValueError, match="Ano inválido"):
            validate_date_range("04/11/1800")

    def test_invalid_date_format(self):
        """Testa formato de data inválido."""
        with pytest.raises(ValueError):
            validate_date_range("04-11-2025")


class TestValidateTextLength:
    """Testes para validação de comprimento de texto."""

    def test_valid_text_length(self):
        """Testa texto com comprimento válido."""
        assert validate_text_length_for_rendering("EXPANSÃO", max_chars=100) is True

    def test_text_too_long(self):
        """Testa texto muito longo."""
        long_text = "A" * 101
        with pytest.raises(ValueError, match="Texto muito longo"):
            validate_text_length_for_rendering(long_text, max_chars=100)

    def test_empty_text(self):
        """Testa texto vazio."""
        assert validate_text_length_for_rendering("", max_chars=100) is True


class TestValidateComunicadoFull:
    """Testes para validação completa de comunicado."""

    def test_valid_comunicado(self):
        """Testa comunicado completamente válido."""
        comunicado = ComunicadoRequest(
            origem="EXPANSÃO",
            evento="CONCLUSÃO DE ESTÁGIO",
            nome_integrante="XANDECO (183)",
            resultado="SEM APROVEITAMENTO:",
            localizacao="EXPANSÃO REGIONAL",
            grau="GRAU V",
            data="04/11/2025"
        )
        assert validate_comunicado_full(comunicado) is True

    def test_comunicado_with_utf8(self):
        """Testa comunicado com caracteres UTF-8."""
        comunicado = ComunicadoRequest(
            origem="EXPANSÃO",
            evento="PROMOÇÃO DE GRAU",
            nome_integrante="JOSÉ DA CONCEIÇÃO (245)",
            resultado="APROVADO:",
            localizacao="EXPANSÃO NACIONAL",
            grau="GRAU III",
            data="15/12/2025"
        )
        assert validate_comunicado_full(comunicado) is True

    def test_invalid_date_in_comunicado(self):
        """Testa comunicado com data inválida."""
        comunicado = ComunicadoRequest(
            origem="EXPANSÃO",
            evento="CONCLUSÃO DE ESTÁGIO",
            nome_integrante="XANDECO (183)",
            resultado="SEM APROVEITAMENTO:",
            localizacao="EXPANSÃO REGIONAL",
            grau="GRAU V",
            data="32/11/2025"
        )
        with pytest.raises(ValueError, match="Dia inválido"):
            validate_comunicado_full(comunicado)
