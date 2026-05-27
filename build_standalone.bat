@echo off
REM TASMA Booking System - Build Standalone Executable
REM This script creates a professional standalone .exe file

echo.
echo ===================================================
echo   TASMA Board Room Booking System - Build Script
echo ===================================================
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Building standalone executable...
echo.

REM Clean old build artifacts
if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1

REM Get the current directory as absolute path
for /f "delims=" %%A in ('cd') do set PROJ_DIR=%%A

REM Build the executable with server deployment optimization using absolute paths
pyinstaller --onefile ^
    --windowed ^
    --name "TASMA Board Room Booking System" ^
    --icon=%PROJ_DIR%\booking_icon.ico ^
    --add-data "%PROJ_DIR%\tasma_logo.webp;." ^
    --add-data "%PROJ_DIR%\booking_icon.ico;." ^
    --add-data "%PROJ_DIR%\bookings.db;." ^
    --add-data "%PROJ_DIR%\config.ini;." ^
    --add-data "%PROJ_DIR%\db_optimized.py;." ^
    --distpath "%PROJ_DIR%\dist" ^
    --workpath "%PROJ_DIR%\build" ^
    --specpath "%PROJ_DIR%" ^
    --clean ^
    %PROJ_DIR%\main.py

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo ===================================================
echo   Build Successful!
echo ===================================================
echo.
echo Executable location: dist\TASMA Board Room Booking System.exe
echo.
echo You can now:
echo 1. Run the executable directly
echo 2. Create an installer using the exe
echo 3. Copy to other computers
echo.
pause
