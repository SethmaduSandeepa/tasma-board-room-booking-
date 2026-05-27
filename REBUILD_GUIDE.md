# Rebuild Installer - Quick Guide

## Problem
Your installer files are from May 17, but you have new code from May 24 (with user data sync, updated database modules, etc.)

## Solution
Rebuild the installer files with the latest code.

---

## Option 1: Full Automated Build (Easiest)

**If you have Inno Setup installed:**

```bash
# Double-click this file:
REBUILD_AND_COMPILE.bat
```

**What it does:**
1. ✓ Cleans old build files
2. ✓ Collects all latest source code
3. ✓ Builds standalone TASMA.exe
4. ✓ Automatically compiles with Inno Setup
5. ✓ Creates new installer in setup_output\

**Time:** ~5 minutes

**Result:** `setup_output\TASMA_User_Setup_v2.2.exe`

---

## Option 2: Manual Build (If Inno Setup not installed)

**Step 1: Build the bundle**
```bash
REBUILD_INSTALLERS.bat
```

**Step 2: Install Inno Setup** (if needed)
- Download: https://jrsoftware.org/isinfo.php
- Install normally

**Step 3: Compile the installer**
- Open: `TASMA_User_Installer.iss`
- In Inno Setup, click: Build > Compile
- New installer in: `setup_output\TASMA_User_Setup_v2.2.exe`

**Time:** ~10 minutes

---

## What's New in v2.2

- ✓ User data sync module
- ✓ Enhanced database connection handling
- ✓ Improved configuration tools
- ✓ Better error diagnostics
- ✓ Activity logging
- ✓ Multi-device user support

---

## After Rebuild

**Verify the new installer:**
```
setup_output\TASMA_User_Setup_v2.2.exe
- Size: ~42-45 MB
- Date modified: Today
- Type: Application
```

**Distribute to users:**
- Send: `TASMA_User_Setup_v2.2.exe`
- Users double-click to install
- Configuration wizard runs automatically

---

## Troubleshooting

**"REBUILD_AND_COMPILE.bat" won't run?**
- Right-click > Run as Administrator
- OR open Command Prompt as Admin, then run the script

**"Inno Setup not found"?**
- Download and install Inno Setup
- Run REBUILD_INSTALLERS.bat instead
- Then manually compile with Inno Setup

**"PyInstaller error"?**
- Run: `pip install pyinstaller`
- Try rebuilding again

**"Python not found"?**
- Install Python 3.8+
- Add to PATH
- Run the script again

---

## Files Included in New Installer

```
✓ TASMA.exe (main application)
✓ db_optimized.py (database module)
✓ user_data_sync.py (user sync)
✓ SETUP_USER.py (configuration)
✓ test_network_db.py (diagnostics)
✓ config.ini.template (template config)
✓ LICENSE.txt
```

---

## Next Steps

1. Run: `REBUILD_AND_COMPILE.bat` (or REBUILD_INSTALLERS.bat)
2. Wait for build to complete
3. Find new installer in: `setup_output\TASMA_User_Setup_v2.2.exe`
4. Test on a clean machine (optional but recommended)
5. Distribute to users

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 5/15/2026 | Initial release |
| 2.1 | 5/15/2026 | Professional edition |
| 2.2 | Today | User data sync, latest modules |

---

Done! Your users will get the latest code. 🎉
