# Quickstart: Setup de Ambiente Virtual Python - Insanos MC Expansão

**Duration**: ~10 minutes
**Prerequisites**: Python 3.11+ installed on your machine
**Goal**: Ready to run ETL scripts and test database connections

---

## 🚀 Quick Setup (Choose Your OS)

### Linux / macOS

```bash
# 1. Validate Python version (recommended first step)
bash scripts/validate-python.sh

# 2. Create isolated environment
python3 -m venv expansao

# 3. Activate environment
source expansao/bin/activate

# 4. Install dependencies (with exact versions)
pip install -r requirements.txt

# 5. Setup credentials (copy template)
cp .env.example .env

# 6. Edit .env with your credentials
nano .env
# OR vim .env
# Fill in: DB_HOST, DB_USER, DB_PASSWORD, API_TOKEN

# 7. Verify setup
python3 -c "from dotenv import load_dotenv; load_dotenv(); import os; print('DB_HOST:', os.getenv('DB_HOST'))"

# Expected output: DB_HOST: localhost (or your configured value)
```

### Windows (PowerShell or CMD)

```batch
REM 1. Validate Python version (recommended first step)
scripts\validate-python.bat

REM 2. Create isolated environment
python -m venv expansao

REM 3. Activate environment
expansao\Scripts\activate.bat

REM 4. Install dependencies (with exact versions)
pip install -r requirements.txt

REM 5. Setup credentials (copy template)
copy .env.example .env

REM 6. Edit .env with your credentials
notepad .env
REM Fill in: DB_HOST, DB_USER, DB_PASSWORD, API_TOKEN

REM 7. Verify setup
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('DB_HOST:', os.getenv('DB_HOST'))"

REM Expected output: DB_HOST: localhost (or your configured value)
```

---

## ✅ Validation Checklist

After setup, verify everything works:

- [ ] Python version ≥ 3.11 (run: `python --version`)
- [ ] Virtual environment activated (prompt shows `(expansao)`)
- [ ] All packages installed (run: `pip list` and see pandas, psycopg2, etc.)
- [ ] .env file exists and populated (run: `ls .env` or `dir .env` on Windows)
- [ ] .env is ignored by git (run: `git status | grep .env` should be empty)
- [ ] Environment variables readable (test script above worked)

---

## 🔧 What Each Step Does

| Step | Command | What It Does | Why Important |
|------|---------|-------------|---------------|
| 1 | validate-python.sh/.bat | Checks Python 3.11+ installed | Prevents mysterious errors later |
| 2 | python -m venv expansao | Creates isolated Python environment | Keeps project deps separate from system |
| 3 | source/call activate | Activates the virtual environment | Ensures `pip` installs to venv, not system |
| 4 | pip install -r requirements.txt | Installs exact versions of packages | Ensures reproducible environment across devs |
| 5 | cp .env.example .env | Creates local credentials file | Safe way to manage secrets locally |
| 6 | nano/notepad .env | Fills in real credentials | Authenticates to PostgreSQL + APIs |
| 7 | python -c (load_dotenv) | Verifies env vars are accessible | Confirms setup complete |

---

## 🏃 Quick Troubleshooting

### "Command not found: python3"
→ **Install Python 3.11** from https://www.python.org/downloads/
→ Or use: `python -m venv expansao` (Windows typically uses `python`, not `python3`)

### "python: command not found" (Windows)
→ Make sure Python is in your **PATH**. Reinstall checking "Add Python to PATH" box.
→ Or use absolute path: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe -m venv expansao`

### "No module named 'dotenv'"
→ Ensure you ran: `pip install -r requirements.txt`
→ Ensure venv is **active** (prompt shows `(expansao)`)

### "permission denied: scripts/validate-python.sh" (Linux/macOS)
→ Make script executable: `chmod +x scripts/validate-python.sh`
→ Then run: `bash scripts/validate-python.sh`

### ".env: No such file or directory"
→ You're in the wrong directory. Ensure you're in the project root (where `requirements.txt` exists)
→ Or: Create it manually: `cp .env.example .env`

### "psycopg2 error: could not connect"
→ PostgreSQL is not running. Start it:
  - **macOS** (Homebrew): `brew services start postgresql@14`
  - **Linux** (systemd): `sudo systemctl start postgresql`
  - **Windows**: Start PostgreSQL service from Services app
→ Ensure `DB_HOST`, `DB_USER`, `DB_PASSWORD` in .env match your PostgreSQL setup

### "DB_HOST returned None"
→ .env file exists but variable not found. Verify:
  ```bash
  cat .env | grep DB_HOST  # should print: DB_HOST=...
  ```
→ Make sure there's no space around `=` (should be `DB_HOST=localhost`, not `DB_HOST = localhost`)

---

## 🔐 Environment File (.env)

**Example .env.example** (in repo, safe):
```env
# PostgreSQL Connection (REQUIRED)
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password

# External APIs (REQUIRED)
API_TOKEN=your_api_key_here
```

**Your .env** (local only, in .gitignore, NOT in repo):
```env
# PostgreSQL Connection (REQUIRED)
DB_HOST=db.internal.company.com
DB_USER=jonasplima
DB_PASSWORD=my_secure_password_12345!

# External APIs (REQUIRED)
API_TOKEN=sk-abc123xyz789ghp_xyz
```

⚠️ **NEVER COMMIT .env FILE** - It contains credentials!

---

## 📚 Next Steps

1. **Run ETL scripts**: Scripts can now import Pandas, connect to PostgreSQL
2. **Test API integration**: requests library is ready for HTTP calls
3. **See detailed setup**: Read `docs/SETUP.md` for advanced configuration

---

## 💡 Tips

- Keep your `expansao` environment activated during development (prompt will remind you)
- If you mess up the environment, just delete it: `rm -rf expansao` (on Linux/macOS) or `rmdir /s expansao` (Windows)
- Then recreate: `python -m venv expansao` and repeat the 4 setup steps
- Update `requirements.txt` when adding new packages via PR (never auto-install)

---

✅ **You're ready to code!** 🚀

Questions? Check `docs/SETUP.md` for detailed troubleshooting per OS.

