# TASMA Board Room Booking System
## Enhanced Edition v2.0

A professional, feature-rich board room booking system built with Python and Tkinter.

## 🎯 Quick Start

### Installation

1. **Python Version Required:** Python 3.7+

2. **Install Dependencies:**
   ```bash
   pip install tkcalendar
   ```

3. **Run the Application:**
   ```bash
   python main.py
   ```

---

## ✨ Key Features

### 📅 User-Friendly Interface
- **Calendar Date Picker** - Click to select dates instead of typing
- **Tabbed Layout** - Separate tabs for "New Booking" and "Manage Bookings"
- **Color-Coded Buttons** - Easy to understand action buttons
- **Status Bar** - Real-time feedback on all actions

### 💼 Core Functionality
- ✅ **Create Bookings** - Add new board room reservations
- ✅ **Edit Bookings** - Modify existing reservations
- ✅ **Delete Bookings** - Cancel reservations with confirmation
- ✅ **Search & Filter** - Find bookings by date, department, user, or reason
- ✅ **Export to CSV** - Export all bookings for reporting

### 🔒 Data Integrity
- Input validation for all fields
- Time format enforcement (HH:MM)
- Overlap detection - warns if time slot is already booked
- Automatic database management with SQLite

### 🎨 Professional Design
- Modern blue header
- Clean interface with proper spacing
- Alternating row colors for easy reading
- Responsive layout that adapts to window size
- Large, readable fonts

---

## 📖 How to Use

### Creating a Booking

1. Click on the **"New Booking"** tab
2. **Select Date:** Click the calendar icon and pick a date
3. **Enter Time:** Type in HH:MM format (e.g., `14:30`)
4. **Select Department:** Choose from dropdown (Finance, HR, IT, Marketing, Operations, Sales, Other)
5. **Enter User Name:** Type the person making the booking
6. **Enter Reason:** Provide detailed meeting purpose (multi-line supported)
7. Click **"Book Room"** button
8. Confirmation message appears when successful

### Editing a Booking

1. Go to **"Manage Bookings"** tab
2. Click on the booking you want to modify
3. Go back to **"New Booking"** tab
4. Click **"Edit Selected"** button
5. Modify the details as needed
6. Click **"Book Room"** to save changes

### Searching Bookings

1. Go to **"Manage Bookings"** tab
2. Type in the search box at the top
3. Results filter as you type
4. Clear the search box to show all bookings

### Sorting Bookings

1. In **"Manage Bookings"** tab
2. Click any column header (ID, Date, Time, Department, User, Reason)
3. Bookings sort by that column

### Exporting Data

1. Go to **"Manage Bookings"** tab
2. Click **"Export to CSV"** button
3. Choose a location and filename
4. Open the file in Excel or any spreadsheet application

### Deleting a Booking

1. Go to **"Manage Bookings"** tab
2. Click on the booking to delete
3. Click **"Delete Selected"** button
4. Confirm deletion in the dialog
5. Booking is permanently removed

---

## 🎨 Color Guide

| Button | Color | Action |
|--------|-------|--------|
| Book Room | Green | Create new booking |
| Edit Selected | Orange | Edit existing booking |
| Clear Form | Purple | Clear all form fields |
| Refresh List | Blue | Reload bookings |
| Delete Selected | Red | Remove booking |
| Export to CSV | Cyan | Export data |

---

## ⚙️ Technical Details

### Database
- **Type:** SQLite3
- **File:** `bookings.db` (automatically created)
- **Backup:** Stored in application directory

### Data Format
- **Dates:** YYYY-MM-DD format
- **Times:** HH:MM format (24-hour)
- **Timestamps:** Automatic creation timestamp

### System Requirements
- Windows/Mac/Linux compatible
- Minimum: 50MB free disk space
- No internet connection required

---

## 🐛 Troubleshooting

### Module Not Found: tkcalendar
**Solution:** Install tkcalendar
```bash
pip install tkcalendar
```

### Application Won't Start
**Solution:** Ensure Python 3.7+ is installed
```bash
python --version
```

### Database Locked Error
**Solution:** Close all instances of the application and try again

### Time Validation Error
**Solution:** Use HH:MM format (e.g., `09:30`, `14:45` - not `9:30` or `2:45 PM`)

---

## 📊 Data Backup

The database file `bookings.db` is stored in the application directory. To backup:
1. Locate `bookings.db` file
2. Copy it to a safe location
3. To restore, replace the current file with the backup

---

## 🔐 Data Security Notes

- All data is stored locally in SQLite
- No cloud storage or internet transmission
- Database is plain text (can be read by editing tools)
- Implement proper access controls on your computer

---

## 📝 Tips & Best Practices

1. **Backup Regularly** - Keep copies of `bookings.db`
2. **Consistent Department Names** - Use the dropdown to maintain consistency
3. **Detailed Reasons** - Provide clear meeting purposes for future reference
4. **Review Calendar** - Check for overlaps before booking
5. **Export Monthly** - Keep CSV exports for archiving

---

## 🎓 Educational Use

This application is perfect for learning:
- Python GUI development with Tkinter
- SQLite database management
- Object-oriented programming
- Event handling and callbacks
- Data validation techniques
- File I/O operations

---

## 📄 License

This software is provided as-is for use by TASMA organization.

---

## 👥 Support

For issues or feature requests, contact the development team.

**Version:** 2.0 Enhanced Edition  
**Last Updated:** February 28, 2026  
**Status:** ✅ Production Ready

---

## 🚀 What's New in v2.0

✨ Calendar date picker  
✨ Edit booking functionality  
✨ Real-time search & filter  
✨ CSV export capability  
✨ Advanced validation  
✨ Professional UI design  
✨ Status bar with timestamps  
✨ Column sorting  
✨ Tab-based interface  
✨ Department dropdown  

Enjoy your enhanced board room booking system! 🎉
