"""
Testes unitários para o módulo generator.

Testa a lógica de geração de imagens e manipulação de nomes de arquivo.
"""

import pytest
from automacoes.comunicado_imagem.generator import ComunicadoGenerator
from automacoes.comunicado_imagem.models import ComunicadoRequest, Integrante


class TestComunicadoGenerator:
    """Testes para ComunicadoGenerator."""

    @pytest.fixture
    def generator(self):
        """Fixture que retorna instância do gerador."""
        return ComunicadoGenerator()

    @pytest.fixture
    def comunicado_basico(self):
        """Fixture com comunicado básico."""
        return ComunicadoRequest(
            origem="EXPANSÃO",
            evento="CONCLUSÃO DE ESTÁGIO",
            nome_integrante="XANDECO (183)",
            resultado="SEM APROVEITAMENTO:",
            localizacao="EXPANSÃO REGIONAL",
            grau="GRAU V",
            data="04/11/2025"
        )

    @pytest.fixture
    def comunicado_utf8(self):
        """Fixture com comunicado contendo UTF-8."""
        return ComunicadoRequest(
            origem="EXPANSÃO",
            evento="PROMOÇÃO DE GRAU",
            nome_integrante="JOSÉ DA CONCEIÇÃO (245)",
            resultado="APROVADO:",
            localizacao="EXPANSÃO NACIONAL",
            grau="GRAU III",
            data="15/12/2025"
        )

    def test_generator_initialization(self, generator):
        """Testa inicialização do gerador."""
        assert generator is not None
        assert generator.font_bold_path is not None
        assert generator.font_regular_path is not None

    def test_normalize_filename(self, generator):
        """Testa normalização de nome de arquivo."""
        assert generator._normalize_filename("XANDECO") == "XANDECO"
        assert generator._normalize_filename("JOSÉ DA CONCEIÇÃO") == "JOSEDACONCEICAO"
        assert generator._normalize_filename("João Maria") == "JOAOMARIA"

    def test_generate_filename_basic(self, generator, comunicado_basico):
        """Testa geração de nome de arquivo básico."""
        filename = generator._generate_filename(comunicado_basico)
        assert filename == "20251104_XANDECO.jpeg"

    def test_generate_filename_utf8(self, generator, comunicado_utf8):
        """Testa geração de nome de arquivo com UTF-8."""
        filename = generator._generate_filename(comunicado_utf8)
        assert filename == "20251215_JOSEDACONCEICAO.jpeg"

    def test_generate_comunicado_creates_file(self, generator, comunicado_basico):
        """Testa que a geração de comunicado cria arquivo."""
        import os
        file_path = generator.generate_comunicado(comunicado_basico)

        # Verificar que arquivo foi criado
        assert os.path.exists(file_path)

        # Verificar que arquivo tem tamanho > 0
        assert os.path.getsize(file_path) > 0

    def test_generate_comunicado_utf8(self, generator, comunicado_utf8):
        """Testa geração de comunicado com caracteres UTF-8."""
        import os
        file_path = generator.generate_comunicado(comunicado_utf8)

        # Verificar que arquivo foi criado
        assert os.path.exists(file_path)

        # Verificar que arquivo tem tamanho > 0
        assert os.path.getsize(file_path) > 0


class TestIntegrante:
    """Testes para modelo Integrante."""

    def test_from_comunicado_basic(self):
        """Testa extração de integrante de comunicado básico."""
        comunicado = ComunicadoRequest(
            origem="EXPANSÃO",
            evento="CONCLUSÃO DE ESTÁGIO",
            nome_integrante="XANDECO (183)",
            resultado="SEM APROVEITAMENTO:",
            localizacao="EXPANSÃO REGIONAL",
            grau="GRAU V",
            data="04/11/2025"
        )

        integrante = Integrante.from_comunicado(comunicado)

        assert integrante.nome_colete == "XANDECO"
        assert integrante.numero == 183
        assert integrante.grau == "GRAU V"
        assert integrante.localizacao == "EXPANSÃO REGIONAL"

    def test_from_comunicado_utf8(self):
        """Testa extração de integrante com UTF-8."""
        comunicado = ComunicadoRequest(
            origem="EXPANSÃO",
            evento="PROMOÇÃO DE GRAU",
            nome_integrante="JOSÉ DA CONCEIÇÃO (245)",
            resultado="APROVADO:",
            localizacao="EXPANSÃO NACIONAL",
            grau="GRAU III",
            data="15/12/2025"
        )

        integrante = Integrante.from_comunicado(comunicado)

        assert integrante.nome_colete == "JOSÉ DA CONCEIÇÃO"
        assert integrante.numero == 245
