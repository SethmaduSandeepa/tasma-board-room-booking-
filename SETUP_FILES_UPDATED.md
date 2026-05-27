# Setup Files - Updated Guide

## What Was Updated

I've updated the setup files to include all the latest features from May 24, 2026.

---

## SETUP_SERVER.py (Updated)

**New features:**
- ✓ Creates all 5 user data sync tables
- ✓ Initializes user_preferences table
- ✓ Initializes user_activity_log table
- ✓ Enhanced database schema
- ✓ Better validation

**Tables created:**
1. `users` - User accounts
2. `user_preferences` - User settings
3. `bookings` - Room bookings
4. `rooms` - Room information
5. `user_activity_log` - Activity audit trail

**Run by:** Administrator on server (one-time)

```bash
python SETUP_SERVER.py
```

---

## SETUP_USER.py (Updated)

**New features:**
- ✓ Enhanced connection testing with diagnostics
- ✓ Network path validation
- ✓ Better error messages
- ✓ Table verification
- ✓ Improved troubleshooting info

**User flow:**
1. Verify TASMA installed
2. Enter server name/IP
3. Test connection (with detailed diagnostics)
4. Create config.ini
5. Create desktop shortcut
6. Launch TASMA

**Run by:** Each user on their workstation

```bash
python SETUP_USER.py
```

---

## What Changed

### Server Setup
```
Before: Basic 3 tables (users, bookings, rooms)
After:  All 5 tables including user_preferences and activity_log
```

### User Setup
```
Before: Simple connection test
After:  Detailed diagnostics, table verification, network path validation
```

---

## Configuration Files

Both setup scripts now use:
- `config.ini` - Database and performance settings
- `user_data_sync.py` - User synchronization
- `db_optimized.py` - Database connection pooling
- `test_network_db.py` - Diagnostics (available for users)

---

## Installation Workflow (Updated)

### Phase 1: Server Setup (5-10 minutes)
```
1. Administrator runs: python SETUP_SERVER.py
2. Creates C:\TASMA_Data folder
3. Creates database with 5 tables
4. Sets up network sharing
5. Documents UNC path
```

### Phase 2: User Setup (5 minutes each)
```
1. User installs TASMA application
2. User runs: python SETUP_USER.py
3. Enters: server name or IP
4. Script tests connection thoroughly
5. Creates config and desktop shortcut
6. Ready to use!
```

---

## New Capabilities

Users now get:
- ✓ Multi-user data sync
- ✓ Shared bookings
- ✓ User preferences on server
- ✓ Activity logging
- ✓ Multi-device support

---

## Usage Instructions

### For Administrators
```bash
# 1. On server machine
# 2. Run as Administrator:
python SETUP_SERVER.py

# 3. Share the database folder
# 4. Note the UNC path: \\SERVER_NAME\TASMA_Data
```

### For End Users
```bash
# 1. Install TASMA application
# 2. Run:
python SETUP_USER.py

# 3. Enter server details when prompted
# 4. Click TASMA to launch
```

---

## Configuration (config.ini)

Auto-created by setup scripts:

```ini
[SERVER]
database_path = \\SERVER_NAME\TASMA_Data\bookings.db
db_timeout = 30
enable_cache = true
connection_pool_size = 5

[USER]
last_user = [current_username]
auto_login = false
```

---

## Error Handling (Improved)

If connection fails, users now see:

```
✗ Cannot connect to database
  Error: [specific error message]

Possible issues:
  1. Server name/IP is incorrect
  2. Server is offline or not accessible
  3. Permission denied to shared folder
  4. Network path not configured correctly

Please contact your IT administrator.
```

---

## Table Details

### users
```sql
user_id (PK), username, password, full_name, email, department,
role (user/admin/manager), phone, is_active, last_login,
created_date, updated_date
```

### user_preferences
```sql
preference_id (PK), user_id (FK), theme (light/dark),
auto_refresh, notifications_enabled, settings_json, updated_date
```

### bookings
```sql
booking_id (PK), room_id, user_id (FK), booking_date,
start_time, end_time, title, description, status,
created_date, updated_date, created_by (FK)
```

### rooms
```sql
room_id (PK), room_name, capacity, location, amenities, is_active
```

### user_activity_log
```sql
activity_id (PK), user_id (FK), action, details,
ip_address, timestamp
```

---

## Next Steps

1. **Rebuild installers** with updated setup scripts
   ```bash
   REBUILD_AND_COMPILE.bat
   ```

2. **Distribute new installer** to users
   ```
   setup_output\TASMA_User_Setup_v2.2.exe
   ```

3. **On server:** Run `python SETUP_SERVER.py` (if not done)

4. **On each client:** Users run installer or `python SETUP_USER.py`

---

## Troubleshooting

### "Setup script not found"
- Ensure you're in the project folder
- Check file spelling: `SETUP_SERVER.py` or `SETUP_USER.py`

### "Python not installed"
- Install Python 3.8+
- Add to PATH
- Try again

### "Permission denied" (server)
- Run Command Prompt as Administrator
- Then run the setup script

### "Database connection failed" (user)
- Check server is online
- Verify server name/IP is correct
- Check network connectivity
- Contact IT administrator

---

## Files Summary

| File | Purpose | When |
|------|---------|------|
| `SETUP_SERVER.py` | Server initialization | Once on server |
| `SETUP_USER.py` | User configuration | Per user on client |
| `REBUILD_AND_COMPILE.bat` | Rebuild installer | When needed |
| `config.ini` | Configuration template | Reference |

---

## Version Information

- **SETUP_SERVER.py** - v2.2 (Updated 5/24/2026)
- **SETUP_USER.py** - v2.2 (Updated 5/24/2026)
- **Database schema** - 5 tables (full user data sync)
- **Status** - Production ready

---

**Ready to use!** Both setup files are updated with full user data sync support. 🎉
