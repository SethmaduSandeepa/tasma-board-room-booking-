@echo off
REM TASMA Booking System - Portable Client Installer
REM This script can be copied to a USB drive or shared folder for easy distribution
REM Copy to USB/share along with this file and run it on any client machine

setlocal enabledelayedexpansion

cls
echo.
echo ========================================
echo TASMA Booking System - Client Installer
echo ========================================
echo.

REM Check if this script is on a USB or removable media
echo This installer will create a desktop shortcut for TASMA Booking System
echo.

set /p SERVER_NAME="Enter your server name or IP address: "
if "!SERVER_NAME!"=="" (
    echo ERROR: Server name/IP is required!
    echo Example: MYSERVER or 192.168.1.100
    pause
    exit /b 1
)

set /p CONTINUE="Continue with server: !SERVER_NAME! (Y/N)? "
if /i not "!CONTINUE!"=="Y" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo Verifying server connection...
timeout /t 1 /nobreak > nul

REM Test connection
ping -n 1 "!SERVER_NAME!" >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Could not reach server !SERVER_NAME!
    echo.
    echo Please verify:
    echo   - Server name is spelled correctly
    echo   - Server is powered on
    echo   - Network cable is connected
    echo   - You are on the correct network
    echo.
    echo You can:
    echo   1. Try again with correct server name
    echo   2. Contact IT support
    echo.
    pause
    exit /b 1
)

echo Server found at: !SERVER_NAME!
echo.

REM Test share access
echo Checking TASMA application share...
dir "\\!SERVER_NAME!\TASMA_App" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Cannot access TASMA application on server
    echo Path: \\!SERVER_NAME!\TASMA_App
    echo.
    echo Please verify:
    echo   - Server name is correct
    echo   - Server has been set up with deploy_server_complete.bat
    echo   - Network shares are properly configured
    echo.
    pause
    exit /b 1
)

echo TASMA application found!
echo.

REM Get Desktop path
for /f "tokens=3*" %%a in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Desktop ^| findstr /i desktop') do set DESKTOP_PATH=%%b

if "!DESKTOP_PATH!"=="" (
    echo ERROR: Could not find Desktop folder
    pause
    exit /b 1
)

echo.
echo Creating desktop shortcut...
echo.

REM Create shortcut using VBScript
set "SHORTCUT_PATH=!DESKTOP_PATH!\TASMA Board Room Booking System.lnk"
set "TARGET=\\!SERVER_NAME!\TASMA_App\TASMA Board Room Booking System.exe"
set "WORK_DIR=\\!SERVER_NAME!\TASMA_App"
set "ICON_PATH=\\!SERVER_NAME!\TASMA_App\booking_icon.ico"

(
    echo Set oWS = WScript.CreateObject("WScript.Shell"^)
    echo sLinkFile = "!SHORTCUT_PATH!"
    echo Set oLink = oWS.CreateShortcut(sLinkFile^)
    echo oLink.TargetPath = "!TARGET!"
    echo oLink.WorkingDirectory = "!WORK_DIR!"
    echo oLink.Description = "TASMA Board Room Booking System"
    echo oLink.IconLocation = "!ICON_PATH!"
    echo oLink.WindowStyle = 1
    echo oLink.Save
) > create_shortcut.vbs

cscript.exe create_shortcut.vbs >nul 2>&1
del create_shortcut.vbs

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Shortcut created on your desktop:
echo   Name: TASMA Board Room Booking System
echo   Location: !DESKTOP_PATH!
echo.
echo Server: \\!SERVER_NAME!\TASMA_App
echo.
echo You can now:
echo   1. Double-click the desktop shortcut to launch TASMA
echo   2. Right-click and select "Pin to Start" to add to Start menu
echo.
echo First launch will take 2-3 seconds while connecting to the database.
echo Subsequent launches will be faster.
echo.
echo Default Login (for first time only):
echo   Username: admin
echo   Password: admin
echo.
echo IMPORTANT: Change the admin password immediately after first login!
echo.
echo For help, see USER_QUICK_START.md
echo.
pause
