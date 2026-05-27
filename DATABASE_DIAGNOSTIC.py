"""
TASMA - Database Diagnostic Tool
Check what users exist in the server database and debug login issues

Run this on the SERVER computer to verify user accounts
"""

import sqlite3
import hashlib
import sys

def hash_password(password, username=""):
    """Hash password same way as TASMA app"""
    salt = "tasma_salt_2024"
    return hashlib.sha256((username + password + salt).encode()).hexdigest()

def check_database():
    """Check database and list all users"""
    
    db_path = r"C:\Users\Administrator\AppData\Roaming\TASMA\bookings.db"
    
    print("="*70)
    print("TASMA DATABASE DIAGNOSTIC")
    print("="*70)
    print(f"\nDatabase: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path, timeout=10)
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("\n✗ ERROR: users table does not exist!")
            print("  Run SETUP_SERVER.py to create database")
            conn.close()
            return False
        
        print("\n✓ Database connected successfully")
        
        # List all tables
        print("\nDatabase Tables:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        for table in tables:
            print(f"  - {table}")
        
        # List all users
        print("\n" + "="*70)
        print("USERS IN DATABASE")
        print("="*70)
        
        cursor.execute("SELECT id, username, full_name, role, department FROM users ORDER BY id")
        users = cursor.fetchall()
        
        if not users:
            print("\n✗ NO USERS FOUND in database!")
            print("  Run ADD_USER_TO_SERVER.py to add users")
        else:
            print(f"\nFound {len(users)} user(s):\n")
            for user_id, username, full_name, role, department in users:
                print(f"  ID: {user_id}")
                print(f"    Username: {username}")
                print(f"    Full Name: {full_name}")
                print(f"    Role: {role}")
                print(f"    Department: {department}")
                print()
        
        # Check for pending registration requests
        print("="*70)
        print("PENDING REGISTRATION REQUESTS")
        print("="*70)
        
        cursor.execute("SELECT id, username, full_name, department, status FROM user_requests WHERE status='pending' ORDER BY created_at")
        requests = cursor.fetchall()
        
        if not requests:
            print("\n✓ No pending requests")
        else:
            print(f"\nFound {len(requests)} pending request(s):\n")
            for req_id, username, full_name, department, status in requests:
                print(f"  ID: {req_id}")
                print(f"    Username: {username}")
                print(f"    Full Name: {full_name}")
                print(f"    Department: {department}")
                print(f"    Status: {status}")
                print(f"  → Need to APPROVE in admin panel to activate")
                print()
        
        conn.close()
        return True
        
    except FileNotFoundError:
        print(f"\n✗ ERROR: Database file not found!")
        print(f"  Expected: {db_path}")
        print(f"\n  Solution:")
        print(f"    1. Check if TASMA is installed in: C:\\Program Files\\TASMA Board Room Booking System\\")
        print(f"    2. Run SETUP_SERVER.py to initialize database")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        return False

def test_login(username, password):
    """Test if a specific username/password works"""
    
    print("\n" + "="*70)
    print(f"TEST LOGIN: {username}")
    print("="*70)
    
    db_path = r"C:\Users\Administrator\AppData\Roaming\TASMA\bookings.db"
    
    try:
        conn = sqlite3.connect(db_path, timeout=10)
        cursor = conn.cursor()
        
        # Hash the password
        hashed_password = hash_password(password, username)
        print(f"\nPassword hash for '{password}': {hashed_password[:16]}...")
        
        # Try to find user
        cursor.execute("SELECT id, username, full_name, role FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        
        if not user:
            print(f"\n✗ Username '{username}' NOT FOUND in database")
            print(f"  Check spelling and capitalization")
        else:
            user_id, found_username, full_name, role = user
            print(f"\n✓ User found!")
            print(f"  Username: {found_username}")
            print(f"  Full Name: {full_name}")
            print(f"  Role: {role}")
            
            # Check password
            cursor.execute("SELECT password FROM users WHERE id=?", (user_id,))
            stored_hash = cursor.fetchone()[0]
            
            print(f"\nStored hash: {stored_hash[:16]}...")
            
            if stored_hash == hashed_password:
                print(f"✓ PASSWORD MATCHES!")
                print(f"\n✓✓ Login should work!")
            else:
                print(f"✗ PASSWORD DOES NOT MATCH")
                print(f"\nSolution:")
                print(f"  1. Run ADD_USER_TO_SERVER.py again")
                print(f"  2. When prompted for password, enter: {password}")
                print(f"  3. Choose 'yes' to overwrite if user already exists")
        
        conn.close()
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")

if __name__ == "__main__":
    # First, check database and list users
    success = check_database()
    
    if success:
        # If user wants to test specific login
        print("\n" + "="*70)
        response = input("Test a specific login? (yes/no): ").strip().lower()
        if response == 'yes':
            username = input("  Username: ").strip()
            password = input("  Password: ").strip()
            test_login(username, password)
    
    print("\n" + "="*70)
    print("TROUBLESHOOTING CHECKLIST")
    print("="*70)
    print("\nIf users still can't login:")
    print("  1. ✓ User exists in database (see list above)")
    print("  2. ✓ Username spelling matches exactly (case-sensitive)")
    print("  3. ✓ Password is correct (you typed it when running ADD_USER_TO_SERVER.py)")
    print("  4. ✓ Role is 'user' (not blank or 'admin')")
    print("  5. ✓ Client connects to server database (check console in TASMA)")
    print("\nIf problems persist:")
    print("  - Delete user and recreate with ADD_USER_TO_SERVER.py")
    print("  - Restart TASMA app on client computer")
    print("  - Check network connection: ping GVBSERVER")
    print("  - Verify C$ admin share is accessible")
    
    input("\nPress Enter to exit...")
