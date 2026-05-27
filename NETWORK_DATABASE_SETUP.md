# TASMA Network Database Deployment Guide

## Overview
This guide explains how to set up TASMA for multiple users connecting to a centralized database on a server.

## Architecture

```
    Server Machine
    ├── Shared Folder: \\SERVER_NAME\TASMA_Data\
    │   └── bookings.db (Centralized Database)
    │
    Client Machine 1 (User A)
    ├── TASMA Application
    └── config.ini → points to \\SERVER_NAME\TASMA_Data\bookings.db
    
    Client Machine 2 (User B)
    ├── TASMA Application
    └── config.ini → points to \\SERVER_NAME\TASMA_Data\bookings.db
```

---

## Server Setup (One-time, as Administrator)

### Step 1: Create Shared Folder
1. On the server machine, create a folder: `C:\TASMA_Data`
2. Copy your `bookings.db` file to this folder
3. Right-click the folder → **Properties**
4. Go to **Sharing** tab → **Share this folder**
5. Click **Permissions** and set:
   - **Everyone**: Read/Write
   - Apply to this folder, subfolders, and files

### Step 2: Note Your Server Details
- **Server Name**: (e.g., `SERVER-PC` or `OFFICE-SERVER`)
- **Server IP Address**: (e.g., `192.168.1.100`)
- **Shared Path**: `\\SERVER_NAME\TASMA_Data` or `\\192.168.1.100\TASMA_Data`

Test the share is accessible:
```
On Windows, type in File Explorer: \\SERVER_NAME\TASMA_Data
You should see the bookings.db file
```

---

## Client Setup (Per User)

### Option 1: Automatic Setup (Recommended)

After installing TASMA on a client machine:

1. **Run the Configuration Tool**:
   ```
   python setup_database_config.py
   ```

2. **Configure Database Path**:
   - Click "Browse Network" to select the shared folder, OR
   - Manually enter: `\\SERVER_NAME\TASMA_Data\bookings.db`
   - Replace `SERVER_NAME` with your actual server name or IP

3. **Click "Save & Test Connection"**:
   - The tool will save your configuration
   - It will automatically test the connection
   - You should see a success message

### Option 2: Manual Configuration

Edit `config.ini` directly:

```ini
[SERVER]
# For network server deployment
database_path = \\SERVER_NAME\TASMA_Data\bookings.db
# For local development
# database_path = E:\tasma_booking_syst\bookings.db

# Connection timeout (increase for slow networks)
db_timeout = 30

# Cache settings
enable_cache = true
cache_timeout = 300

[PERFORMANCE]
# Connection pool (reduce for many concurrent users)
connection_pool_size = 5
batch_size = 100

[LOGGING]
debug_mode = false
log_file = tasma_app.log
```

---

## Testing & Troubleshooting

### Run Diagnostic Test
```bash
python test_network_db.py
```

This will check:
- ✓ Database file exists
- ✓ Network path format is valid
- ✓ Database is readable
- ✓ Database is writable
- ✓ Network connectivity to server
- ✓ Configuration settings

**Test Results** are saved to: `database_test_results.txt`

### Common Issues & Solutions

#### Issue 1: "Cannot access network path"
**Possible causes:**
- Server name/IP is incorrect
- Server is offline
- Network connectivity issue

**Solutions:**
1. Verify server is running: `ping SERVER_NAME` or `ping 192.168.1.100`
2. Test network share manually in File Explorer: `\\SERVER_NAME\TASMA_Data`
3. Check network permissions (credentials)

#### Issue 2: "Database is locked"
**Possible causes:**
- Multiple users accessing same database simultaneously
- Another user running a backup or maintenance

**Solutions:**
1. Wait a few seconds and retry
2. Increase `db_timeout` in config.ini (e.g., 60 seconds)
3. Reduce `connection_pool_size` to 2-3

#### Issue 3: "Connection timeout"
**Possible causes:**
- Slow network connection
- Server is far away on network
- Network congestion

**Solutions:**
1. Increase `db_timeout` in config.ini:
   ```ini
   db_timeout = 60  # 60 seconds instead of 30
   ```
2. Check network speed: `ping -t SERVER_NAME`
3. Consider moving database to faster server

#### Issue 4: "Permission denied"
**Possible causes:**
- User doesn't have Read/Write access to shared folder
- Server permissions not configured correctly

**Solutions:**
1. Ask your IT administrator to grant access
2. Verify shared folder permissions:
   - Right-click folder → Properties → Sharing → Permissions
   - Ensure your user has Read/Write access

---

## Performance Optimization

### For Small Teams (2-5 users)
```ini
[SERVER]
db_timeout = 30
enable_cache = true

[PERFORMANCE]
connection_pool_size = 3
```

### For Medium Teams (5-20 users)
```ini
[SERVER]
db_timeout = 45
enable_cache = true
cache_timeout = 300

[PERFORMANCE]
connection_pool_size = 5
```

### For Large Teams (20+ users)
```ini
[SERVER]
db_timeout = 60
enable_cache = true
cache_timeout = 600

[PERFORMANCE]
connection_pool_size = 10
```

---

## Backup & Maintenance

### Regular Backups
Since `bookings.db` is on the server, back it up regularly:

```batch
REM Daily backup script
@echo off
set SOURCE=\\SERVER_NAME\TASMA_Data\bookings.db
set BACKUP_FOLDER=\\SERVER_NAME\TASMA_Backups

REM Create backup with timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)

copy "%SOURCE%" "%BACKUP_FOLDER%\bookings_%mydate%_%mytime%.db"
echo Backup completed
```

### Database Maintenance
Periodically optimize the database:

```python
import sqlite3

db_path = r'\\SERVER_NAME\TASMA_Data\bookings.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Optimize database
cursor.execute('VACUUM')
cursor.execute('ANALYZE')

conn.commit()
conn.close()

print("Database optimized")
```

---

## Uninstalling / Removing Server Configuration

If you want to revert to local database:

1. Edit `config.ini`:
   ```ini
   [SERVER]
   database_path = bookings.db
   ```

2. Copy `bookings.db` to your local application folder

3. Restart TASMA

---

## Network Path Examples

| Scenario | Path Format | Example |
|----------|------------|---------|
| Server Name | `\\SERVER_NAME\SHARE\bookings.db` | `\\office-server\TASMA_Data\bookings.db` |
| Server IP | `\\IP_ADDRESS\SHARE\bookings.db` | `\\192.168.1.100\TASMA_Data\bookings.db` |
| Domain User | Same with domain credentials in Windows | `\\DOMAIN\SERVER\SHARE\bookings.db` |
| Local Path | `D:\path\bookings.db` | `E:\tasma_booking_syst\bookings.db` |

---

## Technical Details

### Connection Pool
The app uses connection pooling for efficiency:
- Maintains N connections to database (default: 5)
- Reuses connections instead of creating new ones
- Improves performance for multiple concurrent operations

### Caching
When enabled, frequently read data is cached:
- Reduces database load
- Faster UI response
- Cache expires after `cache_timeout` seconds

### Isolation Level
Connections use `DEFERRED` isolation for:
- Better concurrency
- Reduced locking conflicts
- Appropriate for multi-user scenarios

---

## Support

If you encounter issues:

1. Run `test_network_db.py` for diagnostics
2. Check `tasma_app.log` for error messages
3. Review this guide's troubleshooting section
4. Contact your IT administrator for network issues

---

## Checklist

- [ ] Server folder created: `C:\TASMA_Data`
- [ ] Database copied to server: `\\SERVER_NAME\TASMA_Data\bookings.db`
- [ ] Shared folder permissions set (Read/Write)
- [ ] Server name/IP noted
- [ ] Client installed with TASMA
- [ ] Configuration tool run on client
- [ ] Connection test passed
- [ ] Users can log in and book rooms
- [ ] Backup strategy implemented

---

**Last Updated**: May 2026
