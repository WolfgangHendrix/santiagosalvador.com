@echo off
title Santiago Salvador - Database Sync Tool
color 0b
echo =========================================================
echo    Santiago Salvador Portfolio & Labels Database Sync
echo =========================================================
echo.
echo Scanning files, removing deleted images, and updating catalogs...
echo.

python "%~dp0sync_database.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Python execution failed. Please check Python is installed.
) else (
    echo.
    echo Database synchronized successfully!
    echo Refresh your website in your browser to see all updates.
)

echo.
pause
