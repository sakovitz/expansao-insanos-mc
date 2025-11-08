#!/usr/bin/env python3
"""
Test PostgreSQL Database Connection

Script to validate that PostgreSQL is running and accessible with configured credentials.
Uses environment variables from .env file.

Usage:
    python scripts/test-postgres-connection.py

Requirements:
    - .env file must exist with DB_HOST, DB_USER, DB_PASSWORD
    - PostgreSQL must be running and accessible
    - psycopg2 library must be installed

Exit Codes:
    0: Connection successful
    1: Connection failed
"""

import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
    import psycopg2
except ImportError as e:
    print(f"❌ Erro: Biblioteca não encontrada: {e}")
    print("Instale as dependências com: pip install -r requirements.txt")
    sys.exit(1)


def test_connection():
    """Test PostgreSQL connection with configured credentials."""

    # Load environment variables from .env
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        print(f"❌ Erro: Arquivo .env não encontrado em {env_path}")
        print("Crie o arquivo .env copiando .env.example:")
        print(f"  cp .env.example .env")
        return False

    load_dotenv(env_path)

    # Get required environment variables
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_database = os.getenv("DB_NAME", "postgres")  # Default to 'postgres'

    # Validate required variables
    missing_vars = []
    if not db_host:
        missing_vars.append("DB_HOST")
    if not db_user:
        missing_vars.append("DB_USER")
    if not db_password:
        missing_vars.append("DB_PASSWORD")

    if missing_vars:
        print(f"❌ Erro: Variáveis de ambiente obrigatórias não definidas: {', '.join(missing_vars)}")
        print("Verifique seu arquivo .env e certifique-se de preencher todas as variáveis obrigatórias.")
        return False

    # Attempt connection
    try:
        print(f"🔄 Testando conexão com PostgreSQL...")
        print(f"   Host: {db_host}")
        print(f"   Usuário: {db_user}")
        print(f"   Banco: {db_database}")

        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_database,
            connect_timeout=5
        )

        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        print(f"\n✓ Conexão PostgreSQL OK")
        print(f"  Conectado a: {db_host} / {db_user}")
        print(f"  Versão: {db_version.split(',')[0] if db_version else 'Unknown'}")
        return True

    except psycopg2.OperationalError as e:
        error_msg = str(e)

        # Provide helpful error messages
        if "could not connect to server" in error_msg or "Connection refused" in error_msg:
            print(f"\n❌ Erro: PostgreSQL não está funcionando")
            print(f"   Causa: Serviço PostgreSQL não está rodando ou não está acessível em {db_host}")
            print(f"\n   Solução:")
            print(f"   macOS:  brew services start postgresql@14")
            print(f"   Linux:  sudo systemctl start postgresql")
            print(f"   Windows: Inicie PostgreSQL no aplicativo Services")

        elif "password authentication failed" in error_msg:
            print(f"\n❌ Erro: Falha na autenticação")
            print(f"   Causa: Senha incorreta para usuário '{db_user}'")
            print(f"\n   Solução:")
            print(f"   1. Verifique a senha no arquivo .env")
            print(f"   2. Se necessário, resete a senha PostgreSQL:")
            print(f"      macOS/Linux: sudo -u postgres psql")
            print(f"                   ALTER USER {db_user} WITH PASSWORD 'nova_senha';")
            print(f"                   \\q")
            print(f"   3. Atualize .env com a senha correta")

        elif "does not exist" in error_msg:
            print(f"\n❌ Erro: Banco de dados não existe")
            print(f"   Causa: O banco '{db_database}' não foi criado")
            print(f"\n   Solução:")
            print(f"   createdb -U {db_user} {db_database}")

        else:
            print(f"\n❌ Erro: Não foi possível conectar ao PostgreSQL")
            print(f"   Detalhes: {error_msg}")
            print(f"\n   Verificações:")
            print(f"   1. PostgreSQL está rodando?")
            print(f"   2. Host '{db_host}' é acessível?")
            print(f"   3. Usuário '{db_user}' existe?")
            print(f"   4. Senha está correta?")

        return False

    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
