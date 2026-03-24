@echo off
:: ================================================
:: Hourly Tracker - Windows Auto-Start Setup
:: Run this once to add the app to Windows Startup
:: ================================================

set SCRIPT_DIR=%~dp0
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set VBS_PATH=%STARTUP_DIR%\HourlyTracker.vbs

echo Creating silent startup script...

:: Create a VBScript that runs Python silently (no console window)
echo Set oShell = CreateObject("WScript.Shell") > "%VBS_PATH%"
echo oShell.Run "pythonw ""%SCRIPT_DIR%main.py""", 0, False >> "%VBS_PATH%"

echo.
echo ✅ Done! Hourly Tracker will now start automatically on Windows login.
echo.
echo To remove auto-start, delete this file:
echo %VBS_PATH%
echo.
pause
