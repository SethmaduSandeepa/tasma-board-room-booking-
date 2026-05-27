# TASMA User Installer - Build & Distribution Guide

## Overview

I've created a complete installer package system that lets you build a professional EXE installer for users. Users will get everything they need in one setup file.

---

## What's Included in the Installer

When users run the installer, they get:

```
TASMA Installation (Automatic):
├── TASMA.exe (Main application)
├── SETUP_USER.py (Configuration wizard)
├── db_optimized.py (Server connection)
├── user_data_sync.py (User data sync)
├── config.ini (Database configuration)
├── Documentation (Help files)
└── Desktop shortcut
```

---

## Build Process (2 Methods)

### **Method 1: Full Installer (Recommended)**

Creates a professional MSI/EXE installer with uninstall, shortcuts, etc.

#### Prerequisites:
1. Install [Inno Setup](https://jrsoftware.org/isinfo.php) (free)
2. Have Python 3.8+ installed
3. Have PyInstaller available

#### Build Steps:

```bash
# Step 1: Build the executable bundle
.\build_user_installer.bat

# This creates: installer_build\dist\
# Contains all Python modules compiled to EXE
```

```
Step 2: Open Inno Setup
- Open: TASMA_User_Installer.iss
- Click: Build > Compile
- Installer will be created in: setup_output\TASMA_User_Setup_v2.0.exe
```

#### Result:
- Professional installer EXE
- Automatic shortcuts
- Easy uninstall
- All dependencies included

---

### **Method 2: Simple Folder Distribution**

Users manually copy files (simpler but less convenient).

```bash
# After running build_user_installer.bat
# Copy entire "installer_build\dist\" folder to users
# They extract and run TASMA.exe
```

---

## Detailed Build Steps

### Step 1: Run Builder Script

```bash
# Open Command Prompt in project folder
cd E:\tasma_booking_syst

# Run the build script
build_user_installer.bat
```

**What it does:**
1. ✓ Installs PyInstaller
2. ✓ Collects all necessary files
3. ✓ Builds standalone TASMA.exe
4. ✓ Packages everything for installer

**Output:** `installer_build\dist\`

### Step 2: Build Installer with Inno Setup

```
1. Download & install Inno Setup (if not already installed)
   https://jrsoftware.org/isinfo.php

2. Open file: TASMA_User_Installer.iss

3. In Inno Setup:
   - Click: Build Menu > Compile
   - Wait for compilation to complete
   - You'll see: "Successful Compile"

4. Final installer:
   Location: setup_output\TASMA_User_Setup_v2.0.exe
```

### Step 3: Distribute to Users

```
1. Copy: setup_output\TASMA_User_Setup_v2.0.exe
   
2. Send to users via:
   - Email
   - File share
   - USB drive
   - Download link
   
3. Users double-click to install
```

---

## User Installation Experience

### User receives: `TASMA_User_Setup_v2.0.exe`

**User clicks → Installation begins:**

```
1. Welcome screen
   "Welcome to TASMA Board Room Booking System Setup"
   ✓ Have server details ready

2. Choose installation location
   Default: C:\Program Files\TASMA\

3. Choose start menu shortcuts
   ✓ Create desktop icon (optional)

4. Installation progress
   Files are unpacked and installed

5. Completion
   Message: "Configuration wizard will run automatically"
   - User clicks "Configuration" shortcut
   - SETUP_USER.py launches
   - User enters server name/IP
   - Connection is tested
   - User can now launch TASMA
```

---

## File Locations After Installation

**On User's Computer:**

```
C:\Program Files\TASMA\
├── TASMA.exe                    ← Main app (double-click to run)
├── SETUP_USER.py                ← Config wizard
├── db_optimized.py
├── user_data_sync.py
├── config.ini                   ← Auto-configured by wizard
├── booking_icon.ico
├── LICENSE.txt
└── Documentation\
    ├── SETUP_GUIDE.md
    ├── USER_DATA_SYNC_GUIDE.md
    └── NETWORK_DATABASE_SETUP.md

Start Menu:
├── TASMA
├── TASMA Configuration
└── Uninstall TASMA

Desktop:
└── TASMA (shortcut)
```

---

## Customization Options

### Modify Installation Properties

Edit `TASMA_User_Installer.iss`:

```ini
; Change these to customize:

[Setup]
AppName=TASMA Board Room Booking System    ← App name
AppVersion=2.0                              ← Version
AppPublisher=TASMA                          ← Publisher
DefaultDirName={autopf}\TASMA               ← Install folder
OutputBaseFilename=TASMA_User_Setup_v2.0    ← Installer filename
```

### Add Custom Splash Screen

```ini
; Add to [Setup] section:
AppIconDir=.\
AppIcon=booking_icon.ico
```

### Change Start Menu Group

```ini
DefaultGroupName=TASMA Board Room Booking System
```

---

## Troubleshooting Build Issues

### Issue: PyInstaller not found
```
Error: "PyInstaller is not installed"
Solution: 
  python -m pip install pyinstaller
```

### Issue: Icon not found
```
Error: "booking_icon.ico not found"
Solution:
  Make sure booking_icon.ico is in the project root
  Or change icon path in TASMA_User_Installer.iss
```

### Issue: Inno Setup won't compile
```
Error: Source files not found
Solution:
  1. Run build_user_installer.bat first
  2. Ensure installer_build\dist\ folder exists
  3. Check all source paths in .iss file
```

### Issue: SETUP_USER.py won't run
```
Error: "Python script not recognized"
Solution:
  1. Install Python on user machines, OR
  2. Convert SETUP_USER.py to EXE using PyInstaller
  3. Update reference in installer
```

---

## Distribution Checklist

- [ ] Run: `build_user_installer.bat` successfully
- [ ] Install Inno Setup on build machine
- [ ] Open and compile: `TASMA_User_Installer.iss`
- [ ] Verify installer created: `setup_output\TASMA_User_Setup_v2.0.exe`
- [ ] Test installer on clean machine
- [ ] Copy installer to distribution location
- [ ] Send download link or file to users
- [ ] Users install and run configuration wizard
- [ ] Users connect to server successfully

---

## System Requirements for Users

After installation, users need:

**Minimum:**
- Windows 7 or later
- 50 MB disk space
- Network connection to server
- Python 3.8+ (if running from source)

**Recommended:**
- Windows 10 or later
- 100 MB disk space
- Broadband network connection

---

## Version Updates

### To release a new version:

1. Update version in `TASMA_User_Installer.iss`:
   ```
   AppVersion=2.1
   OutputBaseFilename=TASMA_User_Setup_v2.1
   ```

2. Run: `build_user_installer.bat`

3. Compile with Inno Setup

4. Release new installer EXE

---

## Alternative: Portable Version (No Installation)

To create a portable version (no installer needed):

```bash
# After running build_user_installer.bat
# Users simply copy and run: installer_build\dist\TASMA.exe

# No installation needed
# Works from USB drive
# Can move folders around
```

---

## Support Scripts Included

Users get these tools automatically:

| Tool | Purpose |
|------|---------|
| `TASMA.exe` | Main application |
| `SETUP_USER.py` | Database configuration |
| `test_network_db.py` | Connection testing |
| `setup_database_config.py` | GUI configuration |

---

## Next Steps

1. **Build the executable:**
   ```bash
   .\build_user_installer.bat
   ```

2. **Install Inno Setup** (if needed)

3. **Compile the installer:**
   ```
   Open TASMA_User_Installer.iss in Inno Setup
   Click Build > Compile
   ```

4. **Test the installer:**
   - Install on a test machine
   - Run configuration wizard
   - Verify it connects to your server

5. **Distribute to users:**
   - Send: `setup_output\TASMA_User_Setup_v2.0.exe`
   - Users double-click to install
   - Done!

---

## Files Created

| File | Purpose |
|------|---------|
| `build_user_installer.bat` | Builder script |
| `TASMA_User_Installer.iss` | Installer script |
| `installer_build\dist\` | Built files (after running .bat) |
| `setup_output\` | Final installer EXE (after Inno Setup) |

---

**Version:** 2.0
**Last Updated:** May 2026
**Status:** Ready for distribution
