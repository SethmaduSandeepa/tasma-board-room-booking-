import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("bookings.db", timeout=30.0)
cursor = conn.cursor()

# Show all users
cursor.execute("SELECT id, username, role FROM users")
users = cursor.fetchall()
print("All users in database:")
for user in users:
    print(f"  ID: {user[0]}, Username: {user[1]}, Role: {user[2]}")

# Check if admin exists with correct password
admin_pass = hash_password("admin")
cursor.execute("SELECT id FROM users WHERE username='admin' AND password=?", (admin_pass,))
admin = cursor.fetchone()

if admin:
    print("\n✓ Admin user found with correct password!")
else:
    print("\n✗ Admin user not found or password incorrect")

conn.close()
