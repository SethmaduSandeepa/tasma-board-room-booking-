# TASMA Multi-User Network Deployment - Quick Reference

## For System Administrators / IT Support

This is a quick reference for deploying TASMA to multiple users with a centralized database.

---

## Server Setup (5 minutes)

### 1. Create Shared Folder
```bash
# On server, create and share folder
mkdir C:\TASMA_Data

# Share with appropriate permissions (Right-click Properties → Sharing)
# Everyone: Read/Write
```

### 2. Set Up Database
```bash
# Copy your existing bookings.db or create new one
copy C:\backup\bookings.db C:\TASMA_Data\bookings.db
```

### 3. Verify Share
```bash
# From any client machine, test access:
# In Windows File Explorer: \\SERVER_NAME\TASMA_Data
# Should see bookings.db file
```

---

## Client Installation (Per User)

### Option A: Automated Setup
```bash
# After installing TASMA on client:
python setup_database_config.py

# Enter network path and click Save & Test
```

### Option B: Manual Configuration
Edit `config.ini` on each client:
```ini
[SERVER]
database_path = \\SERVER_NAME\TASMA_Data\bookings.db
db_timeout = 30
```

---

## Verification

### Quick Test
```bash
python test_network_db.py
```

Should output:
```
✓ Database file exists
✓ Valid network path format
✓ Database is readable
✓ Database is writable
✓ Network connectivity OK
✓ Configuration OK
```

---

## Configuration Presets

### For 2-5 Users
```ini
[SERVER]
database_path = \\SERVER_NAME\TASMA_Data\bookings.db
db_timeout = 30
connection_pool_size = 3
```

### For 5-20 Users
```ini
[SERVER]
database_path = \\SERVER_NAME\TASMA_Data\bookings.db
db_timeout = 45
connection_pool_size = 5
```

### For 20+ Users
```ini
[SERVER]
database_path = \\SERVER_NAME\TASMA_Data\bookings.db
db_timeout = 60
connection_pool_size = 10
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| "Cannot access network path" | Server offline / wrong path | `ping SERVER_NAME` / verify path |
| "Database locked" | Concurrent access | Increase `db_timeout` |
| "Connection timeout" | Slow network | Increase `db_timeout` to 60 |
| "Permission denied" | No access rights | Add user to shared folder permissions |

---

## Deployment Checklist

- [ ] Server folder created: `C:\TASMA_Data`
- [ ] Database in shared folder: `\\SERVER_NAME\TASMA_Data\bookings.db`
- [ ] Shared folder permissions set correctly
- [ ] Server name documented
- [ ] TASMA installed on each client
- [ ] `config.ini` updated on each client with server path
- [ ] `test_network_db.py` passed on each client
- [ ] Users can successfully login and book rooms

---

## Files Included

- **`db_optimized.py`** - Database module with connection pooling
- **`config.ini`** - Configuration (update `database_path` here)
- **`test_network_db.py`** - Run this to verify connection
- **`setup_database_config.py`** - GUI tool for easy configuration
- **`NETWORK_DATABASE_SETUP.md`** - Detailed setup guide

---

## Support Commands

```bash
# Test connection
python test_network_db.py

# Configure database
python setup_database_config.py

# View logs
type tasma_app.log

# Optimize database (admin)
python -c "import sqlite3; c=sqlite3.connect('\\\\SERVER\\TASMA_Data\\bookings.db'); c.execute('VACUUM'); c.execute('ANALYZE'); c.close(); print('Done')"
```

---

## Network Path Examples

```
\\office-server\TASMA_Data\bookings.db      (Server name)
\\192.168.1.100\TASMA_Data\bookings.db      (IP address)
\\domain.com\server\TASMA_Data\bookings.db  (Domain path)
E:\tasma_booking_syst\bookings.db           (Local path - for single user)
```

---

## Contact / Escalation

For issues that can't be resolved:
1. Run `test_network_db.py` and save output
2. Check `tasma_app.log` for errors
3. Verify network and server connectivity
4. Contact IT for network/permissions issues

---

**Last Updated**: May 2026
**Version**: 1.0
