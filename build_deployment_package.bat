@echo off
REM TASMA Booking System - Complete Professional Deployment Package
REM This script prepares everything for professional deployment

setlocal enabledelayedexpansion

echo.
echo ====================================================================
echo      TASMA Board Room Booking System - Deployment Package
echo ====================================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [2/5] Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo [3/5] Creating standalone executable...
if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1

python -m PyInstaller --onefile --windowed --name "TASMA Board Room Booking System" --icon=booking_icon.ico --add-data "tasma_logo.webp;." main.py

if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)

REM Move the executable to dist folder if it's in a different location
if exist "dist" (
    echo Executable created successfully
) else (
    mkdir dist
    move /Y "TASMA Board Room Booking System.exe" "dist\" >nul 2>&1
)

echo [4/5] Creating deployment folders...
if not exist "deployment" mkdir deployment
copy "dist\TASMA Board Room Booking System.exe" "deployment\"
copy "bookings.db" "deployment\"
copy "booking_icon.ico" "deployment\"
copy "tasma_logo.webp" "deployment\"
copy "DEPLOYMENT_GUIDE.md" "deployment\"

echo [5/5] Generating summary...
echo.
echo ====================================================================
echo                    DEPLOYMENT SUCCESSFUL!
echo ====================================================================
echo.
echo Files ready for distribution:
echo   - deployment\TASMA Board Room Booking System.exe  (Standalone App)
echo   - deployment\bookings.db                          (Database)
echo   - deployment\tasma_logo.webp                      (Logo)
echo   - deployment\DEPLOYMENT_GUIDE.md                  (Instructions)
echo.
echo Next Steps:
echo   1. Test the executable: deployment\TASMA Board Room Booking System.exe
echo   2. Read DEPLOYMENT_GUIDE.md for distribution options
echo   3. Create installer (optional): makensis installer.nsi
echo   4. Copy files to deployment media or network share
echo.
echo System Requirements for End Users:
echo   - Windows 7 or newer
echo   - 50 MB disk space
echo   - No Python installation required
echo.
pause
