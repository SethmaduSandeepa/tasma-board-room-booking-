import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("bookings.db", timeout=30.0)
conn.execute("PRAGMA busy_timeout=30000")
cursor = conn.cursor()

# First, check all users in the database
print("=== ALL USERS IN DATABASE ===")
cursor.execute("SELECT id, username, full_name, role, department FROM users")
users = cursor.fetchall()

if users:
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Name: {user[2]}, Role: {user[3]}, Department: {user[4]}")
else:
    print("No users found in database")

print("\n=== TESTING LOGIN WITH DEPARTMENT RETRIEVAL ===")

# Test with sandeepa user (assuming it exists)
username = "sandeepa"
password = "sandeepa123"
hashed = hash_password(password)

print(f"Testing login for: {username}")

cursor.execute("SELECT id, role, department FROM users WHERE username=? AND password=? AND role='user'",
             (username, hashed))
result = cursor.fetchone()

if result:
    user_id = result[0]
    role = result[1]
    department = result[2]
    print(f"✓ LOGIN SUCCESSFUL!")
    print(f"  User ID: {user_id}")
    print(f"  Role: {role}")
    print(f"  Department: {department if department else 'None/Not set'}")
else:
    print(f"✗ Login failed - user not found or credentials incorrect")

conn.close()
