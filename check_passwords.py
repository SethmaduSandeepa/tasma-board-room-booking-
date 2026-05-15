import sqlite3
import hashlib

db_path = "bookings.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Get sandeepa from both tables
print("Checking sandeepa records:\n")

c.execute("SELECT username, password FROM users WHERE username='sandeepa'")
result = c.fetchone()
if result:
    print(f"✓ Users table (approved users):")
    print(f"  Username: {result[0]}")
    print(f"  Password hash: {result[1][:20]}...")
else:
    print("✗ sandeepa NOT found in users table")

c.execute("SELECT username, password FROM user_requests WHERE username='sandeepa'")
result = c.fetchone()
if result:
    print(f"\n✓ User_requests table (pending approval):")
    print(f"  Username: {result[0]}")
    print(f"  Password hash: {result[1][:20]}...")
else:
    print("\n✗ sandeepa NOT found in user_requests table")

# Test password hashing
print(f"\n\nPassword hashing test:")
test_password = "123456"  # Try common password
hashed = hashlib.sha256(test_password.encode()).hexdigest()
print(f"  If password was '123456', hash would be: {hashed[:20]}...")

conn.close()
