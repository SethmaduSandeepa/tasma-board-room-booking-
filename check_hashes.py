import sqlite3

conn = sqlite3.connect("bookings.db", timeout=30.0)
conn.execute("PRAGMA busy_timeout=30000")
cursor = conn.cursor()

# Check what's stored in the database
print("=== ALL USERS WITH PASSWORD HASHES ===\n")
cursor.execute("SELECT username, password FROM users")
users = cursor.fetchall()

for username, password_hash in users:
    print(f"Username: {username}")
    print(f"Password Hash: {password_hash}")
    print()

conn.close()
