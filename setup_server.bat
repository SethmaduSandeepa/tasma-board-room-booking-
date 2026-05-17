@echo off
REM TASMA Server Setup Script
REM This script sets up shared folders on a server for the TASMA application
REM Run as Administrator

setlocal enabledelayedexpansion

cls
echo.
echo ========================================
echo TASMA Booking System - Server Setup
echo ========================================
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Get user input
echo.
echo Enter the following information:
echo.
set /p APP_DRIVE="Application drive (default C:): "
if "!APP_DRIVE!"=="" set APP_DRIVE=C:

set /p DATA_DRIVE="Data drive (default C:): "
if "!DATA_DRIVE!"=="" set DATA_DRIVE=C:

set /p SHARE_NAME="Server name/hostname (used in shortcuts): "
if "!SHARE_NAME!"=="" (
    for /f %%A in ('hostname') do set SHARE_NAME=%%A
)

echo.
echo Configuration:
echo Application folder: !APP_DRIVE!\SharedApps\TASMA
echo Data folder: !DATA_DRIVE!\SharedData\TASMA
echo Server name: !SHARE_NAME!
echo.

set /p CONFIRM="Is this correct (Y/N)? "
if /i not "!CONFIRM!"=="Y" (
    echo Setup cancelled.
    exit /b 0
)

REM Create folders
echo.
echo Creating folders...
if not exist "!APP_DRIVE!\SharedApps\TASMA" (
    mkdir "!APP_DRIVE!\SharedApps\TASMA"
    echo Created: !APP_DRIVE!\SharedApps\TASMA
)

if not exist "!DATA_DRIVE!\SharedData\TASMA" (
    mkdir "!DATA_DRIVE!\SharedData\TASMA"
    echo Created: !DATA_DRIVE!\SharedData\TASMA
)

echo.
echo Copying application files...
REM Copy files from current directory or deployment folder
if exist "deployment\TASMA Board Room Booking System.exe" (
    copy "deployment\TASMA Board Room Booking System.exe" "!APP_DRIVE!\SharedApps\TASMA\"
    echo Copied executable
)

if exist "deployment\tasma_logo.webp" (
    copy "deployment\tasma_logo.webp" "!APP_DRIVE!\SharedApps\TASMA\"
    echo Copied logo
)

if exist "deployment\booking_icon.ico" (
    copy "deployment\booking_icon.ico" "!APP_DRIVE!\SharedApps\TASMA\"
    echo Copied icon
)

if exist "config.ini" (
    copy "config.ini" "!APP_DRIVE!\SharedApps\TASMA\"
    echo Copied config
)

echo.
echo Creating network shares...

REM Remove existing shares
net share TASMA_App /delete /y >nul 2>&1
net share TASMA_Data /delete /y >nul 2>&1

REM Create new shares
net share TASMA_App="!APP_DRIVE!\SharedApps\TASMA" /grant:Everyone,FULL
if errorlevel 1 (
    echo ERROR: Failed to create TASMA_App share
) else (
    echo Created share: TASMA_App
)

net share TASMA_Data="!DATA_DRIVE!\SharedData\TASMA" /grant:Everyone,FULL
if errorlevel 1 (
    echo ERROR: Failed to create TASMA_Data share
) else (
    echo Created share: TASMA_Data
)

echo.
echo Setting folder permissions...

REM Set NTFS permissions
icacls "!APP_DRIVE!\SharedApps\TASMA" /grant:r Everyone:(OI)(CI)F /t >nul 2>&1
icacls "!DATA_DRIVE!\SharedData\TASMA" /grant:r Everyone:(OI)(CI)F /t >nul 2>&1

echo.
echo Updating config.ini with database path...

REM Update config file with network path
setlocal enabledelayedexpansion
set CONFIG_FILE="!APP_DRIVE!\SharedApps\TASMA\config.ini"

if exist !CONFIG_FILE! (
    REM Create temporary config with updated path
    (
        echo [SERVER]
        echo database_path = \\!SHARE_NAME!\TASMA_Data\bookings.db
        echo db_timeout = 60
        echo enable_cache = true
        echo cache_timeout = 300
        echo.
        echo [LOGGING]
        echo debug_mode = false
        echo log_file = tasma_app.log
        echo.
        echo [PERFORMANCE]
        echo connection_pool_size = 10
        echo batch_size = 100
    ) > !CONFIG_FILE!
    
    echo Config updated with server path: \\!SHARE_NAME!\TASMA_Data\bookings.db
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy database file to: !DATA_DRIVE!\SharedData\TASMA\bookings.db
echo 2. Run deploy_shortcuts.bat on each client machine
echo 3. Verify by checking: \\!SHARE_NAME!\TASMA_App
echo.
echo To verify shares were created, run: net share
echo To access from client: \\!SHARE_NAME!\TASMA_App
echo.
pause
