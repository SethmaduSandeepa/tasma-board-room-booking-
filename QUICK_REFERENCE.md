# TASMA Server Deployment - Quick Reference Card

## Installation Steps (5-10 Minutes)

### Step 1: Server Setup (Run as Administrator)
```batch
REM On server machine:
setup_server.bat

REM Enter:
# Application drive: C:
# Data drive: C:
# Server name: your-server-name
```

### Step 2: Client Setup (Run as Administrator on Each Client)
```batch
REM On each user's machine:
setup_client_shortcut.bat

REM Enter:
# Server name: your-server-name
# Share name: TASMA_App
```

### Step 3: Verify
```batch
REM Test from any client:
dir \\your-server-name\TASMA_App
dir \\your-server-name\TASMA_Data\bookings.db
```

**Done!** Users can now double-click the desktop shortcut.

---

## Folder Structure (After Setup)

```
SERVER COMPUTER:
C:\SharedApps\TASMA\
  ├── TASMA Board Room Booking System.exe
  ├── tasma_logo.webp
  ├── booking_icon.ico
  └── config.ini

C:\SharedData\TASMA\
  └── bookings.db

NETWORK SHARES:
  ✓ TASMA_App     → C:\SharedApps\TASMA
  ✓ TASMA_Data    → C:\SharedData\TASMA

CLIENT COMPUTER (Each User):
Desktop\
  └── TASMA Booking System.lnk  (Shortcut)
```

---

## Common Commands

```batch
REM Test network access:
ping SERVER_NAME
dir \\SERVER_NAME\TASMA_App

REM Test database:
dir \\SERVER_NAME\TASMA_Data\bookings.db

REM Check shares created:
net share

REM Remove share:
net share TASMA_App /delete

REM Reset and recreate shares:
net share TASMA_App /delete
net share TASMA_Data /delete
setup_server.bat
```

---

## Configuration Tuning (config.ini)

```ini
# For slow networks:
db_timeout = 120

# For many users:
connection_pool_size = 20

# For fast networks:
cache_timeout = 180
```

---

## Performance Expectations

| Scenario | Expected Time |
|----------|---------------|
| First launch | 3-5 seconds |
| Repeat launch | 1-2 seconds |
| Database operations | 100-500ms |
| Support up to | 10-20 users |

---

## Troubleshooting

**Problem: Application won't open**
- Solution: `troubleshoot_optimize.bat` → Option 1 (Test Connectivity)

**Problem: "Database is locked"**
- Solution: Increase `db_timeout` in config.ini to 120

**Problem: Slow startup**
- Solution: Use server IP instead of hostname in shortcut

**Problem: Access Denied**
- Solution: `setup_server.bat` to reset permissions

---

## For IT Administrators

### Automated Deployment (PowerShell)
```powershell
.\deploy_tasma_company_wide.ps1 -ServerName "MYSERVER" `
  -ComputerNames @("PC1", "PC2", "PC3")
```

### Diagnostic Report
```batch
troubleshoot_optimize.bat
# Select: Option 6 (Create Diagnostic Report)
```

### Performance Monitoring
```batch
# Check database file size:
dir \\SERVER_NAME\TASMA_Data\bookings.db

# Monitor connections:
Get-NetTCPConnection | findstr ESTABLISHED | findstr 445
```

---

## File Reference

| File | Purpose |
|------|---------|
| setup_server.bat | Run on server (creates shares) |
| setup_client_shortcut.bat | Run on each client (creates shortcut) |
| deploy_tasma_company_wide.ps1 | Automated deployment for IT |
| troubleshoot_optimize.bat | Diagnostics and troubleshooting |
| config.ini | Performance configuration |
| db_optimized.py | Performance optimization code |

---

## Documentation

- **DEPLOYMENT_IMPLEMENTATION_SUMMARY.md** ← Start here!
- **SERVER_DEPLOYMENT_README.md** ← Quick reference
- **SERVER_DEPLOYMENT_GUIDE.md** ← Complete technical guide

---

## Support Priority

1. Check: `troubleshoot_optimize.bat` Option 6 (diagnostic report)
2. Read: Relevant section in SERVER_DEPLOYMENT_GUIDE.md
3. Verify: Network connectivity and share access
4. Contact: IT support with diagnostic report

---

**Quick Support** 🆘

```batch
REM Three-step diagnosis:
1. ping SERVER_NAME
2. dir \\SERVER_NAME\TASMA_App
3. dir \\SERVER_NAME\TASMA_Data\bookings.db

REM If all pass: Network is good, check config.ini
REM If any fail: Network issue, use troubleshoot_optimize.bat
```

---

**Deployment Completed:** May 17, 2026
**Version:** 2.1 Professional
**Status:** Ready for Company-Wide Deployment ✓
