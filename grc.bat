@echo off

set COMMAND=%1

if "%COMMAND%" == "" (
    echo.
    echo GRC: No command passed
    echo.
    exit /b 1
)

powershell -ep Bypass %~dp0grc-helper.ps1 %*
