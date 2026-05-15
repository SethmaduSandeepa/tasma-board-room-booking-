import sqlite3

# Migration script to add role column to users table and create user_requests table

conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()

try:
    # Check if role column exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'role' not in columns:
        print("Adding 'role' column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
        
        # Set admin role for users with id=1 (first user, usually admin)
        cursor.execute("UPDATE users SET role='admin' WHERE id=1")
        print("Updated first user to admin role")
    
    # Check if full_name column exists
    if 'full_name' not in columns:
        print("Adding 'full_name' column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
    
    # Create user_requests table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            full_name TEXT,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending'
        )
    ''')
    print("User requests table ready")
    
    conn.commit()
    print("Migration completed successfully!")
    
except Exception as e:
    print(f"Error during migration: {e}")
    conn.rollback()
finally:
    conn.close()
