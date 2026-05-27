# TASMA Setup Files - Quick Guide

## Two Setup Scripts

I've created **two separate setup scripts** to make deployment simple and clear.

---

## 1. SETUP_SERVER.py - For the Server Administrator

**When to run:** Once on the server machine

**What it does:**
- Creates shared folder: `C:\TASMA_Data`
- Creates/validates the centralized database
- Generates configuration for network sharing
- Tests database connectivity
- Provides UNC path for clients

**Who runs it:**
- IT Administrator or Server Manager
- **Must have Administrator privileges**
- Runs on the SERVER machine only

**How to run:**
```bash
# On the server, open Command Prompt as Administrator
python SETUP_SERVER.py
```

**What you'll get:**
- Network share path: `\\SERVER_NAME\TASMA_Data\bookings.db`
- Ready-to-use centralized database
- Configuration file

---

## 2. SETUP_USER.py - For Each User

**When to run:** On each user's workstation after TASMA is installed

**What it does:**
- Verifies TASMA is installed
- Asks for server connection details
- Tests connection to shared database
- Configures local settings
- Creates desktop shortcut
- Optionally launches the app

**Who runs it:**
- Each end user
- Regular user account (no admin needed)
- Runs on CLIENT machines

**How to run:**
```bash
# On each user's computer
python SETUP_USER.py

# Follow the prompts to enter server information
```

**What the user enters:**
- Server name (e.g., `OFFICE-SERVER`) OR
- Server IP address (e.g., `192.168.1.100`) OR
- Local database path (single user only)

---

## Installation Workflow

### Phase 1: Server Setup (One-time, ~10 minutes)

```
1. Administrator gets TASMA files
2. Copies files to server
3. Runs: python SETUP_SERVER.py
4. Follows prompts to create shared folder
5. Notes the network path (e.g., \\OFFICE-SERVER\TASMA_Data)
6. Provides path to IT support / users
```

### Phase 2: User Setup (Per user, ~5 minutes)

```
1. User installs TASMA on their workstation
2. User runs: python SETUP_USER.py
3. User enters server name or IP
4. Script tests connection
5. Script creates config and desktop shortcut
6. User is ready to go!
```

---

## Comparison Table

| Aspect | SETUP_SERVER.py | SETUP_USER.py |
|--------|-----------------|---------------|
| **Run location** | Server machine | User workstation |
| **Admin required** | YES | NO |
| **Frequency** | Once | Per user |
| **Time** | ~10 min | ~5 min |
| **Creates** | Database, shares | Config, shortcut |
| **Tests** | Database file | Network connection |

---

## File Locations

After running the scripts, you'll have:

**On Server:**
```
C:\TASMA_Data\
├── bookings.db          (shared database)
├── config.ini           (server config)
└── backups\             (backup folder)
```

**On Each User's Machine:**
```
[Installation Folder]\
├── main.py
├── config.ini           (updated with server path)
└── TASMA.lnk            (desktop shortcut)
```

---

## Troubleshooting

### Server Setup Issues

**Problem:** "Must run as Administrator"
- **Solution:** Right-click Command Prompt → "Run as Administrator"

**Problem:** Folder sharing dialog doesn't appear
- **Solution:** Share folder manually using File Explorer (see script output for steps)

### User Setup Issues

**Problem:** "TASMA not found"
- **Solution:** Make sure TASMA is installed before running this script

**Problem:** "Cannot connect to database"
- **Solution:** 
  - Verify server is online
  - Check server name/IP is correct
  - Ensure network connection is working
  - Run `python test_network_db.py` for detailed diagnostics

**Problem:** "Permission denied"
- **Solution:** Check folder permissions on server (should be Read/Write for all users)

---

## Next Steps

### For Administrators

1. ✓ Run `SETUP_SERVER.py` on the server
2. ✓ Note the network path (e.g., `\\OFFICE-SERVER\TASMA_Data`)
3. ✓ Create a simple instruction document for users
4. ✓ Distribute SETUP_USER.py to users

### For End Users

1. Install TASMA (if not already installed)
2. Run `SETUP_USER.py`
3. Enter server name or IP when prompted
4. Test connection
5. Click TASMA on desktop to start using it

---

## Additional Tools

**Database Testing:**
```bash
python test_network_db.py
```
Run on any machine to verify database connectivity.

**Manual Configuration:**
```bash
python setup_database_config.py
```
GUI tool for advanced configuration changes.

---

## Support Checklist

- [ ] Server name/IP documented
- [ ] SETUP_SERVER.py run as Administrator
- [ ] Database created and shared
- [ ] Network path verified (can access from File Explorer)
- [ ] SETUP_USER.py distributed to users
- [ ] Each user has run SETUP_USER.py
- [ ] Connection tests passing
- [ ] Users can log in and see booking screen

---

**Status:** Ready for deployment
**Version:** 1.0
**Last Updated:** May 2026
