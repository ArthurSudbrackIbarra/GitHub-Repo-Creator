@echo off

:: Checking if python or python3.
python3 --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    python %~dp0.program-files\main.py %*
    exit /b %ERRORLEVEL%
) 

python3 %~dp0.program-files\main.py %*s