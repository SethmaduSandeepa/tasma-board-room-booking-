import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()

print("=== USERS TABLE (Approved Users) ===")
cursor.execute("SELECT id, username, full_name, role FROM users")
users = cursor.fetchall()
for user in users:
    print(f"ID: {user[0]}, Username: '{user[1]}', Name: {user[2]}, Role: {user[3]}")

print("\n=== USER_REQUESTS TABLE (Pending/Approved Requests) ===")
cursor.execute("SELECT id, username, full_name, status FROM user_requests")
requests = cursor.fetchall()
for req in requests:
    print(f"ID: {req[0]}, Username: '{req[1]}', Name: {req[2]}, Status: {req[3]}")

print("\n=== Testing Login with sandeepa ===")
username = "sandeepa"
password = "sandeepa"
hashed = hash_password(password)
print(f"Username: {username}")
print(f"Password hash: {hashed}")

cursor.execute("SELECT id, role FROM users WHERE username=? AND password=? AND role='user'",
             (username, hashed))
result = cursor.fetchone()

if result:
    print(f"✓ Login would succeed! ID: {result[0]}, Role: {result[1]}")
else:
    print(f"✗ Login would FAIL!")
    
    # Debug why
    cursor.execute("SELECT username, role FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if user:
        print(f"  - Found user: {user[0]}, role: {user[1]}")
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        stored_pass = cursor.fetchone()
        if stored_pass:
            print(f"  - Stored password hash: {stored_pass[0]}")
            print(f"  - Login password hash:  {hashed}")
            print(f"  - Hashes match: {stored_pass[0] == hashed}")
    else:
        print(f"  - User '{username}' NOT found in users table!")

conn.close()
