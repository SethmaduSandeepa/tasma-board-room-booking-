@echo off
REM TASMA Troubleshooting & Performance Optimization Tool
REM Run with Administrator privileges
REM Helps diagnose and fix performance issues

setlocal enabledelayedexpansion

:MENU
cls
echo.
echo ========================================
echo TASMA Troubleshooting & Optimization
echo ========================================
echo.
echo Select an option:
echo.
echo 1. Test Server Connectivity
echo 2. Optimize Network Settings (Windows)
echo 3. Check Database Performance
echo 4. View Recent Errors
echo 5. Configure Optimal Settings
echo 6. Create Diagnostic Report
echo 7. Reset Application Data
echo 8. Exit
echo.
set /p CHOICE="Enter your choice (1-8): "

if "!CHOICE!"=="1" goto TEST_CONNECTIVITY
if "!CHOICE!"=="2" goto OPTIMIZE_NETWORK
if "!CHOICE!"=="3" goto CHECK_DATABASE
if "!CHOICE!"=="4" goto VIEW_ERRORS
if "!CHOICE!"=="5" goto CONFIGURE_SETTINGS
if "!CHOICE!"=="6" goto DIAGNOSTIC_REPORT
if "!CHOICE!"=="7" goto RESET_DATA
if "!CHOICE!"=="8" goto EXIT_SCRIPT
goto MENU

:TEST_CONNECTIVITY
cls
echo.
echo Testing Server Connectivity...
echo.
set /p SERVER_NAME="Enter server name or IP address: "
if "!SERVER_NAME!"=="" goto MENU

echo.
echo 1. Pinging server...
ping !SERVER_NAME! -c 4
if errorlevel 1 (
    echo ERROR: Server is not reachable!
    pause
    goto MENU
)

echo.
echo 2. Testing share access...
dir "\\!SERVER_NAME!\TASMA_App" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Cannot access \\!SERVER_NAME!\TASMA_App
    echo Please verify:
    echo   - Share name is correct (default: TASMA_App)
    echo   - User has permissions
    echo   - Firewall allows SMB (port 445)
) else (
    echo SUCCESS: Share is accessible!
    echo.
    echo Files on server:
    dir "\\!SERVER_NAME!\TASMA_App"
)

echo.
echo 3. Testing database access...
dir "\\!SERVER_NAME!\TASMA_Data\bookings.db" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Cannot access database
) else (
    echo SUCCESS: Database is accessible!
    for /F %%A in ('dir "\\!SERVER_NAME!\TASMA_Data\bookings.db" ^| find "bookings.db"') do (
        echo File found: %%A
    )
)

echo.
echo 4. Measuring latency...
for /f "tokens=4" %%a in ('ping -n 1 !SERVER_NAME! ^| find "time="') do echo Response time: %%a

echo.
pause
goto MENU

:OPTIMIZE_NETWORK
cls
echo.
echo Optimizing Network Settings...
echo.
echo WARNING: This requires Administrator privileges
net session >nul 2>&1
if errorlevel 1 (
    echo ERROR: Please run as Administrator!
    pause
    goto MENU
)

echo.
echo Applying optimizations:
echo.

echo 1. Disabling TCP Auto-Tuning Level...
netsh int tcp set global autotuninglevel=normal
echo    ✓ Done

echo 2. Enabling TCP 1323 Options...
netsh int tcp set global tcp1323opts=enabled
echo    ✓ Done

echo 3. Enabling ECN...
netsh int tcp set global ecncapability=enabled
echo    ✓ Done

echo 4. Setting TCP Window Scaling...
netsh int tcp set global autotuninglevel=normal
echo    ✓ Done

echo.
echo 5. Checking SMB version...
Get-SmbConnection 2>nul
if errorlevel 1 (
    echo    (Windows 7/Server 2008 - SMB2)
) else (
    echo    (SMB3 available)
)

echo.
echo Optimization complete!
echo Your network performance should improve, especially on high-latency connections.
echo.
pause
goto MENU

:CHECK_DATABASE
cls
echo.
echo Checking Database Performance...
echo.
set /p SERVER_NAME="Enter server name or IP address: "
set /p DB_PATH="Enter database path (default bookings.db): "
if "!DB_PATH!"=="" set DB_PATH=bookings.db

set FULL_PATH="\\!SERVER_NAME!\TASMA_Data\!DB_PATH!"

if exist !FULL_PATH! (
    echo.
    echo Database Found: !FULL_PATH!
    echo.
    
    echo File Information:
    for /F "tokens=1,2,3,4,5" %%A in ('dir !FULL_PATH! ^| find "bookings"') do (
        echo   Date Modified: %%A %%B
        echo   Time: %%C
        echo   Size: %%D %%E
    )
    
    echo.
    echo Testing database access speed...
    REM Use Python if available to test SQLite
    python -c "import sqlite3, time; start=time.time(); conn=sqlite3.connect('!FULL_PATH!'); conn.execute('SELECT COUNT(*) FROM sqlite_master'); elapsed=time.time()-start; print('   Database access time: {:.3f} seconds'.format(elapsed))" 2>nul
    if errorlevel 1 (
        echo   (Install Python to enable SQLite testing)
    )
    
) else (
    echo ERROR: Database not found at !FULL_PATH!
)

echo.
pause
goto MENU

:VIEW_ERRORS
cls
echo.
echo Recent Errors and Logs...
echo.

if exist tasma_app.log (
    echo Showing last 30 lines from tasma_app.log:
    echo.
    powershell -Command "Get-Content tasma_app.log -Tail 30"
) else (
    echo No log file found. This is normal for first run.
    echo Log files appear at: tasma_app.log (in application directory)
)

echo.
echo To enable debug logging, edit config.ini:
echo   [LOGGING]
echo   debug_mode = true
echo.
pause
goto MENU

:CONFIGURE_SETTINGS
cls
echo.
echo Configuring Optimal Settings...
echo.
set /p SERVER_NAME="Enter server name: "

if exist config.ini (
    echo.
    echo Current config.ini:
    type config.ini
    echo.
)

set /p DB_TIMEOUT="Database timeout in seconds (default 60): "
if "!DB_TIMEOUT!"=="" set DB_TIMEOUT=60

set /p CACHE_TIMEOUT="Cache timeout in seconds (default 300): "
if "!CACHE_TIMEOUT!"=="" set CACHE_TIMEOUT=300

set /p POOL_SIZE="Connection pool size (default 10): "
if "!POOL_SIZE!"=="" set POOL_SIZE=10

echo.
echo Generating optimal config.ini...
echo.

(
    echo [SERVER]
    echo database_path = \\!SERVER_NAME!\TASMA_Data\bookings.db
    echo db_timeout = !DB_TIMEOUT!
    echo enable_cache = true
    echo cache_timeout = !CACHE_TIMEOUT!
    echo.
    echo [LOGGING]
    echo debug_mode = false
    echo log_file = tasma_app.log
    echo.
    echo [PERFORMANCE]
    echo connection_pool_size = !POOL_SIZE!
    echo batch_size = 100
) > config.ini.new

echo New config generated as config.ini.new
echo.
set /p CONFIRM="Apply these settings (Y/N)? "
if /i "!CONFIRM!"=="Y" (
    move /y config.ini.new config.ini >nul
    echo ✓ Settings applied!
) else (
    del config.ini.new
    echo Settings not applied.
)

echo.
pause
goto MENU

:DIAGNOSTIC_REPORT
cls
echo.
echo Creating Diagnostic Report...
echo.

set REPORT_FILE=TASMA_Diagnostic_%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%.txt

(
    echo ========================================
    echo TASMA Booking System - Diagnostic Report
    echo ========================================
    echo.
    echo Generated: %date% %time%
    echo Computer: %COMPUTERNAME%
    echo User: %USERNAME%
    echo.
    
    echo System Information:
    echo ----------------------------------------
    systeminfo | findstr /i "OS Version Processor Memory"
    
    echo.
    echo Network Configuration:
    echo ----------------------------------------
    ipconfig | findstr /i "IPv4 Gateway DNS"
    
    echo.
    echo Application Files:
    echo ----------------------------------------
    if exist "deployment\TASMA Board Room Booking System.exe" (
        echo ✓ Executable found
        for /F %%A in ('dir "deployment\TASMA Board Room Booking System.exe" ^| find "Board"') do echo   %%A
    ) else (
        echo ✗ Executable not found
    )
    
    if exist config.ini (
        echo ✓ Config file found
        type config.ini
    ) else (
        echo ✗ Config file not found
    )
    
    echo.
    echo Recent Logs:
    echo ----------------------------------------
    if exist tasma_app.log (
        powershell -Command "Get-Content tasma_app.log -Tail 20"
    ) else (
        echo No logs found
    )
    
    echo.
    echo Performance Metrics:
    echo ----------------------------------------
    for /F "tokens=2 delims=:" %%A in ('wmic OS get TotalVisibleMemorySize /value') do set TOTAL_MEM=%%A
    for /F "tokens=2 delims=:" %%A in ('wmic OS get FreePhysicalMemory /value') do set FREE_MEM=%%A
    echo Total Memory: !TOTAL_MEM! KB
    echo Free Memory: !FREE_MEM! KB
    
) > !REPORT_FILE!

echo Report saved to: !REPORT_FILE!
echo.
echo Contents:
type !REPORT_FILE!

echo.
pause
goto MENU

:RESET_DATA
cls
echo.
echo WARNING: Reset Application Data
echo.
echo This will:
echo  - Clear all cached data
echo  - Reset configuration to defaults
echo  - Remove temporary files
echo.
set /p CONFIRM="Continue (Y/N)? "
if /i not "!CONFIRM!"=="Y" goto MENU

echo.
echo Resetting...

if exist config.ini (
    del config.ini
    echo ✓ Removed config.ini
)

if exist tasma_app.log (
    del tasma_app.log
    echo ✓ Cleared log file
)

REM Clear AppData TASMA folder
if exist "%APPDATA%\TASMA" (
    rmdir /s /q "%APPDATA%\TASMA"
    echo ✓ Cleared local app data
)

echo.
echo Reset complete! 
echo Restart the application to initialize defaults.
echo.
pause
goto MENU

:EXIT_SCRIPT
echo.
echo Exiting...
exit /b 0
