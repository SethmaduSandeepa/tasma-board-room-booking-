import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()

# Get sandeepa's approved password from user_requests
cursor.execute("SELECT password FROM user_requests WHERE username='sandeepa'")
result = cursor.fetchone()

if result:
    correct_password_hash = result[0]
    print(f"Found sandeepa's password hash in requests: {correct_password_hash}")
    
    # Update sandeepa in users table with correct password and role='user'
    cursor.execute("UPDATE users SET password=?, role='user' WHERE username='sandeepa'",
                 (correct_password_hash,))
    conn.commit()
    print("✓ Updated sandeepa's password and role to 'user'")
else:
    print("✗ Could not find sandeepa's password in requests")

conn.close()
