"""
Test Network Database Connection
Validates that the app can connect to the server database
Run this on the client machine to verify network database setup
"""
import sqlite3
import os
import configparser
from pathlib import Path
import sys

class DatabaseConnectionTester:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = self._load_config()
        self.db_path = self._get_db_path()
        self.results = []
        
    def _load_config(self):
        """Load configuration from ini file"""
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
        else:
            self._log("WARNING", f"Config file not found: {self.config_file}")
        return config
    
    def _get_db_path(self):
        """Get database path from config"""
        return self.config.get('SERVER', 'database_path', fallback='E:\\tasma_booking_syst\\bookings.db')
    
    def _log(self, level, message):
        """Log test results"""
        msg = f"[{level}] {message}"
        print(msg)
        self.results.append(msg)
    
    def test_path_exists(self):
        """Test 1: Check if database path exists"""
        self._log("INFO", f"Testing database path: {self.db_path}")
        
        try:
            if os.path.exists(self.db_path):
                self._log("PASS", f"✓ Database file exists at {self.db_path}")
                return True
            else:
                self._log("FAIL", f"✗ Database file NOT found at {self.db_path}")
                return False
        except Exception as e:
            self._log("ERROR", f"✗ Error checking path: {str(e)}")
            return False
    
    def test_network_path_format(self):
        """Test 2: Validate network path format"""
        if '\\\\' in self.db_path or self.db_path.startswith('//'):
            self._log("PASS", f"✓ Valid network path format detected")
            
            # Parse UNC path
            parts = self.db_path.replace('//', '\\\\').split('\\\\')
            if len(parts) >= 4:
                server = parts[1]
                share = parts[2]
                self._log("INFO", f"  Server: {server}, Share: {share}")
                return True
        else:
            self._log("INFO", "Local database path (not a network path)")
            return True
    
    def test_database_readability(self):
        """Test 3: Test reading from database"""
        try:
            db_timeout = int(self.config.get('SERVER', 'db_timeout', fallback=30))
            self._log("INFO", f"Connection timeout: {db_timeout} seconds")
            
            conn = sqlite3.connect(self.db_path, timeout=db_timeout)
            cursor = conn.cursor()
            
            # Try to read from database
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            conn.close()
            
            if tables:
                self._log("PASS", f"✓ Database is readable. Found {len(tables)} tables")
                for table in tables:
                    self._log("INFO", f"  - Table: {table[0]}")
                return True
            else:
                self._log("WARN", "Database is readable but appears empty (no tables)")
                return True
                
        except sqlite3.DatabaseError as e:
            self._log("FAIL", f"✗ Database is corrupted or locked: {str(e)}")
            return False
        except sqlite3.OperationalError as e:
            self._log("FAIL", f"✗ Cannot connect to database: {str(e)}")
            return False
        except Exception as e:
            self._log("ERROR", f"✗ Unexpected error: {str(e)}")
            return False
    
    def test_database_writability(self):
        """Test 4: Test writing to database"""
        try:
            db_timeout = int(self.config.get('SERVER', 'db_timeout', fallback=30))
            conn = sqlite3.connect(self.db_path, timeout=db_timeout)
            cursor = conn.cursor()
            
            # Create a test table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS connection_test (
                    id INTEGER PRIMARY KEY,
                    test_time TEXT,
                    status TEXT
                )
            ''')
            
            # Try to insert
            from datetime import datetime
            cursor.execute(
                "INSERT INTO connection_test (test_time, status) VALUES (?, ?)",
                (datetime.now().isoformat(), "test")
            )
            conn.commit()
            
            # Clean up
            cursor.execute("DELETE FROM connection_test WHERE status = 'test'")
            conn.commit()
            
            conn.close()
            
            self._log("PASS", f"✓ Database is writable")
            return True
            
        except sqlite3.OperationalError as e:
            if 'locked' in str(e):
                self._log("WARN", f"Database is locked (possible concurrent access): {str(e)}")
                return True
            else:
                self._log("FAIL", f"✗ Cannot write to database: {str(e)}")
                return False
        except Exception as e:
            self._log("ERROR", f"✗ Unexpected error during write test: {str(e)}")
            return False
    
    def test_network_connectivity(self):
        """Test 5: Test network share connectivity"""
        if '\\\\' not in self.db_path and not self.db_path.startswith('//'):
            self._log("INFO", "Local database (network test skipped)")
            return True
        
        try:
            # Try to access the share parent directory
            db_dir = os.path.dirname(self.db_path)
            
            if os.path.exists(db_dir):
                self._log("PASS", f"✓ Network share is accessible: {db_dir}")
                return True
            else:
                self._log("FAIL", f"✗ Cannot access network share: {db_dir}")
                self._log("INFO", "  Possible issues:")
                self._log("INFO", "  - Network path is incorrect")
                self._log("INFO", "  - Server is offline")
                self._log("INFO", "  - Network credentials are not provided")
                return False
        except Exception as e:
            self._log("ERROR", f"✗ Network connectivity error: {str(e)}")
            return False
    
    def test_config_settings(self):
        """Test 6: Verify configuration settings"""
        settings_ok = True
        
        db_timeout = self.config.get('SERVER', 'db_timeout', fallback=None)
        if db_timeout:
            try:
                timeout_val = int(db_timeout)
                if timeout_val > 10:
                    self._log("PASS", f"✓ db_timeout is reasonable: {timeout_val}s")
                else:
                    self._log("WARN", f"⚠ db_timeout is very low: {timeout_val}s (recommended: 30s+)")
                    settings_ok = False
            except:
                self._log("WARN", f"⚠ Invalid db_timeout value: {db_timeout}")
                settings_ok = False
        
        pool_size = self.config.get('PERFORMANCE', 'connection_pool_size', fallback=None)
        if pool_size:
            try:
                size = int(pool_size)
                if size > 0:
                    self._log("PASS", f"✓ connection_pool_size: {size}")
                else:
                    self._log("WARN", f"⚠ connection_pool_size should be > 0")
                    settings_ok = False
            except:
                self._log("WARN", f"⚠ Invalid connection_pool_size: {pool_size}")
                settings_ok = False
        
        return settings_ok
    
    def run_all_tests(self):
        """Run all tests and display summary"""
        print("\n" + "="*70)
        print("TASMA Network Database Connection Test")
        print("="*70 + "\n")
        
        tests = [
            ("Path Exists", self.test_path_exists),
            ("Network Path Format", self.test_network_path_format),
            ("Database Readability", self.test_database_readability),
            ("Database Writability", self.test_database_writability),
            ("Network Connectivity", self.test_network_connectivity),
            ("Configuration Settings", self.test_config_settings),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            print(f"\n[TEST] {test_name}")
            print("-" * 70)
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self._log("ERROR", f"Test crashed: {str(e)}")
                failed += 1
        
        print("\n" + "="*70)
        print(f"SUMMARY: {passed} passed, {failed} failed")
        print("="*70 + "\n")
        
        if failed == 0:
            print("✓ All tests passed! Database connection is ready.")
            return True
        else:
            print("✗ Some tests failed. Please review the errors above.")
            return False


def main():
    tester = DatabaseConnectionTester()
    success = tester.run_all_tests()
    
    # Save results to file
    with open('database_test_results.txt', 'w') as f:
        f.write('\n'.join(tester.results))
    
    print(f"\nResults saved to: database_test_results.txt")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
