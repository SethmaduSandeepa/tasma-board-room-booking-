@echo off
REM REBUILD_AND_COMPILE.bat
REM Rebuilds installers AND automatically compiles with Inno Setup
REM Requires: Inno Setup to be installed

setlocal enabledelayedexpansion

echo.
echo =====================================================
echo TASMA Installer - Full Build and Compile
echo =====================================================
echo.

REM Run the rebuild script
echo Step 1: Building executable bundle...
call REBUILD_INSTALLERS.bat
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

REM Check if Inno Setup is installed
echo.
echo Step 2: Checking Inno Setup installation...

set "INNO_SETUP_PATH=C:\Program Files (x86)\Inno Setup 6"
if not exist "%INNO_SETUP_PATH%\ISCC.exe" (
    echo WARNING: Inno Setup not found at default location
    echo Searching for Inno Setup...
    
    REM Try to find Inno Setup
    for /d %%D in (C:\Program Files*\Inno Setup*) do (
        if exist "%%D\ISCC.exe" (
            set "INNO_SETUP_PATH=%%D"
        )
    )
)

if not exist "%INNO_SETUP_PATH%\ISCC.exe" (
    echo ERROR: Inno Setup not found
    echo Please install Inno Setup from: https://jrsoftware.org/isinfo.php
    echo Then run this script again
    pause
    exit /b 1
)

echo Found Inno Setup at: %INNO_SETUP_PATH%

REM Compile the installer
echo.
echo Step 3: Compiling installer with Inno Setup...
echo This may take 1-2 minutes...

"%INNO_SETUP_PATH%\ISCC.exe" /O"setup_output" TASMA_User_Installer.iss

if errorlevel 1 (
    echo ERROR: Inno Setup compilation failed
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo =====================================================
echo SUCCESS!
echo =====================================================
echo.
echo New installer created: setup_output\TASMA_User_Setup_v2.2.exe
echo File size: See details below
echo.

REM Show final file info
if exist "setup_output\TASMA_User_Setup_v2.2.exe" (
    for %%F in (setup_output\TASMA_User_Setup_v2.2.exe) do (
        echo File: %%~nxF
        echo Size: %%~zF bytes
        echo Modified: %%~tF
    )
    echo.
    echo Ready to distribute to users!
    echo.
) else (
    echo ERROR: Installer file not created
    pause
    exit /b 1
)

pause
