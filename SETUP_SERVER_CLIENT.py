#!/usr/bin/env python3
"""
TASMA Client Setup - Configure to connect to centralized server database
Guides user through connecting to the server database at GVBSERVER
"""

import os
import sys
import configparser
import sqlite3
import socket
import time

def test_network_path(server_path):
    """Test if network path is accessible"""
    try:
        # Try to access the path
        if os.path.exists(server_path):
            print(f"✓ Network path accessible: {server_path}")
            return True
        else:
            print(f"✗ Network path NOT found: {server_path}")
            return False
    except Exception as e:
        print(f"✗ Error accessing network path: {str(e)}")
        return False

def test_database_connection(db_path):
    """Test database connection"""
    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        conn.execute("PRAGMA busy_timeout=30000")
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        conn.close()
        
        print(f"✓ Database connection successful")
        print(f"  Found {user_count} users in database")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {str(e)}")
        return False

def create_client_config(db_path, config_file):
    """Create config.ini for client"""
    config = configparser.ConfigParser()
    
    config['Database'] = {
        'database_path': db_path,
        'db_timeout': '30',
        'connection_pool_size': '3',
        'enable_cache': 'true',
        'cache_ttl': '300'
    }
    
    config['Network'] = {
        'server_name': 'GVBSERVER',
        'is_client': 'true',
        'retry_attempts': '3',
        'retry_delay': '1'
    }
    
    config['User'] = {
        'theme': 'light',
        'auto_login': 'false',
        'notifications': 'true'
    }
    
    with open(config_file, 'w') as f:
        config.write(f)
    
    print(f"✓ Config file created: {config_file}")

def get_config_file():
    """Get the config file path"""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle - store in AppData
        app_data = os.getenv('APPDATA')
        config_dir = os.path.join(app_data, 'TASMA')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, 'config.ini')
    else:
        # Running as normal Python script
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

def main():
    print("=" * 70)
    print("TASMA - Client Server Connection Setup")
    print("=" * 70)
    print()
    
    # Server database path (fixed)
    server_db_path = r"\\GVBSERVER\C$\Users\Administrator\AppData\Roaming\TASMA\bookings.db"
    
    print("SERVER DATABASE CONFIGURATION")
    print("-" * 70)
    print(f"Server Name:    GVBSERVER")
    print(f"Database Path:  {server_db_path}")
    print()
    
    # Get config file location
    config_file = get_config_file()
    print(f"Client Config:  {config_file}")
    print()
    
    # Step 1: Test network accessibility
    print("STEP 1: Testing network path accessibility...")
    print("-" * 70)
    if not test_network_path(server_db_path):
        print()
        print("⚠ WARNING: Cannot access server database!")
        print()
        print("TROUBLESHOOTING:")
        print("1. Ensure you are connected to the network")
        print("2. Verify GVBSERVER is reachable: ping GVBSERVER")
        print("3. Check firewall settings")
        print("4. Ensure you have permissions to access the share")
        print("5. The server must be running TASMA with the database shared")
        print()
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            return
    print()
    
    # Step 2: Test database connection
    print("STEP 2: Testing database connection...")
    print("-" * 70)
    if not test_database_connection(server_db_path):
        print()
        print("⚠ WARNING: Cannot connect to database!")
        print()
        print("TROUBLESHOOTING:")
        print("1. Verify the database file exists at the path")
        print("2. Check that the database is not corrupted")
        print("3. Ensure no exclusive locks on the database")
        print("4. Try again after a few seconds")
        print()
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            return
    print()
    
    # Step 3: Create config file
    print("STEP 3: Creating client configuration...")
    print("-" * 70)
    create_client_config(server_db_path, config_file)
    print()
    
    # Step 4: Summary
    print("=" * 70)
    print("✓ CLIENT SETUP COMPLETE")
    print("=" * 70)
    print()
    print("Your TASMA client is now configured to connect to:")
    print(f"  {server_db_path}")
    print()
    print("NEXT STEPS:")
    print("1. Launch TASMA application")
    print("2. Login with your username and password")
    print("3. Your data will sync from the server database")
    print()
    print("NOTE:")
    print("- The server must be running with the database at the configured path")
    print("- Your login credentials must be created on the server")
    print("- All bookings will be stored on the server database")
    print("- Data syncs automatically when you login")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        sys.exit(1)
    
    input("\nPress Enter to exit...")
