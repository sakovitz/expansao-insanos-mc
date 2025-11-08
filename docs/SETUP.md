# Guia Completo de Configuração: Projeto Insanos MC Expansão

Este guia completo cobre a configuração do ambiente para o projeto Insanos MC Expansão em **Windows**, **macOS** e **Linux**.

**Tempo Estimado**: 10 minutos (configuração primeira vez)

---

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Passo 1: Validar Python](#passo-1-validar-python)
3. [Passo 2: Criar Ambiente Virtual](#passo-2-criar-ambiente-virtual)
4. [Passo 3: Ativar Ambiente Virtual](#passo-3-ativar-ambiente-virtual)
5. [Passo 4: Instalar Dependências](#passo-4-instalar-dependências)
6. [Passo 5: Configurar Variáveis de Ambiente](#passo-5-configurar-variáveis-de-ambiente)
7. [Passo 6: Testar Conexão PostgreSQL](#passo-6-testar-conexão-postgresql)
8. [Instruções Específicas por SO](#instruções-específicas-por-so)
9. [Troubleshooting](#troubleshooting)
10. [Checklist de Segurança](#checklist-de-segurança)

---

## Pré-requisitos

Antes de começar, certifique-se de ter:

- ✅ **Python 3.11+** - [Download](https://www.python.org/downloads/)
- ✅ **PostgreSQL** - [Download](https://www.postgresql.org/download/)
- ✅ **pip** (incluído com Python)
- ✅ **Git** (para clonar este repositório)

### Verificar Pré-requisitos

```bash
# Verificar versão Python
python --version
# Esperado: Python 3.11.x ou superior

# Verificar PostgreSQL
psql --version
# Esperado: psql (PostgreSQL) 12.x ou superior

# Verificar pip
pip --version
# Esperado: pip x.x.x from ...
```

---

## Passo 1: Validar Python

Antes de prosseguir com a configuração, valide que sua versão Python atende aos requisitos.

### Em macOS/Linux

```bash
bash scripts/validate-python.sh
```

**Saída Esperada**:
```
✓ Python 3.11.x detectado
Pronto para proceder com pip install
```

### Em Windows (CMD)

```batch
scripts\validate-python.bat
```

**Saída Esperada**:
```
[OK] Python 3.11.x detectado
Pronto para proceder com pip install
```

Se a validação falhar, instale Python 3.11+ antes de prosseguir.

---

## Passo 2: Criar Ambiente Virtual

Um ambiente virtual isola as dependências deste projeto do Python do seu sistema.

**Comando** (funciona identicamente em todas as plataformas):
```bash
python -m venv expansao
```

**O que isso cria:**
- Diretório `expansao/` contendo:
  - `bin/` (macOS/Linux) ou `Scripts/` (Windows): Scripts executáveis e comandos de ativação
  - `lib/`: Pacotes Python instalados
  - `pyvenv.cfg`: Configuração do ambiente

**Se você precisar recriar o ambiente**, delete e recrie:
```bash
# macOS/Linux
rm -rf expansao

# Windows
rmdir /s /q expansao
```

---

## Passo 3: Ativar Ambiente Virtual

A ativação modifica seu shell para usar o ambiente Python isolado.

### macOS/Linux

```bash
source expansao/bin/activate
```

**O que esperar**: O prompt do seu shell muda para mostrar o prefixo `(expansao)`:
```
(expansao) $ _
```

### Windows - CMD

```batch
expansao\Scripts\activate.bat
```

**O que esperar**: Seu prompt muda para:
```
(expansao) C:\Users\SeuNome\projeto>
```

### Windows - PowerShell

```powershell
& "expansao\Scripts\Activate.ps1"
```

> **Nota**: Se PowerShell der um erro "cannot be loaded because running scripts is disabled", execute:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Desativar Ambiente

Quando terminar de trabalhar, saia do ambiente virtual:
```bash
deactivate
```

---

## Passo 4: Instalar Dependências

Com o ambiente virtual ativado, instale todos os pacotes necessários.

```bash
pip install -r requirements.txt
```

**Saída Esperada**:
```
Collecting pandas==2.1.x
  Downloading pandas-2.1.x-...
  ...
Successfully installed pandas-2.1.x psycopg2-2.9.x python-dotenv-1.0.x requests-2.31.x
```

**Verificar Instalação**:
```bash
pip list
```

Você deve ver:
```
pandas            2.1.x
psycopg2          2.9.x
python-dotenv     1.0.x
requests          2.31.x
```

---

## Passo 5: Configurar Variáveis de Ambiente

O arquivo `.env` armazena configuração sensível (credenciais, tokens de API) sem registrá-los no git.

### Passo 5a: Criar .env do template

```bash
# macOS/Linux
cp .env.example .env

# Windows
copy .env.example .env
```

### Passo 5b: Editar com suas credenciais

**macOS/Linux**:
```bash
nano .env
# ou: vim .env, code .env
```

**Windows**:
```batch
notepad .env
```

### Passo 5c: Variáveis Obrigatórias

Edite `.env` e preencha com seus valores reais:

```ini
# Conexão PostgreSQL (OBRIGATÓRIO)
DB_HOST=localhost              # ou: db.company.com, 192.168.1.x
DB_USER=seu_usuario_real       # Usuário PostgreSQL
DB_PASSWORD=sua_senha_real     # Senha PostgreSQL

# APIs Externas (OBRIGATÓRIO)
API_TOKEN=seu_token_real       # Chave de API/token
```

### Passo 5d: Verificar Variáveis São Legíveis

Teste se Python pode carregar suas variáveis de ambiente:

```bash
python -c "
from dotenv import load_dotenv
import os

load_dotenv()
print('DB_HOST:', os.getenv('DB_HOST'))
print('DB_USER:', os.getenv('DB_USER'))
print('API_TOKEN:', os.getenv('API_TOKEN'))
"
```

**Saída Esperada**:
```
DB_HOST: localhost
DB_USER: seu_usuario_real
API_TOKEN: seu_token_real
```

Se algum valor mostrar `None`, verifique se a variável existe em `.env` com ortografia correta.

---

## Passo 6: Testar Conexão PostgreSQL

Verifique se PostgreSQL está funcionando e acessível com suas credenciais.

```bash
python scripts/test-postgres-connection.py
```

**Saída Esperada**:
```
✓ Conexão PostgreSQL OK
Conectado a: localhost / seu_usuario
```

**Se isso falhar**, consulte a seção [Erros de Conexão PostgreSQL](#erros-de-conexão-postgresql) abaixo.

---

## Instruções Específicas por SO

### macOS

#### Instalar Python 3.11

Usando Homebrew (recomendado):
```bash
brew install python@3.11
python3 --version
```

Ou baixe em [python.org](https://www.python.org/downloads/macos/)

#### Instalar PostgreSQL

```bash
brew install postgresql@14
brew services start postgresql@14
```

Verificar se está funcionando:
```bash
brew services list | grep postgres
# Saída: postgresql@14 started
```

Criar um usuário (se necessário):
```bash
createuser -P seu_usuario
# Digite a senha quando solicitado
```

---

### Linux (Ubuntu/Debian)

#### Instalar Python 3.11

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
python3 --version
```

#### Instalar PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl status postgresql
```

Criar um usuário (se necessário):
```bash
sudo -u postgres createuser -P seu_usuario
# Digite a senha quando solicitado
```

---

### Windows

#### Instalar Python 3.11

1. Vá para [python.org/downloads](https://www.python.org/downloads/)
2. Baixe "Windows installer" para Python 3.11.x
3. Execute o instalador
4. **IMPORTANTE**: Marque "Add Python 3.11 to PATH"
5. Clique em "Install Now"
6. Verifique no Prompt de Comando:
   ```batch
   python --version
   ```

#### Instalar PostgreSQL

1. Vá para [postgresql.org/download](https://www.postgresql.org/download/windows/)
2. Baixe o instalador Windows
3. Execute o instalador e siga os prompts
4. Lembre-se da senha do superuser que você definir
5. Verifique se PostgreSQL está rodando no aplicativo Services

---

## Troubleshooting

### Erros de Versão Python

**Erro**: `ERROR: Python 3.9.x encontrado. Projeto requer Python 3.11+.`

**Causa**: Você tem uma versão Python mais antiga instalada.

**Solução**:
1. Instale Python 3.11+ em [python.org](https://www.python.org/downloads/)
2. Verifique nova versão: `python --version`
3. Re-execute validação: `bash scripts/validate-python.sh` (ou `.bat` no Windows)

**Nota em macOS**: Se usar Homebrew, você pode precisar usar `python3.11` explicitamente:
```bash
python3.11 --version
python3.11 -m venv expansao
```

---

### Ativação de Ambiente Virtual

**Erro**: `command not found: activate` (macOS/Linux)

**Solução**:
```bash
# Certifique-se de estar no diretório raiz do projeto
source ./expansao/bin/activate
```

**Erro**: `O caminho especificado não foi encontrado` (Windows)

**Solução**:
```batch
REM Certifique-se de estar no diretório raiz do projeto
expansao\Scripts\activate.bat
```

---

### Erros de pip Install

#### Erro "Permissão negada"

**Erro**: `error: externally-managed-environment`

**Causa**: Você está tentando instalar no Python do sistema em vez do venv.

**Solução**: Certifique-se de que o ambiente virtual está ativado:
```bash
source expansao/bin/activate  # macOS/Linux
# ou
expansao\Scripts\activate.bat  # Windows

# Depois tente novamente
pip install -r requirements.txt
```

#### Erro "Não foi possível encontrar uma versão"

**Erro**: `ERROR: Could not find a version that satisfies the requirement pandas==2.1.*`

**Causa**: Versão do pacote não existe ou pip está desatualizado.

**Solução**:
```bash
# Atualize pip
pip install --upgrade pip

# Tente novamente
pip install -r requirements.txt
```

#### Conflitos de Dependências

**Erro**: `pip's dependency resolver does not currently take into account all the packages...`

**Solução**: Isso geralmente é um aviso, não um erro. Prossiga com:
```bash
python -c "import pandas, psycopg2, dotenv, requests; print('Todas as importações OK')"
```

Se as importações funcionam, você está bem. Se não, tente:
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

### Erros de Variáveis de Ambiente

**Erro**: Arquivo `.env` não encontrado

**Causa**: Você não copiou `.env.example` para `.env`

**Solução**:
```bash
cp .env.example .env  # macOS/Linux
# ou
copy .env.example .env  # Windows
```

**Erro**: Variável retorna `None` em Python

**Causa**: Nome da variável não corresponde no arquivo `.env`

**Solução**:
```bash
# Verifique se arquivo .env contém a variável
cat .env  # macOS/Linux
type .env  # Windows

# Verifique ortografia exata: DB_HOST, DB_USER, DB_PASSWORD, API_TOKEN
```

---

### Erros de Conexão PostgreSQL

#### "could not connect to server: Connection refused"

**Causa**: Serviço PostgreSQL não está funcionando

**Solução**:

**macOS**:
```bash
brew services start postgresql@14
```

**Linux**:
```bash
sudo systemctl start postgresql
```

**Windows**: Inicie PostgreSQL no aplicativo Services

Então verifique:
```bash
psql --version
```

#### "FATAL: password authentication failed"

**Causa**: Senha errada no arquivo `.env`

**Solução**:
1. Resete a senha PostgreSQL:

   **macOS/Linux**:
   ```bash
   sudo -u postgres psql
   ALTER USER seu_usuario WITH PASSWORD 'nova_senha';
   \q
   ```

   **Windows**: Use a ferramenta GUI pgAdmin

2. Atualize `.env` com a senha correta:
   ```ini
   DB_PASSWORD=nova_senha
   ```

#### "FATAL: database 'X' does not exist"

**Causa**: Banco de dados não existe ainda

**Solução**:
```bash
# Crie um banco de dados
createdb -U seu_usuario nome_seu_banco

# Atualize .env se usando um banco específico
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

---

## Checklist de Segurança

Antes de fazer commit de código ou compartilhar sua configuração, verifique:

- ✅ `.env` está em `.gitignore` (verifique: `git status | grep .env` deve estar vazio)
- ✅ Arquivo `.env` NÃO existe no histórico git: `git log --all -- .env` deve estar vazio
- ✅ `.env.example` contém NÃO CONTÉM segredos reais (todos valores template)
- ✅ Código Python usa `load_dotenv()` antes de acessar `os.getenv()`
- ✅ `.env` tem permissões seguras: `ls -la .env` deve mostrar `rw-------` (600)

**Corrija permissões se necessário**:
```bash
chmod 600 .env
```

---

## Próximos Passos

Uma vez que a configuração está completa:

1. ✅ Verifique todas as dependências instaladas: `pip list`
2. ✅ Teste conexão PostgreSQL: `python scripts/test-postgres-connection.py`
3. ✅ Execute seu primeiro script ou teste:
   ```bash
   python -c "import pandas; print('Versão Pandas:', pandas.__version__)"
   ```

---

## Suporte

Se encontrar problemas não listados acima:

1. Leia a mensagem de erro cuidadosamente - a maioria é auto-explicativa
2. Verifique que todos os pré-requisitos estão instalados e nas versões corretas
3. Consulte `README.md` para referência rápida de setup
4. Consulte seções específicas do SO acima para problemas específicos da plataforma

---

**Última Atualização**: 2025-11-07
