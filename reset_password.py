import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()

# Reset sandeepa to a simple password "sandeepa123"
new_password = "sandeepa123"
hashed = hash_password(new_password)

cursor.execute("UPDATE users SET password=? WHERE username='sandeepa'", (hashed,))
cursor.execute("UPDATE user_requests SET password=? WHERE username='sandeepa'", (hashed,))
conn.commit()

print(f"✓ Reset sandeepa's password to: '{new_password}'")
print(f"  Password hash: {hashed}")

conn.close()
