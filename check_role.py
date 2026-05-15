import sqlite3

db_path = "bookings.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Get all user details
c.execute("SELECT username, role, department FROM users WHERE username='sandeepa'")
result = c.fetchone()

if result:
    username, role, department = result
    print(f"Username: {username}")
    print(f"Role: {role}")
    print(f"Department: {department}")
    print(f"\nLogin will succeed if role='user': {role == 'user'}")
else:
    print("sandeepa not found in users table")

conn.close()
