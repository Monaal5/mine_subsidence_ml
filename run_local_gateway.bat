@echo off
title Mine Subsidence Gateway & Web Dashboard
echo =====================================================================
echo  Mine Subsidence AI Platform — Local Gateway & Dashboard Starter
echo =====================================================================
echo.
cd /d "%~dp0"

IF NOT EXIST "ml_venv\Scripts\python.exe" (
    echo [1/2] Setting up Python Virtual Environment...
    python -m venv ml_venv
    call ml_venv\Scripts\activate
    pip install -r requirements.txt
) ELSE (
    echo [1/2] Virtual Environment Ready!
    call ml_venv\Scripts\activate
)

echo.
echo [2/2] Starting Gateway Server & Web Dashboard on Port 8050...
echo.
echo Dashboard URL: http://localhost:8050
echo API Health:    http://localhost:8050/api/health
echo.
python web_app/server.py
pause
