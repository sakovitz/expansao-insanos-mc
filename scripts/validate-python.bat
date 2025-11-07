@echo off
REM Validate Python 3.11+ for Windows
REM Usage: scripts\validate-python.bat
REM Exit code: 0 = success, 1 = failure

setlocal enabledelayedexpansion

REM Check if python command exists
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: python not found
    echo Install Python from: https://www.python.org/downloads/
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i

REM Parse major and minor version
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

REM Check version is 3.11 or higher
if %MAJOR% lss 3 (
    echo ERROR: Python %PYTHON_VERSION% found
    echo Project requires Python 3.11 or higher
    echo Install from: https://www.python.org/downloads/
    exit /b 1
)

if %MAJOR% equ 3 if %MINOR% lss 11 (
    echo ERROR: Python %PYTHON_VERSION% found
    echo Project requires Python 3.11 or higher
    echo Install from: https://www.python.org/downloads/
    exit /b 1
)

echo [OK] Python %PYTHON_VERSION% detected
echo Ready to proceed with pip install
exit /b 0
