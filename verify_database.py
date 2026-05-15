import sqlite3
import os

# Get database path
app_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(app_dir, "bookings.db")

print(f"Checking database at: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}\n")

try:
    conn = sqlite3.connect(db_path, timeout=30.0)
    conn.execute("PRAGMA busy_timeout=30000")
    cursor = conn.cursor()
    
    # Check users table
    print("=" * 60)
    print("APPROVED USERS (in 'users' table):")
    print("=" * 60)
    cursor.execute("SELECT username, full_name, department, role FROM users ORDER BY username")
    users = cursor.fetchall()
    if users:
        for user in users:
            print(f"  Username: {user[0]:<15} | Name: {user[1]:<20} | Dept: {user[2]:<15} | Role: {user[3]}")
    else:
        print("  (No approved users found)")
    
    # Check pending requests
    print("\n" + "=" * 60)
    print("PENDING REQUESTS (in 'user_requests' table):")
    print("=" * 60)
    cursor.execute("SELECT username, full_name, department, status FROM user_requests WHERE status='pending' ORDER BY username")
    requests = cursor.fetchall()
    if requests:
        for req in requests:
            print(f"  Username: {req[0]:<15} | Name: {req[1]:<20} | Dept: {req[2]:<15} | Status: {req[3]}")
    else:
        print("  (No pending requests found)")
    
    # Check all request statuses
    print("\n" + "=" * 60)
    print("ALL REGISTRATION REQUESTS:")
    print("=" * 60)
    cursor.execute("SELECT username, full_name, status FROM user_requests ORDER BY username")
    all_reqs = cursor.fetchall()
    if all_reqs:
        for req in all_reqs:
            print(f"  Username: {req[0]:<15} | Name: {req[1]:<20} | Status: {req[2]}")
    else:
        print("  (No requests found)")
    
    conn.close()
    print("\n✅ Database check complete!")
    
except Exception as e:
    print(f"❌ Error checking database: {e}")
