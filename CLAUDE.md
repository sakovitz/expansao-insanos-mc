# expansao-insanos-mc Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-11-07

## Active Technologies

- Python 3.11 (stable, good library support, released 2022) + Pandas (==2.1.*), psycopg2/psycopg3 (PostgreSQL), python-dotenv (env loading), requests (HTTP API) (001-setup-venv)
- Pillow (>=10.4.0) for image manipulation with UTF-8 support (automacoes/001-comunicado-imagem)
- FastAPI (0.115.x) + Uvicorn (0.32.x) for RESTful API endpoints (automacoes/001-comunicado-imagem)

## Project Structure

```text
src/
tests/
```

## Commands

cd src
pytest
ruff check .
uvicorn automacoes.comunicado_imagem.api:app --reload  # Start API server

## Code Style

Python 3.11 (stable, good library support, released 2022): Follow standard conventions

## Recent Changes

- 001-setup-venv: Added Python 3.11 (stable, good library support, released 2022) + Pandas (==2.1.*), psycopg2/psycopg3 (PostgreSQL), python-dotenv (env loading), requests (HTTP API)
- automacoes/001-comunicado-imagem: Added Pillow (>=10.4.0) for image generation, FastAPI (0.115.x) + Uvicorn (0.32.x) for REST API

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
