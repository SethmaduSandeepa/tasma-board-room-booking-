import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()

username = "sandeepa"
password = "sandeepa123"
hashed = hash_password(password)

print(f"Testing login for: {username}")
print(f"Password: {password}")

cursor.execute("SELECT id, role FROM users WHERE username=? AND password=? AND role='user'",
             (username, hashed))
result = cursor.fetchone()

if result:
    print(f"✓ LOGIN SUCCESSFUL!")
else:
    print(f"✗ Login failed")

conn.close()
