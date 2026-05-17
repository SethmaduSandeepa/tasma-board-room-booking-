@echo off
REM TASMA Client Shortcut Deployment Script
REM This script creates a desktop shortcut for the TASMA application
REM Run on each client machine

setlocal enabledelayedexpansion

cls
echo.
echo ========================================
echo TASMA Booking System - Client Setup
echo ========================================
echo.

REM Get server information
set /p SERVER_NAME="Enter server name or IP address: "
if "!SERVER_NAME!"=="" (
    echo ERROR: Server name is required!
    pause
    exit /b 1
)

set /p SHARE_NAME="Enter share name (default TASMA_App): "
if "!SHARE_NAME!"=="" set SHARE_NAME=TASMA_App

echo.
echo Server: !SERVER_NAME!
echo Share: !SHARE_NAME!
echo Application path: \\!SERVER_NAME!\!SHARE_NAME!
echo.

set /p CONFIRM="Is this correct (Y/N)? "
if /i not "!CONFIRM!"=="Y" (
    echo Setup cancelled.
    exit /b 0
)

echo.
echo Testing network access...
timeout /t 1 /nobreak > nul

dir "\\!SERVER_NAME!\!SHARE_NAME!" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Cannot access \\!SERVER_NAME!\!SHARE_NAME!
    echo Please verify:
    echo   - Server name is correct
    echo   - Network connection is working
    echo   - Share is properly configured
    echo Run: ping !SERVER_NAME!
    pause
    exit /b 1
)

echo Network access verified!

echo.
echo Creating desktop shortcut...

REM Create shortcut using VBScript via PowerShell
powershell -NoProfile -Command ^
  "$desktopPath = [System.Environment]::GetFolderPath('Desktop'); " ^
  "$shortcutPath = Join-Path $desktopPath 'TASMA Booking System.lnk'; " ^
  "$appPath = '\\!SERVER_NAME!\!SHARE_NAME!'; " ^
  "$exePath = Join-Path $appPath 'TASMA Board Room Booking System.exe'; " ^
  "$iconPath = Join-Path $appPath 'booking_icon.ico'; " ^
  "$WshShell = New-Object -ComObject WScript.Shell; " ^
  "$shortcut = $WshShell.CreateShortcut($shortcutPath); " ^
  "$shortcut.TargetPath = $exePath; " ^
  "$shortcut.WorkingDirectory = $appPath; " ^
  "$shortcut.IconLocation = $iconPath; " ^
  "$shortcut.Description = 'TASMA Board Room Booking System'; " ^
  "$shortcut.Save(); " ^
  "Write-Host 'Shortcut created successfully at: ' $shortcutPath"

if errorlevel 1 (
    echo ERROR: Failed to create shortcut!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Desktop shortcut created!
echo You can now double-click 'TASMA Booking System' to launch the app.
echo.
echo First launch will take 3-5 seconds. Subsequent launches will be faster.
echo.
pause
