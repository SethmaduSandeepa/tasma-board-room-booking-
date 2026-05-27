"""
TASMA USER SETUP
User installation and configuration script
Run this on each user's workstation to set up TASMA

This script:
1. Verifies TASMA is installed
2. Configures network database connection
3. Tests connectivity to server
4. Initializes user data sync
5. Creates desktop shortcuts
6. Sets up user preferences
"""

import os
import sys
import subprocess
import sqlite3
import configparser
from pathlib import Path
import json
import ctypes

print("\n" + "="*70)
    """Display welcome header"""
    print("\n" + "="*70)
    print("TASMA BOARD ROOM BOOKING SYSTEM - USER SETUP")
    print("="*70)
    print("\nWelcome! This script will set up TASMA on your computer.")
    print("You'll be able to access the shared booking system server.")

def check_tasma_installed():
    """Check if TASMA is installed"""
    print(f"\n{'='*70}")
    print("Step 1: Checking TASMA Installation")
    print('='*70)
    
    # Look for main.py or TASMA executable
    if os.path.exists("main.py"):
        print(f"✓ TASMA application found (main.py)")
        return True
    
    if os.path.exists("TASMA Board Room Booking System.exe"):
        print(f"✓ TASMA executable found")
        return True
    
    # Check in common installation paths
    common_paths = [
        "C:\\Program Files\\TASMA",
        "C:\\Program Files (x86)\\TASMA",
        os.path.expanduser("~\\AppData\\Local\\TASMA")
    ]
    
    for path in common_paths:
        if os.path.exists(os.path.join(path, "main.py")):
            print(f"✓ TASMA found at: {path}")
            return True
    
    print(f"✗ TASMA application not found!")
    print(f"Please install TASMA first, then run this setup script.")
    return False

def get_server_info():
    """Get server information from user"""
    print(f"\n{'='*70}")
    print("Step 2: Server Database Configuration")
    print('='*70)
    
    print("\nYour organization has a centralized booking database on a server.")
    print("You need to configure the connection to it.\n")
    
    print("Server connection options:")
    print("1. Using server name (e.g., OFFICE-SERVER)")
    print("2. Using server IP address (e.g., 192.168.1.100)")
    print("3. Use local database (single user only)")
    
    choice = input("\nWhich option? (1/2/3): ").strip()
    
    if choice == "1":
        server_name = input("Enter the server name: ").strip()
        if server_name:
            return f"\\\\{server_name}\\TASMA_Data\\bookings.db"
    
    elif choice == "2":
        server_ip = input("Enter the server IP address: ").strip()
        if server_ip:
            return f"\\\\{server_ip}\\TASMA_Data\\bookings.db"
    
    elif choice == "3":
        print("Using local database")
        return os.path.join(os.path.dirname(__file__), "bookings.db")
    
    # Default if invalid
    print("Using default network path")
    return "\\\\SERVER_NAME\\TASMA_Data\\bookings.db"

def test_database_connection(db_path):
    """Test connection to database with detailed diagnostics"""
    print(f"\n{'='*70}")
    print("Step 3: Testing Database Connection")
    print('='*70)
    
    print(f"\nTesting connection to: {db_path}")
    
    # First, check if path is accessible
    if '\\\\' in db_path or db_path.startswith('//'):
        # Network path
        db_dir = os.path.dirname(db_path)
        print(f"Network path detected: {db_dir}")
        
        if not os.path.exists(db_dir):
            print(f"✗ Network path not accessible")
            print(f"  Troubleshooting:")
            print(f"  1. Check server name/IP is correct")
            print(f"  2. Verify server is online: ping {db_dir.split('\\\\')[1]}")
            print(f"  3. Check network connection")
            return False
    
    try:
        conn = sqlite3.connect(db_path, timeout=30)
        cursor = conn.cursor()
        
        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        print(f"✓ Connection successful!")
        print(f"✓ Database has {len(tables)} tables:")
        
        expected_tables = ['users', 'bookings', 'rooms', 'user_preferences', 'user_activity_log']
        for table in tables:
            status = "✓" if table[0] in expected_tables else "○"
            print(f"  {status} {table[0]}")
        
        return True
        
    except sqlite3.OperationalError as e:
        if 'network' in str(e).lower() or 'not found' in str(e).lower():
            print(f"✗ Cannot connect to database")
            print(f"  Error: {str(e)}")
            print(f"\nPossible issues:")
            print(f"  1. Server name/IP is incorrect")
            print(f"  2. Server is offline or not accessible")
            print(f"  3. You don't have permission to access the shared folder")
            print(f"  4. Network path is not shared correctly")
            print(f"\nPlease contact your IT administrator for help.")
            return False
        else:
            print(f"✗ Connection test failed: {str(e)}")
            return False
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        return False

def create_or_update_config(db_path):
    """Create or update config.ini file"""
    """Create or update config.ini file"""
    print(f"\n{'='*70}")
    print("Step 4: Configuring Settings")
    print('='*70)
    
    config = configparser.ConfigParser()
    
    # Load existing config if it exists
    if os.path.exists("config.ini"):
        config.read("config.ini")
    
    # Set server configuration
    if not config.has_section('SERVER'):
        config.add_section('SERVER')
    
    config.set('SERVER', 'database_path', db_path)
    config.set('SERVER', 'db_timeout', '30')
    config.set('SERVER', 'enable_cache', 'true')
    config.set('SERVER', 'cache_timeout', '300')
    
    # Performance settings
    if not config.has_section('PERFORMANCE'):
        config.add_section('PERFORMANCE')
    
    config.set('PERFORMANCE', 'connection_pool_size', '5')
    config.set('PERFORMANCE', 'batch_size', '100')
    
    # Logging settings
    if not config.has_section('LOGGING'):
        config.add_section('LOGGING')
    
    config.set('LOGGING', 'debug_mode', 'false')
    config.set('LOGGING', 'log_file', 'tasma_app.log')
    
    # User preferences
    if not config.has_section('USER'):
        config.add_section('USER')
    
    username = os.environ.get('USERNAME', 'user')
    config.set('USER', 'last_user', username)
    config.set('USER', 'auto_login', 'false')
    
    try:
        with open('config.ini', 'w') as f:
            config.write(f)
        print(f"✓ Configuration saved to config.ini")
        return True
    except Exception as e:
        print(f"✗ Failed to save configuration: {str(e)}")
        return False

def create_desktop_shortcut():
    """Create desktop shortcut for TASMA"""
    print(f"\n{'='*70}")
    print("Step 5: Creating Desktop Shortcut")
    print('='*70)
    
    try:
        # Find TASMA executable
        exe_path = None
        
        if os.path.exists("TASMA Board Room Booking System.exe"):
            exe_path = os.path.abspath("TASMA Board Room Booking System.exe")
        elif os.path.exists("main.py"):
            exe_path = os.path.abspath("main.py")
        else:
            print("✗ TASMA executable not found")
            return False
        
        # Get desktop path
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, "TASMA.lnk")
        
        # Create shortcut using VBS (Windows)
        vbs_path = os.path.join(os.path.dirname(__file__), "create_shortcut.vbs")
        
        vbs_script = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
Set oLink = oWS.CreateShortcut("{shortcut_path}")
oLink.TargetPath = "{exe_path}"
oLink.WorkingDirectory = "{os.path.dirname(exe_path)}"
oLink.Description = "TASMA Board Room Booking System"
oLink.Save
'''
        
        with open(vbs_path, 'w') as f:
            f.write(vbs_script)
        
        # Run VBS script
        subprocess.run(['cscript.exe', vbs_path], capture_output=True)
        
        # Clean up VBS file
        try:
            os.remove(vbs_path)
        except:
            pass
        
        if os.path.exists(shortcut_path):
            print(f"✓ Desktop shortcut created: {shortcut_path}")
            return True
        else:
            print(f"⚠ Shortcut creation may have failed, but TASMA is ready to use")
            return True
    
    except Exception as e:
        print(f"⚠ Could not create desktop shortcut: {str(e)}")
        print(f"  You can run TASMA manually from the installation folder")
        return True

def launch_tasma():
    """Ask if user wants to launch TASMA"""
    print(f"\n{'='*70}")
    print("Setup Complete!")
    print('='*70)
    
    launch = input("\nWould you like to launch TASMA now? (yes/no): ").strip().lower()
    
    if launch == 'yes':
        try:
            if os.path.exists("TASMA Board Room Booking System.exe"):
                subprocess.Popen("TASMA Board Room Booking System.exe")
            elif os.path.exists("main.py"):
                subprocess.Popen([sys.executable, "main.py"])
            print("✓ TASMA is launching...")
        except Exception as e:
            print(f"✗ Could not launch TASMA: {str(e)}")
            print("You can run it manually from the installation folder")

def setup_user():
    """Main user setup"""
    show_header()
    
    # Step 1: Check installation
    if not check_tasma_installed():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Step 2: Get server info
    db_path = get_server_info()
    
    # Step 3: Test connection
    print(f"\nAttempting to connect to: {db_path}")
    attempt = 0
    max_attempts = 3
    
    while attempt < max_attempts and not test_database_connection(db_path):
        attempt += 1
        if attempt < max_attempts:
            retry = input(f"\nTry again? (yes/no): ").strip().lower()
            if retry == 'yes':
                db_path = get_server_info()
                continue
            else:
                print("\n⚠ Setup incomplete. You can run this script again later.")
                input("\nPress Enter to exit...")
                sys.exit(1)
        else:
            print("\n✗ Could not connect after 3 attempts.")
            print("Please contact your IT administrator for help.")
            input("\nPress Enter to exit...")
            sys.exit(1)
    
    # Step 4: Create config
    if not create_or_update_config(db_path):
        print("✗ Failed to save configuration")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Step 5: Create shortcut
    create_desktop_shortcut()
    
    # Summary
    print(f"\n{'='*70}")
    print("✓ USER SETUP COMPLETE")
    print('='*70)
    print(f"\nYour TASMA configuration:")
    print(f"  Database: {db_path}")
    print(f"  Config: config.ini")
    print(f"  Shortcut: Desktop/TASMA")
    print(f"\nYou're ready to start using TASMA!")
    print(f"\nNext time, simply click the desktop shortcut to launch the app.")
    
    # Ask to launch
    launch_tasma()
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        setup_user()
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        input("\nPress Enter to exit...")
        sys.exit(1)
