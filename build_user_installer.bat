"""
BUILD_USER_INSTALLER.bat
Creates a standalone installer EXE for users
Includes: TASMA app + database config + all dependencies

Run this on the build machine:
    build_user_installer.bat
"""
@echo off
setlocal enabledelayedexpansion

echo.
echo =====================================================
echo TASMA User Installer Builder
echo =====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo [1/5] Installing PyInstaller...
python -m pip install pyinstaller --quiet
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo [2/5] Preparing build directory...
if exist "installer_build" rmdir /s /q "installer_build"
mkdir "installer_build"
mkdir "installer_build\dist"

echo [3/5] Collecting files...
REM Copy essential files to build directory
copy "main.py" "installer_build\" >nul
copy "db_optimized.py" "installer_build\" >nul
copy "user_data_sync.py" "installer_build\" >nul
copy "SETUP_USER.py" "installer_build\" >nul
copy "config.ini" "installer_build\config.ini.template" >nul
copy "booking_icon.ico" "installer_build\" >nul
copy "requirements.txt" "installer_build\" >nul
copy "LICENSE.txt" "installer_build\" >nul

echo [4/5] Building standalone executable...
REM Build TASMA main EXE
pyinstaller ^
    --onefile ^
    --windowed ^
    --icon="booking_icon.ico" ^
    --name="TASMA" ^
    --add-data="booking_icon.ico;." ^
    --add-data="config.ini.template;." ^
    --distpath="installer_build\dist" ^
    --buildpath="build\tasma_build" ^
    --specpath="build" ^
    "installer_build\main.py"

if errorlevel 1 (
    echo ERROR: Failed to build main executable
    pause
    exit /b 1
)

echo [5/5] Creating installer package...
REM Copy additional files to dist
copy "installer_build\db_optimized.py" "installer_build\dist\" >nul
copy "installer_build\user_data_sync.py" "installer_build\dist\" >nul
copy "installer_build\SETUP_USER.py" "installer_build\dist\" >nul
copy "installer_build\config.ini.template" "installer_build\dist\" >nul
copy "installer_build\LICENSE.txt" "installer_build\dist\" >nul

echo.
echo =====================================================
echo SUCCESS!
echo =====================================================
echo.
echo Built files are in: installer_build\dist\
echo.
echo Files included in the installer:
echo   - TASMA.exe (Main application)
echo   - db_optimized.py (Database module)
echo   - user_data_sync.py (User sync module)
echo   - SETUP_USER.py (Configuration wizard)
echo   - config.ini.template (Configuration template)
echo   - LICENSE.txt
echo.
echo Next step: Use Inno Setup to create the final installer
echo   1. Open: TASMA_User_Installer.iss
echo   2. Click: Build > Compile
echo   3. Final .exe will be in: setup_output\
echo.
pause
