# TASMA Booking System - Network Server Deployment Guide

## Quick Start

### On Server Machine:
1. Run: `deploy_server_complete.bat` (as Administrator)
2. Follow the prompts to set up shares

### On Each Client Machine:
1. Run: `setup_client_desktop.bat [SERVER_NAME]`
2. Click the desktop shortcut to launch

---

## Detailed Setup Instructions

### Phase 1: Server Configuration

#### 1.1 Prepare Server Machine
- **OS**: Windows Server 2012+ or Windows 7+
- **Administrator Access**: Required for initial setup
- **Disk Space**: ~200MB (100MB for app + 100MB for database)
- **Network**: Server must be accessible to client machines

#### 1.2 Run Server Setup Script
```batch
# On the server, run as Administrator:
deploy_server_complete.bat
```

This script will:
- Create application folder (default: `C:\SharedApps\TASMA`)
- Create database folder (default: `C:\SharedData\TASMA`)
- Copy application files to the shared folders
- Set up Windows network shares:
  - `\\SERVER_NAME\TASMA_App` (application)
  - `\\SERVER_NAME\TASMA_Data` (database)
- Update configuration with server paths

#### 1.3 Verify Server Setup
```batch
# Test from server machine:
dir \\LOCALHOST\TASMA_App
dir \\LOCALHOST\TASMA_Data
```

### Phase 2: Client Configuration

#### 2.1 Prepare Client Machines
- **OS**: Windows 7+ or Windows Server
- **Network Access**: Must be able to reach the server
- **Admin Access**: NOT required for shortcut creation

#### 2.2 Test Network Connection (from client)
```batch
# Test connectivity to server:
ping SERVER_NAME

# Test share access:
dir \\SERVER_NAME\TASMA_App
dir \\SERVER_NAME\TASMA_Data
```

Replace `SERVER_NAME` with your server's hostname or IP address.

#### 2.3 Create Desktop Shortcut
```batch
# On each client machine, run:
setup_client_desktop.bat SERVER_NAME
```

Or without parameters (will prompt):
```batch
setup_client_desktop.bat
```

#### 2.4 Verify Client Setup
- Look for "TASMA Board Room Booking System" shortcut on desktop
- Double-click to launch
- Login window should appear within 2-3 seconds

---

## Network Architecture

```
┌─────────────────────────────────────┐
│      SERVER MACHINE                 │
├─────────────────────────────────────┤
│ C:\SharedApps\TASMA\                │
│   ├─ TASMA Board Room Booking..exe  │
│   ├─ tasma_logo.webp                │
│   ├─ booking_icon.ico               │
│   └─ config.ini                     │
│                                     │
│ C:\SharedData\TASMA\                │
│   └─ bookings.db                    │
└──────────────────────────────────────┘
         ↑                     ↑
    TASMA_App share      TASMA_Data share
         ↑                     ↑
    ┌────┴─────────────────────┴────┐
    │                               │
    ↓                               ↓
┌─────────────────┐         ┌──────────────────┐
│ CLIENT 1 DESK   │         │ CLIENT 2 DESK    │
│ (shortcut.lnk)  │         │ (shortcut.lnk)   │
└──────┬──────────┘         └────────┬─────────┘
       │                            │
       └────────────┬───────────────┘
                    │
           RUNS FROM SHORTCUT
           (exe on TASMA_App share)
           (connects to DB on TASMA_Data share)
```

---

## Configuration

### Server-Side Config
File: `C:\SharedApps\TASMA\config.ini`

```ini
[SERVER]
database_path = \\SERVER_NAME\TASMA_Data\bookings.db
db_timeout = 30
enable_cache = true
cache_timeout = 300
lazy_load_ui = true
preload_assets = false

[LOGGING]
debug_mode = false
log_file = tasma_app.log

[PERFORMANCE]
connection_pool_size = 2
batch_size = 100
```

**Key Settings for Network:**
- `database_path`: UNC path to shared database
- `db_timeout`: 30s (increased from 60s for local, reduced for network)
- `connection_pool_size`: 2 (reduced from 5 to minimize network overhead)
- `lazy_load_ui`: true (app launches instantly without database connection)

---

## Troubleshooting

### Problem: "Cannot access \\SERVER_NAME\TASMA_App"

**Solution:**
```batch
# Test network connectivity:
ping SERVER_NAME

# If ping works but share doesn't, check:
# 1. Share exists
net share

# 2. Firewall allows SMB (port 445)
# 3. User has share permissions
```

### Problem: Application Opens Slowly

**Checks:**
1. First launch is slower (database initialization)
2. Subsequent launches should be 2-3 seconds
3. If consistently slow:
   - Check network latency: `ping -t SERVER_NAME`
   - Monitor disk I/O on server
   - Consider moving database closer to clients

### Problem: "Database is locked"

**Solution:**
- Only one user can write to database at a time
- This is normal SQLite behavior
- App will retry automatically with 30-second timeout
- If persistent:
  1. Check if another user is accessing the database
  2. Restart the application
  3. Consider upgrading to client-server database (e.g., SQL Server)

### Problem: Shortcut Not Working

**Solution:**
```batch
# Verify the shortcut points to:
# Target: \\SERVER_NAME\TASMA_App\TASMA Board Room Booking System.exe
# Start in: \\SERVER_NAME\TASMA_App

# Recreate shortcut:
setup_client_desktop.bat SERVER_NAME
```

---

## Performance Optimization

### For LAN (Local Area Network):
- Expected launch time: 2-3 seconds
- Performance: Near-local speed

### For WAN (Wide Area Network):
- Use VPN for secure connection
- Consider caching booking data locally
- Increase timeouts in config.ini:
  ```ini
  db_timeout = 60
  ```

### Database Performance:
- For 100+ concurrent users, consider SQL Server or PostgreSQL
- Current SQLite solution supports up to ~20 concurrent connections
- Monitor server disk usage (especially if bookings.db grows large)

---

## Maintenance

### Regular Backups
```batch
# Backup database weekly:
copy \\SERVER_NAME\TASMA_Data\bookings.db C:\Backups\bookings_backup_%DATE%.db
```

### Database Optimization
```batch
# Run maintenance on database:
python verify_database.py
```

### Share Permissions
```batch
# Review current shares:
net share

# Modify share permissions (Admin):
net share TASMA_App /grant:DOMAIN\GROUP,FULL
```

---

## Security Considerations

### Current Configuration:
- Everyone has FULL access (for testing)
- Database is shared without encryption
- Passwords are hashed (SHA256)

### For Production:
1. Restrict share access to specific user groups:
   ```batch
   net share TASMA_App /grant:DOMAIN\Finance,FULL
   net share TASMA_Data /grant:DOMAIN\Finance,FULL
   ```

2. Enable network encryption:
   - Use VPN between clients and server
   - Or use Windows Credential Guard

3. Database security:
   - Regular backups to secure location
   - Consider full disk encryption on server
   - Implement SQL Server with encryption

---

## Deployment Checklist

### Server Setup:
- [ ] Administrator access obtained
- [ ] Disk space verified (200MB available)
- [ ] Network connectivity tested
- [ ] `deploy_server_complete.bat` executed
- [ ] Shares created and visible
- [ ] Database file copied to shared location
- [ ] Config.ini updated with server paths

### Client Setup (per user):
- [ ] Network connectivity to server verified
- [ ] `setup_client_desktop.bat SERVER_NAME` executed
- [ ] Desktop shortcut created
- [ ] Application launches successfully
- [ ] Can login and access booking system

### Post-Deployment:
- [ ] First user can launch and login
- [ ] Multiple concurrent users can access
- [ ] Database backups scheduled
- [ ] Users trained on system usage
- [ ] Support contact information provided

---

## Support & Troubleshooting

### Logs:
- Client logs: `%APPDATA%\TASMA\tasma_app.log`
- Server logs: `C:\SharedApps\TASMA\tasma_app.log`

### Common Commands:
```batch
# Test server connection:
ping SERVER_NAME
dir \\SERVER_NAME\TASMA_App

# Check available shares:
net share

# Remove a share:
net share SHARE_NAME /delete

# View share permissions:
net share SHARE_NAME
```

---

## Support Contact

For issues or questions:
1. Check the logs for error messages
2. Verify network connectivity
3. Review troubleshooting section above
4. Contact system administrator
