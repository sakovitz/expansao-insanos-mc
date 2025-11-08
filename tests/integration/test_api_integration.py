"""
Testes de integração para a API de geração de comunicados.

Testa o fluxo completo end-to-end da API.
"""

import pytest
from fastapi.testclient import TestClient
from automacoes.comunicado_imagem.api import app
import os


@pytest.fixture
def client():
    """Fixture que retorna cliente de teste da API."""
    return TestClient(app)


class TestHealthEndpoint:
    """Testes para endpoint de health check."""

    def test_health_check(self, client):
        """Testa endpoint de health check."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "status": "healthy",
            "service": "comunicado-api"
        }


class TestRootEndpoint:
    """Testes para endpoint raiz."""

    def test_root(self, client):
        """Testa endpoint raiz."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Comunicado Image Generation API"
        assert data["version"] == "1.0.0"


class TestGerarComunicadoEndpoint:
    """Testes para endpoint de geração de comunicado."""

    def test_gerar_comunicado_sucesso(self, client):
        """Testa geração de comunicado com sucesso."""
        payload = {
            "origem": "EXPANSÃO",
            "evento": "CONCLUSÃO DE ESTÁGIO",
            "nome_integrante": "XANDECO (183)",
            "resultado": "SEM APROVEITAMENTO:",
            "localizacao": "EXPANSÃO REGIONAL",
            "grau": "GRAU V",
            "data": "04/11/2025"
        }

        response = client.post("/gerar-comunicado", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "file_path" in data
        assert data["file_path"].endswith(".jpeg")
        assert "generation_time_ms" in data
        assert data["generation_time_ms"] > 0
        assert data["generation_time_ms"] < 10000  # Menos de 10 segundos

        # Verificar que arquivo foi criado
        assert os.path.exists(data["file_path"])

    def test_gerar_comunicado_utf8(self, client):
        """Testa geração de comunicado com caracteres UTF-8."""
        payload = {
            "origem": "EXPANSÃO",
            "evento": "PROMOÇÃO DE GRAU",
            "nome_integrante": "JOSÉ DA CONCEIÇÃO (245)",
            "resultado": "APROVADO:",
            "localizacao": "EXPANSÃO NACIONAL",
            "grau": "GRAU III",
            "data": "15/12/2025"
        }

        response = client.post("/gerar-comunicado", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert os.path.exists(data["file_path"])

    def test_gerar_comunicado_campo_faltando(self, client):
        """Testa erro quando campo obrigatório está faltando."""
        payload = {
            "origem": "EXPANSÃO",
            "evento": "CONCLUSÃO DE ESTÁGIO",
            # nome_integrante faltando
            "resultado": "SEM APROVEITAMENTO:",
            "localizacao": "EXPANSÃO REGIONAL",
            "grau": "GRAU V",
            "data": "04/11/2025"
        }

        response = client.post("/gerar-comunicado", json=payload)

        assert response.status_code == 422  # Unprocessable Entity (validação Pydantic)

    def test_gerar_comunicado_data_invalida(self, client):
        """Testa erro com formato de data inválido."""
        payload = {
            "origem": "EXPANSÃO",
            "evento": "CONCLUSÃO DE ESTÁGIO",
            "nome_integrante": "XANDECO (183)",
            "resultado": "SEM APROVEITAMENTO:",
            "localizacao": "EXPANSÃO REGIONAL",
            "grau": "GRAU V",
            "data": "2025-11-04"  # Formato errado
        }

        response = client.post("/gerar-comunicado", json=payload)

        assert response.status_code == 422  # Validação Pydantic

    def test_gerar_comunicado_nome_invalido(self, client):
        """Testa erro com formato de nome inválido."""
        payload = {
            "origem": "EXPANSÃO",
            "evento": "CONCLUSÃO DE ESTÁGIO",
            "nome_integrante": "XANDECO 183",  # Sem parênteses
            "resultado": "SEM APROVEITAMENTO:",
            "localizacao": "EXPANSÃO REGIONAL",
            "grau": "GRAU V",
            "data": "04/11/2025"
        }

        response = client.post("/gerar-comunicado", json=payload)

        assert response.status_code == 422  # Validação Pydantic

    def test_gerar_comunicado_dia_invalido(self, client):
        """Testa erro com dia inválido."""
        payload = {
            "origem": "EXPANSÃO",
            "evento": "CONCLUSÃO DE ESTÁGIO",
            "nome_integrante": "XANDECO (183)",
            "resultado": "SEM APROVEITAMENTO:",
            "localizacao": "EXPANSÃO REGIONAL",
            "grau": "GRAU V",
            "data": "32/11/2025"  # Dia 32 não existe
        }

        response = client.post("/gerar-comunicado", json=payload)

        assert response.status_code == 400  # Validação customizada
