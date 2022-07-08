@echo off

set COMMAND=%1

if "%COMMAND%" == "" (
    echo.
    echo GRC is installed, use 'grc help' to see the list of commands.
    echo.
    exit /b 1
)

powershell -ep Bypass %~dp0grc-helper.ps1 %*

exit /b %ERRORLEVEL%
