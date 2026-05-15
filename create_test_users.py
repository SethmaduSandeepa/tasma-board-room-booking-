import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("bookings.db", timeout=30.0)
cursor = conn.cursor()

# Create test users
test_users = [
    ("testuser", "Test User", "test123", "IT"),
    ("john", "John Smith", "john123", "HR"),
    ("sarah", "Sarah Johnson", "sarah123", "Finance"),
]

for username, full_name, password, department in test_users:
    hashed_pass = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, full_name, password, department, role) VALUES (?, ?, ?, ?, ?)",
            (username, full_name, hashed_pass, department, "user")
        )
        print(f"✓ Created user: {username} (password: {password}, dept: {department})")
    except sqlite3.IntegrityError:
        print(f"✗ User {username} already exists")

conn.commit()
conn.close()

print("\nTest users created! You can now login with:")
print("  - Username: testuser, Password: test123")
print("  - Username: john, Password: john123")
print("  - Username: sarah, Password: sarah123")
