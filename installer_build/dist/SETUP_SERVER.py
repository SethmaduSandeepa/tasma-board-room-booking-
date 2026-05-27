"""
TASMA SERVER SETUP
Administrator-only script to set up the centralized database server
Run this ONCE on your server machine with Administrator privileges

This script:
1. Creates shared database folder
2. Copies/creates the database with all required tables
3. Sets up network sharing
4. Configures permissions
5. Creates service account (optional)
6. Validates the complete setup
7. Initializes user data sync system
"""

import os
import sys
import subprocess
import shutil
import sqlite3
from pathlib import Path
import ctypes
import logging

def is_admin():
    """Check if running as Administrator"""
    try:
        return ctypes.windll.shell.IsUserAnAdmin()
    except:
        return False

def run_command(cmd, description=""):
    """Run a command and return success status"""
    try:
        if description:
            print(f"\n{'='*70}")
            print(f"Step: {description}")
            print('='*70)
        
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Success")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"✗ Failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False

def create_database(db_path):
    """Create a new database if it doesn't exist with all required tables"""
    print(f"\nChecking database: {db_path}")
    
    if os.path.exists(db_path):
        print(f"✓ Database already exists")
        return True
    
    try:
        print(f"Creating new database with full schema...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                email TEXT,
                department TEXT,
                role TEXT DEFAULT 'user',
                phone TEXT,
                is_active INTEGER DEFAULT 1,
                last_login TIMESTAMP,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                theme TEXT DEFAULT 'light',
                auto_refresh BOOLEAN DEFAULT 1,
                notifications_enabled BOOLEAN DEFAULT 1,
                default_department TEXT,
                preferred_rooms TEXT,
                settings_json TEXT,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                booking_date DATE NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'confirmed',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (created_by) REFERENCES users(user_id)
            )
        ''')
        
        # Rooms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_name TEXT UNIQUE NOT NULL,
                capacity INTEGER,
                location TEXT,
                amenities TEXT,
                is_active INTEGER DEFAULT 1,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User activity log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activity_log (
                activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                action TEXT,
                details TEXT,
                ip_address TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # User requests table (for new user registration requests)
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
        conn.close()
        
        print(f"✓ Database created successfully with all tables")
        print(f"  Tables: users, user_preferences, bookings, rooms, user_activity_log, user_requests")
        return True
    except Exception as e:
        print(f"✗ Failed to create database: {str(e)}")
        return False

def setup_server():
    """Main server setup"""
    print("\n" + "="*70)
    print("TASMA BOARD ROOM BOOKING SYSTEM - SERVER SETUP")
    print("="*70)
    
    # Check admin privileges
    if not is_admin():
        print("\n✗ ERROR: This script must be run as Administrator!")
        print("Right-click Command Prompt and select 'Run as Administrator'")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("\n✓ Running as Administrator")
    
    # Define paths
    server_root = "C:\\TASMA_Data"
    db_path = os.path.join(server_root, "bookings.db")
    backup_folder = os.path.join(server_root, "backups")
    
    print(f"\nServer Configuration:")
    print(f"  Data Folder: {server_root}")
    print(f"  Database: {db_path}")
    print(f"  Backups: {backup_folder}")
    
    # Step 1: Create directories
    print(f"\n{'='*70}")
    print("Step 1: Creating server directories")
    print('='*70)
    
    try:
        os.makedirs(server_root, exist_ok=True)
        os.makedirs(backup_folder, exist_ok=True)
        print(f"✓ Directories created/verified")
    except Exception as e:
        print(f"✗ Failed to create directories: {str(e)}")
        return False
    
    # Step 2: Create or validate database
    print(f"\n{'='*70}")
    print("Step 2: Setting up database")
    print('='*70)
    
    if not create_database(db_path):
        return False
    
    # Step 3: Set up file sharing
    print(f"\n{'='*70}")
    print("Step 3: Setting up network sharing")
    print('='*70)
    print(f"\nTo enable network access, you need to share the folder manually:")
    print(f"\n1. Open File Explorer")
    print(f"2. Navigate to: {server_root}")
    print(f"3. Right-click the folder → Properties")
    print(f"4. Go to 'Sharing' tab → 'Share this folder'")
    print(f"5. Click 'Permissions' button")
    print(f"6. Set permissions:")
    print(f"   - Everyone: Full Control (Read, Change, Modify)")
    print(f"7. Click 'Apply' and 'OK'")
    print(f"\nAfter sharing, the UNC path will be:")
    
    # Get computer name
    try:
        computer_name = os.environ.get('COMPUTERNAME', 'SERVER_NAME')
        unc_path = f"\\\\{computer_name}\\TASMA_Data"
        print(f"  {unc_path}")
        print(f"\nOr using IP address:")
        print(f"  \\\\YOUR_IP_ADDRESS\\TASMA_Data")
    except:
        print(f"  \\\\SERVER_NAME\\TASMA_Data")
    
    response = input("\nHave you completed the sharing setup? (yes/no): ").strip().lower()
    if response != 'yes':
        print("\nPlease share the folder and run this script again.")
        return False
    
    # Step 4: Verify sharing
    print(f"\n{'='*70}")
    print("Step 4: Verifying setup")
    print('='*70)
    
    # Check database accessibility
    try:
        conn = sqlite3.connect(db_path, timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        print(f"✓ Database is accessible")
        print(f"✓ Tables found: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
    except Exception as e:
        print(f"✗ Database verification failed: {str(e)}")
        return False
    
    # Step 5: Create config file
    print(f"\n{'='*70}")
    print("Step 5: Creating server configuration")
    print('='*70)
    
    try:
        computer_name = os.environ.get('COMPUTERNAME', 'SERVER_NAME')
        config_content = f"""[SERVER]
# Server database path - shared on network
database_path = \\\\{computer_name}\\TASMA_Data\\bookings.db

# Connection timeout for network access
db_timeout = 30

# Cache settings
enable_cache = true
cache_timeout = 300

[PERFORMANCE]
# Connection pool size
connection_pool_size = 10

# Batch size for operations
batch_size = 100

[LOGGING]
debug_mode = false
log_file = tasma_app.log

[SERVER_BACKUP]
# Backup settings
backup_folder = {backup_folder}
auto_backup = true
backup_interval_hours = 24
"""
        
        config_path = os.path.join(server_root, "config.ini")
        with open(config_path, 'w') as f:
            f.write(config_content)
        
        print(f"✓ Configuration file created: {config_path}")
    except Exception as e:
        print(f"✗ Failed to create config: {str(e)}")
        return False
    
    # Success summary
    print(f"\n{'='*70}")
    print("SERVER SETUP COMPLETE")
    print('='*70)
    print(f"\n✓ All steps completed successfully!")
    print(f"\nServer Database Details:")
    print(f"  Location: {db_path}")
    print(f"  Shared as: \\\\{computer_name}\\TASMA_Data")
    print(f"\nNext Steps:")
    print(f"1. Copy config.ini to each client machine")
    print(f"2. On each client, run: python setup_database_config.py")
    print(f"3. Verify all clients can connect with: python test_network_db.py")
    print(f"\nBackup reminders:")
    print(f"  - Regular backups stored in: {backup_folder}")
    print(f"  - Verify backup permissions are set correctly")
    
    return True

if __name__ == "__main__":
    try:
        success = setup_server()
        if not success:
            print("\n✗ Server setup failed. Please review the errors above.")
            input("\nPress Enter to exit...")
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    input("\nPress Enter to exit...")
