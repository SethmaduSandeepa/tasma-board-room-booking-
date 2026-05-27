"""
TASMA - Database Migration for User Requests Table
Run this if you get "unable to open database file" error during registration

This script adds the missing user_requests table to existing databases
that were initialized with older versions of SETUP_SERVER.py
"""

import sqlite3
import os
import sys

def migrate_database(db_path=None):
    """Add missing user_requests table to database"""
    
    # Determine database path
    if db_path is None:
        # Try server location first
        server_db = r"C:\Users\Administrator\AppData\Roaming\TASMA\bookings.db"
        if os.path.exists(server_db):
            db_path = server_db
        else:
            # Try network path
            db_path = r"\\GVBSERVER\C$\Users\Administrator\AppData\Roaming\TASMA\bookings.db"
    
    print("="*70)
    print("TASMA - Database Migration")
    print("="*70)
    print(f"\nTarget Database: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"\n✗ Database file not found!")
        print(f"  Expected location: {db_path}")
        print(f"\n  Please run SETUP_SERVER.py first to initialize the database.")
        return False
    
    try:
        print(f"\nConnecting to database...")
        conn = sqlite3.connect(db_path, timeout=30)
        cursor = conn.cursor()
        
        # Check if user_requests table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_requests'")
        if cursor.fetchone():
            print(f"✓ user_requests table already exists")
            print(f"  No migration needed!")
            conn.close()
            return True
        
        # Add user_requests table
        print(f"\n  Adding user_requests table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                full_name TEXT,
                password TEXT NOT NULL,
                department TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        ''')
        conn.commit()
        
        # Verify it was created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_requests'")
        if cursor.fetchone():
            print(f"✓ user_requests table created successfully!")
            
            # List all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"\n✓ Database now contains {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")
        else:
            print(f"✗ Failed to create table")
            conn.close()
            return False
        
        conn.close()
        print(f"\n✓ Migration completed successfully!")
        print(f"\nNow you can:")
        print(f"  1. Users can register new accounts (registration requests)")
        print(f"  2. Admin can approve/deny requests")
        print(f"  3. Users can login with their approved accounts")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Migration failed: {str(e)}")
        print(f"\nPossible solutions:")
        print(f"  1. Check database file permissions")
        print(f"  2. Verify the database path is correct")
        print(f"  3. Try running as Administrator")
        print(f"  4. Check that SETUP_SERVER.py was run")
        return False

if __name__ == "__main__":
    print("\n")
    success = migrate_database()
    
    if success:
        print(f"\n✓ Ready to use!")
    else:
        print(f"\n✗ Migration incomplete")
        print(f"\nFor help, contact your system administrator")
    
    input("\nPress Enter to exit...")
