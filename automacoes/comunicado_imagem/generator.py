"""
Módulo de geração de imagens de comunicados.

Este módulo contém a lógica principal para gerar imagens JPEG padronizadas
com elementos fixos e variáveis, suporte UTF-8 e ajuste dinâmico de fontes.
"""

import logging
import os
import re
from pathlib import Path
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
from .models import ComunicadoRequest, Integrante

logger = logging.getLogger(__name__)

# Constantes de template
TEMPLATE_WIDTH = 1542
TEMPLATE_HEIGHT = 1600
JPEG_QUALITY = 90

# Cores
COLOR_AMARELO = "#FFD700"  # Ouro/Amarelo
COLOR_BRANCO = "#FFFFFF"   # Branco
COLOR_PRETO = "#000000"    # Preto

# Elementos fixos
TITULO_COMUNICADO = "COMUNICADO"
RODAPE_LINHA1 = "COMANDO MUNDIAL"
RODAPE_LINHA2 = "COMUNICADO INTERNO"
RODAPE_LINHA3 = "PROIBIDA A DIVULGAÇÃO EM QUALQUER REDE SOCIAL"

# Caminhos
BASE_DIR = Path(__file__).parent
TEMPLATE_PATH = BASE_DIR / "templates" / "base_template.png"
FONT_DIR = BASE_DIR / "templates" / "fonts"
FONT_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
FONT_REGULAR = FONT_DIR / "DejaVuSans.ttf"
OUTPUT_DIR = Path("automacoes") / "outputs"


class ComunicadoGenerator:
    """
    Classe principal para geração de imagens de comunicados.

    Esta classe carrega templates, renderiza texto com suporte UTF-8,
    ajusta tamanhos de fonte dinamicamente e salva imagens JPEG otimizadas.
    """

    def __init__(self):
        """Inicializa o gerador de comunicados."""
        self.font_bold_path = str(FONT_BOLD)
        self.font_regular_path = str(FONT_REGULAR)
        self.template_path = str(TEMPLATE_PATH)
        self.output_dir = OUTPUT_DIR

        # Verificar se recursos existem
        self._validate_resources()

        logger.info("ComunicadoGenerator inicializado com sucesso")

    def _validate_resources(self):
        """
        Valida que todos os recursos necessários existem.

        Raises:
            FileNotFoundError: Se algum recurso obrigatório não for encontrado
        """
        if not os.path.exists(self.font_bold_path):
            raise FileNotFoundError(f"Fonte bold não encontrada: {self.font_bold_path}")
        if not os.path.exists(self.font_regular_path):
            raise FileNotFoundError(f"Fonte regular não encontrada: {self.font_regular_path}")

        logger.info("Recursos validados: fontes encontradas")

    def _normalize_filename(self, nome: str) -> str:
        """
        Normaliza nome para uso em nome de arquivo (remove acentos e caracteres especiais).

        Args:
            nome: Nome a ser normalizado

        Returns:
            Nome normalizado sem caracteres especiais

        Example:
            >>> gen = ComunicadoGenerator()
            >>> gen._normalize_filename("JOSÉ DA CONCEIÇÃO")
            'JOSEDACONCEICAO'
        """
        # Remover acentos e caracteres especiais
        import unicodedata
        nome_normalizado = unicodedata.normalize('NFKD', nome)
        nome_normalizado = nome_normalizado.encode('ASCII', 'ignore').decode('ASCII')
        # Remover espaços e caracteres não alfanuméricos
        nome_normalizado = re.sub(r'[^A-Za-z0-9]', '', nome_normalizado)
        return nome_normalizado.upper()

    def _generate_filename(self, comunicado: ComunicadoRequest) -> str:
        """
        Gera nome do arquivo no formato YYYYMMDD_INTEGRANTE.jpeg.

        Args:
            comunicado: Dados do comunicado

        Returns:
            Nome do arquivo gerado

        Example:
            >>> gen = ComunicadoGenerator()
            >>> req = ComunicadoRequest(
            ...     nome_integrante="XANDECO (183)",
            ...     data="04/11/2025",
            ...     # ... outros campos
            ... )
            >>> gen._generate_filename(req)
            '20251104_XANDECO.jpeg'
        """
        # Extrair integrante
        integrante = Integrante.from_comunicado(comunicado)
        nome_normalizado = self._normalize_filename(integrante.nome_colete)

        # Converter data DD/MM/AAAA -> YYYYMMDD
        dia, mes, ano = comunicado.data.split('/')
        data_formatada = f"{ano}{mes}{dia}"

        filename = f"{data_formatada}_{nome_normalizado}.jpeg"
        logger.info(f"Nome de arquivo gerado: {filename}")
        return filename

    def _get_font_with_size(self, font_path: str, size: int) -> ImageFont.FreeTypeFont:
        """
        Carrega fonte TrueType com tamanho específico.

        Args:
            font_path: Caminho para arquivo TTF
            size: Tamanho da fonte em pixels

        Returns:
            Objeto de fonte carregado
        """
        return ImageFont.truetype(font_path, size)

    def _fit_text_to_width(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        font_path: str,
        initial_size: int,
        max_width: int,
        min_size: int = 30
    ) -> Tuple[ImageFont.FreeTypeFont, int]:
        """
        Ajusta tamanho da fonte para que o texto caiba na largura especificada.

        Args:
            draw: Objeto ImageDraw para medir texto
            text: Texto a ser renderizado
            font_path: Caminho para arquivo de fonte
            initial_size: Tamanho inicial da fonte
            max_width: Largura máxima permitida
            min_size: Tamanho mínimo da fonte (padrão: 30px)

        Returns:
            Tupla (fonte ajustada, tamanho final)

        Raises:
            ValueError: Se o texto não couber mesmo com tamanho mínimo
        """
        current_size = initial_size

        while current_size >= min_size:
            font = self._get_font_with_size(font_path, current_size)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]

            if text_width <= max_width:
                logger.debug(f"Fonte ajustada: {current_size}px para texto '{text[:20]}...'")
                return font, current_size

            current_size -= 2  # Decrementar 2px por iteração

        raise ValueError(
            f"Texto muito longo para caber na imagem: '{text}'. "
            f"Mesmo com fonte mínima ({min_size}px), largura excede {max_width}px"
        )

    def _draw_text_centered(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        y_position: int,
        font: ImageFont.FreeTypeFont,
        color: str,
        width: int = TEMPLATE_WIDTH
    ):
        """
        Desenha texto centralizado horizontalmente.

        Args:
            draw: Objeto ImageDraw
            text: Texto a ser desenhado
            y_position: Posição Y (vertical)
            font: Fonte a ser usada
            color: Cor do texto (hex)
            width: Largura total para centralização
        """
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x_position = (width - text_width) // 2
        draw.text((x_position, y_position), text, font=font, fill=color)

    def generate_comunicado(self, comunicado: ComunicadoRequest) -> str:
        """
        Gera imagem de comunicado completa.

        Args:
            comunicado: Dados do comunicado a ser gerado

        Returns:
            Caminho do arquivo JPEG gerado

        Raises:
            FileNotFoundError: Se template não for encontrado
            ValueError: Se texto não couber na imagem

        Example:
            >>> gen = ComunicadoGenerator()
            >>> req = ComunicadoRequest(
            ...     origem="EXPANSÃO",
            ...     evento="CONCLUSÃO DE ESTÁGIO",
            ...     nome_integrante="XANDECO (183)",
            ...     resultado="SEM APROVEITAMENTO:",
            ...     localizacao="EXPANSÃO REGIONAL",
            ...     grau="GRAU V",
            ...     data="04/11/2025"
            ... )
            >>> filepath = gen.generate_comunicado(req)
            >>> print(filepath)
            'automacoes/outputs/20251104_XANDECO.jpeg'
        """
        logger.info(f"Iniciando geração de comunicado para {comunicado.nome_integrante}")

        # Criar ou carregar imagem base
        if os.path.exists(self.template_path):
            logger.info(f"Carregando template: {self.template_path}")
            img = Image.open(self.template_path).convert('RGB')
            img = img.resize((TEMPLATE_WIDTH, TEMPLATE_HEIGHT), Image.Resampling.LANCZOS)
        else:
            logger.warning(f"Template não encontrado: {self.template_path}. Criando imagem em branco.")
            # Criar imagem com fundo escuro
            img = Image.new('RGB', (TEMPLATE_WIDTH, TEMPLATE_HEIGHT), color='#1a1a1a')

        draw = ImageDraw.Draw(img)

        # Largura máxima para texto (com margem)
        max_text_width = TEMPLATE_WIDTH - 100

        # TÍTULO "COMUNICADO" - Topo (120px, amarelo, bold)
        font_titulo = self._get_font_with_size(self.font_bold_path, 120)
        self._draw_text_centered(draw, TITULO_COMUNICADO, 50, font_titulo, COLOR_AMARELO)

        # ORIGEM - Abaixo do título (90px, branco, bold)
        font_origem, _ = self._fit_text_to_width(draw, comunicado.origem, self.font_bold_path, 90, max_text_width)
        self._draw_text_centered(draw, comunicado.origem, 200, font_origem, COLOR_BRANCO)

        # EVENTO - Centro superior (100px, amarelo, bold)
        font_evento, _ = self._fit_text_to_width(draw, comunicado.evento, self.font_bold_path, 100, max_text_width)
        self._draw_text_centered(draw, comunicado.evento, 350, font_evento, COLOR_AMARELO)

        # NOME INTEGRANTE - Centro (70px, branco, regular)
        font_nome, _ = self._fit_text_to_width(draw, comunicado.nome_integrante, self.font_regular_path, 70, max_text_width)
        self._draw_text_centered(draw, comunicado.nome_integrante, 550, font_nome, COLOR_BRANCO)

        # RESULTADO - Centro inferior (90px, amarelo, bold)
        font_resultado, _ = self._fit_text_to_width(draw, comunicado.resultado, self.font_bold_path, 90, max_text_width)
        self._draw_text_centered(draw, comunicado.resultado, 700, font_resultado, COLOR_AMARELO)

        # LOCALIZAÇÃO - Mesma linha do resultado, abaixo (80px, amarelo, bold)
        font_localizacao, _ = self._fit_text_to_width(draw, comunicado.localizacao, self.font_bold_path, 80, max_text_width)
        self._draw_text_centered(draw, comunicado.localizacao, 850, font_localizacao, COLOR_AMARELO)

        # GRAU - Mesma linha, abaixo (80px, amarelo, bold)
        font_grau, _ = self._fit_text_to_width(draw, comunicado.grau, self.font_bold_path, 80, max_text_width)
        self._draw_text_centered(draw, comunicado.grau, 1000, font_grau, COLOR_AMARELO)

        # DATA - Base (70px, branco, regular)
        font_data, _ = self._fit_text_to_width(draw, comunicado.data, self.font_regular_path, 70, max_text_width)
        self._draw_text_centered(draw, comunicado.data, 1150, font_data, COLOR_BRANCO)

        # RODAPÉ - 3 linhas (50px, branco, regular)
        font_rodape = self._get_font_with_size(self.font_regular_path, 50)
        self._draw_text_centered(draw, RODAPE_LINHA1, 1300, font_rodape, COLOR_BRANCO)
        self._draw_text_centered(draw, RODAPE_LINHA2, 1370, font_rodape, COLOR_BRANCO)
        self._draw_text_centered(draw, RODAPE_LINHA3, 1440, font_rodape, COLOR_BRANCO)

        # Gerar nome de arquivo e salvar
        filename = self._generate_filename(comunicado)
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = self.output_dir / filename

        logger.info(f"Salvando imagem: {output_path}")
        img.save(str(output_path), 'JPEG', quality=JPEG_QUALITY, optimize=True)

        logger.info(f"Comunicado gerado com sucesso: {output_path}")
        return str(output_path)
