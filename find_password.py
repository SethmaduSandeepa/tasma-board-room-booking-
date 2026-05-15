import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("bookings.db", timeout=30.0)
conn.execute("PRAGMA busy_timeout=30000")
cursor = conn.cursor()

# Try different passwords for samarakoon
username = "samarakoon"
test_passwords = ["samarakoon123", "samarakoon", "password", "123456", "test123"]

print(f"=== TESTING LOGIN FOR {username} ===\n")

for password in test_passwords:
    hashed = hash_password(password)
    cursor.execute("SELECT id, role, department FROM users WHERE username=? AND password=? AND role='user'",
                 (username, hashed))
    result = cursor.fetchone()
    
    if result:
        print(f"✓ PASSWORD FOUND: {password}")
        print(f"  User ID: {result[0]}")
        print(f"  Role: {result[1]}")
        print(f"  Department: {result[2]}")
        break
    else:
        print(f"✗ Password '{password}' - Failed")

conn.close()
