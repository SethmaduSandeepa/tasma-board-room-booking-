# TASMA Server Installation - Final Steps

## Status: ✅ Application Ready for Server Deployment

The application has been prepared and files have been copied to the local server locations:
- **Application Files**: `C:\SharedApps\TASMA\`
- **Database Location**: `C:\SharedData\TASMA\`

---

## Next Steps: Complete Server Setup (Admin Required)

### Step 1: Open PowerShell as Administrator

1. Press `Windows Key + R`
2. Type: `powershell`
3. Right-click and select "Run as Administrator"
4. Confirm when prompted

### Step 2: Create Network Shares

Run these commands in Administrator PowerShell:

```powershell
# Create SMB shares for network access
New-SmbShare -Name "TASMA_App" -Path "C:\SharedApps\TASMA" -FullAccess "Everyone" -Force -ErrorAction SilentlyContinue
New-SmbShare -Name "TASMA_Data" -Path "C:\SharedData\TASMA" -FullAccess "Everyone" -Force -ErrorAction SilentlyContinue

# Verify shares were created
Get-SmbShare | grep TASMA
```

**Expected Output:**
```
Name          Path
----          ----
TASMA_App     C:\SharedApps\TASMA
TASMA_Data    C:\SharedData\TASMA
```

### Step 3: Set Folder Permissions

```powershell
# Set NTFS permissions for proper access
icacls "C:\SharedApps\TASMA" /grant:r "Everyone:(OI)(CI)F" /t
icacls "C:\SharedData\TASMA" /grant:r "Everyone:(OI)(CI)F" /t
```

### Step 4: Verify Network Access

From any computer on your network:

```batch
REM Test share access
ping SERVER_NAME
dir \\SERVER_NAME\TASMA_App
dir \\SERVER_NAME\TASMA_Data
```

Replace `SERVER_NAME` with your server's hostname or IP address.

---

## Deploy Client Shortcuts

### For Individual Users:

Run this on each user's computer (as Administrator):

```batch
@echo off
setlocal enabledelayedexpansion

set SERVER_NAME=YOUR_SERVER_NAME_OR_IP
set SHORTCUT_NAME=TASMA Booking System

REM Create shortcut on Desktop
powershell -Command ^
  "$WshShell = New-Object -ComObject WScript.Shell; " ^
  "$shortcut = $WshShell.CreateShortcut($env:USERPROFILE + '\Desktop\%SHORTCUT_NAME%.lnk'); " ^
  "$shortcut.TargetPath = '\\!SERVER_NAME!\TASMA_App\TASMA Board Room Booking System.exe'; " ^
  "$shortcut.WorkingDirectory = '\\!SERVER_NAME!\TASMA_App'; " ^
  "$shortcut.IconLocation = '\\!SERVER_NAME!\TASMA_App\booking_icon.ico'; " ^
  "$shortcut.Save(); " ^
  "Write-Host 'Shortcut created on Desktop'"
```

Or use the provided script:
```batch
.\setup_client_shortcut.bat
```

### For Multiple Computers (Automated):

```powershell
.\deploy_tasma_company_wide.ps1 -ServerName "YOUR_SERVER_NAME" `
  -ComputerNames @("COMPUTER1", "COMPUTER2", "COMPUTER3")
```

---

## Optimization Integrated ✅

### What's Optimized:

1. **Connection Pooling** (db_optimized.py)
   - 5-10 pre-opened database connections
   - Reused across users
   - Eliminates "database locked" errors

2. **In-Memory Caching** (db_optimized.py)
   - Frequently accessed data cached in RAM
   - 5-minute cache timeout (configurable)
   - Reduces network round-trips

3. **Configuration-Based** (config.ini)
   ```ini
   [SERVER]
   database_path = \\SERVER_NAME\TASMA_Data\bookings.db
   db_timeout = 60
   enable_cache = true
   cache_timeout = 300

   [PERFORMANCE]
   connection_pool_size = 10
   ```

4. **Application Integration** (main.py)
   - Automatically imports and uses optimization module
   - Falls back to standard database if optimization unavailable
   - Zero code changes needed for users

---

## Expected Performance

After setup is complete:

| Scenario | Expected Time |
|----------|---------------|
| First launch | 3-5 seconds |
| Repeat launch | 1-2 seconds |
| Database query | 100-500ms |
| Concurrent users | 10-20+ supported |

---

## Verify Installation

### Test from Server:

```batch
REM Check application files
dir C:\SharedApps\TASMA\

REM Expected output:
REM  - TASMA Board Room Booking System.exe
REM  - tasma_logo.webp
REM  - booking_icon.ico
REM  - config.ini
REM  - db_optimized.py

REM Check database location
dir C:\SharedData\TASMA\

REM Expected output:
REM  - bookings.db
```

### Test from Client:

1. **Open File Explorer**
2. **Type in address bar**: `\\SERVER_NAME\TASMA_App`
3. **Verify files are accessible**
4. **Double-click executable** to test launch
5. **Expected**: Application opens in 3-5 seconds

---

## Troubleshooting

### Shares not appearing on clients:

```batch
REM Force network refresh on client
net use \\SERVER_NAME\TASMA_App /delete
net use \\SERVER_NAME\TASMA_App
```

### "Access Denied" error:

- Run share creation commands again as Administrator
- Verify firewall allows SMB (port 445)
- Check permissions:
  ```batch
  icacls C:\SharedApps\TASMA
  icacls C:\SharedData\TASMA
  ```

### Application won't open from network:

- Test directly:
  ```batch
  \\SERVER_NAME\TASMA_App\TASMA Board Room Booking System.exe
  ```
- Check AppData folder for logs:
  ```batch
  %APPDATA%\TASMA\tasma_app.log
  ```

### Slow startup:

1. Verify network latency:
   ```batch
   ping -l 1024 SERVER_NAME
   ```
   (Should be < 100ms)

2. Use IP address instead of hostname in shortcuts:
   ```
   \\192.168.1.100\TASMA_App
   ```

3. Increase cache timeout in config.ini:
   ```ini
   cache_timeout = 600
   ```

---

## Configuration Reference

### Server Tuning (config.ini)

**For Slow Networks:**
```ini
[SERVER]
db_timeout = 120
cache_timeout = 600

[PERFORMANCE]
connection_pool_size = 15
```

**For Many Users (20+):**
```ini
[PERFORMANCE]
connection_pool_size = 20
```

**For Fast Networks:**
```ini
[SERVER]
cache_timeout = 180
connection_pool_size = 5
```

---

## Maintenance Tasks

### Daily Backups:

```batch
REM Create scheduled backup (Windows Task Scheduler)
schtasks /create /tn "TASMA Backup" ^
  /tr "copy C:\SharedData\TASMA\bookings.db C:\Backups\bookings_backup.db" ^
  /sc daily /st 02:00
```

### Monitor Usage:

```batch
REM Check database file size
dir C:\SharedData\TASMA\bookings.db

REM Monitor active connections
Get-NetTCPConnection | findstr ESTABLISHED | findstr 445
```

---

## Documentation

For detailed information, see:
- **QUICK_REFERENCE.md** - One-page cheat sheet
- **SERVER_DEPLOYMENT_README.md** - Quick start guide
- **SERVER_DEPLOYMENT_GUIDE.md** - Complete technical reference
- **DEPLOYMENT_IMPLEMENTATION_SUMMARY.md** - Implementation details

---

## Summary

| Item | Status | Details |
|------|--------|---------|
| Application Integration | ✅ Complete | main.py updated with optimization module |
| Optimization Module | ✅ Ready | db_optimized.py with connection pooling |
| Server Setup | ⏳ Pending | Requires admin PowerShell commands |
| Network Shares | ⏳ Pending | Must run New-SmbShare commands |
| Client Deployment | ⏳ Ready | Scripts prepared for user distribution |

---

## Quick Command Reference

```powershell
# Run these AS ADMINISTRATOR on the server:

# Create shares
New-SmbShare -Name "TASMA_App" -Path "C:\SharedApps\TASMA" -FullAccess "Everyone" -Force
New-SmbShare -Name "TASMA_Data" -Path "C:\SharedData\TASMA" -FullAccess "Everyone" -Force

# Set permissions
icacls "C:\SharedApps\TASMA" /grant:r "Everyone:(OI)(CI)F" /t
icacls "C:\SharedData\TASMA" /grant:r "Everyone:(OI)(CI)F" /t

# Verify
Get-SmbShare | Select Name, Path
```

```batch
# On each client (as ADMINISTRATOR):
setup_client_shortcut.bat
```

---

**Status**: Ready for Final Deployment ✅
**Date**: May 17, 2026
**Version**: TASMA 2.1 Professional - Server Edition

Next: Run administrator PowerShell commands in "Step 2" above.
