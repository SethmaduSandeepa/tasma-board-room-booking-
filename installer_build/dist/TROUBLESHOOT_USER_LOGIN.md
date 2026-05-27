# TASMA - User Login Not Working (Database Issue)

## Problem
User shows in database but login says:
```
"Invalid username or password, or account not approved yet"
```

Even though:
- ✓ App connects to server (shows "Using server database: \\GVBSERVER...")
- ✓ User was added via ADD_USER_TO_SERVER.py on server
- ✓ Admin "approved" the user

## Root Causes

### 1. **Password Mismatch** (Most Common)
```
When you ran ADD_USER_TO_SERVER.py:
  You entered: password123

When user tries to login:
  They enter: password123

But the hash doesn't match!
→ Reason: Password hashing is case-sensitive and includes username
```

### 2. **Username Case Mismatch**
```
When you added user:
  Username: Sandeepa

When user tries to login:
  Username: sandeepa

→ Error: Usernames must match EXACTLY (case-sensitive)
```

### 3. **User Not Actually in Database**
```
You think you added it, but it failed silently
→ Check if user really exists in database
```

### 4. **Wrong User Role**
```
User added as 'admin' instead of 'user'
→ Login code only allows role='user'
```

## Solution: Step-by-Step

### Step 1: Check What's in the Database

**On SERVER computer:**

1. Go to: `e:\tasma_booking_syst\` (or your project folder)
2. Find: `DATABASE_DIAGNOSTIC.py`
3. Double-click to run
4. You'll see:
   ```
   ✓ Database connected successfully
   
   USERS IN DATABASE
   
   Found 1 user(s):
   
   ID: 1
     Username: sandeepa
     Full Name: Sandeepa Kumar
     Role: user
     Department: IT
   ```

### Step 2: Check User Details

The diagnostic will show:
- ✓ User exists or ✗ User missing
- ✓ Username spelling
- ✓ Role (should be "user")
- ✓ Full name and department

### Step 3: Test the Password

When prompted:
```
Test a specific login? (yes/no): yes
  Username: sandeepa
  Password: password123
```

Diagnostic will show:
```
✓ User found!
  Username: sandeepa
  
✓ PASSWORD MATCHES!
✓✓ Login should work!
```

Or:
```
✗ PASSWORD DOES NOT MATCH

Solution:
  1. Run ADD_USER_TO_SERVER.py again
  2. When prompted for password, enter correct password
  3. Choose 'yes' to overwrite existing user
```

### Step 4: Fix the Problem

**If user not found:**
```
1. Run ADD_USER_TO_SERVER.py
2. Enter: sandeepa (exact username)
3. Enter: password123 (what user will use)
4. Enter: Sandeepa Kumar (full name)
5. Enter: IT (department)
6. Choose: yes if it asks to overwrite
```

**If password doesn't match:**
```
1. Run ADD_USER_TO_SERVER.py again
2. Enter SAME USERNAME: sandeepa
3. Enter: password123 (the password they will use)
4. Choose: yes to overwrite password
```

**If role is wrong:**
```
✗ This shouldn't happen, but if you see Role: 'admin'
  1. Delete user from database
  2. Run ADD_USER_TO_SERVER.py again to recreate
```

## Testing After Fix

### On CLIENT computer:

1. **Restart TASMA**
2. **Click Login tab**
3. **Enter:**
   - Username: `sandeepa` (exactly as added to database)
   - Password: `password123` (exactly as entered in ADD_USER_TO_SERVER.py)
4. **Click Login**

**Expected result:**
```
✓ "Welcome, Sandeepa Kumar!" message
✓ Login succeeds
✓ Can see booking calendar
```

## Common Mistakes

| Mistake | Solution |
|---------|----------|
| **Username different case** | `Sandeepa` vs `sandeepa` - must match exactly |
| **Password different** | When added: `pass123`, Try login: `password123` - doesn't work |
| **Forgot what password was** | Delete user, recreate with known password |
| **User not in database at all** | Run ADD_USER_TO_SERVER.py to create |
| **Edited database directly** | Don't! Use ADD_USER_TO_SERVER.py tool |
| **Multiple same users** | Database allows only one per username |

## Detailed Diagnostic Output Example

```
DATABASE_DIAGNOSTIC.py output:

Database: C:\Program Files\TASMA Board Room Booking System\bookings.db

✓ Database connected successfully

Database Tables:
  - bookings
  - rooms
  - user_activity_log
  - user_preferences
  - user_requests
  - users

USERS IN DATABASE

Found 2 user(s):

ID: 1
  Username: admin
  Full Name: Administrator
  Role: admin
  Department: 

ID: 2
  Username: sandeepa
  Full Name: Sandeepa Kumar
  Role: user
  Department: IT

PENDING REGISTRATION REQUESTS

✓ No pending requests
```

## If Still Not Working

### 1. Verify Network Connection
```
On client computer, open CMD and type:
  ping GVBSERVER
  
Should see:
  Reply from 192.168.x.x: bytes=32 time=2ms TTL=64
  
If error: Network/server issue
```

### 2. Verify Database File Access
```
On client computer, open File Explorer:
  \\GVBSERVER\C$\Program Files\TASMA Board Room Booking System\
  
Should see: bookings.db file

If not: Permissions/sharing issue
```

### 3. Check TASMA Console Output
```
Start TASMA, look at console window for:
  "Using server database: \\GVBSERVER..."
  
If shows local path: Config not set up
```

### 4. Restart and Try Again
```
1. Close TASMA completely
2. Wait 5 seconds
3. Delete local config file:
   C:\Users\[USERNAME]\AppData\Roaming\TASMA\config.ini
4. Restart TASMA
5. Setup wizard should run again
6. Try login again
```

## Quick Checklist

Before login test:
- [ ] Run DATABASE_DIAGNOSTIC.py on server
- [ ] Verify user exists in database
- [ ] Verify password matches
- [ ] Verify role = 'user'
- [ ] Verify client can reach \\GVBSERVER
- [ ] Verify TASMA shows "Using server database"
- [ ] Verify username is spelled exactly right
- [ ] Verify password is exactly what was set

---

## Command Reference

| Task | Command | Where |
|------|---------|-------|
| **Check database** | DATABASE_DIAGNOSTIC.py | Server computer |
| **Add/modify user** | ADD_USER_TO_SERVER.py | Server computer |
| **Migrate database** | MIGRATE_ADD_USER_REQUESTS.py | Server computer |
| **Initialize database** | SETUP_SERVER.py | Server computer (one-time) |

---

**Run DATABASE_DIAGNOSTIC.py on your server computer first to see what's in the database!**

