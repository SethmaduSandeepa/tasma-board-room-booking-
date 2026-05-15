import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()

# Get what's stored for sandeepa
cursor.execute("SELECT password FROM user_requests WHERE username='sandeepa'")
result = cursor.fetchone()
stored_hash = result[0]
print(f"Password hash in user_requests: {stored_hash}")

# Try different passwords
test_passwords = ["sandeepa", "123456", "password"]
for pwd in test_passwords:
    test_hash = hash_password(pwd)
    match = "✓ MATCH!" if test_hash == stored_hash else ""
    print(f"  Password '{pwd}': {test_hash} {match}")

# Also check the actual raw data
print("\n=== Raw data in user_requests ===")
cursor.execute("SELECT username, full_name, password FROM user_requests WHERE username='sandeepa'")
user = cursor.fetchone()
print(f"Username: {user[0]}")
print(f"Full Name: {user[1]}")
print(f"Password: {user[2]}")

conn.close()
