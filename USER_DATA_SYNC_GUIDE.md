# TASMA User Data Sync - Implementation Guide

## Overview

All user data is now synchronized with the centralized server database. This means:

✓ **Users sync across devices** - Log in on any computer, see the same data
✓ **Shared bookings** - All users see the same bookings
✓ **User profiles on server** - Names, emails, departments stored centrally
✓ **Activity tracking** - System logs all user actions
✓ **Preferences sync** - User preferences saved to server

---

## Database Tables

### 1. users
Stores all user account information

```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,           -- Login username
    password TEXT,                   -- Hashed password
    full_name TEXT,                  -- User's full name
    email TEXT,                      -- User email
    department TEXT,                 -- Department/team
    role TEXT,                       -- user, admin, manager
    phone TEXT,
    is_active INTEGER,               -- 1=active, 0=inactive
    last_login TIMESTAMP,            -- Last login time
    created_date TIMESTAMP,
    updated_date TIMESTAMP
)
```

### 2. user_preferences
Stores user preferences and settings

```sql
CREATE TABLE user_preferences (
    preference_id INTEGER PRIMARY KEY,
    user_id INTEGER,                -- Link to user
    theme TEXT,                      -- UI theme (light/dark)
    auto_refresh BOOLEAN,            -- Auto-refresh bookings
    notifications_enabled BOOLEAN,   -- Email notifications
    default_department TEXT,
    preferred_rooms TEXT,            -- JSON list of favorite rooms
    settings_json TEXT,              -- Custom settings
    updated_date TIMESTAMP
)
```

### 3. bookings
Stores all room bookings

```sql
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY,
    room_id INTEGER,                 -- Room being booked
    user_id INTEGER,                 -- User making booking
    booking_date DATE,               -- Date of booking
    start_time TEXT,                 -- Start time
    end_time TEXT,                   -- End time
    title TEXT,                      -- Meeting title
    description TEXT,
    status TEXT,                     -- confirmed, cancelled
    created_date TIMESTAMP,
    updated_date TIMESTAMP,
    created_by INTEGER               -- User who created booking
)
```

### 4. rooms
Stores room information

```sql
CREATE TABLE rooms (
    room_id INTEGER PRIMARY KEY,
    room_name TEXT UNIQUE,           -- Room name
    capacity INTEGER,                -- Room capacity
    location TEXT,                   -- Building/location
    amenities TEXT,                  -- Projector, whiteboard, etc.
    is_active INTEGER                -- 1=available, 0=unavailable
)
```

### 5. user_activity_log
Audit log of all user actions

```sql
CREATE TABLE user_activity_log (
    activity_id INTEGER PRIMARY KEY,
    user_id INTEGER,                 -- User performing action
    action TEXT,                     -- CREATE_BOOKING, DELETE_BOOKING, LOGIN, etc.
    details TEXT,                    -- Action details
    ip_address TEXT,
    timestamp TIMESTAMP
)
```

---

## Usage in Code

### Initialize User Data Sync

```python
from db_optimized import get_db
from user_data_sync import get_user_sync

# Get database and user sync
db = get_db()
user_sync = get_user_sync(db)

# Initialize tables
user_sync.init_user_tables()
```

### Create User Account

```python
user_id = user_sync.create_user(
    username="john.doe",
    password="hashed_password",
    full_name="John Doe",
    email="john@company.com",
    department="Sales",
    role="user"
)
```

### Login (Verify User)

```python
# Check credentials
if user_sync.verify_user_password("john.doe", "password"):
    user = user_sync.get_user_by_username("john.doe")
    user_id = user['user_id']
    
    # Update last login
    user_sync.update_last_login(user_id)
    
    # Log activity
    user_sync.log_activity(user_id, "LOGIN", "User logged in")
```

### Create Booking

```python
booking_id = user_sync.create_booking(
    room_id=1,
    user_id=user_id,
    booking_date="2026-05-25",
    start_time="10:00",
    end_time="11:00",
    title="Team Meeting",
    description="Weekly sync"
)
```

### Get User's Bookings

```python
bookings = user_sync.get_user_bookings(user_id)
# Returns list of all bookings for this user

# Or get bookings in date range
bookings = user_sync.get_user_bookings(
    user_id=user_id,
    date_from="2026-05-01",
    date_to="2026-05-31"
)
```

### Get All Bookings (Admin View)

```python
all_bookings = user_sync.get_all_bookings()
# Returns all bookings from all users

# Or get bookings for specific date range
all_bookings = user_sync.get_all_bookings(
    date_from="2026-05-01",
    date_to="2026-05-31"
)
```

### Update User Preferences

```python
user_sync.update_user_preferences(
    user_id=user_id,
    theme="dark",
    auto_refresh=True,
    notifications_enabled=True
)
```

### Get User Activity

```python
activity = user_sync.get_user_activity(user_id)
# Returns recent activity log for user
```

---

## Data Sync Flow

### User Login on Device A
```
1. User enters username/password
2. verify_user_password() checks server database
3. get_user_by_username() retrieves user data from server
4. update_last_login() records login time on server
5. log_activity() logs login event
6. User preferences loaded from server_preferences table
7. User bookings fetched from server_bookings table
```

### Same User Logs In on Device B
```
1. Same login process
2. Server returns same user data
3. Same bookings are visible
4. Same preferences applied
5. All new bookings created on Device B are stored on server
6. Other users immediately see the new bookings
```

### Booking Created by User A, Visible to User B
```
1. User A creates booking (stored in server database)
2. User B queries all_bookings() from server
3. User B sees booking from User A immediately
4. All users sync to the same database = unified view
```

---

## Benefits of Server-Side User Data

| Feature | Benefit |
|---------|---------|
| **Centralized users** | Add users once, all clients see them |
| **Synced bookings** | No conflicts, real-time updates |
| **User profiles** | Consistent user info across devices |
| **Activity logging** | Full audit trail of actions |
| **Multi-device** | User can work from multiple computers |
| **Team visibility** | All team members see shared calendar |

---

## Implementation Checklist

- [ ] SETUP_SERVER.py creates all user tables
- [ ] SETUP_USER.py initializes user_data_sync
- [ ] User registration creates entry in users table
- [ ] Login verifies against server users table
- [ ] Bookings stored in server database
- [ ] Preferences stored on server
- [ ] Activity logged for all actions
- [ ] All clients query same server database

---

## Example: Complete User Flow

```python
from db_optimized import get_db
from user_data_sync import get_user_sync

# Initialize
db = get_db()
user_sync = get_user_sync(db)
user_sync.init_user_tables()

# 1. CREATE USER (Admin/Registration)
user_id = user_sync.create_user(
    username="alice",
    password="hash123",
    full_name="Alice Smith",
    email="alice@company.com",
    department="Marketing",
    role="user"
)
# Result: User created and stored on server

# 2. USER LOGS IN
user = user_sync.get_user_by_username("alice")
user_sync.update_last_login(user['user_id'])
user_sync.log_activity(user['user_id'], "LOGIN")
# Result: Login recorded on server

# 3. USER CREATES BOOKING
booking_id = user_sync.create_booking(
    room_id=1,
    user_id=user['user_id'],
    booking_date="2026-05-25",
    start_time="10:00",
    end_time="11:00",
    title="Client Meeting"
)
# Result: Booking stored on server, visible to all users

# 4. ANOTHER USER SEES THE BOOKING
all_bookings = user_sync.get_all_bookings()
# Result: Returns all bookings including Alice's new booking

# 5. USER SETS PREFERENCES
user_sync.update_user_preferences(
    user_id=user['user_id'],
    theme="dark",
    auto_refresh=True
)
# Result: Preferences saved on server, apply everywhere user logs in

# 6. USER LOGS IN FROM DIFFERENT COMPUTER
# Same data is loaded because it's all on the server
prefs = user_sync.get_user_preferences(user['user_id'])
# Result: Same preferences, same bookings
```

---

## Key Points

✓ **All user data is on the server** - Not stored locally
✓ **Multiple devices access same data** - Login anywhere, see everything
✓ **Real-time updates** - Changes visible immediately to all users
✓ **Audit trail** - Activity log tracks all actions
✓ **Consistent state** - No data conflicts or sync issues

---

## Configuration in config.ini

The database path in config.ini determines where user data is stored:

```ini
[SERVER]
# For network deployment - all users connect to same database
database_path = \\SERVER_NAME\TASMA_Data\bookings.db

# For local development
# database_path = bookings.db
```

---

**Version:** 1.0
**Last Updated:** May 2026
