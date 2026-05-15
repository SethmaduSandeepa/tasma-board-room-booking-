import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Create/reset admin in bookings.db
conn = sqlite3.connect("bookings.db", timeout=30.0)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA busy_timeout=30000")
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        full_name TEXT,
        password TEXT NOT NULL,
        department TEXT,
        role TEXT DEFAULT 'user'
    )
''')

# Delete existing admin and recreate
cursor.execute("DELETE FROM users WHERE username='admin'")
admin_pass = hash_password("admin")
cursor.execute("INSERT INTO users (username, full_name, password, role) VALUES (?, ?, ?, ?)",
             ("admin", "Administrator", admin_pass, "admin"))

# Create bookings table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_date TEXT NOT NULL,
        booking_time TEXT NOT NULL,
        duration_minutes INTEGER DEFAULT 60,
        department TEXT NOT NULL,
        user_name TEXT NOT NULL,
        reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Create user_requests table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        full_name TEXT,
        password TEXT NOT NULL,
        department TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'pending'
    )
''')

conn.commit()
conn.close()

print("✓ Admin user created: username='admin', password='admin'")
