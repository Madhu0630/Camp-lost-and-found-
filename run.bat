@echo off
title CampusConnect - Lost and Found Management System
echo ===================================================
echo     CampusConnect - Lost and Found Management System
echo ===================================================
echo.

cd /d "%~dp0"

REM Check for py or python
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=py
) else (
    where python >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set PYTHON_CMD=python
    ) else (
        echo [ERROR] Python is not found on your system!
        echo Please install Python 3.8+ from https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

echo Using Python command: %PYTHON_CMD%

REM Check if .venv exists
if not exist ".venv\Scripts\activate.bat" (
    echo [INFO] Creating Python virtual environment (.venv)...
    %PYTHON_CMD% -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [INFO] Installing / updating required dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo   Launching CampusConnect in your default browser...
echo   Press Ctrl+C in this window to stop the server.
echo ===================================================
echo.

python -m streamlit run app.py

pause
