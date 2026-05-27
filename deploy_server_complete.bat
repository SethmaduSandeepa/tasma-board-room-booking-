@echo off
REM TASMA Booking System - Complete Server Deployment Script
REM This script sets up the server with shared folders and database
REM Run as Administrator on the server machine

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
echo Step 1: Configure Server Paths
echo ========================================
echo.
set /p APP_DRIVE="Application drive (default C:): "
if "!APP_DRIVE!"=="" set APP_DRIVE=C:

set /p APP_PATH="Application folder (default \SharedApps\TASMA): "
if "!APP_PATH!"=="" set APP_PATH=\SharedApps\TASMA

set /p DATA_PATH="Database folder (default \SharedData\TASMA): "
if "!DATA_PATH!"=="" set DATA_PATH=\SharedData\TASMA

set "APP_FULL=!APP_DRIVE!!APP_PATH!"
set "DATA_FULL=!APP_DRIVE!!DATA_PATH!"

echo.
echo Step 2: Create Directories
echo ========================================
echo Creating: !APP_FULL!
mkdir "!APP_FULL!" 2>nul
if errorlevel 1 (
    echo ERROR: Could not create application directory
    pause
    exit /b 1
)
echo Created successfully.

echo Creating: !DATA_FULL!
mkdir "!DATA_FULL!" 2>nul
if errorlevel 1 (
    echo ERROR: Could not create database directory
    pause
    exit /b 1
)
echo Created successfully.

echo.
echo Step 3: Copy Application Files
echo ========================================
echo.
echo NOTE: Ensure the following files exist in the current directory:
echo   - TASMA Board Room Booking System.exe
echo   - tasma_logo.webp
echo   - booking_icon.ico
echo   - config.ini
echo.
set /p COPY_FILES="Copy files now (Y/N)? "
if /i "!COPY_FILES!"=="Y" (
    echo.
    echo Copying executable...
    copy "TASMA Board Room Booking System.exe" "!APP_FULL!" >nul 2>&1
    if errorlevel 1 (
        echo WARNING: Could not copy exe file
    ) else (
        echo Copied: TASMA Board Room Booking System.exe
    )

    echo Copying logo...
    copy tasma_logo.webp "!APP_FULL!" >nul 2>&1
    if errorlevel 1 (
        echo WARNING: Could not copy logo
    ) else (
        echo Copied: tasma_logo.webp
    )

    echo Copying icon...
    copy booking_icon.ico "!APP_FULL!" >nul 2>&1
    if errorlevel 1 (
        echo WARNING: Could not copy icon
    ) else (
        echo Copied: booking_icon.ico
    )

    echo Copying config...
    copy config.ini "!APP_FULL!" >nul 2>&1
    if errorlevel 1 (
        echo WARNING: Could not copy config
    ) else (
        echo Copied: config.ini
    )

    echo Copying database...
    copy bookings.db "!DATA_FULL!" >nul 2>&1
    if errorlevel 1 (
        echo WARNING: Could not copy database
    ) else (
        echo Copied: bookings.db
    )
    echo.
)

echo.
echo Step 4: Configure Network Shares
echo ========================================
echo.
echo Creating network shares...

REM Get computer name for share creation
for /f "delims=" %%i in ('hostname') do set COMPUTER_NAME=%%i

echo Computer Name: !COMPUTER_NAME!
echo.

REM Create application share
echo Creating TASMA_App share...
net share TASMA_App="!APP_FULL!" /grant:Everyone,FULL >nul 2>&1
if errorlevel 1 (
    echo WARNING: Could not create TASMA_App share
    echo Try manually: net share TASMA_App="!APP_FULL!" /grant:Everyone,FULL
) else (
    echo TASMA_App share created.
)

REM Create database share
echo Creating TASMA_Data share...
net share TASMA_Data="!DATA_FULL!" /grant:Everyone,FULL >nul 2>&1
if errorlevel 1 (
    echo WARNING: Could not create TASMA_Data share
    echo Try manually: net share TASMA_Data="!DATA_FULL!" /grant:Everyone,FULL
) else (
    echo TASMA_Data share created.
)

echo.
echo Step 5: Update Configuration
echo ========================================
echo.
echo For Windows Server, update UNC paths in shared config.ini:
echo   - Set database_path = \\!COMPUTER_NAME!\TASMA_Data\bookings.db
echo.

REM Update config.ini in the shared app folder
if exist "!APP_FULL!\config.ini" (
    echo Updating config.ini with server paths...
    
    REM Create a temporary config file with server paths
    (
        echo [SERVER]
        echo # Network database path
        echo database_path = \\!COMPUTER_NAME!\TASMA_Data\bookings.db
        echo db_timeout = 30
        echo enable_cache = true
        echo cache_timeout = 300
        echo lazy_load_ui = true
        echo preload_assets = false
        echo.
        echo [LOGGING]
        echo debug_mode = false
        echo log_file = tasma_app.log
        echo.
        echo [PERFORMANCE]
        echo connection_pool_size = 2
        echo batch_size = 100
    ) > "!APP_FULL!\config.ini"
    echo Config updated.
)

echo.
echo ========================================
echo Server Setup Complete!
echo ========================================
echo.
echo Server Information:
echo   Computer Name: !COMPUTER_NAME!
echo   Application Share: \\!COMPUTER_NAME!\TASMA_App
echo   Database Share: \\!COMPUTER_NAME!\TASMA_Data
echo.
echo Next Steps:
echo 1. Run client setup on each user's computer
echo 2. Use setup_client_desktop.bat to create desktop shortcuts
echo 3. Provide users with the desktop shortcut
echo.
echo For client setup, run:
echo   setup_client_desktop.bat !COMPUTER_NAME!
echo.
pause
