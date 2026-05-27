# TASMA - Fix Registration Issue

## Problem
When trying to register a new user, you see:
```
Registration failed: unable to open database file
```

## Root Cause
The database was initialized with an older version of SETUP_SERVER.py that didn't create the `user_requests` table. This table is required for user registration.

## Solution

### Option 1: Quick Fix (Recommended - No reinstall needed)

**On the SERVER computer:**

1. Go to: `e:\tasma_booking_syst\` (or your project folder)
2. Find: `MIGRATE_ADD_USER_REQUESTS.py`
3. Double-click to run
4. You'll see:
   ```
   ✓ user_requests table created successfully!
   ```
5. Done! Users can now register.

### Option 2: Full Reinstall (If migration fails)

**On the SERVER computer:**

1. Delete the old database:
   - Go to: `C:\Program Files\TASMA Board Room Booking System\`
   - Delete: `bookings.db` file

2. Run the updated setup script:
   - Download the latest: `SETUP_SERVER.py`
   - Double-click to run as Administrator
   - Follow the prompts

3. Add users again:
   - Run: `ADD_USER_TO_SERVER.py`
   - Create each user account

## Testing the Fix

After applying the fix:

1. **On user computer**, open TASMA
2. Click **Register** 
3. Fill in:
   - Full Name: `Test User`
   - Username: `testuser`
   - Password: `password123`
   - Confirm Password: `password123`
   - Department: `IT`
4. Click **Submit Request**
5. Should see: ✓ Registration request submitted!

## Database Structure After Fix

Your database now has:
- ✓ users (approved user accounts)
- ✓ user_requests (pending registration requests)
- ✓ bookings
- ✓ rooms
- ✓ user_preferences
- ✓ user_activity_log

## User Registration Workflow

```
User Registration Request
    ↓
Saved to: user_requests table (status: pending)
    ↓
Admin Reviews
    ↓
Admin Approves → Moved to users table
         ↓
         Admin Denies → Deleted from user_requests
    ↓
User Can Login
```

## Admin Approval Process

**On SERVER computer:**

1. Run: `TASMA.exe` (the desktop app)
2. Click: **Admin Panel** (if you have admin account)
3. View **Pending Requests**
4. Click **Approve** to accept registration
5. User can now login!

Alternatively, you can:
- Run `ADD_USER_TO_SERVER.py` to directly add approved users
- Skip the registration request process

## Still Having Issues?

| Error | Solution |
|-------|----------|
| "Database is locked" | Wait 10 seconds and try again |
| "Permission denied" | Run as Administrator |
| "Network path not found" | Check GVBSERVER is online |
| "Migration completed but still fails" | Restart TASMA app |

## What Changed

**SETUP_SERVER.py** now creates:
- Added: `user_requests` table
- For: Storing pending user registration requests
- Schema: id, username, full_name, password, department, created_at, status

**MIGRATE_ADD_USER_REQUESTS.py** is:
- A new utility script
- For: Adding table to existing databases
- One-time: Only needs to run once

## Files Updated

- ✓ SETUP_SERVER.py (updated - now includes user_requests table)
- ✓ MIGRATE_ADD_USER_REQUESTS.py (new - migration script)
- ✓ Both are in installer_build\dist\ for future installs

## Next Steps

1. ✓ Run migration script OR update SETUP_SERVER.py
2. ✓ Test registration on client computer
3. ✓ See "Registration request submitted!" message
4. ✓ Done!

---

**Questions?** Check COMPLETE_DEPLOYMENT_GUIDE.md for more details.
