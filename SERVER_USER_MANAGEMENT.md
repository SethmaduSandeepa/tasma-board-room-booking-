# Adding Users to TASMA Server Database

## Quick Steps

### On SERVER Computer:

1. **Navigate to installation folder:**
   ```
   C:\Program Files\TASMA Board Room Booking System\
   ```

2. **Find the user management script:**
   ```
   ADD_USER_TO_SERVER.py
   ```

3. **Run the script:**
   - Double-click: `ADD_USER_TO_SERVER.py`
   - OR from Command Prompt:
   ```cmd
   python ADD_USER_TO_SERVER.py
   ```

4. **Fill in user details:**
   - Username: `sandeepa` (or any username)
   - Password: `password123` (or any password)
   - Full Name: `Sandeepa Kumar`
   - Department: `IT`

5. **Script will:**
   - ✓ Connect to server database
   - ✓ Create user account
   - ✓ Set password

6. **Result:**
   ```
   ✓ User created successfully!
     Username: sandeepa
     Name: Sandeepa Kumar
   
   User can now login with:
     Username: sandeepa
     Password: password123
   ```

---

## Complete Flow

### 1️⃣ **Server Setup** (One-time, on SERVER)
```
SETUP_SERVER.py 
→ Creates database at C:\Program Files\TASMA Board Room Booking System\bookings.db
```

### 2️⃣ **Add Users** (On SERVER, for each user)
```
ADD_USER_TO_SERVER.py
→ Adds user accounts to server database
→ Example: sandeepa, john, mary, etc.
```

### 3️⃣ **Client Installation** (On each USER computer)
```
TASMA_User_Setup_v2.2.exe
→ Installs TASMA
→ First-run wizard configures server connection
→ Connects to server database automatically
```

### 4️⃣ **User Login** (On USER computer)
```
Login with credentials from Step 2
→ Username: sandeepa
→ Password: password123
→ ✓ Welcome sandeepa!
```

---

## Example: Adding Multiple Users

```
Run ADD_USER_TO_SERVER.py 4 times:

1st run:
   Username: sandeepa
   Password: pass123
   Full Name: Sandeepa Kumar
   Department: IT

2nd run:
   Username: john
   Password: john123
   Full Name: John Smith
   Department: HR

3rd run:
   Username: mary
   Password: mary123
   Full Name: Mary Johnson
   Department: Finance

4th run:
   Username: admin
   Password: admin123
   Full Name: Admin User
   Department: IT
```

Now all 4 users can login from their client computers!

---

## Troubleshooting

### "Database not found at..."
- Verify SETUP_SERVER.py was run first
- Check path: `C:\Program Files\TASMA Board Room Booking System\bookings.db`
- Make sure server computer has TASMA installed

### "Invalid username or password" on login
- User was not created with ADD_USER_TO_SERVER.py
- Run the script to add the user
- Verify username and password match

### "User already exists"
- User already in database
- Press `y` to update password
- Or use different username

### Still having issues
1. Verify server database exists
2. Run SETUP_SERVER.py if database missing
3. Run ADD_USER_TO_SERVER.py to add users
4. Have clients run setup wizard again

---

## File Locations

| File | Location | Purpose |
|------|----------|---------|
| SETUP_SERVER.py | Server \| C:\Program Files\TASMA... | Initialize server database |
| ADD_USER_TO_SERVER.py | Server \| C:\Program Files\TASMA... | Add users to database |
| SETUP_SERVER_CLIENT.py | Client \| C:\Program Files\TASMA... | Configure client connection |
| bookings.db | Server \| C:\Program Files\TASMA... | Actual database file |

---

## Next Steps

1. **On SERVER:** Run `ADD_USER_TO_SERVER.py` to add users
2. **On USERS:** Install TASMA → Automatic setup → Login with credentials
3. **Result:** All users connected to shared server database! ✓

---

**Version:** 2.2  
**Date:** May 25, 2026
