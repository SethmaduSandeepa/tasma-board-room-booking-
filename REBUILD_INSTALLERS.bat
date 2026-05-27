@echo off
REM REBUILD_INSTALLERS.bat
REM Rebuilds all installer files with latest code
REM Creates fresh: TASMA_User_Setup_v2.2.exe
REM
REM Usage:
REM   1. Run this script
REM   2. Open TASMA_User_Installer.iss in Inno Setup
REM   3. Click Build > Compile
REM   4. New installer will be in setup_output\
setlocal enabledelayedexpansion

echo.
echo =====================================================
echo TASMA Installer Rebuild Script
echo =====================================================
echo Latest version: 2.2
echo Build date: %date% %time%
echo.

REM Clean old build files
echo [1/6] Cleaning old build files...
if exist "installer_build" (
    rmdir /s /q "installer_build" >nul 2>&1
    echo   Removed: installer_build
)
if exist "build" (
    rmdir /s /q "build" >nul 2>&1
    echo   Removed: build
)
if exist "dist" (
    rmdir /s /q "dist" >nul 2>&1
    echo   Removed: dist
)
if exist "*.spec" (
    del /q "*.spec" >nul 2>&1
    echo   Removed: spec files
)

REM Verify Python
echo [2/6] Verifying Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo   Found: Python %PYTHON_VERSION%

REM Check PyInstaller
echo [3/6] Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo   Installing PyInstaller...
    pip install pyinstaller --quiet >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo   PyInstaller installed
) else (
    echo   PyInstaller already installed
)

REM Create build directories
echo [4/6] Creating build directories...
mkdir "installer_build\dist" >nul 2>&1
echo   Created: installer_build\dist

REM Collect latest files
echo [5/6] Gathering latest source files...
copy "main.py" "installer_build\" >nul 2>&1 && echo   ✓ main.py
copy "db_optimized.py" "installer_build\" >nul 2>&1 && echo   ✓ db_optimized.py
copy "user_data_sync.py" "installer_build\" >nul 2>&1 && echo   ✓ user_data_sync.py
copy "SETUP_USER.py" "installer_build\" >nul 2>&1 && echo   ✓ SETUP_USER.py
copy "SETUP_SERVER_CLIENT.py" "installer_build\" >nul 2>&1 && echo   ✓ SETUP_SERVER_CLIENT.py
copy "ADD_USER_TO_SERVER.py" "installer_build\" >nul 2>&1 && echo   ✓ ADD_USER_TO_SERVER.py
copy "config.ini" "installer_build\config.ini.template" >nul 2>&1 && echo   ✓ config.ini
copy "booking_icon.ico" "installer_build\" >nul 2>&1 && echo   ✓ booking_icon.ico
copy "tasma_logo.webp" "installer_build\" >nul 2>&1 && echo   ✓ tasma_logo.webp
copy "requirements.txt" "installer_build\" >nul 2>&1 && echo   ✓ requirements.txt
copy "LICENSE.txt" "installer_build\" >nul 2>&1 && echo   ✓ LICENSE.txt
copy "test_network_db.py" "installer_build\" >nul 2>&1 && echo   ✓ test_network_db.py
copy "CLIENT_QUICK_SETUP.txt" "installer_build\" >nul 2>&1 && echo   ✓ CLIENT_QUICK_SETUP.txt
copy "QUICK_SETUP_CARD.txt" "installer_build\" >nul 2>&1 && echo   ✓ QUICK_SETUP_CARD.txt

REM Build executable
echo [6/6] Building standalone executable...
echo   This may take 2-3 minutes...

cd installer_build

pyinstaller ^
    --onefile ^
    --windowed ^
    --icon="booking_icon.ico" ^
    --name="TASMA" ^
    --add-data="booking_icon.ico;." ^
    --add-data="config.ini.template;." ^
    --distpath="dist" ^
    --console ^
    main.py

if errorlevel 1 (
    cd ..
    echo ERROR: Failed to build executable
    echo Please check the error messages above
    pause
    exit /b 1
)

cd ..

REM Copy additional files to dist
echo   Copying additional modules...
copy "db_optimized.py" "installer_build\dist\" >nul 2>&1
copy "user_data_sync.py" "installer_build\dist\" >nul 2>&1
copy "SETUP_USER.py" "installer_build\dist\" >nul 2>&1
copy "SETUP_SERVER_CLIENT.py" "installer_build\dist\" >nul 2>&1
copy "installer_build\config.ini.template" "installer_build\dist\" >nul 2>&1
copy "installer_build\tasma_logo.webp" "installer_build\dist\" >nul 2>&1
copy "test_network_db.py" "installer_build\dist\" >nul 2>&1
copy "LICENSE.txt" "installer_build\dist\" >nul 2>&1
copy "CLIENT_QUICK_SETUP.txt" "installer_build\dist\" >nul 2>&1
copy "ADD_USER_TO_SERVER.py" "installer_build\dist\" >nul 2>&1
copy "QUICK_SETUP_CARD.txt" "installer_build\dist\" >nul 2>&1

REM Update version in ISS file
echo Updating installer version...
powershell -Command "(Get-Content TASMA_User_Installer.iss) -replace 'AppVersion=.*', 'AppVersion=2.2' | Set-Content TASMA_User_Installer.iss"
powershell -Command "(Get-Content TASMA_User_Installer.iss) -replace 'OutputBaseFilename=.*', 'OutputBaseFilename=TASMA_User_Setup_v2.2' | Set-Content TASMA_User_Installer.iss"

echo.
echo =====================================================
echo BUILD COMPLETE
echo =====================================================
echo.
echo Successfully built: TASMA v2.2
echo Output location: installer_build\dist\
echo.
echo Next Steps:
echo   1. Open: TASMA_User_Installer.iss in Inno Setup
echo   2. Click: Build ^> Compile
echo   3. Installer will be created in: setup_output\
echo      Final file: setup_output\TASMA_User_Setup_v2.2.exe
echo.
echo Included files:
echo   - TASMA.exe (application)
echo   - db_optimized.py (server connection)
echo   - user_data_sync.py (user data sync)
echo   - SETUP_USER.py (configuration wizard)
echo   - test_network_db.py (connection testing)
echo   - config.ini.template (configuration template)
echo.
pause
