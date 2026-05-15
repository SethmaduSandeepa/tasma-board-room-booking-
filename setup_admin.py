import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()

# Check existing users
print("=== Current Users in Database ===")
cursor.execute("SELECT id, username, full_name, role FROM users")
users = cursor.fetchall()
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}, Name: {user[2]}, Role: {user[3]}")

print("\n=== Creating/Updating Admin Account ===")

admin_password = hash_password("admin")
print(f"Admin password hash: {admin_password}")

# Delete existing admin if any
cursor.execute("DELETE FROM users WHERE username='admin'")

# Insert new admin account
cursor.execute('''
    INSERT INTO users (username, full_name, password, role)
    VALUES (?, ?, ?, ?)
''', ("admin", "Administrator", admin_password, "admin"))

conn.commit()

# Verify
print("\nVerifying admin account...")
cursor.execute("SELECT username, role FROM users WHERE username='admin'")
admin = cursor.fetchone()
if admin:
    print(f"✓ Admin account created: {admin[0]} (role: {admin[1]})")
else:
    print("✗ Failed to create admin account")

conn.close()
