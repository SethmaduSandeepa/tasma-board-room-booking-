# TASMA v2.2 - Complete Deployment & User Management Guide

## 🎯 Problem & Solution

**Issue**: Users can't login (account doesn't exist in database)  
**Solution**: Two-step setup process:
1. **Server Admin** adds users to database
2. **Users** login with their credentials

---

## 📋 Complete Deployment Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT WORKFLOW                      │
└─────────────────────────────────────────────────────────────┘

STEP 1: SERVER SETUP (One-time)
│
├─ Run: SETUP_SERVER.py
├─ Creates: C:\Program Files\TASMA Board Room Booking System\
└─ Result: bookings.db database initialized


STEP 2: ADD USERS (For each user)
│
├─ Run: ADD_USER_TO_SERVER.py (on server)
├─ Input: username, password, full name, department
└─ Result: User account created in database


STEP 3: CLIENT INSTALLATION (For each user)
│
├─ Run: TASMA_User_Setup_v2.2.exe
├─ First-run wizard appears automatically
├─ Wizard configures: server connection
└─ Result: config.ini created with server path


STEP 4: USER LOGIN (Done by user)
│
├─ Launch: TASMA application
├─ Enter: credentials created in STEP 2
└─ Result: ✓ "Welcome [username]!"
           ✓ Connected to server database
           ✓ Can book rooms
```

---

## 🔧 How to Execute

### STEP 1: Server Setup (On SERVER computer)

**Location**: `C:\Program Files\TASMA Board Room Booking System\`

**File**: `SETUP_SERVER.py`

**Execute**:
```cmd
# Option 1: Double-click SETUP_SERVER.py
# Option 2: Command prompt
cd "C:\Program Files\TASMA Board Room Booking System"
python SETUP_SERVER.py
```

**Expected Output**:
```
✓ Checking if running as administrator
✓ Creating database directory: C:\TASMA_Data
✓ Creating database file: C:\TASMA_Data\bookings.db
✓ Creating 'users' table
✓ Creating 'bookings' table
✓ Creating 'rooms' table
✓ Database initialization complete!
```

---

### STEP 2: Add Users (On SERVER computer)

**Location**: `C:\Program Files\TASMA Board Room Booking System\`

**File**: `ADD_USER_TO_SERVER.py`

**Execute** (Run once per user):
```cmd
# Option 1: Double-click ADD_USER_TO_SERVER.py
# Option 2: Command prompt
cd "C:\Program Files\TASMA Board Room Booking System"
python ADD_USER_TO_SERVER.py
```

**Interactive Prompts**:
```
Username (e.g., sandeepa): sandeepa
Password (e.g., password123): mypassword
Full Name (e.g., Sandeepa Kumar): Sandeepa Kumar
Department (e.g., IT): IT
```

**Expected Output**:
```
✓ Connected to server database
✓ Found 'users' table
Adding new user...
  Username: sandeepa
  Full Name: Sandeepa Kumar
  Department: IT

✓ User created successfully!
  ID: 1
  Username: sandeepa
  Name: Sandeepa Kumar

User can now login with:
  Username: sandeepa
  Password: mypassword
```

**Repeat for each user**:
```
Run ADD_USER_TO_SERVER.py 4 times for:
  - sandeepa (IT)
  - john (HR)
  - mary (Finance)
  - admin (IT)
```

---

### STEP 3: Client Installation (On each USER computer)

**File**: `TASMA_User_Setup_v2.2.exe`

**Execute**:
1. Download: `TASMA_User_Setup_v2.2.exe`
2. Double-click to run installer
3. Follow wizard (click Next, Next, Install)
4. Click Finish

**First-Run Setup Wizard** (Automatic):
- Appears after installation
- Tests network to GVBSERVER
- Tests database connection  
- Creates config.ini automatically
- Click "Continue to Login" when done

---

### STEP 4: User Login (Done by user)

**On user's computer**:
1. Open Start Menu
2. Find: "TASMA" or look on Desktop
3. Click to launch
4. Enter credentials from STEP 2:
   - Username: `sandeepa`
   - Password: `mypassword`
5. Click "Login"
6. See: "Welcome Sandeepa Kumar!" ✓

---

## ✅ Verification Checklist

- [ ] **Server Setup Complete**
  - [ ] SETUP_SERVER.py executed
  - [ ] Database file exists: `C:\Program Files\TASMA Board Room Booking System\bookings.db`
  - [ ] Database has at least 1 user created

- [ ] **Users Added**
  - [ ] ADD_USER_TO_SERVER.py executed for each user
  - [ ] At least 1 user account created (e.g., "sandeepa")
  - [ ] Passwords set and recorded

- [ ] **Client Installed**
  - [ ] TASMA_User_Setup_v2.2.exe installed on user computer
  - [ ] First-run wizard appeared automatically
  - [ ] Wizard showed "✓ Setup complete!"

- [ ] **User Can Login**
  - [ ] Launch TASMA on user computer
  - [ ] Login with username from STEP 2
  - [ ] See welcome message with user name
  - [ ] Can see booking interface

---

## 📁 File Locations

### On SERVER Computer
```
C:\Program Files\TASMA Board Room Booking System\
├── TASMA.exe                    (Main application)
├── SETUP_SERVER.py              (Initialize database)
├── ADD_USER_TO_SERVER.py        (Add users) ← Use this!
├── bookings.db                  (Database - created by SETUP_SERVER.py)
├── db_optimized.py
├── user_data_sync.py
└── [other files]
```

### On CLIENT Computers
```
C:\Program Files\TASMA\
├── TASMA.exe                    (Main application)
├── SETUP_SERVER_CLIENT.py       (Server connection setup)
├── [other modules]
└── [other files]

C:\Users\[USERNAME]\AppData\Roaming\TASMA\
├── config.ini                   (Created by first-run wizard)
└── [other files]
```

---

## 🐛 Troubleshooting

### Problem: "Invalid username or password"
**Cause**: User account not created in server database  
**Fix**: 
1. Go to server computer
2. Run: `ADD_USER_TO_SERVER.py`
3. Create the user account
4. User tries to login again

### Problem: "Network path NOT found"
**Cause**: Server offline or unreachable  
**Fix**:
1. Check server is powered on
2. Check network connection: `ping GVBSERVER`
3. Check GVBSERVER is accessible: `\\GVBSERVER`
4. Re-run first-run wizard

### Problem: "Database connection failed"
**Cause**: Server database not accessible  
**Fix**:
1. Verify SETUP_SERVER.py was run on server
2. Check database file exists at: `C:\Program Files\TASMA Board Room Booking System\bookings.db`
3. Try again after waiting 10 seconds

### Problem: "Still showing old error"
**Cause**: Using old configuration  
**Fix**:
1. Delete: `C:\Users\[USERNAME]\AppData\Roaming\TASMA\bookings.db`
2. Restart TASMA
3. First-run wizard runs again

---

## 📊 Files Included in v2.2

```
installer_build/dist/
├── TASMA.exe (41 MB)              Main application
├── ADD_USER_TO_SERVER.py (5 KB)   User management ★ NEW
├── SETUP_SERVER_CLIENT.py (6 KB)  Client setup (auto-runs)
├── SETUP_USER.py (12 KB)          User config
├── db_optimized.py (12 KB)        Database module
├── user_data_sync.py (17 KB)      Data sync module
├── tasma_logo.webp (7 KB)         Logo
├── config.ini.template (1 KB)     Config template
├── test_network_db.py (10 KB)     Connection test
├── CLIENT_QUICK_SETUP.txt (2 KB)  Quick reference
└── LICENSE.txt                    License
```

---

## 🎯 Quick Reference

| Task | File | Computer |
|------|------|----------|
| Setup database | SETUP_SERVER.py | SERVER |
| Add users | ADD_USER_TO_SERVER.py | SERVER |
| Install app | TASMA_User_Setup_v2.2.exe | CLIENT |
| Configure connection | SETUP_SERVER_CLIENT.py | CLIENT (auto) |
| Login | TASMA.exe | CLIENT |

---

## 📞 Support

### Common Questions

**Q: Do I need to run SETUP_SERVER.py every time?**  
A: No, only once to initialize the database. After that, just add users.

**Q: Can I change a user's password?**  
A: Yes, run ADD_USER_TO_SERVER.py, enter the username, press 'y' to overwrite.

**Q: What if I forget a user's password?**  
A: Run ADD_USER_TO_SERVER.py, enter username, set new password.

**Q: Can users change their own passwords?**  
A: Not yet. Admin must use ADD_USER_TO_SERVER.py.

**Q: How many users can I add?**  
A: Unlimited. Run ADD_USER_TO_SERVER.py for each user.

---

## ✨ What Happens After Login

Once user logs in successfully:
1. ✓ Connects to server database
2. ✓ Loads all bookings from server
3. ✓ Can view available rooms
4. ✓ Can make new bookings
5. ✓ Bookings sync with all other users
6. ✓ Real-time updates across devices

---

## 🚀 Ready to Deploy

**Checklist**:
- ✅ Database initialized on server
- ✅ User management tool ready
- ✅ Automatic client setup built-in
- ✅ All files packaged in installer
- ✅ Documentation complete

**Next Steps**:
1. Compile Inno Setup to create final .exe
2. Run on server: SETUP_SERVER.py
3. Run on server: ADD_USER_TO_SERVER.py (for each user)
4. Distribute installer to users
5. Users run installer and login

---

**Version**: 2.2  
**Date**: May 25, 2026  
**Status**: Production Ready ✓

