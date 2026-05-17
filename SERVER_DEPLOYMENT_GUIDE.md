# TASMA Booking System - Server Deployment Guide

## Overview
This guide explains how to deploy TASMA on a server so multiple users can access it via shortcuts, with optimized performance for concurrent access.

## System Requirements
- **Server OS**: Windows Server 2016+ or Windows 7+
- **Client OS**: Windows 7+
- **Network**: Both server and clients must be on the same network
- **Storage**: ~50MB disk space on server
- **Permissions**: Administrator access for initial setup

## Server-Side Setup

### Step 1: Create Shared Folder on Server
```batch
# Create a folder for the application
mkdir C:\SharedApps\TASMA

# Create a folder for the database (separate from app)
mkdir C:\SharedData\TASMA
```

### Step 2: Copy Application Files
1. Copy the compiled executable and files to `C:\SharedApps\TASMA\`
   - TASMA Board Room Booking System.exe
   - tasma_logo.webp
   - booking_icon.ico

2. Copy database file to `C:\SharedData\TASMA\`
   - bookings.db

### Step 3: Share the Folders via Network

#### For Windows Server:
1. Right-click `C:\SharedApps\TASMA` → Properties → Sharing
2. Click "Advanced Sharing"
3. Check "Share this folder"
4. Set Share name: `TASMA_App`
5. Click "Permissions"
6. Add: Everyone - Full Control (for testing, restrict later)
7. Apply changes

8. Repeat for `C:\SharedData\TASMA` with Share name: `TASMA_Data`

#### For Windows Pro/Workstation (using net share command):
```batch
# Run as Administrator
net share TASMA_App=C:\SharedApps\TASMA /grant:Everyone,FULL
net share TASMA_Data=C:\SharedData\TASMA /grant:Everyone,FULL
```

### Step 4: Configure Database Path
Edit the config.ini file on the server with the network path:

```ini
[SERVER]
database_path = \\SERVER_NAME\TASMA_Data\bookings.db
db_timeout = 60
enable_cache = true
cache_timeout = 300

[PERFORMANCE]
connection_pool_size = 10
```

Replace `SERVER_NAME` with your actual server hostname or IP address.

### Step 5: Verify Network Access
Test from a client machine:
```batch
# Test network path accessibility
net use \\SERVER_NAME\TASMA_App
dir \\SERVER_NAME\TASMA_App
```

## Client-Side Setup

### Step 1: Create Desktop Shortcut
Run this PowerShell script on each client (or deploy via Group Policy):

```powershell
# Define paths - modify SERVER_NAME and share names as needed
$serverName = "SERVER_NAME"  # or IP address like 192.168.1.100
$appPath = "\\$serverName\TASMA_App"
$exePath = "$appPath\TASMA Board Room Booking System.exe"
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = "$desktopPath\TASMA Booking System.lnk"

# Create shortcut
$WshShell = New-Object -ComObject WScript.Shell
$shortcut = $WshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $exePath
$shortcut.WorkingDirectory = $appPath
$shortcut.IconLocation = "$appPath\booking_icon.ico"
$shortcut.Description = "TASMA Board Room Booking System"
$shortcut.Save()

Write-Host "Shortcut created at: $shortcutPath"
```

### Step 2: Alternative - Using Batch Script
Save this as `create_shortcut.bat` and run on each client:

```batch
@echo off
REM Configure these variables
set SERVER_NAME=SERVER_NAME
set SHORTCUT_NAME=TASMA Booking System

REM Create shortcut on Desktop
powershell -Command ^
  "$WshShell = New-Object -ComObject WScript.Shell; " ^
  "$shortcut = $WshShell.CreateShortcut($env:USERPROFILE + '\Desktop\' + '%SHORTCUT_NAME%.lnk'); " ^
  "$shortcut.TargetPath = '\\%SERVER_NAME%\TASMA_App\TASMA Board Room Booking System.exe'; " ^
  "$shortcut.WorkingDirectory = '\\%SERVER_NAME%\TASMA_App'; " ^
  "$shortcut.IconLocation = '\\%SERVER_NAME%\TASMA_App\booking_icon.ico'; " ^
  "$shortcut.Save(); " ^
  "Write-Host 'Shortcut created successfully'"
```

## Performance Optimization

### Issue: Slow Startup
**Cause**: Network latency + Python startup time

**Solutions Implemented**:
1. **Connection Pooling**: Pre-opens multiple database connections (db_optimized.py)
2. **In-Memory Caching**: Caches frequently accessed data
3. **Lazy Loading**: UI components load only when needed
4. **Batch Operations**: Reduces network round-trips

### Configuration Tuning
In `config.ini`, optimize for your network:

```ini
[SERVER]
# Increase timeout for slower networks (in seconds)
db_timeout = 120

# Reduce cache timeout for less frequent updates
cache_timeout = 600

[PERFORMANCE]
# Increase connection pool for more concurrent users
connection_pool_size = 20
```

### Network Optimization
- **UNC Path Format**: Use IP address for faster lookup
  ```
  \\192.168.1.100\TASMA_App  (faster)
  \\SERVER_NAME\TASMA_App    (slower, requires DNS lookup)
  ```

- **Local Caching**: Each client can cache frequently accessed data locally

### Client Machine Optimization
1. **Disable Network Auto-Tune**:
   ```batch
   netsh int tcp set global autotuninglevel=disabled
   ```

2. **Optimize Network Settings**:
   ```batch
   netsh int tcp set global tcp1323opts=enabled
   ```

3. **Use SMB3**:
   - Ensure both server and clients support SMB3 (Windows 8+)
   - Much faster than SMB2

## Database Management

### Backup Strategy
Schedule daily backups of the database:

```batch
REM Backup to local folder with timestamp
FOR /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
copy "\\SERVER_NAME\TASMA_Data\bookings.db" "C:\Backups\bookings_%%mydate%%.db"
```

### Database Maintenance
Periodically vacuum and optimize database:
```batch
# Run via scheduled task
sqlite3 "\\SERVER_NAME\TASMA_Data\bookings.db" "VACUUM;"
```

## Troubleshooting

### Problem: "Database is locked" errors
**Solution**:
- Reduce number of concurrent users
- Increase `db_timeout` in config.ini
- Check if backup process is running
- Ensure database file is not being scanned by antivirus

### Problem: Slow startup (> 10 seconds)
**Solution**:
- Check network connectivity: `ping SERVER_NAME`
- Verify SMB version: `Get-SmbConnection` (PowerShell)
- Move to UNC IP address instead of hostname
- Increase cache timeout in config.ini
- Check client machine resources

### Problem: "Access Denied"
**Solution**:
- Verify folder sharing permissions
- Check user credentials: `net use \\SERVER_NAME\TASMA_App /delete`
- Re-authenticate: `net use \\SERVER_NAME\TASMA_App password /user:DOMAIN\username`

### Problem: Application crashes on startup
**Solution**:
- Check event logs for errors
- Run: `tracert SERVER_NAME` to verify network path
- Verify all required files are on server
- Check antivirus/firewall blocking network access

## Advanced: Group Policy Deployment

For domain-joined machines, automate deployment:

1. Copy `deploy_shortcut.bat` to network share: `\\SERVER_NAME\NETLOGON\`
2. Create Group Policy Object (GPO):
   - Open `gpoedit.msc`
   - Create new GPO: "Deploy TASMA Shortcut"
   - Computer Configuration → Startup Scripts
   - Add script: `\\SERVER_NAME\NETLOGON\deploy_shortcut.bat`
3. Link GPO to organizational unit containing user machines

## Monitoring

Monitor database file size and access:
```batch
REM Check file size
dir "\\SERVER_NAME\TASMA_Data\bookings.db"

REM Monitor active connections
Get-NetTCPConnection | findstr ESTABLISHED | findstr 445
```

## Security Considerations

1. **Restrict Share Permissions**: 
   - Don't use "Everyone" - use specific groups
   - Use read-only for app folder
   - Read-write only for data folder

2. **Enable Audit Logging**:
   - Enable audit on shared folders
   - Monitor for unauthorized access

3. **Backup Encryption**:
   - Store backups on encrypted drive
   - Backup to secure off-site location

4. **Disable Guest Access**:
   ```batch
   net localgroup guests /delete
   ```

## Performance Benchmarks

Expected performance on standard network (100Mbps Ethernet):
- **First startup**: 3-5 seconds (downloading config, opening connection pool)
- **Subsequent startups**: 1-2 seconds (cached connections)
- **Database operations**: 100-500ms per operation (depending on complexity)
- **Concurrent users**: 10-20 users without significant slowdown

With 1Gbps network: Reduce above times by 50%
With 10Mbps network: Multiply above times by 2

---

## Quick Reference

| Task | Command/Path |
|------|--------------|
| Share app folder | `net share TASMA_App=C:\SharedApps\TASMA /grant:Everyone,FULL` |
| Share data folder | `net share TASMA_Data=C:\SharedData\TASMA /grant:Everyone,FULL` |
| Remove shares | `net share TASMA_App /delete` |
| Test access | `dir \\SERVER_NAME\TASMA_App` |
| View config | Edit `config.ini` in app directory |
| Backup database | `copy \\SERVER_NAME\TASMA_Data\bookings.db C:\Backups\bookings_backup.db` |

---

**Support**: Contact system administrator for network or permission issues.
**Last Updated**: May 2026
