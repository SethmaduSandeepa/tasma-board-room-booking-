@echo off
REM TASMA Booking System - Build with Inno Setup
REM Creates standalone .exe and professional installer

setlocal enabledelayedexpansion

echo.
echo ====================================================================
echo      TASMA Board Room Booking System - Build & Setup Creator
echo ====================================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [STEP 1] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [STEP 2] Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo [STEP 3] Creating standalone executable (this may take 2-5 minutes)...

REM Clean previous builds completely - More aggressive cleanup
echo Cleaning previous build artifacts...
if exist "build" (
    echo Waiting for file locks to release...
    timeout /t 1 /nobreak >nul
    rmdir /s /q "build" >nul 2>&1
)
if exist "dist" (
    timeout /t 1 /nobreak >nul
    rmdir /s /q "dist" >nul 2>&1
)
if exist "*.spec" del /q "*.spec" >nul 2>&1

echo Starting PyInstaller build...
python -m PyInstaller --onefile --windowed --name "TASMA Board Room Booking System" --icon=booking_icon.ico --add-data "tasma_logo.webp;." main.py

if errorlevel 1 (
    echo ERROR: Failed to build executable
    echo This may be due to files being locked by another process
    echo Please close any running instances of the application and try again
    pause
    exit /b 1
)

REM Verify dist folder
if not exist "dist" (
    echo ERROR: dist folder not created
    pause
    exit /b 1
)

echo.
echo [STEP 4] Creating deployment folder...
if not exist "deployment" mkdir deployment
copy "dist\TASMA Board Room Booking System.exe" "deployment\"
copy "bookings.db" "deployment\"
copy "booking_icon.ico" "deployment\"
copy "tasma_logo.webp" "deployment\"
copy "DEPLOYMENT_GUIDE.md" "deployment\"
copy "README.md" "deployment\"
copy "FEATURES.md" "deployment\"

echo.
echo [STEP 5] Checking for Inno Setup...
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    echo Found Inno Setup 6
    echo [STEP 6] Creating professional installer...
    
    if not exist "setup_output" mkdir setup_output
    "C:\Program Files\Inno Setup 6\ISCC.exe" "TASMA_Installer.iss"
    
    if errorlevel 1 (
        echo WARNING: Inno Setup compilation failed
        echo You can manually compile by:
        echo 1. Open Inno Setup
        echo 2. File ^> Open
        echo 3. Select TASMA_Installer.iss
        echo 4. Click Build
    ) else (
        echo INSTALLER CREATED SUCCESSFULLY!
        if exist "setup_output\TASMA_Booking_System_Setup_v2.0.exe" (
            echo Location: setup_output\TASMA_Booking_System_Setup_v2.0.exe
        )
    )
) else (
    echo.
    echo NOTE: Inno Setup not found at default location
    echo To create installer manually:
    echo 1. Open Inno Setup
    echo 2. File ^> Open ^> TASMA_Installer.iss
    echo 3. Click Build
)

echo.
echo ====================================================================
echo                    BUILD COMPLETE!
echo ====================================================================
echo.
echo Ready for Distribution:
echo   Standalone .exe: deployment\TASMA Board Room Booking System.exe
echo   Professional Installer: setup_output\TASMA_Booking_System_Setup_v2.0.exe (if built)
echo.
echo System Requirements for End Users:
echo   - Windows 7 or newer
echo   - 50-100 MB disk space
echo   - NO Python installation required!
echo.
pause
