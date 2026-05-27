#!/usr/bin/env python3
"""
TASMA - Add User to Server Database
This script adds a user account to the server database
Run this on the SERVER COMPUTER
"""

import sqlite3
import hashlib
import os
import sys

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user_to_server(username, password, full_name, department):
    """Add a user to the server database"""
    
    server_db_path = r"C:\Users\Administrator\AppData\Roaming\TASMA\bookings.db"
    
    print("=" * 70)
    print("TASMA - Add User to Server Database")
    print("=" * 70)
    print()
    
    # Check if database exists
    if not os.path.exists(server_db_path):
        print(f"✗ ERROR: Database not found at {server_db_path}")
        print()
        print("Make sure TASMA has been set up on the server first.")
        return False
    
    try:
        # Connect to server database
        conn = sqlite3.connect(server_db_path, timeout=30.0)
        conn.execute("PRAGMA busy_timeout=30000")
        cursor = conn.cursor()
        
        print(f"✓ Connected to server database")
        print(f"  Path: {server_db_path}")
        print()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("✗ ERROR: 'users' table not found in database")
            print("  Run SETUP_SERVER.py to initialize the database first")
            conn.close()
            return False
        
        print("✓ Found 'users' table")
        
        # Check if user already exists
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print(f"⚠ User '{username}' already exists")
            response = input("Overwrite password? (y/n): ").strip().lower()
            if response == 'y':
                hashed_pwd = hash_password(password)
                cursor.execute("""
                    UPDATE users 
                    SET password_hash = ?, updated_at = datetime('now')
                    WHERE username = ?
                """, (hashed_pwd, username))
                conn.commit()
                print(f"✓ Password updated for user '{username}'")
            else:
                print("  No changes made")
            conn.close()
            return True
        
        # Add new user
        print()
        print(f"Adding new user...")
        print(f"  Username: {username}")
        print(f"  Full Name: {full_name}")
        print(f"  Department: {department}")
        print()
        
        hashed_pwd = hash_password(password)
        
        cursor.execute("""
            INSERT INTO users (username, password_hash, full_name, department, approved, created_at)
            VALUES (?, ?, ?, ?, 1, datetime('now'))
        """, (username, hashed_pwd, full_name, department))
        
        conn.commit()
        
        # Verify user was added
        cursor.execute("SELECT id, username, full_name FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user:
            print(f"✓ User created successfully!")
            print(f"  ID: {user[0]}")
            print(f"  Username: {user[1]}")
            print(f"  Name: {user[2]}")
            print()
            print(f"User can now login with:")
            print(f"  Username: {username}")
            print(f"  Password: {password}")
            conn.close()
            return True
        else:
            print("✗ ERROR: User was not created")
            conn.close()
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def main():
    """Main function"""
    
    # Get user input
    print("=" * 70)
    print("TASMA - Add User to Server Database")
    print("=" * 70)
    print()
    print("This will add a user account to the server database.")
    print("Run this script on the SERVER COMPUTER.")
    print()
    
    username = input("Username (e.g., sandeepa): ").strip()
    if not username:
        print("✗ Username cannot be empty")
        return
    
    password = input("Password (e.g., password123): ").strip()
    if not password:
        print("✗ Password cannot be empty")
        return
    
    full_name = input("Full Name (e.g., Sandeepa Kumar): ").strip()
    if not full_name:
        full_name = username
    
    department = input("Department (e.g., IT): ").strip()
    if not department:
        department = "General"
    
    print()
    
    # Add user
    success = add_user_to_server(username, password, full_name, department)
    
    if success:
        print()
        print("=" * 70)
        print("✓ USER ADDED SUCCESSFULLY")
        print("=" * 70)
    else:
        print()
        print("=" * 70)
        print("✗ FAILED TO ADD USER")
        print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        sys.exit(1)
    
    input("\nPress Enter to exit...")
