# TASMA Client-Server Connection Setup Guide

## Problem
- User computer: Shows "Invalid username or password, or account not approved yet"
- Server computer: Shows "Welcome sandeepa!" (user exists on server)

**Root Cause**: Client computer is using local database, not server database

## Solution

### Step 1: Run Setup Script on CLIENT Computer
After installing TASMA on the user computer:

1. **Locate the setup script:**
   - Installation folder: `C:\Program Files\TASMA\SETUP_SERVER_CLIENT.py`

2. **Run the setup script:**
   - Double-click: `SETUP_SERVER_CLIENT.py`
   - OR run from Command Prompt: `python SETUP_SERVER_CLIENT.py`

3. **What the script does:**
   - ✓ Tests network connection to GVBSERVER
   - ✓ Verifies database file is accessible
   - ✓ Tests database connection
   - ✓ Creates `config.ini` with server database path
   - ✓ Displays configuration summary

### Step 2: Expected Output

```
======================================================================
TASMA - Client Server Connection Setup
======================================================================

SERVER DATABASE CONFIGURATION
----------------------------------------------------------------------
Server Name:    GVBSERVER
Database Path:  \\GVBSERVER\C$\Users\Administrator\AppData\Roaming\TASMA\bookings.db
Client Config:  C:\Users\[USERNAME]\AppData\Roaming\TASMA\config.ini

STEP 1: Testing network path accessibility...
----------------------------------------------------------------------
✓ Network path accessible: \\GVBSERVER\C$\Users\Administrator\AppData\Roaming\TASMA\bookings.db

STEP 2: Testing database connection...
----------------------------------------------------------------------
✓ Database connection successful
  Found 1 users in database

STEP 3: Creating client configuration...
----------------------------------------------------------------------
✓ Config file created: C:\Users\[USERNAME]\AppData\Roaming\TASMA\config.ini

======================================================================
✓ CLIENT SETUP COMPLETE
======================================================================

Your TASMA client is now configured to connect to:
  \\GVBSERVER\C$\Program Files\TASMA Board Room Booking System\bookings.db

NEXT STEPS:
1. Launch TASMA application
2. Login with your username and password
3. Your data will sync from the server database
```

### Step 3: Launch TASMA and Login

1. **Close any running TASMA instances**
2. **Launch TASMA** from Start Menu or Desktop shortcut
3. **Login** with your credentials:
   - Username: `sandeepa`
   - Password: (your password)
4. **You should now see**: "Welcome sandeepa!" ✓

## Troubleshooting

### If you see: "Network path NOT found"
```
✗ Network path NOT found: \\GVBSERVER\C$\Users\Administrator\AppData\Roaming\TASMA\bookings.db
```

**Fixes:**
1. Check network connection: `ping GVBSERVER`
2. Verify GVBSERVER is on and running
3. Verify database path exists on server:
   - `C:\Program Files\TASMA Board Room Booking System\bookings.db`
4. Check Windows firewall (might be blocking network access)
5. Ensure you have network permissions

### If you see: "Database connection failed"
```
✗ Database connection failed: [error message]
```

**Fixes:**
1. Wait a few seconds and try again
2. Verify database file is not corrupted on server
3. Ensure server TASMA is not running (conflicts can occur)
4. Check file permissions on server

### If TASMA still shows old error after setup
1. Delete the local database: `C:\Users\[USERNAME]\AppData\Roaming\TASMA\bookings.db`
2. Launch TASMA - it will recreate config from server

## Configuration Details

The setup script creates `config.ini` with:
```ini
[Database]
database_path = \\GVBSERVER\C$\Users\Administrator\AppData\Roaming\TASMA\bookings.db
db_timeout = 30
connection_pool_size = 3
enable_cache = true
cache_ttl = 300

[Network]
server_name = GVBSERVER
is_client = true
retry_attempts = 3
retry_delay = 1

[User]
theme = light
auto_login = false
notifications = true
```

## What Happens Next

Once configured:
1. **Application launches** → Connects to server database
2. **User logins** → Authenticates against server users table
3. **Data syncs** → All bookings stored on server database
4. **Multi-device support** → Same user can login from different computers
5. **Real-time updates** → Bookings visible across all clients connected to server

## Questions or Issues?

If setup script fails:
1. Check network connectivity
2. Verify server database path and permissions
3. Run setup script again
4. Contact system administrator

---

**Version**: 2.2
**Last Updated**: 2026-05-25
