
@echo off
setlocal
cd /d "%~dp0"
title NutriBot Launcher

echo Starting NutriBot...
echo Project folder: %CD%
echo.

if not exist "app.py" (
    echo ERROR: app.py was not found in this folder.
    pause
    exit /b 1
)

if exist "venv\Scripts\python.exe" (
    "venv\Scripts\python.exe" -m streamlit run app.py
) else (
    python -m streamlit run app.py
)

echo.
echo NutriBot has stopped or could not start.
pause
