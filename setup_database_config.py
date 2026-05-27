"""
TASMA Database Configuration Setup Utility
Helps users configure the network database path during installation
Run this after installation to set up server database connectivity
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import configparser
import os
import subprocess
from pathlib import Path

class DatabaseConfigUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TASMA Database Configuration")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        self.config = configparser.ConfigParser()
        self.config_file = 'config.ini'
        self.load_config()
        
        self.setup_ui()
        self.load_current_values()
    
    def load_config(self):
        """Load existing configuration"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            # Create default config
            self.config['SERVER'] = {
                'database_path': '\\\\SERVER_NAME\\TASMA_Data\\bookings.db',
                'db_timeout': '30',
                'enable_cache': 'true',
                'cache_timeout': '300'
            }
            self.config['PERFORMANCE'] = {
                'connection_pool_size': '5',
                'batch_size': '100'
            }
            self.config['LOGGING'] = {
                'debug_mode': 'false',
                'log_file': 'tasma_app.log'
            }
    
    def setup_ui(self):
        """Create the UI"""
        # Title
        title = ttk.Label(
            self.root,
            text="TASMA Database Configuration",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=20)
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Database Path Section
        path_frame = ttk.LabelFrame(main_frame, text="Database Location", padding=10)
        path_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(path_frame, text="Database Path:", font=("Arial", 10)).pack(anchor=tk.W)
        
        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=70)
        path_entry.pack(anchor=tk.W, pady=5)
        
        button_frame = ttk.Frame(path_frame)
        button_frame.pack(anchor=tk.W, pady=5)
        
        ttk.Button(button_frame, text="Browse Network", command=self.browse_network).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Browse Local", command=self.browse_local).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Use Default", command=self.use_default_path).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(path_frame, text="Examples:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(10, 5))
        examples_text = (
            "• Network: \\\\SERVER_NAME\\TASMA_Data\\bookings.db\n"
            "• Network IP: \\\\192.168.1.100\\TASMA_Data\\bookings.db\n"
            "• Local: E:\\tasma_booking_syst\\bookings.db"
        )
        ttk.Label(path_frame, text=examples_text, foreground="#666", font=("Arial", 8)).pack(anchor=tk.W)
        
        # Connection Settings
        settings_frame = ttk.LabelFrame(main_frame, text="Connection Settings", padding=10)
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Timeout
        timeout_frame = ttk.Frame(settings_frame)
        timeout_frame.pack(fill=tk.X, pady=5)
        ttk.Label(timeout_frame, text="Connection Timeout (seconds):", width=30).pack(side=tk.LEFT)
        self.timeout_var = tk.StringVar()
        ttk.Spinbox(timeout_frame, from_=10, to=120, textvariable=self.timeout_var, width=10).pack(side=tk.LEFT)
        
        # Pool Size
        pool_frame = ttk.Frame(settings_frame)
        pool_frame.pack(fill=tk.X, pady=5)
        ttk.Label(pool_frame, text="Connection Pool Size:", width=30).pack(side=tk.LEFT)
        self.pool_var = tk.StringVar()
        ttk.Spinbox(pool_frame, from_=2, to=20, textvariable=self.pool_var, width=10).pack(side=tk.LEFT)
        
        # Cache
        self.cache_var = tk.BooleanVar()
        ttk.Checkbutton(settings_frame, text="Enable caching for faster startup", variable=self.cache_var).pack(anchor=tk.W, pady=5)
        
        # Information
        info_frame = ttk.LabelFrame(main_frame, text="Network Configuration Guide", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        info_text = tk.Text(info_frame, height=8, width=80, wrap=tk.WORD)
        info_text.pack(fill=tk.BOTH, expand=True)
        
        guide = """Server Setup (One-time):
1. Create shared folder: C:\\TASMA_Data on your server
2. Share it with all users (Read/Write permissions)
3. Copy bookings.db to this shared folder
4. Note the server name or IP address

Client Installation:
1. Install TASMA on each client machine
2. Run this configuration tool on each client
3. Enter the server path and click 'Save & Test'
4. The app will connect to the shared database on the server

Troubleshooting:
• Verify server name/IP is correct
• Check network connectivity
• Ensure you have access permissions to the shared folder"""
        
        info_text.insert(1.0, guide)
        info_text.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)
        
        ttk.Button(button_frame, text="Save & Test Connection", command=self.save_and_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View Test Results", command=self.view_test_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Default", command=self.reset_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
    
    def load_current_values(self):
        """Load current config values into UI"""
        self.path_var.set(self.config.get('SERVER', 'database_path', fallback=''))
        self.timeout_var.set(self.config.get('SERVER', 'db_timeout', fallback='30'))
        self.pool_var.set(self.config.get('PERFORMANCE', 'connection_pool_size', fallback='5'))
        cache_enabled = self.config.get('SERVER', 'enable_cache', fallback='true').lower() == 'true'
        self.cache_var.set(cache_enabled)
    
    def browse_network(self):
        """Browse for network path"""
        # Show directory selection dialog
        path = filedialog.askdirectory(title="Select Network Database Folder")
        if path:
            # Convert to UNC path if needed
            if not path.startswith('\\\\'):
                # Assume it's a network path
                self.path_var.set(os.path.join(path, 'bookings.db'))
            else:
                self.path_var.set(os.path.join(path, 'bookings.db'))
    
    def browse_local(self):
        """Browse for local database file"""
        path = filedialog.askopenfilename(
            title="Select Database File",
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")]
        )
        if path:
            self.path_var.set(path)
    
    def use_default_path(self):
        """Use default local path"""
        default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bookings.db')
        self.path_var.set(default_path)
    
    def save_and_test(self):
        """Save configuration and test connection"""
        # Update config
        db_path = self.path_var.get().strip()
        
        if not db_path:
            messagebox.showerror("Error", "Please specify a database path")
            return
        
        self.config['SERVER']['database_path'] = db_path
        self.config['SERVER']['db_timeout'] = self.timeout_var.get()
        self.config['PERFORMANCE']['connection_pool_size'] = self.pool_var.get()
        self.config['SERVER']['enable_cache'] = 'true' if self.cache_var.get() else 'false'
        
        # Save config
        try:
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
            return
        
        # Run connection test
        self.test_connection(db_path)
    
    def test_connection(self, db_path):
        """Test database connection"""
        try:
            import sqlite3
            
            timeout = int(self.timeout_var.get())
            conn = sqlite3.connect(db_path, timeout=timeout)
            cursor = conn.cursor()
            
            # Get table info
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()
            
            table_list = '\n'.join([f"  • {t[0]}" for t in tables]) if tables else "  (database is empty)"
            
            message = f"✓ Connection successful!\n\nDatabase: {db_path}\nTables found:\n{table_list}"
            messagebox.showinfo("Connection Test Passed", message)
            
        except sqlite3.OperationalError as e:
            messagebox.showerror("Connection Failed", f"Cannot connect to database:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Connection test error:\n{str(e)}")
    
    def view_test_results(self):
        """View detailed test results"""
        try:
            # Run the network test script
            if os.path.exists('test_network_db.py'):
                subprocess.Popen(['python', 'test_network_db.py'])
            else:
                messagebox.showwarning("Not Found", "test_network_db.py not found.\nRun 'test_network_db.py' manually to get detailed diagnostics.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run test: {str(e)}")
    
    def reset_config(self):
        """Reset to default configuration"""
        if messagebox.askyesno("Confirm", "Reset configuration to defaults?"):
            self.use_default_path()
            self.timeout_var.set('30')
            self.pool_var.set('5')
            self.cache_var.set(True)


def main():
    root = tk.Tk()
    app = DatabaseConfigUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
