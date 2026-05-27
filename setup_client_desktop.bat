@echo off
REM TASMA Booking System - Client Desktop Shortcut Installer
REM This script creates a desktop shortcut to the server application
REM Run on each client machine (Administrator not required)

setlocal enabledelayedexpansion

cls
echo.
echo ========================================
echo TASMA Booking System - Client Setup
echo ========================================
echo.

REM Check if server name was passed as parameter
if not "!%1!"=="" (
    set SERVER_NAME=%1
    echo Using server: !SERVER_NAME!
) else (
    set /p SERVER_NAME="Enter server name or IP address: "
    if "!SERVER_NAME!"=="" (
        echo ERROR: Server name is required!
        pause
        exit /b 1
    )
)

set SHARE_NAME=TASMA_App
set APP_PATH=\\!SERVER_NAME!\!SHARE_NAME!
set EXE_NAME=TASMA Board Room Booking System.exe

echo.
echo Verifying server connection...
echo Server Path: !APP_PATH!
echo.

REM Test access to server
timeout /t 1 /nobreak > nul
dir "!APP_PATH!" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Cannot access \\!SERVER_NAME!\!SHARE_NAME!
    echo.
    echo Please verify:
    echo   - Server name is correct
    echo   - Network connection is working
    echo   - Server shares are configured
    echo.
    echo Test connection with:
    echo   ping !SERVER_NAME!
    echo   dir \\!SERVER_NAME!\TASMA_App
    echo.
    pause
    exit /b 1
)

echo Server found! Creating shortcut...
echo.

REM Get Desktop path
for /f "tokens=3*" %%a in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Desktop ^| findstr /i desktop') do set DESKTOP_PATH=%%b

if "!DESKTOP_PATH!"=="" (
    echo ERROR: Could not find Desktop folder
    pause
    exit /b 1
)

echo Desktop Path: !DESKTOP_PATH!
echo.

REM Create shortcut using VBScript
set "SHORTCUT_PATH=!DESKTOP_PATH!\TASMA Board Room Booking System.lnk"
set "TARGET=!APP_PATH!\!EXE_NAME!"

echo Creating VBScript to generate shortcut...
(
    echo Set oWS = WScript.CreateObject("WScript.Shell"^)
    echo sLinkFile = "!SHORTCUT_PATH!"
    echo Set oLink = oWS.CreateShortcut(sLinkFile^)
    echo oLink.TargetPath = "!TARGET!"
    echo oLink.WorkingDirectory = "!APP_PATH!"
    echo oLink.Description = "TASMA Board Room Booking System"
    echo oLink.IconLocation = "!APP_PATH!\booking_icon.ico"
    echo oLink.Save
    echo WScript.Echo "Shortcut created successfully"
) > create_shortcut.vbs

REM Execute VBScript
cscript.exe create_shortcut.vbs

REM Clean up VBScript
del create_shortcut.vbs

echo.
echo.
echo ========================================
echo Client Setup Complete!
echo ========================================
echo.
echo Shortcut created on your desktop:
echo   Name: TASMA Board Room Booking System
echo   Location: !DESKTOP_PATH!
echo.
echo Server: \\!SERVER_NAME!\!SHARE_NAME!
echo.
echo You can now:
echo 1. Double-click the desktop shortcut to launch TASMA
echo 2. Right-click the shortcut and select "Pin to Start" to add to Start Menu
echo.
echo First launch may take a few seconds as it connects to the server database.
echo.
pause
