# TASMA Booking System - User Quick Start Guide

## For End Users

### Launching TASMA

**Method 1: Desktop Shortcut (Recommended)**
1. Double-click "TASMA Board Room Booking System" shortcut on your desktop
2. Wait 2-3 seconds for the login window to appear
3. Enter your username and password
4. Click Login

**Method 2: From Start Menu**
1. Press `Win` key to open Start Menu
2. Search for "TASMA"
3. Click "TASMA Board Room Booking System"

**Method 3: Network Path**
1. Open File Explorer
2. Type in address bar: `\\SERVER_NAME\TASMA_App`
3. Double-click `TASMA Board Room Booking System.exe`

### Initial Login

**Default Credentials** (for first login):
- **Username**: admin
- **Password**: admin

⚠️ **IMPORTANT**: Change the admin password immediately after first login!

### First-Time Setup

1. **Login as Admin**
   - Username: `admin`
   - Password: `admin`

2. **Change Admin Password**
   - Go to Settings
   - Change Password
   - Enter new secure password

3. **Create User Accounts**
   - Admin Panel → Manage Users
   - Add new users from registration requests
   - Assign departments as needed

4. **Make Booking**
   - Return to regular user mode
   - Select room and date/time
   - Confirm booking

### Booking a Room

1. **Select Date**
   - Click calendar icon or date selector
   - Choose the date you want to book

2. **Select Room**
   - Click dropdown to see available rooms
   - Click to select

3. **Select Time**
   - Set start hour and minute
   - Set end hour and minute
   - Click "Select Time"

4. **Confirm Booking**
   - Review booking details
   - Click "Book Room"
   - Confirmation message will appear

### View Your Bookings

1. **Click "My Bookings" tab**
2. **Select date range** (optional)
3. **View upcoming bookings**
4. **Cancel booking** (if needed)
   - Select booking
   - Click "Cancel"

### Troubleshooting

#### Application Won't Start
- Check network connection to server: `ping SERVER_NAME`
- Verify shortcut path is correct
- Restart computer
- Contact IT support

#### Login Failed
- Verify username and password are correct
- Check CAPS LOCK
- Account may not be approved yet (contact admin)

#### Slow Launch
- First launch: 2-3 seconds is normal
- Subsequent launches: <2 seconds
- If consistently slow, restart application

#### "Database is locked"
- Another user is making a change
- Wait a few seconds and try again
- If persists, restart application

#### Cannot Access Server
```
Error: "Cannot access \\SERVER_NAME\TASMA_App"
Fix:
  1. Restart computer
  2. Reconnect to network
  3. Contact IT support
```

### Tips & Tricks

1. **Pin to Start Menu**
   - Right-click shortcut → Pin to Start
   - Quick access from Start Menu

2. **Use PIN to Taskbar**
   - After launching, right-click taskbar icon
   - Click "Pin to taskbar"
   - Quick launch from taskbar next time

3. **Schedule Regular Bookings**
   - Most used rooms can be booked regularly
   - Recurring bookings feature available in Admin mode

4. **Export Bookings**
   - Admin can export booking data to CSV
   - Useful for reports and audits

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Q` | Quit application |
| `Ctrl+L` | Logout |
| `Ctrl+R` | Refresh bookings |
| `Tab` | Move to next field |
| `Enter` | Confirm selection |
| `Esc` | Cancel dialog |

### System Requirements

- **OS**: Windows 7 or newer
- **Network**: Must be connected to network
- **Browser**: Not required (desktop app)
- **Internet**: Not required (uses local server)

### Data Protection

- Your password is securely hashed
- Bookings are stored on central server
- Database is backed up regularly
- Do not share credentials with others

### Getting Help

**For Technical Issues:**
- Email IT Support: [IT_EMAIL]
- Phone: [IT_PHONE]
- Internal Helpdesk: [EXTENSION]

**For Booking Issues:**
- Contact Room Manager: [MANAGER_EMAIL]
- Check facilities calendar for room details

---

**Version**: 1.0  
**Last Updated**: May 2026  
**Support**: Contact your IT department
