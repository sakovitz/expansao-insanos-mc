# Insanos MC - Área de Expansão

Este repositório centraliza os projetos de **engenharia de dados**, **inteligência artificial** e **automações** da área de **Expansão do Insanos MC**.
Aqui estão as ferramentas que impulsionam o crescimento do clube, conectando tecnologia, estratégia e irmandade.

## 💀 Estrutura do repositório
- **pipelines/** – Processos de engenharia e tratamento de dados (ETL, integrações, etc.)
- **ia/** – Workflows e modelos de IA usados pela expansão (incluindo automações via n8n)
- **automacoes/** – Scripts e sistemas automatizados, como a geração de flyers e bots de suporte
- **data/** – Dados brutos, tratados e saídas de relatórios
- **docs/** – Documentações técnicas e de arquitetura

## 💀 Objetivo
Unir dados, automação e inteligência para acelerar o crescimento e a organização do Insanos MC, mantendo o espírito do clube em cada linha de código.

## 💀 Tecnologias
- Python / SQL / n8n
- Automação de tarefas e geração de conteúdo
- Integrações com APIs internas e externas

---

## 🚀 Configuração Rápida

Configure o ambiente completo em ~10 minutos. Para troubleshooting detalhado, consulte [docs/SETUP.md](docs/SETUP.md).

### Pré-requisitos

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **PostgreSQL** ([Download](https://www.postgresql.org/download/))
- **pip** (incluído com Python)

### Passo 1: Validar Python

```bash
# macOS/Linux
bash scripts/validate-python.sh

# Windows CMD
scripts\validate-python.bat
```

Esperado: `Python 3.11.x detectado`

### Passo 2: Criar e Ativar Ambiente Virtual

```bash
# Criar ambiente virtual (todas as plataformas)
python -m venv expansao

# Ativar: macOS/Linux
source expansao/bin/activate

# Ativar: Windows CMD
expansao\Scripts\activate.bat

# Ativar: Windows PowerShell
& "expansao\Scripts\Activate.ps1"
```

Após ativação, seu prompt mostrará o prefixo `(expansao)`.

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

Verificar: `pip list` deve mostrar pandas, psycopg2, python-dotenv, requests

### Passo 4: Configurar Credenciais

```bash
# Copiar template
cp .env.example .env     # macOS/Linux
copy .env.example .env   # Windows

# Editar com suas credenciais
nano .env    # macOS/Linux
notepad .env # Windows
```

**Variáveis obrigatórias** em `.env`:
```ini
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
API_TOKEN=seu_token
```

### Passo 5: Testar Conexão

```bash
python scripts/test-postgres-connection.py
```

Esperado: `✓ Conexão PostgreSQL OK`

### Desativar Ambiente

```bash
deactivate
```

---

### Checklist de Validação

- [ ] Versão Python 3.11+: `python --version`
- [ ] Ambiente virtual criado: `ls expansao/` ou `dir expansao\`
- [ ] Ambiente virtual ativado: Prompt mostra `(expansao)`
- [ ] Dependências instaladas: `pip list` mostra 4 pacotes
- [ ] Arquivo `.env` existe: `cat .env` ou `type .env`
- [ ] `.env` ignorado por git: `git status | grep .env` (resultado vazio)
- [ ] Variáveis de ambiente legíveis: Teste com comando Python acima
- [ ] Conexão PostgreSQL funciona: `python scripts/test-postgres-connection.py`

### Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| `Versão Python muito antiga` | Instale Python 3.11+ de [python.org](https://www.python.org/downloads/) |
| `Permissão negada: activate` | Certifique-se de estar no diretório raiz: `source ./expansao/bin/activate` |
| `.env não encontrado` | Copie o template: `cp .env.example .env` |
| `conexão recusada` | Inicie PostgreSQL (veja [docs/SETUP.md](docs/SETUP.md) para passos específicos do SO) |
| `módulo não encontrado` | Ative o venv primeiro: `source expansao/bin/activate` |

### Documentação Completa

Para guia completo de setup com instruções específicas do SO e troubleshooting detalhado, consulte [📖 docs/SETUP.md](docs/SETUP.md).

---
**"Dividir e Conquistar"**
