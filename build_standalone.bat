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

REM Build the executable with server deployment optimization
pyinstaller --onefile ^
    --windowed ^
    --name "TASMA Board Room Booking System" ^
    --icon=booking_icon.ico ^
    --add-data "tasma_logo.webp;." ^
    --add-data "booking_icon.ico;." ^
    --add-data "bookings.db;." ^
    --add-data "config.ini;." ^
    --distpath "./dist" ^
    --workpath "./build" ^
    --specpath "./build" ^
    main.py

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
