# TASMA Board Room Booking System - Professional Deployment Guide

## Overview
This guide explains how to deploy TASMA as a standalone professional application to other computers without requiring Python installation.

---

## Step 1: Create Standalone Executable

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Windows OS

### Build Process

1. **Navigate to the project directory:**
   ```
   cd e:\tasma_booking_syst
   ```

2. **Install build dependencies:**
   ```
   pip install pyinstaller
   pip install -r requirements.txt
   ```

3. **Run the build script:**
   ```
   build_standalone.bat
   ```

   This will:
   - Install PyInstaller (if not installed)
   - Create a standalone executable: `dist\TASMA Board Room Booking System.exe`
   - Package all dependencies into the executable
   - Include the logo and database

4. **Test the executable:**
   - Navigate to `dist` folder
   - Double-click `TASMA Board Room Booking System.exe`
   - Verify all features work correctly

---

## Step 2: Create Professional Installer (Optional but Recommended)

### Prerequisites
- NSIS (Nullsoft Scriptable Install System) - Download from: https://nsis.sourceforge.io/
- The standalone executable from Step 1

### Installation Process

1. **Install NSIS:**
   - Download NSIS from https://nsis.sourceforge.io/
   - Run the installer and follow the prompts
   - Accept default installation path

2. **Build the installer:**
   ```
   "C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
   ```

   This creates: `TASMA_Booking_System_Installer.exe`

3. **Test the installer:**
   - Double-click `TASMA_Booking_System_Installer.exe`
   - Follow the installation wizard
   - Verify shortcuts are created
   - Launch the application

---

## Step 3: Deploy to Other Computers

### Option A: Using Standalone Executable (Simple)
1. Copy `dist\TASMA Board Room Booking System.exe` to other computers
2. Double-click to run
3. No installation needed

### Option B: Using Installer (Professional - Recommended)
1. Distribute `TASMA_Booking_System_Installer.exe`
2. Users run the installer
3. Application appears in:
   - Start Menu → TASMA Booking System
   - Desktop Shortcut
   - Control Panel → Programs and Features (for uninstall)

### Option C: Network/USB Distribution
1. Copy to USB drive or network share:
   - `TASMA_Booking_System_Installer.exe` (Professional)
   - `dist\TASMA Board Room Booking System.exe` (Simple)

2. Users can install from:
   - USB drive
   - Network share
   - Downloaded file

---

## Database Management for Multiple Installations

### Single Shared Database (Recommended for offices)
1. Place `bookings.db` on a network share
2. Edit `main.py` line where database is defined:
   ```python
   self.db_name = "\\\\SERVER\\Share\\bookings.db"  # Network path
   ```
3. Rebuild executable with network path

### Local Databases
1. Each computer has its own `bookings.db`
2. Use data export/import to sync between systems

---

## Troubleshooting

### Issue: "Python not found" error
**Solution:** Ensure you're using the `.exe` file, not the Python script

### Issue: Database file not found
**Solution:** Ensure `bookings.db` is in the same directory as the executable

### Issue: Logo not displaying
**Solution:** Ensure `tasma_logo.webp` is in the same directory

### Issue: Installer won't create shortcuts
**Solution:** Run installer with administrator privileges

---

## System Requirements for End Users

### Minimum Requirements
- Windows 7 or newer
- 50 MB disk space
- 256 MB RAM
- Network connection (if using shared database)

### Recommended Requirements
- Windows 10 or newer
- 100 MB disk space
- 512 MB RAM

---

## File Structure After Build

```
TASMA_Booking_System/
├── build_standalone.bat          # Script to create executable
├── installer.nsi                 # Script to create installer
├── requirements.txt              # Python dependencies
├── DEPLOYMENT_GUIDE.md           # This file
├── main.py                       # Main application source
├── tasma_logo.webp               # Application logo
├── bookings.db                   # Database file
└── dist/
    └── TASMA Board Room Booking System.exe  # Standalone executable
```

---

## Version Management

When updating the application:

1. Update `main.py` with new features
2. Rebuild standalone executable: `build_standalone.bat`
3. Rebuild installer: `makensis installer.nsi`
4. Test thoroughly before distribution
5. Version the files: `TASMA_v2.0_Installer.exe`

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review FEATURES.md for feature documentation
3. Review README.md for user guide

---

Last Updated: May 15, 2026
Version: 2.0 Professional Deployment
