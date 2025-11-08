"""
Modelos de dados para a API de Geração de Comunicados.

Este módulo define os modelos Pydantic para requisições e respostas da API,
bem como entidades derivadas como Integrante.
"""

from pydantic import BaseModel, Field, field_validator
import re
from typing import Optional


class ComunicadoRequest(BaseModel):
    """
    Modelo de requisição para geração de comunicado.

    Atributos:
        origem: Fonte do comunicado (ex: "EXPANSÃO")
        evento: Tipo de evento (ex: "CONCLUSÃO DE ESTÁGIO")
        nome_integrante: Nome do colete com número no formato "NOME (NÚMERO)"
        resultado: Resultado do evento (ex: "SEM APROVEITAMENTO:")
        localizacao: Localização do integrante (ex: "EXPANSÃO REGIONAL")
        grau: Grau do colete (ex: "GRAU V")
        data: Data do comunicado no formato DD/MM/AAAA
    """

    origem: str = Field(..., min_length=1, max_length=200, description="Fonte do comunicado")
    evento: str = Field(..., min_length=1, max_length=200, description="Tipo de evento")
    nome_integrante: str = Field(..., min_length=1, max_length=200, description="Nome do colete com número")
    resultado: str = Field(..., min_length=1, max_length=200, description="Resultado do evento")
    localizacao: str = Field(..., min_length=1, max_length=200, description="Localização do integrante")
    grau: str = Field(..., min_length=1, max_length=200, description="Grau do colete")
    data: str = Field(..., description="Data no formato DD/MM/AAAA")

    @field_validator('data')
    @classmethod
    def validate_data(cls, v: str) -> str:
        """
        Valida formato de data DD/MM/AAAA.

        Args:
            v: String de data a ser validada

        Returns:
            String de data validada

        Raises:
            ValueError: Se formato for inválido
        """
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', v):
            raise ValueError('Data inválida. Formato esperado: DD/MM/AAAA')
        return v

    @field_validator('nome_integrante')
    @classmethod
    def validate_nome_integrante(cls, v: str) -> str:
        """
        Valida formato de nome "NOME (NÚMERO)".

        Args:
            v: String de nome a ser validada

        Returns:
            String de nome validada

        Raises:
            ValueError: Se formato for inválido
        """
        if not re.match(r'^.+\s\(\d+\)$', v):
            raise ValueError('Nome inválido. Formato esperado: NOME (NÚMERO)')
        return v


class ComunicadoResponse(BaseModel):
    """
    Modelo de resposta da API de geração de comunicado.

    Atributos:
        success: Indica se a geração foi bem-sucedida
        file_path: Caminho do arquivo JPEG gerado
        generation_time_ms: Tempo de geração em milissegundos
    """

    success: bool = Field(..., description="Indica se a geração foi bem-sucedida")
    file_path: str = Field(..., description="Caminho do arquivo JPEG gerado")
    generation_time_ms: float = Field(..., description="Tempo de geração em milissegundos")


class Integrante(BaseModel):
    """
    Entidade derivada representando um membro do clube.

    Esta classe extrai informações do campo nome_integrante do Comunicado.

    Atributos:
        nome_colete: Nome extraído (parte antes do parênteses)
        numero: Número do colete (extraído de dentro dos parênteses)
        grau: Grau do colete
        localizacao: Localização do integrante
    """

    nome_colete: str = Field(..., description="Nome do colete sem número")
    numero: int = Field(..., description="Número do colete")
    grau: str = Field(..., description="Grau do colete")
    localizacao: str = Field(..., description="Localização do integrante")

    @classmethod
    def from_comunicado(cls, comunicado: ComunicadoRequest) -> "Integrante":
        """
        Cria um Integrante a partir de um ComunicadoRequest.

        Args:
            comunicado: Objeto ComunicadoRequest com dados do comunicado

        Returns:
            Objeto Integrante com dados extraídos

        Example:
            >>> req = ComunicadoRequest(
            ...     nome_integrante="XANDECO (183)",
            ...     grau="GRAU V",
            ...     localizacao="EXPANSÃO REGIONAL",
            ...     # ... outros campos
            ... )
            >>> integrante = Integrante.from_comunicado(req)
            >>> integrante.nome_colete
            'XANDECO'
            >>> integrante.numero
            183
        """
        # Extrair nome e número usando regex
        match = re.match(r'^(.+)\s\((\d+)\)$', comunicado.nome_integrante)
        if not match:
            raise ValueError("Formato de nome_integrante inválido")

        nome_colete = match.group(1).strip()
        numero = int(match.group(2))

        return cls(
            nome_colete=nome_colete,
            numero=numero,
            grau=comunicado.grau,
            localizacao=comunicado.localizacao
        )
