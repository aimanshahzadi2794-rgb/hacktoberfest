@echo off
setlocal
cd /d "%~dp0"
echo ========================================
echo IssuePilot AI - Windows setup
echo ========================================
where py >nul 2>nul
if errorlevel 1 (
    echo Python launcher "py" was not found.
    echo Install Python 3.11 or 3.12 from https://www.python.org/downloads/windows/
    echo During installation, enable "Add Python to PATH".
    pause
    exit /b 1
)
py -3.11 --version >nul 2>nul
if not errorlevel 1 (
    set PYTHON_CMD=py -3.11
) else (
    py -3.12 --version >nul 2>nul
    if not errorlevel 1 (
        set PYTHON_CMD=py -3.12
    ) else (
        echo Python 3.11 or 3.12 was not found.
        echo Install Python 3.11 or 3.12, then run this file again.
        pause
        exit /b 1
    )
)
%PYTHON_CMD% -m venv .venv
if errorlevel 1 goto error
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
if errorlevel 1 goto error
python -m pip install -r requirements.txt
if errorlevel 1 goto error
echo.
echo Setup complete. Double-click run.bat to start IssuePilot AI.
pause
exit /b 0
:error
echo.
echo Setup failed. Read the error above, check internet access, and try again.
pause
exit /b 1
