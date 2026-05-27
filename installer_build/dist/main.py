import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import configparser
from datetime import datetime
import csv
import hashlib
import time
from tkcalendar import DateEntry, Calendar
from PIL import Image, ImageTk

# Import optimized database module for server deployment
try:
    from db_optimized import get_db
    USE_OPTIMIZED_DB = True
except ImportError:
    USE_OPTIMIZED_DB = False

class TimePickerWidget(tk.Frame):
    """A simple time picker with spinboxes for hours and minutes"""
    def __init__(self, parent, hour=0, minute=0, on_time_changed=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.hour = hour if 0 <= hour <= 23 else 0
        self.minute = minute if 0 <= minute <= 59 else 0
        self.on_time_changed = on_time_changed
        
        # Title
        title_label = tk.Label(self, text="Select Time (24-hour format)", 
                              font=("Arial", 12, "bold"), fg="#0052cc",
                              bg=self.cget("bg"))
        title_label.pack(pady=10)
        
        # Hour and Minute frame
        time_input_frame = tk.Frame(self, bg=self.cget("bg"))
        time_input_frame.pack(pady=20)
        
        # Hour section
        tk.Label(time_input_frame, text="Hour", font=("Arial", 11, "bold"),
                fg="#0052cc", bg=self.cget("bg")).grid(row=0, column=0, padx=20)
        self.hour_spinbox = tk.Spinbox(time_input_frame, from_=0, to=23, width=4,
                                       font=("Arial", 14, "bold"), justify="center",
                                       bg="#f0f4f8", fg="#1f2937", borderwidth=2, relief="solid")
        self.hour_spinbox.set(self.hour)
        self.hour_spinbox.grid(row=0, column=1, padx=20)
        self.hour_spinbox.bind("<KeyRelease>", self.on_value_changed)
        
        # Colon
        tk.Label(time_input_frame, text=":", font=("Arial", 14, "bold"),
                fg="#1f2937", bg=self.cget("bg")).grid(row=0, column=2)
        
        # Minute section
        tk.Label(time_input_frame, text="Minute", font=("Arial", 11, "bold"),
                fg="#0052cc", bg=self.cget("bg")).grid(row=0, column=3, padx=20)
        self.minute_spinbox = tk.Spinbox(time_input_frame, from_=0, to=59, width=4,
                                        font=("Arial", 14, "bold"), justify="center",
                                        bg="#f0f4f8", fg="#1f2937", borderwidth=2, relief="solid")
        self.minute_spinbox.set(self.minute)
        self.minute_spinbox.grid(row=0, column=4, padx=20)
        self.minute_spinbox.bind("<KeyRelease>", self.on_value_changed)
        
        # Digital display
        display_frame = tk.Frame(self, bg=self.cget("bg"))
        display_frame.pack(pady=20)
        
        tk.Label(display_frame, text="Selected Time:", font=("Arial", 10),
                fg="#6b7280", bg=self.cget("bg")).pack()
        
        self.time_display = tk.Label(display_frame, text=f"{self.hour:02d}:{self.minute:02d}",
                                     font=("Arial", 28, "bold"), fg="#0052cc",
                                     bg=self.cget("bg"))
        self.time_display.pack(pady=10)
    
    def on_value_changed(self, event=None):
        """Called when spinbox values change"""
        try:
            self.hour = int(self.hour_spinbox.get())
            self.minute = int(self.minute_spinbox.get())
            
            # Clamp values
            self.hour = max(0, min(23, self.hour))
            self.minute = max(0, min(59, self.minute))
            
            # Update spinboxes with clamped values
            self.hour_spinbox.set(self.hour)
            self.minute_spinbox.set(self.minute)
            
            # Update display
            self.time_display.config(text=f"{self.hour:02d}:{self.minute:02d}")
            
            if self.on_time_changed:
                self.on_time_changed(self.hour, self.minute)
        except:
            pass

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("TASMA Login")
        self.root.resizable(False, False)
        
        # Center window on screen - calculate position before creating geometry
        width = 450
        height = 570
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Light Theme Colors
        self.bg_main = "#f5f7fa"
        self.bg_white = "#ffffff"
        self.bg_light = "#f0f4f8"
        self.accent_blue = "#0052cc"
        self.text_primary = "#1f2937"
        self.text_secondary = "#6b7280"
        self.border_color = "#d1d5db"
        
        # Run first-setup check in background (non-blocking)
        threading.Thread(target=self._check_and_run_first_setup, daemon=True).start()
        
        self.root.configure(bg=self.bg_main)
        
        # Flag to track if database has been initialized
        self._db_initialized = False
        
        self.logged_in_user = None
        self.is_admin = False
        self.user_department = None
        
        # Main container
        main_frame = tk.Frame(root, bg=self.bg_main)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Logo - Display text immediately, load image asynchronously
        self.logo_frame = tk.Frame(main_frame, bg=self.bg_main)
        self.logo_frame.pack(pady=20)
        
        # Show text logo immediately (instant UI)
        self.logo_label = tk.Label(self.logo_frame, text="🏢 TASMA", font=("Helvetica", 28, "bold"),
                                   fg=self.accent_blue, bg=self.bg_main)
        self.logo_label.pack()
        
        # Lazy initialize database on first login attempt
        self.root.after(100, self._ensure_db_initialized)
        
        # Load actual logo image asynchronously after UI is shown (200ms delay)
        self.root.after(200, self._load_logo_async)
        
        subtitle = tk.Label(main_frame, text="Board Room Booking System", 
                          font=("Arial", 11), fg=self.text_secondary, bg=self.bg_main)
        subtitle.pack(pady=(0, 30))
        
        # Notebook for Login/Register/Admin tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)
        
        style = ttk.Style()
        style.configure('TNotebook', background=self.bg_main, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[15, 8], font=("Arial", 10, "bold"))
        style.map('TNotebook.Tab',
                 background=[('selected', self.bg_white), ('active', self.bg_white)],
                 foreground=[('selected', self.accent_blue)])
        
        # === LOGIN TAB ===
        login_tab = tk.Frame(notebook, bg=self.bg_white)
        notebook.add(login_tab, text="🔐  Login")
        
        login_frame = tk.Frame(login_tab, bg=self.bg_white)
        login_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(login_frame, text="Username", font=("Arial", 10, "bold"),
                fg=self.accent_blue, bg=self.bg_white).pack(anchor="w", pady=(0, 5))
        self.login_user = tk.Entry(login_frame, font=("Arial", 11), bg=self.bg_light,
                                  fg=self.text_primary, insertbackground=self.accent_blue,
                                  borderwidth=1, relief="solid")
        self.login_user.pack(fill="x", pady=(0, 15))
        
        tk.Label(login_frame, text="Password", font=("Arial", 10, "bold"),
                fg=self.accent_blue, bg=self.bg_white).pack(anchor="w", pady=(0, 5))
        self.login_pass = tk.Entry(login_frame, font=("Arial", 11), bg=self.bg_light,
                                  fg=self.text_primary, insertbackground=self.accent_blue,
                                  borderwidth=1, relief="solid", show="●")
        self.login_pass.pack(fill="x", pady=(0, 25))
        
        login_btn = tk.Button(login_frame, text="🔓  Login", command=self.login,
                             bg=self.accent_blue, fg="white", font=("Arial", 11, "bold"),
                             cursor="hand2", relief="flat", bd=0, pady=10)
        login_btn.pack(fill="x")
        
        # === REGISTER TAB ===
        reg_tab = tk.Frame(notebook, bg=self.bg_white)
        notebook.add(reg_tab, text="✍️  Register")
        
        # Create canvas and scrollbar for scrollable form
        reg_canvas = tk.Canvas(reg_tab, bg=self.bg_white, highlightthickness=0)
        reg_scrollbar = ttk.Scrollbar(reg_tab, orient="vertical", command=reg_canvas.yview)
        reg_scrollable_frame = tk.Frame(reg_canvas, bg=self.bg_white)
        
        reg_scrollable_frame.bind(
            "<Configure>",
            lambda e: reg_canvas.configure(scrollregion=reg_canvas.bbox("all"))
        )
        
        reg_window = reg_canvas.create_window((0, 0), window=reg_scrollable_frame, anchor="nw")
        reg_canvas.configure(yscrollcommand=reg_scrollbar.set)
        
        # Make frame expand to canvas width
        def _on_canvas_configure(event):
            reg_canvas.itemconfig(reg_window, width=event.width)
        reg_canvas.bind("<Configure>", _on_canvas_configure)
        
        # Bind mousewheel to canvas for scrolling
        def _on_mousewheel(event):
            reg_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        reg_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        reg_canvas.pack(side="left", fill="both", expand=True)
        reg_scrollbar.pack(side="right", fill="y")
        
        reg_frame = reg_scrollable_frame
        
        tk.Label(reg_frame, text="Full Name", font=("Arial", 10, "bold"),
                fg=self.accent_blue, bg=self.bg_white).pack(anchor="w", pady=(0, 5), padx=20)
        self.reg_name = tk.Entry(reg_frame, font=("Arial", 11), bg=self.bg_light,
                                fg=self.text_primary, insertbackground=self.accent_blue,
                                borderwidth=1, relief="solid")
        self.reg_name.pack(fill="x", pady=(0, 15), padx=20)
        
        tk.Label(reg_frame, text="New Username", font=("Arial", 10, "bold"),
                fg=self.accent_blue, bg=self.bg_white).pack(anchor="w", pady=(0, 5), padx=20)
        self.reg_user = tk.Entry(reg_frame, font=("Arial", 11), bg=self.bg_light,
                                fg=self.text_primary, insertbackground=self.accent_blue,
                                borderwidth=1, relief="solid")
        self.reg_user.pack(fill="x", pady=(0, 15), padx=20)
        
        tk.Label(reg_frame, text="Password", font=("Arial", 10, "bold"),
                fg=self.accent_blue, bg=self.bg_white).pack(anchor="w", pady=(0, 5), padx=20)
        self.reg_pass = tk.Entry(reg_frame, font=("Arial", 11), bg=self.bg_light,
                                fg=self.text_primary, insertbackground=self.accent_blue,
                                borderwidth=1, relief="solid", show="●")
        self.reg_pass.pack(fill="x", pady=(0, 15), padx=20)
        
        tk.Label(reg_frame, text="Confirm Password", font=("Arial", 10, "bold"),
                fg=self.accent_blue, bg=self.bg_white).pack(anchor="w", pady=(0, 5), padx=20)
        self.reg_pass_confirm = tk.Entry(reg_frame, font=("Arial", 11), bg=self.bg_light,
                                        fg=self.text_primary, insertbackground=self.accent_blue,
                                        borderwidth=1, relief="solid", show="●")
        self.reg_pass_confirm.pack(fill="x", pady=(0, 15), padx=20)
        
        tk.Label(reg_frame, text="🏢  Department", font=("Arial", 10, "bold"),
                fg=self.accent_blue, bg=self.bg_white).pack(anchor="w", pady=(0, 5), padx=20)
        self.reg_dept = ttk.Combobox(reg_frame, font=("Arial", 11),
                                    values=["Admin", "Finance", "HR", "IT", "Marketing", "Operations", "Sales", "Other"],
                                    state="readonly")
        self.reg_dept.pack(fill="x", pady=(0, 15), padx=20)
        
        reg_btn = tk.Button(reg_frame, text="✍️  Submit Request", command=self.register,
                           bg="#10b981", fg="white", font=("Arial", 11, "bold"),
                           cursor="hand2", relief="flat", bd=0, pady=10)
        reg_btn.pack(fill="x", padx=20)
        
        info_label = tk.Label(reg_frame, text="⏳ Registration pending admin approval",
                            font=("Arial", 8, "italic"), fg="#ef4444", bg=self.bg_white)
        info_label.pack(anchor="w", pady=10, padx=20)
        
        # === ADMIN TAB ===
        admin_tab = tk.Frame(notebook, bg=self.bg_white)
        notebook.add(admin_tab, text="👨‍💼  Admin")
        
        admin_frame = tk.Frame(admin_tab, bg=self.bg_white)
        admin_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(admin_frame, text="Admin Username", font=("Arial", 10, "bold"),
                fg=self.accent_blue, bg=self.bg_white).pack(anchor="w", pady=(0, 5))
        self.admin_user = tk.Entry(admin_frame, font=("Arial", 11), bg=self.bg_light,
                                  fg=self.text_primary, insertbackground=self.accent_blue,
                                  borderwidth=1, relief="solid")
        self.admin_user.pack(fill="x", pady=(0, 15))
        
        tk.Label(admin_frame, text="Admin Password", font=("Arial", 10, "bold"),
                fg=self.accent_blue, bg=self.bg_white).pack(anchor="w", pady=(0, 5))
        self.admin_pass = tk.Entry(admin_frame, font=("Arial", 11), bg=self.bg_light,
                                  fg=self.text_primary, insertbackground=self.accent_blue,
                                  borderwidth=1, relief="solid", show="●")
        self.admin_pass.pack(fill="x", pady=(0, 25))
        
        admin_btn = tk.Button(admin_frame, text="👨‍💼  Admin Login", command=self.admin_login,
                             bg="#8b5cf6", fg="white", font=("Arial", 11, "bold"),
                             cursor="hand2", relief="flat", bd=0, pady=10)
        admin_btn.pack(fill="x")
    
    def init_database(self):
        """Create users and requests tables - uses optimized database when available"""
        import sys
        import shutil
        
        # Initialize optimized database if available (server deployment)
        if USE_OPTIMIZED_DB:
            try:
                db = get_db()
                # Ensure tables exist
                db.execute_update('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        full_name TEXT,
                        password TEXT NOT NULL,
                        department TEXT,
                        role TEXT DEFAULT 'user'
                    )
                ''')
                
                db.execute_update('''
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
                
                # Ensure at least one admin exists
                result = db.execute_query("SELECT COUNT(*) FROM users WHERE role='admin'", fetch='one')
                if result and result[0] == 0:
                    admin_pass = self.hash_password("admin")
                    db.execute_update(
                        "INSERT INTO users (username, full_name, password, role) VALUES (?, ?, ?, ?)",
                        ("admin", "Administrator", admin_pass, "admin")
                    )
                return
            except Exception as e:
                print(f"Warning: Could not use optimized database: {e}")
                # Fall through to standard sqlite3
        
        # Standard SQLite implementation (fallback)
        # Get the directory where the app/executable is located
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller bundle - store database in AppData for write permissions
            app_data = os.getenv('APPDATA')
            app_dir = os.path.join(app_data, 'TASMA')
            if not os.path.exists(app_dir):
                os.makedirs(app_dir)
        else:
            # Running as normal Python script
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        db_path = os.path.join(app_dir, "bookings.db")
        
        # If database doesn't exist, try to copy template from installation directory
        if not os.path.exists(db_path):
            try:
                if getattr(sys, 'frozen', False):
                    install_dir = os.path.dirname(sys.executable)
                    template_db = os.path.join(install_dir, "bookings.db")
                    if os.path.exists(template_db):
                        shutil.copy2(template_db, db_path)
            except Exception as e:
                pass  # Continue - we'll create empty tables if needed
        
        conn = sqlite3.connect(db_path, timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=30000")
        cursor = conn.cursor()
        
        # Users table (approved users only)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                full_name TEXT,
                password TEXT NOT NULL,
                department TEXT,
                role TEXT DEFAULT 'user'
            )
        ''')
        
        # Pending requests table
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
        
        # Migration: Add department column if it doesn't exist
        try:
            cursor.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cursor.fetchall()]
            if 'department' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN department TEXT")
        except:
            pass
        
        try:
            cursor.execute("PRAGMA table_info(user_requests)")
            columns = [column[1] for column in cursor.fetchall()]
            if 'department' not in columns:
                cursor.execute("ALTER TABLE user_requests ADD COLUMN department TEXT")
        except:
            pass
        
        # Ensure at least one admin exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
        if cursor.fetchone()[0] == 0:
            admin_pass = self.hash_password("admin")
            cursor.execute("INSERT INTO users (username, full_name, password, role) VALUES (?, ?, ?, ?)",
                         ("admin", "Administrator", admin_pass, "admin"))
        
        conn.commit()
        conn.close()
    
    def _ensure_db_initialized(self):
        """Ensure database is initialized (called lazily)"""
        if not self._db_initialized:
            try:
                self.init_database()
                self._db_initialized = True
            except Exception as e:
                print(f"Failed to initialize database: {e}")
    
    def _load_logo_async(self):
        """Load logo image asynchronously without blocking UI"""
        try:
            import sys
            # Get the directory where the app/executable is located
            if getattr(sys, 'frozen', False):
                # Running as PyInstaller bundle - use executable directory for data
                app_dir = os.path.dirname(sys.executable)
            else:
                # Running as normal Python script
                app_dir = os.path.dirname(os.path.abspath(__file__))
            
            logo_path = os.path.join(app_dir, 'tasma_logo.webp')
            
            # Load and display logo if file exists
            if os.path.exists(logo_path):
                try:
                    logo_img = Image.open(logo_path)
                    logo_img = logo_img.resize((280, 180), Image.Resampling.LANCZOS)
                    self.logo_photo = ImageTk.PhotoImage(logo_img)
                    
                    # Replace text logo with image logo
                    self.logo_label.config(image=self.logo_photo, text="")
                    self.logo_label.image = self.logo_photo  # Keep a reference
                    
                except Exception as img_error:
                    # Keep text logo if image fails to load
                    pass
        except Exception as e:
            # Keep text logo as fallback
            pass
    
    def _check_and_run_first_setup(self):
        """Check if first-run setup is needed and run if necessary (non-blocking)"""
        import sys
        config_file = self._get_config_file()
        
        # Check if config.ini exists and has server database path
        server_db_path = r"\\GVBSERVER\C$\Users\Administrator\AppData\Roaming\TASMA\bookings.db"
        has_server_config = False
        
        try:
            if os.path.exists(config_file):
                config = configparser.ConfigParser()
                config.read(config_file)
                if config.has_option('Database', 'database_path'):
                    db_path = config.get('Database', 'database_path')
                    if 'GVBSERVER' in db_path:
                        has_server_config = True
        except:
            pass
        
        # If no server config, show setup wizard (non-blocking via after)
        if not has_server_config:
            # Schedule setup to run after login UI is visible (50ms delay)
            self.root.after(50, lambda: self._show_first_run_setup(server_db_path, config_file))
    
    def _get_config_file(self):
        """Get the config file path"""
        import sys
        if getattr(sys, 'frozen', False):
            app_data = os.getenv('APPDATA')
            app_dir = os.path.join(app_data, 'TASMA')
            if not os.path.exists(app_dir):
                os.makedirs(app_dir)
            return os.path.join(app_dir, 'config.ini')
        else:
            app_dir = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(app_dir, 'config.ini')
    
    def _show_first_run_setup(self, server_db_path, config_file):
        """Show first-run setup wizard"""
        import sys
        # Create a setup window
        setup_window = tk.Toplevel(self.root)
        setup_window.title("TASMA - First Run Setup")
        setup_window.geometry("600x450")
        setup_window.resizable(False, False)
        
        # Center on screen
        x = (self.root.winfo_screenwidth() // 2) - (300)
        y = (self.root.winfo_screenheight() // 2) - (225)
        setup_window.geometry(f"+{x}+{y}")
        setup_window.transient(self.root)
        setup_window.grab_set()
        
        # Setup frame
        setup_frame = tk.Frame(setup_window, bg="#f5f7fa", highlightthickness=0)
        setup_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(setup_frame, text="Welcome to TASMA", 
                        font=("Arial", 18, "bold"), fg="#0052cc", bg="#f5f7fa")
        title.pack(pady=(0, 5))
        
        # Subtitle
        subtitle = tk.Label(setup_frame, text="Configuring Server Connection", 
                           font=("Arial", 11), fg="#6b7280", bg="#f5f7fa")
        subtitle.pack(pady=(0, 20))
        
        # Status text frame
        status_frame = tk.Frame(setup_frame, bg="#ffffff", relief="solid", bd=1)
        status_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        status_text = tk.Text(status_frame, height=12, width=70, bg="#ffffff", 
                             fg="#1f2937", font=("Courier", 9), relief="flat",
                             wrap="word", state="disabled")
        status_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Function to update status
        def add_status(message):
            status_text.config(state="normal")
            status_text.insert("end", message + "\n")
            status_text.see("end")
            status_text.config(state="disabled")
            setup_window.update()
        
        # Start setup process
        add_status("🔧 SERVER CONNECTION SETUP\n")
        add_status(f"Server: GVBSERVER")
        add_status(f"Database: {server_db_path}\n")
        
        # Test network path
        add_status("Testing network connection...")
        network_ok = False
        try:
            # Use shorter timeout (2 seconds instead of blocking indefinitely)
            # Check in a non-blocking way using threading
            import threading
            path_check_result = [False]
            def check_path():
                try:
                    # Quick check with timeout
                    if os.path.exists(server_db_path):
                        path_check_result[0] = True
                except:
                    pass
            
            thread = threading.Thread(target=check_path, daemon=True)
            thread.start()
            thread.join(timeout=2.0)  # Wait max 2 seconds
            
            if path_check_result[0]:
                add_status("✓ Network path accessible\n")
                network_ok = True
            else:
                add_status("⚠ Network path not accessible (server may be offline)")
                add_status("  Will configure for when server is available\n")
        except Exception as e:
            add_status(f"⚠ Network test skipped: {str(e)}\n")
        
        # Test database
        if network_ok:
            add_status("Testing database connection...")
            try:
                # Use shorter timeout (5 seconds instead of 10)
                conn = sqlite3.connect(server_db_path, timeout=5.0)
                conn.execute("PRAGMA busy_timeout=5000")
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                conn.close()
                add_status(f"✓ Database connection successful")
                add_status(f"  Users in database: {user_count}\n")
            except Exception as e:
                add_status(f"⚠ Database test: {str(e)}\n")
        
        # Create config
        add_status("Creating configuration file...")
        try:
            config = configparser.ConfigParser()
            config['Database'] = {
                'database_path': server_db_path,
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
            add_status(f"✓ Configuration saved to:")
            add_status(f"  {config_file}\n")
        except Exception as e:
            add_status(f"✗ Configuration error: {str(e)}\n")
        
        add_status("✓ Setup complete!")
        add_status("Click 'Continue' to proceed to login.\n")
        add_status("NOTE: If you encounter login errors,")
        add_status("verify the server is running and accessible.")
        
        # Button
        continue_btn = tk.Button(setup_frame, text="✓ Continue to Login",
                                command=setup_window.destroy,
                                bg="#0052cc", fg="white", font=("Arial", 11, "bold"),
                                cursor="hand2", relief="flat", bd=0, pady=10)
        continue_btn.pack(fill="x", pady=(10, 0))
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def get_db_path(self):
        """Get database path - checks config.ini first for server path"""
        import sys
        import configparser
        
        # Check for config.ini with server database path
        config_file = None
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller bundle
            app_data = os.getenv('APPDATA')
            app_dir = os.path.join(app_data, 'TASMA')
            config_file = os.path.join(app_dir, 'config.ini')
            if not os.path.exists(app_dir):
                os.makedirs(app_dir)
        else:
            # Running as normal Python script
            app_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(app_dir, 'config.ini')
        
        # Try to read server database path from config
        try:
            if os.path.exists(config_file):
                config = configparser.ConfigParser()
                config.read(config_file)
                if config.has_option('Database', 'database_path'):
                    db_path = config.get('Database', 'database_path')
                    print(f"Using server database: {db_path}")
                    return db_path
        except Exception as e:
            print(f"Warning: Could not read config.ini: {e}")
        
        # Fallback to local database in AppData
        if getattr(sys, 'frozen', False):
            app_data = os.getenv('APPDATA')
            app_dir = os.path.join(app_data, 'TASMA')
            if not os.path.exists(app_dir):
                os.makedirs(app_dir)
        else:
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        local_db = os.path.join(app_dir, "bookings.db")
        print(f"Using local database: {local_db}")
        return local_db
    
    def login(self):
        """Authenticate user login - runs in background thread"""
        username = self.login_user.get().strip()
        password = self.login_pass.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        # Show "Connecting..." dialog
        progress = tk.Toplevel(self.root)
        progress.title("Logging in...")
        progress.geometry("300x100")
        progress.resizable(False, False)
        tk.Label(progress, text="Connecting to database...", font=("Arial", 10)).pack(pady=20)
        progress.update()
        
        # Run login in background thread to prevent UI freeze
        def login_worker():
            try:
                # Ensure database is initialized before login attempt
                self._ensure_db_initialized()
                
                conn = sqlite3.connect(self.get_db_path(), timeout=30.0)
                conn.execute("PRAGMA busy_timeout=30000")
                cursor = conn.cursor()
                
                hashed_password = self.hash_password(password)
                cursor.execute("SELECT id, role, department FROM users WHERE username=? AND password=? AND role='user'",
                             (username, hashed_password))
                user = cursor.fetchone()
                conn.close()
                
                # Close progress dialog
                try:
                    progress.destroy()
                except:
                    pass
                
                if user:
                    self.logged_in_user = username
                    self.is_admin = False
                    self.user_department = user[2] if len(user) > 2 else None  # Store department
                    messagebox.showinfo("Success", f"Welcome, {username}!")
                    self.root.destroy()
                else:
                    messagebox.showerror("Error", "Invalid username or password, or account not approved yet")
            except Exception as e:
                try:
                    progress.destroy()
                except:
                    pass
                messagebox.showerror("Error", f"Login failed:\n{str(e)}")
        
        # Start login in background thread
        import threading
        login_thread = threading.Thread(target=login_worker, daemon=True)
        login_thread.start()
    def register(self):
        """Submit new user registration request"""
        full_name = self.reg_name.get().strip()
        username = self.reg_user.get().strip()
        password = self.reg_pass.get()
        password_confirm = self.reg_pass_confirm.get()
        department = self.reg_dept.get().strip()
        
        if not full_name or len(full_name) < 3:
            messagebox.showerror("Error", "Full name must be at least 3 characters")
            return
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters")
            return
        
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return
        
        if password != password_confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if not department:
            messagebox.showerror("Error", "Please select a department")
            return
        
        # Retry logic for database locked errors with longer delays
        max_retries = 10
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                conn = sqlite3.connect(self.get_db_path(), timeout=30.0)
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA busy_timeout=30000")
                cursor = conn.cursor()
                
                # Check if username already exists in approved users
                cursor.execute("SELECT id FROM users WHERE username=?", (username,))
                if cursor.fetchone():
                    conn.close()
                    messagebox.showerror("Error", f"Username '{username}' is already taken. Please choose a different username.")
                    return
                
                # Check if there's already a PENDING request for this username
                cursor.execute("SELECT id FROM user_requests WHERE username=? AND status='pending'", (username,))
                if cursor.fetchone():
                    conn.close()
                    messagebox.showerror("Error", f"Registration request for '{username}' is already pending admin approval.")
                    return
                
                hashed_password = self.hash_password(password)
                cursor.execute("INSERT INTO user_requests (username, full_name, password, department) VALUES (?, ?, ?, ?)",
                             (username, full_name, hashed_password, department))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", 
                    f"Registration request submitted!\n\nYour account is pending admin approval.\n"
                    f"Please contact your administrator to activate your account.")
                self.reg_name.delete(0, tk.END)
                self.reg_user.delete(0, tk.END)
                self.reg_pass.delete(0, tk.END)
                self.reg_pass_confirm.delete(0, tk.END)
                self.reg_dept.set('')
                return
                
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) or "database is busy" in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        delay = 0.2 * (retry_count ** 1.5)  # Progressive backoff
                        time.sleep(min(delay, 5))  # Cap at 5 seconds
                    else:
                        messagebox.showerror("Error", "Database is busy. Please close the admin panel and try again.")
                else:
                    messagebox.showerror("Error", f"Registration failed:\n{str(e)}")
                    return
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Registration failed. Username may already exist.")
                return
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed:\n{str(e)}")
                return
    
    
    def admin_login(self):
        """Admin login - runs in background thread"""
        username = self.admin_user.get().strip()
        password = self.admin_pass.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter admin credentials")
            return
        
        # Show "Connecting..." dialog
        progress = tk.Toplevel(self.root)
        progress.title("Logging in...")
        progress.geometry("300x100")
        progress.resizable(False, False)
        tk.Label(progress, text="Connecting to database...", font=("Arial", 10)).pack(pady=20)
        progress.update()
        
        # Run login in background thread to prevent UI freeze
        def admin_login_worker():
            try:
                # Ensure database is initialized before login attempt
                self._ensure_db_initialized()
                
                conn = sqlite3.connect(self.get_db_path(), timeout=30.0)
                conn.execute("PRAGMA busy_timeout=30000")
                cursor = conn.cursor()
                
                hashed_password = self.hash_password(password)
                cursor.execute("SELECT id FROM users WHERE username=? AND password=? AND role='admin'",
                             (username, hashed_password))
                admin = cursor.fetchone()
                
                # Close progress dialog
                try:
                    progress.destroy()
                except:
                    pass
                
                if admin:
                    conn.close()
                    self.logged_in_user = username
                    self.is_admin = True
                    messagebox.showinfo("Success", f"Welcome, Admin {username}!")
                    self.root.destroy()
                else:
                    conn.close()
                    messagebox.showerror("Error", "Invalid admin credentials")
            except Exception as e:
                try:
                    progress.destroy()
                except:
                    pass
                messagebox.showerror("Error", f"Admin login failed:\n{str(e)}")
        
        # Start login in background thread
        import threading
        login_thread = threading.Thread(target=admin_login_worker, daemon=True)
        login_thread.start()

class AdminPanel:
    """Admin interface to manage user registration requests and bookings"""
    def __init__(self, root, admin_username):
        self.root = root
        self.admin_username = admin_username
        self.root.title("TASMA - Admin Panel")
        # Set fullscreen
        self.root.state('zoomed')
        
        # Light Theme Colors
        self.bg_main = "#f5f7fa"
        self.bg_white = "#ffffff"
        self.accent_blue = "#0052cc"
        self.accent_blue_lighter = "#e0eaff"
        self.text_primary = "#1f2937"
        self.text_secondary = "#6b7280"
        self.border_color = "#d1d5db"
        self.success_green = "#10b981"
        self.danger_red = "#ef4444"
        
        self.root.configure(bg=self.bg_main)
        
        # Database Configuration - Handle both normal Python and PyInstaller bundled execution
        import sys
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller bundle - store database in AppData for write permissions
            app_data = os.getenv('APPDATA')
            app_dir = os.path.join(app_data, 'TASMA')
            if not os.path.exists(app_dir):
                os.makedirs(app_dir)
        else:
            # Running as normal Python script
            app_dir = os.path.dirname(os.path.abspath(__file__))
        # Use server database path if available, otherwise local
        self.db_name = self.get_db_path()
        
        # Initialize database tables
        self.init_database()
        
        # Header
        header = tk.Frame(self.root, bg=self.accent_blue, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text=f"👨‍💼 Admin Panel - {admin_username}", 
                font=("Helvetica", 16, "bold"), fg="white", bg=self.accent_blue).pack(side="left", padx=20, pady=15)
        
        logout_btn = tk.Button(header, text="🚪 Logout", command=self.logout,
                              bg=self.danger_red, fg="white", font=("Arial", 10, "bold"),
                              cursor="hand2", relief="flat", bd=0)
        logout_btn.pack(side="right", padx=20, pady=10)
        
        # Main content with Notebook
        main_frame = tk.Frame(self.root, bg=self.bg_main)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Notebook for tabs
        style = ttk.Style()
        style.configure('TNotebook', background=self.bg_main, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[15, 8], font=("Arial", 10, "bold"))
        style.map('TNotebook.Tab',
                 background=[('selected', self.bg_white), ('active', self.bg_white)],
                 foreground=[('selected', self.accent_blue)])
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)
        
        # ===== TAB 1: User Requests =====
        requests_tab = tk.Frame(notebook, bg=self.bg_white)
        notebook.add(requests_tab, text="👥  User Requests")
        
        requests_frame = tk.Frame(requests_tab, bg=self.bg_white)
        requests_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(requests_frame, text="User Registration Requests", 
                        font=("Helvetica", 14, "bold"), fg=self.accent_blue, bg=self.bg_white)
        title.pack(anchor="w", pady=(0, 15))
        
        # Table frame
        table_frame = tk.Frame(requests_frame, bg=self.bg_white, relief="solid", bd=1)
        table_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Columns: Full Name | Username | Requested | Status | Actions
        self.tree = ttk.Treeview(table_frame, columns=("Full Name", "Username", "Requested", "Status"), 
                                height=15, show="tree headings")
        
        # Define column headings and widths
        self.tree.column("#0", width=0)
        self.tree.column("Full Name", anchor="w", width=150)
        self.tree.column("Username", anchor="w", width=120)
        self.tree.column("Requested", anchor="w", width=150)
        self.tree.column("Status", anchor="center", width=100)
        
        self.tree.heading("#0", text="")
        self.tree.heading("Full Name", text="Full Name")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Requested", text="Requested At")
        self.tree.heading("Status", text="Status")
        
        # Style alternating rows
        style.configure("Treeview", font=("Arial", 10), rowheight=30, bg=self.bg_white)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background=self.bg_main)
        style.map('Treeview', background=[('selected', self.accent_blue)])
        
        self.tree.pack(fill="both", expand=True, side="left")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscroll=scrollbar.set)
        
        # Action buttons
        button_frame = tk.Frame(requests_frame, bg=self.bg_white)
        button_frame.pack(fill="x", pady=(0, 10))
        
        self.approve_btn = tk.Button(button_frame, text="✅ Approve Selected", 
                                    command=self.approve_request,
                                    bg=self.success_green, fg="white", font=("Arial", 11, "bold"),
                                    cursor="hand2", relief="flat", bd=0, padx=15, pady=8)
        self.approve_btn.pack(side="left", padx=(0, 10))
        
        self.reject_btn = tk.Button(button_frame, text="❌ Reject Selected",
                                   command=self.reject_request,
                                   bg=self.danger_red, fg="white", font=("Arial", 11, "bold"),
                                   cursor="hand2", relief="flat", bd=0, padx=15, pady=8)
        self.reject_btn.pack(side="left")
        
        self.refresh_btn = tk.Button(button_frame, text="🔄 Refresh", 
                                    command=self.load_requests,
                                    bg=self.text_secondary, fg="white", font=("Arial", 11, "bold"),
                                    cursor="hand2", relief="flat", bd=0, padx=15, pady=8)
        self.refresh_btn.pack(side="right")
        
        # ===== TAB 2: Manage Bookings =====
        bookings_tab = tk.Frame(notebook, bg=self.bg_main)
        notebook.add(bookings_tab, text="📋  Manage Bookings")
        
        bookings_frame = tk.Frame(bookings_tab, bg=self.bg_main)
        bookings_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Search Frame (Card style)
        search_card = tk.Frame(bookings_frame, bg=self.bg_white, relief="flat", bd=0, highlightthickness=1,
                              highlightcolor=self.border_color, highlightbackground=self.border_color)
        search_card.pack(fill="x", padx=0, pady=(0, 20))
        
        search_label = tk.Label(search_card, text="🔍  Search Bookings", font=("Arial", 12, "bold"), 
                               fg=self.accent_blue, bg=self.bg_white, padx=15, pady=10)
        search_label.pack(anchor="w")
        
        search_inner_frame = tk.Frame(search_card, bg=self.bg_white)
        search_inner_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_bookings())
        search_entry = tk.Entry(search_inner_frame, textvariable=self.search_var, width=40, 
                               font=("Arial", 11), bg="#f0f4f8", fg=self.text_primary,
                               insertbackground=self.accent_blue, borderwidth=1, relief="solid")
        search_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        search_hint = tk.Label(search_inner_frame, text="(Date, Department, User, Reason)", 
                              font=("Arial", 9), bg=self.bg_white, fg=self.text_secondary)
        search_hint.pack(side="left", padx=10)
        
        # Bookings List Frame (Card style)
        list_card = tk.Frame(bookings_frame, bg=self.bg_white, relief="flat", bd=0, highlightthickness=1,
                            highlightcolor=self.border_color, highlightbackground=self.border_color)
        list_card.pack(fill="both", expand=True, padx=0, pady=(0, 20))
        
        list_label = tk.Label(list_card, text="📅  All Bookings", font=("Arial", 12, "bold"), 
                             fg=self.accent_blue, bg=self.bg_white, padx=15, pady=10)
        list_label.pack(anchor="w")
        
        # Separator
        sep = tk.Frame(list_card, bg=self.border_color, height=1)
        sep.pack(fill="x", padx=15)
        
        list_inner_frame = tk.Frame(list_card, bg=self.bg_white)
        list_inner_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Treeview with light styling
        columns = ("ID", "Date", "Time", "Department", "User", "Reason")
        self.bookings_tree = ttk.Treeview(list_inner_frame, columns=columns, show="headings", height=12)
        
        # Define Headings and widths
        col_widths = {"ID": 40, "Date": 90, "Time": 60, "Department": 110, "User": 110, "Reason": 250}
        for col in columns:
            self.bookings_tree.heading(col, text=col, command=lambda c=col: self.sort_bookings_by_column(c))
            self.bookings_tree.column(col, width=col_widths[col])
        
        # Configure treeview appearance
        style.configure("Treeview", font=("Arial", 10), rowheight=26, background=self.bg_white, 
                       foreground=self.text_primary, fieldbackground=self.bg_white, borderwidth=0)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#f0f4f8", 
                       foreground=self.accent_blue, borderwidth=0)
        
        # Add row colors
        self.bookings_tree.tag_configure('oddrow', background=self.bg_white, foreground=self.text_primary)
        self.bookings_tree.tag_configure('evenrow', background="#f0f4f8", foreground=self.text_primary)
        
        # Scrollbars
        vsb = ttk.Scrollbar(list_inner_frame, orient="vertical", command=self.bookings_tree.yview)
        hsb = ttk.Scrollbar(list_inner_frame, orient="horizontal", command=self.bookings_tree.xview)
        self.bookings_tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        
        self.bookings_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        list_inner_frame.grid_rowconfigure(0, weight=1)
        list_inner_frame.grid_columnconfigure(0, weight=1)
        
        # Action buttons for bookings
        action_frame = tk.Frame(list_card, bg=self.bg_white)
        action_frame.pack(fill="x", padx=15, pady=15)
        
        delete_btn = tk.Button(action_frame, text="🗑️  Delete Booking", command=self.delete_booking,
                              bg=self.danger_red, fg="white", font=("Arial", 10, "bold"),
                              cursor="hand2", relief="flat", bd=0, padx=15, pady=8)
        delete_btn.pack(side="left", padx=(0, 10))
        
        # ===== TAB 3: Manage Users =====
        users_tab = tk.Frame(notebook, bg=self.bg_white)
        notebook.add(users_tab, text="👤  Manage Users")
        
        users_frame = tk.Frame(users_tab, bg=self.bg_white)
        users_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        users_title = tk.Label(users_frame, text="Manage System Users", 
                              font=("Helvetica", 14, "bold"), fg=self.accent_blue, bg=self.bg_white)
        users_title.pack(anchor="w", pady=(0, 15))
        
        # Table frame for users
        users_table_frame = tk.Frame(users_frame, bg=self.bg_white, relief="solid", bd=1)
        users_table_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Treeview for users (Username | Full Name | Role)
        self.users_tree = ttk.Treeview(users_table_frame, columns=("Username", "Full Name", "Role"), 
                                       height=15, show="tree headings")
        
        # Define column headings and widths
        self.users_tree.column("#0", width=0)
        self.users_tree.column("Username", anchor="w", width=150)
        self.users_tree.column("Full Name", anchor="w", width=200)
        self.users_tree.column("Role", anchor="center", width=100)
        
        self.users_tree.heading("#0", text="")
        self.users_tree.heading("Username", text="Username")
        self.users_tree.heading("Full Name", text="Full Name")
        self.users_tree.heading("Role", text="Role")
        
        # Style for users tree
        style.configure("Treeview", font=("Arial", 10), rowheight=30, bg=self.bg_white)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background=self.bg_main)
        style.map('Treeview', background=[('selected', self.accent_blue)])
        
        self.users_tree.pack(fill="both", expand=True, side="left")
        
        # Scrollbar for users
        users_scrollbar = ttk.Scrollbar(users_table_frame, orient="vertical", command=self.users_tree.yview)
        users_scrollbar.pack(side="right", fill="y")
        self.users_tree.configure(yscroll=users_scrollbar.set)
        
        # Action buttons for users
        users_button_frame = tk.Frame(users_frame, bg=self.bg_white)
        users_button_frame.pack(fill="x", pady=(0, 10))
        
        delete_user_btn = tk.Button(users_button_frame, text="🗑️  Delete User", 
                                   command=self.delete_user,
                                   bg=self.danger_red, fg="white", font=("Arial", 11, "bold"),
                                   cursor="hand2", relief="flat", bd=0, padx=15, pady=8)
        delete_user_btn.pack(side="left", padx=(0, 10))
        
        users_refresh_btn = tk.Button(users_button_frame, text="🔄 Refresh", 
                                     command=self.load_users,
                                     bg=self.text_secondary, fg="white", font=("Arial", 11, "bold"),
                                     cursor="hand2", relief="flat", bd=0, padx=15, pady=8)
        users_refresh_btn.pack(side="right")
        
        # Load initial data
        self.load_requests()
        self.load_bookings()
        self.load_users()
    
    def load_requests(self):
        """Load pending user requests from database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Fetch pending requests
            cursor.execute("""
                SELECT id, full_name, username, created_at, status 
                FROM user_requests 
                WHERE status='pending' 
                ORDER BY created_at DESC
            """)
            
            requests = cursor.fetchall()
            conn.close()
            
            if not requests:
                self.tree.insert("", "end", values=("No pending requests", "", "", ""))
                return
            
            # Insert data into tree
            for req in requests:
                req_id, full_name, username, created_at, status = req
                # Format date nicely
                try:
                    formatted_date = created_at.split(" ")[0] if created_at else "Unknown"
                except:
                    formatted_date = created_at
                
                self.tree.insert("", "end", iid=str(req_id),
                               values=(full_name, username, formatted_date, "Pending"))
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load requests:\n{str(e)}")
    
    def approve_request(self):
        """Approve selected user request"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a request to approve")
            return
        
        item = selected[0]
        values = self.tree.item(item, "values")
        username = values[1]
        
        conn = None
        try:
            conn = sqlite3.connect(self.db_name, timeout=30.0)
            conn.execute("PRAGMA busy_timeout=30000")
            cursor = conn.cursor()
            
            # Get the request data including department
            cursor.execute("SELECT full_name, password, department FROM user_requests WHERE username=?", (username,))
            request = cursor.fetchone()
            
            if request:
                full_name, password, department = request
                
                # Check if username already exists in users table
                cursor.execute("SELECT id, role FROM users WHERE username=?", (username,))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    # User exists - update their password, full_name, department, and role to 'user'
                    cursor.execute("UPDATE users SET password=?, full_name=?, department=?, role='user' WHERE username=?",
                                 (password, full_name, department, username))
                    messagebox.showinfo("Info", f"User '{username}' updated and approved.")
                else:
                    # Insert into users table (approved)
                    cursor.execute("INSERT INTO users (username, full_name, password, department, role) VALUES (?, ?, ?, ?, ?)",
                                 (username, full_name, password, department, "user"))
                    messagebox.showinfo("Success", f"User '{username}' has been approved!")
                
                # Update request status
                cursor.execute("UPDATE user_requests SET status='approved' WHERE username=?", (username,))
                
                conn.commit()
                self.load_requests()
            else:
                messagebox.showerror("Error", "Request not found")
        
        except Exception as e:
            messagebox.showerror("Error", f"Approval failed:\n{str(e)}")
        finally:
            if conn:
                conn.close()
    
    
    
    def reject_request(self):
        """Reject selected user request"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a request to reject")
            return
        
        item = selected[0]
        values = self.tree.item(item, "values")
        username = values[1]
        
        # Confirm rejection
        if messagebox.askyesno("Confirm", f"Reject registration request for '{username}'?"):
            conn = None
            try:
                conn = sqlite3.connect(self.db_name, timeout=30.0)
                conn.execute("PRAGMA busy_timeout=30000")
                cursor = conn.cursor()
                
                # Update request status to rejected
                cursor.execute("UPDATE user_requests SET status='rejected' WHERE username=?", (username,))
                
                conn.commit()
                messagebox.showinfo("Success", f"Request from '{username}' has been rejected")
                self.load_requests()
            
            except Exception as e:
                messagebox.showerror("Error", f"Rejection failed:\n{str(e)}")
            finally:
                if conn:
                    conn.close()
    
    def load_bookings(self):
        """Load all bookings from database"""
        try:
            # Clear existing items
            for item in self.bookings_tree.get_children():
                self.bookings_tree.delete(item)
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, booking_date, booking_time, department, user_name, reason 
                FROM bookings 
                ORDER BY booking_date DESC, booking_time DESC
            """)
            bookings = cursor.fetchall()
            conn.close()
            
            if not bookings:
                self.bookings_tree.insert("", "end", values=("", "No bookings", "", "", "", ""))
                return
            
            # Insert data into tree with alternating row colors
            for i, booking in enumerate(bookings):
                booking_id, date, time, dept, user, reason = booking
                tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                self.bookings_tree.insert("", "end", iid=str(booking_id),
                                        values=(booking_id, date, time, dept, user, reason), tags=(tag,))
            
            self.all_bookings = bookings
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bookings:\n{str(e)}")
    
    def filter_bookings(self):
        """Filter bookings based on search"""
        search_term = self.search_var.get().lower().strip()
        
        # Clear treeview
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)
        
        if not search_term:
            # Show all bookings if search is empty
            self.load_bookings()
            return
        
        try:
            # Filter all bookings based on search term
            filtered = [b for b in self.all_bookings if 
                       search_term in str(b[1]).lower() or  # date
                       search_term in str(b[3]).lower() or  # department
                       search_term in str(b[4]).lower() or  # user
                       search_term in str(b[5]).lower()]    # reason
            
            if not filtered:
                self.bookings_tree.insert("", "end", values=("", "No matching bookings", "", "", "", ""))
                return
            
            # Insert filtered data
            for i, booking in enumerate(filtered):
                booking_id, date, time, dept, user, reason = booking
                tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                self.bookings_tree.insert("", "end", iid=str(booking_id),
                                        values=(booking_id, date, time, dept, user, reason), tags=(tag,))
        
        except Exception as e:
            messagebox.showerror("Error", f"Filter failed:\n{str(e)}")
    
    def delete_booking(self):
        """Delete selected booking"""
        selected = self.bookings_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to delete")
            return
        
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this booking?"):
            return
        
        try:
            item = self.bookings_tree.item(selected[0])
            booking_id = item['values'][0]
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Booking deleted successfully!")
            self.load_bookings()
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete booking:\n{str(e)}")
    
    def sort_bookings_by_column(self, col):
        """Sort bookings by column"""
        # Get all current items
        items = [(self.bookings_tree.item(k)["values"], k) for k in self.bookings_tree.get_children()]
        
        # Get column index
        col_index = {"ID": 0, "Date": 1, "Time": 2, "Department": 3, "User": 4, "Reason": 5}
        col_idx = col_index.get(col, 0)
        
        # Sort
        items.sort(key=lambda x: x[0][col_idx])
        
        # Re-insert sorted items
        for i, (values, iid) in enumerate(items):
            self.bookings_tree.delete(iid)
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            self.bookings_tree.insert("", "end", iid=iid, values=values, tags=(tag,))
    
    def load_users(self):
        """Load all users from database"""
        try:
            # Clear existing items
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, full_name, role 
                FROM users 
                ORDER BY username ASC
            """)
            users = cursor.fetchall()
            conn.close()
            
            if not users:
                self.users_tree.insert("", "end", values=("", "No users found", ""))
                return
            
            # Insert data into tree
            for user in users:
                user_id, username, full_name, role = user
                self.users_tree.insert("", "end", iid=str(user_id),
                                     values=(username, full_name, role))
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users:\n{str(e)}")
    
    def delete_user(self):
        """Delete selected user"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        item = selected[0]
        values = self.users_tree.item(item, "values")
        username = values[0]
        
        # Prevent deletion of admin account
        if username == "admin":
            messagebox.showerror("Error", "Cannot delete the admin account")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{username}'?\nThis action cannot be undone."):
            return
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Delete user from users table
            cursor.execute("DELETE FROM users WHERE username=?", (username,))
            
            # Also delete any bookings made by this user
            cursor.execute("DELETE FROM bookings WHERE user_name=?", (username,))
            
            # Also delete any pending registration requests for this user
            cursor.execute("DELETE FROM user_requests WHERE username=?", (username,))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"User '{username}' has been deleted successfully!")
            self.load_users()
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete user:\n{str(e)}")
    
    def init_database(self):
        """Initialize database tables for admin panel"""
        try:
            conn = sqlite3.connect(self.db_name, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=30000")
            cursor = conn.cursor()
            
            # Create users table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    full_name TEXT,
                    password TEXT NOT NULL,
                    department TEXT,
                    role TEXT DEFAULT 'user'
                )
            ''')
            
            # Create user_requests table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    full_name TEXT,
                    password TEXT NOT NULL,
                    department TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create bookings table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    booking_date TEXT NOT NULL,
                    booking_time TEXT NOT NULL,
                    duration_minutes INTEGER DEFAULT 60,
                    department TEXT NOT NULL,
                    user_name TEXT NOT NULL,
                    reason TEXT,
                    building TEXT DEFAULT 'Main Office',
                    room TEXT DEFAULT 'Board Room A',
                    attendees TEXT DEFAULT '5-10',
                    floor TEXT DEFAULT '2nd Floor',
                    priority TEXT DEFAULT 'Regular',
                    setup TEXT DEFAULT 'None',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to initialize database:\n{str(e)}")
    
    def logout(self):
        """Logout and return to login"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            # Restart the application with login screen
            root = tk.Tk()
            login = LoginWindow(root)
            root.mainloop()
            
            if login.logged_in_user:
                if login.is_admin:
                    # Open Admin Panel again
                    admin_root = tk.Tk()
                    admin = AdminPanel(admin_root, login.logged_in_user)
                    admin_root.mainloop()
                else:
                    # Open Regular User App
                    app_root = tk.Tk()
                    app = TasmaBookingApp(app_root, login.logged_in_user, is_admin=login.is_admin, user_department=login.user_department)
                    app_root.mainloop()


class TasmaBookingApp:
    def __init__(self, root, logged_in_user, is_admin=False, user_department=None):
        self.root = root
        self.logged_in_user = logged_in_user
        self.user_department = user_department  # Store user's registered department
        self.is_admin = is_admin  # Track if user is admin
        self.root.title("TASMA Board Room Booking System")
        # Set fullscreen
        self.root.state('zoomed')
        self.root.resizable(True, True)
        
        # Light Theme Colors
        self.bg_main = "#f5f7fa"
        self.bg_white = "#ffffff"
        self.bg_light = "#f0f4f8"
        self.accent_blue = "#0052cc"
        self.accent_blue_light = "#0066ff"
        self.accent_blue_lighter = "#e0eaff"
        self.text_primary = "#1f2937"
        self.text_secondary = "#6b7280"
        self.border_color = "#d1d5db"
        self.button_hover = "#003d99"
        self.success_green = "#10b981"
        self.danger_red = "#ef4444"
        
        # Set root background
        self.root.configure(bg=self.bg_main)
        
        # Database Configuration - Handle both normal Python and PyInstaller bundled execution
        import sys
        import os
        # Get the directory where the app/executable is located
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller bundle - store database in AppData for write permissions
            app_data = os.getenv('APPDATA')
            app_dir = os.path.join(app_data, 'TASMA')
            if not os.path.exists(app_dir):
                os.makedirs(app_dir)
        else:
            # Running as normal Python script
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Use server database path if available, otherwise local
        self.db_name = self.get_db_path()
        self.init_database()
        
        self.selected_booking_id = None
        self.is_edit_mode = False
        self.current_hour = datetime.now().hour
        self.current_minute = 0
        
        # --- Main Container ---
        main_container = tk.Frame(root, bg=self.bg_main)
        main_container.pack(fill="both", expand=True)
        
        # --- Header/Title ---
        title_frame = tk.Frame(main_container, bg=self.bg_white, height=70)
        title_frame.pack(fill="x", padx=20, pady=15)
        
        # Left side - Logo/Title
        left_frame = tk.Frame(title_frame, bg=self.bg_white)
        left_frame.pack(side="left")
        
        try:
            # Try to load and display logo image
            if os.path.exists('tasma_logo.webp'):
                logo_img = Image.open('tasma_logo.webp')
                logo_img = logo_img.resize((120, 50), Image.Resampling.LANCZOS)
                self.header_logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = tk.Label(left_frame, image=self.header_logo_photo, bg=self.bg_white)
                logo_label.image = self.header_logo_photo  # Keep a reference
                logo_label.pack(side="left")
            else:
                title_label = tk.Label(left_frame, text="🏢 TASMA", 
                                      font=("Helvetica", 26, "bold"), fg=self.accent_blue, 
                                      bg=self.bg_white)
                title_label.pack(side="left")
        except Exception as e:
            title_label = tk.Label(left_frame, text="🏢 TASMA", 
                                  font=("Helvetica", 26, "bold"), fg=self.accent_blue, 
                                  bg=self.bg_white)
            title_label.pack(side="left")
        
        subtitle_label = tk.Label(left_frame, text="Board Room Booking System", 
                                 font=("Helvetica", 12), fg=self.text_secondary, 
                                 bg=self.bg_white)
        subtitle_label.pack(side="left", padx=15)
        
        # Right side - User info and logout
        right_frame = tk.Frame(title_frame, bg=self.bg_white)
        right_frame.pack(side="right")
        
        role_text = "👨‍💼 Admin" if self.is_admin else "👤 User"
        user_label = tk.Label(right_frame, text=f"{role_text} - {self.logged_in_user}", 
                             font=("Arial", 10), fg=self.accent_blue, 
                             bg=self.bg_white)
        user_label.pack(side="left", padx=10)
        
        logout_btn = tk.Button(right_frame, text="🚪 Logout", command=self.logout,
                              bg="#ef4444", fg="white", font=("Arial", 9, "bold"),
                              cursor="hand2", relief="flat", bd=0, padx=10, pady=5)
        logout_btn.pack(side="left")
        
        # --- Status Bar ---
        status_frame = tk.Frame(main_container, bg=self.bg_white, height=35)
        status_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.status_label = tk.Label(status_frame, text="✓ Ready", font=("Arial", 10), 
                                    fg=self.accent_blue, bg=self.bg_white, justify="left")
        self.status_label.pack(side="left")
        
        # --- Content Frame ---
        content_frame = tk.Frame(main_container, bg=self.bg_main)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Configure style for tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.bg_main, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 12], font=("Arial", 10, "bold"), 
                       background=self.bg_light, foreground=self.text_secondary)
        style.map('TNotebook.Tab', 
                  background=[('selected', self.bg_white), ('active', self.bg_white)],
                  foreground=[('selected', self.accent_blue)])
        style.configure('TNotebook.Tbackground', background=self.bg_main)
        
        # --- Notebook (Tabs) ---
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # ===== TAB 1: New Booking =====
        book_tab = tk.Frame(self.notebook, bg=self.bg_main)
        self.notebook.add(book_tab, text="📅  New Booking")
        
        # Create scrollable frame with canvas
        canvas = tk.Canvas(book_tab, bg=self.bg_main, highlightthickness=0)
        scrollbar = ttk.Scrollbar(book_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_main)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Bind mousewheel for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Scroll frame inside canvas
        scroll_frame = tk.Frame(scrollable_frame, bg=self.bg_main)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form Card - Modern design
        form_card = tk.Frame(scroll_frame, bg=self.bg_white, relief="solid", bd=1, 
                            highlightthickness=2, highlightcolor=self.border_color, 
                            highlightbackground=self.border_color)
        form_card.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Modern Header with blue background
        header_frame = tk.Frame(form_card, bg=self.accent_blue, height=70)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        card_title = tk.Label(header_frame, text="📅 Create Your Booking", font=("Arial", 18, "bold"), 
                             fg="white", bg=self.accent_blue, pady=15)
        card_title.pack(anchor="w", padx=20)
        
        subtitle = tk.Label(header_frame, text="Fill in the details to reserve your meeting room", 
                           font=("Arial", 10), fg="#cce5ff", bg=self.accent_blue)
        subtitle.pack(anchor="w", padx=20, pady=(0, 5))
        
        form_frame = tk.Frame(form_card, bg=self.bg_white)
        form_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Section 1: Date & Time (grouped together)
        section1_title = tk.Label(form_frame, text="When", font=("Arial", 12, "bold"), 
                                 fg=self.accent_blue, bg=self.bg_white)
        section1_title.pack(anchor="w", pady=(0, 12))
        
        section1_box = tk.Frame(form_frame, bg=self.bg_light, relief="solid", bd=1)
        section1_box.pack(fill="x", pady=(0, 20))
        
        section1_inner = tk.Frame(section1_box, bg=self.bg_light)
        section1_inner.pack(fill="x", padx=15, pady=15)
        
        # Row 1: Date and Time
        self._create_form_field(section1_inner, "📅 Date:", 0, 0)
        
        # Use DateEntry with popup calendar (closes after selection)
        self.entry_date = DateEntry(section1_inner, width=20, background=self.accent_blue, 
                                   foreground="white", borderwidth=2, font=("Arial", 11),
                                   year=datetime.now().year, month=datetime.now().month, 
                                   day=datetime.now().day)
        self.entry_date.grid(row=0, column=1, pady=8, padx=15, sticky="w")
        
        self._create_form_field(section1_inner, "⏰ Time:", 0, 2)
        time_frame = tk.Frame(section1_inner, bg=self.bg_light)
        time_frame.grid(row=0, column=3, pady=8, padx=15, sticky="w")
        
        self.hour_var = tk.IntVar(value=0)
        self.minute_var = tk.IntVar(value=0)
        
        # Hour spinbox
        tk.Label(time_frame, text="Hour:", font=("Arial", 10, "bold"), fg=self.accent_blue, 
                bg=self.bg_light).pack(side="left", padx=(0, 8))
        self.hour_spinbox = tk.Spinbox(time_frame, from_=0, to=23, width=4, 
                                      font=("Arial", 12, "bold"), justify="center",
                                      bg="white", fg=self.text_primary, 
                                      borderwidth=1, relief="solid", command=self.on_time_spinbox_change,
                                      textvariable=self.hour_var)
        self.hour_spinbox.pack(side="left", padx=3)
        
        tk.Label(time_frame, text=":", font=("Arial", 12, "bold"), fg=self.text_primary,
                bg=self.bg_light).pack(side="left", padx=5)
        
        tk.Label(time_frame, text="Min:", font=("Arial", 10, "bold"), fg=self.accent_blue,
                bg=self.bg_light).pack(side="left", padx=(5, 8))
        self.minute_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=4,
                                        font=("Arial", 12, "bold"), justify="center",
                                        bg="white", fg=self.text_primary,
                                        borderwidth=1, relief="solid", command=self.on_time_spinbox_change,
                                        textvariable=self.minute_var)
        self.minute_spinbox.pack(side="left", padx=3)
        
        # Section 2: What (Department, User, Duration)
        section2_title = tk.Label(form_frame, text="What", font=("Arial", 12, "bold"), 
                                 fg=self.accent_blue, bg=self.bg_white)
        section2_title.pack(anchor="w", pady=(15, 12))
        
        section2_box = tk.Frame(form_frame, bg=self.bg_light, relief="solid", bd=1)
        section2_box.pack(fill="x", pady=(0, 20))
        
        section2_inner = tk.Frame(section2_box, bg=self.bg_light)
        section2_inner.pack(fill="x", padx=15, pady=15)
        
        # Row: Department, User, Duration
        self._create_form_field(section2_inner, "🏢 Department:", 0, 0)
        self.entry_dept = ttk.Combobox(section2_inner, width=20, font=("Arial", 11), 
                                       values=["Finance", "HR", "IT", "Marketing", "Operations", "Sales", "Other"],
                                       state="readonly")
        self.entry_dept.grid(row=0, column=1, pady=8, padx=15, sticky="w")
        if self.user_department:
            self.entry_dept.set(self.user_department)
        
        self._create_form_field(section2_inner, "👤 Organizer:", 0, 2)
        self.entry_user = tk.Entry(section2_inner, width=20, font=("Arial", 11), 
                                  bg="white", fg=self.text_primary, 
                                  insertbackground=self.accent_blue, borderwidth=1, 
                                  relief="solid", state="readonly")
        self.entry_user.grid(row=0, column=3, pady=8, padx=15, sticky="w")
        self.entry_user.config(state="normal")
        self.entry_user.insert(0, self.logged_in_user)
        self.entry_user.config(state="readonly")
        
        # Duration on new row
        self._create_form_field(section2_inner, "⏱️ Duration:", 1, 0)
        self.entry_duration = ttk.Combobox(section2_inner, width=20, font=("Arial", 11),
                                          values=["30 minutes", "1 hour", "1.5 hours", "2 hours", "2.5 hours", "3 hours", "4 hours", "Full day (8 hours)"],
                                          state="readonly")
        self.entry_duration.set("1 hour")
        self.entry_duration.grid(row=1, column=1, pady=8, padx=15, sticky="w")
        
        # Section 3: Why (Reason)
        section3_title = tk.Label(form_frame, text="Why", font=("Arial", 12, "bold"), 
                                 fg=self.accent_blue, bg=self.bg_white)
        section3_title.pack(anchor="w", pady=(15, 12))
        
        section3_box = tk.Frame(form_frame, bg=self.bg_light, relief="solid", bd=1)
        section3_box.pack(fill="x", pady=(0, 25))
        
        section3_inner = tk.Frame(section3_box, bg=self.bg_light)
        section3_inner.pack(fill="x", padx=15, pady=15)
        
        reason_label = tk.Label(section3_inner, text="📝 Meeting Purpose (optional):", font=("Arial", 11, "bold"), 
                               fg=self.accent_blue, bg=self.bg_light)
        reason_label.pack(anchor="w", pady=(0, 8))
        
        self.entry_reason = tk.Text(section3_inner, width=70, height=3, font=("Arial", 11),
                                    bg="white", fg=self.text_primary, 
                                    insertbackground=self.accent_blue, borderwidth=1, relief="solid")
        self.entry_reason.pack(fill="both", expand=True)
        
        # Section 4: Additional Details
        section4_title = tk.Label(form_frame, text="Details", font=("Arial", 12, "bold"), 
                                 fg=self.accent_blue, bg=self.bg_white)
        section4_title.pack(anchor="w", pady=(15, 12))
        
        section4_box = tk.Frame(form_frame, bg=self.bg_light, relief="solid", bd=1)
        section4_box.pack(fill="x", pady=(0, 20))
        
        section4_inner = tk.Frame(section4_box, bg=self.bg_light)
        section4_inner.pack(fill="x", padx=15, pady=15)
        
        # Row: Priority and Equipment
        self._create_form_field(section4_inner, "⭐ Priority:", 0, 0)
        self.entry_priority = ttk.Combobox(section4_inner, width=20, font=("Arial", 11),
                                          values=["Regular", "Important", "Urgent", "Critical"],
                                          state="readonly")
        self.entry_priority.set("Regular")
        self.entry_priority.grid(row=0, column=1, pady=8, padx=15, sticky="w")
        
        self._create_form_field(section4_inner, "🔧 Setup Needed:", 0, 2)
        self.entry_setup = ttk.Combobox(section4_inner, width=20, font=("Arial", 11),
                                       values=["None", "Projector", "Video Conference", "Whiteboard", 
                                              "Audio System", "Multiple"],
                                       state="readonly")
        self.entry_setup.set("None")
        self.entry_setup.grid(row=0, column=3, pady=8, padx=15, sticky="w")
        
        # Row: Additional Notes
        notes_label = tk.Label(section4_inner, text="📎 Additional Notes (optional):", font=("Arial", 11, "bold"), 
                              fg=self.accent_blue, bg=self.bg_light)
        notes_label.grid(row=1, column=0, columnspan=4, sticky="w", pady=(10, 8))
        
        self.entry_notes = tk.Text(section4_inner, width=70, height=2, font=("Arial", 10),
                                   bg="white", fg=self.text_primary, 
                                   insertbackground=self.accent_blue, borderwidth=1, relief="solid")
        self.entry_notes.grid(row=2, column=0, columnspan=4, sticky="ew", pady=8)
        
        # Buttons Frame - Modern style
        btn_frame = tk.Frame(form_card, bg=self.bg_white)
        btn_frame.pack(fill="x", padx=25, pady=25)
        
        # Primary button (Book Room) - larger and more prominent
        book_btn = tk.Button(btn_frame, text="✓ BOOK ROOM", command=self.add_booking,
                            bg=self.success_green, fg="white", font=("Arial", 12, "bold"),
                            relief="flat", bd=0, padx=35, pady=14, cursor="hand2",
                            activebackground="#059669", activeforeground="white")
        book_btn.pack(side="left", padx=(0, 12), fill="y")
        
        # Secondary buttons
        if self.is_admin:
            edit_btn = tk.Button(btn_frame, text="✎ Edit", command=self.edit_booking,
                               bg="#f59e0b", fg="white", font=("Arial", 11, "bold"),
                               relief="flat", bd=0, padx=20, pady=12, cursor="hand2",
                               activebackground="#d97706", activeforeground="white")
            edit_btn.pack(side="left", padx=(0, 8), fill="y")
        
        clear_btn = tk.Button(btn_frame, text="⟲ Clear", command=self.clear_inputs,
                             bg="#8b5cf6", fg="white", font=("Arial", 11, "bold"),
                             relief="flat", bd=0, padx=20, pady=12, cursor="hand2",
                             activebackground="#7c3aed", activeforeground="white")
        clear_btn.pack(side="left", fill="y")
        
        # ===== TAB 2: Manage Bookings (ADMIN ONLY) =====
        # Only add this tab if user is admin
        if self.is_admin:
            manage_tab = tk.Frame(self.notebook, bg=self.bg_main)
            self.notebook.add(manage_tab, text="📋  Manage Bookings")
            
            # Create scrollable container
            manage_canvas = tk.Canvas(manage_tab, bg=self.bg_main, highlightthickness=0)
            manage_scrollbar = ttk.Scrollbar(manage_tab, orient="vertical", command=manage_canvas.yview)
            manage_scrollable = tk.Frame(manage_canvas, bg=self.bg_main)
            
            manage_scrollable.bind(
                "<Configure>",
                lambda e: manage_canvas.configure(scrollregion=manage_canvas.bbox("all"))
            )
            
            manage_canvas.create_window((0, 0), window=manage_scrollable, anchor="nw")
            manage_canvas.configure(yscrollcommand=manage_scrollbar.set)
            
            manage_scrollbar.pack(side="right", fill="y")
            manage_canvas.pack(side="left", fill="both", expand=True)
            
            def _on_manage_mousewheel(event):
                manage_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            manage_canvas.bind_all("<MouseWheel>", _on_manage_mousewheel)
            
            # Header Card with Stats
            header_card = tk.Frame(manage_scrollable, bg=self.bg_white, relief="solid", bd=1,
                                  highlightthickness=1, highlightcolor=self.border_color, highlightbackground=self.border_color)
            header_card.pack(fill="x", padx=20, pady=20)
            
            header_frame = tk.Frame(header_card, bg=self.accent_blue, height=60)
            header_frame.pack(fill="x", padx=0, pady=0)
            header_frame.pack_propagate(False)
            
            header_title = tk.Label(header_frame, text="📋 Manage Bookings", font=("Arial", 16, "bold"),
                                   fg="white", bg=self.accent_blue, padx=20, pady=10)
            header_title.pack(anchor="w")
            
            stats_frame = tk.Frame(header_card, bg=self.bg_light)
            stats_frame.pack(fill="x", padx=20, pady=15)
            
            self.booking_count_label = tk.Label(stats_frame, text="📊 Total Bookings: 0", font=("Arial", 10, "bold"),
                                               fg=self.accent_blue, bg=self.bg_light)
            self.booking_count_label.pack(anchor="w", pady=5)
            
            # Search and Filter Frame
            search_card = tk.Frame(manage_scrollable, bg=self.bg_white, relief="solid", bd=1,
                                  highlightthickness=1, highlightcolor=self.border_color, highlightbackground=self.border_color)
            search_card.pack(fill="x", padx=20, pady=(0, 20))
            
            search_header = tk.Label(search_card, text="🔍 Search & Filter Bookings", font=("Arial", 12, "bold"),
                                    fg=self.accent_blue, bg=self.bg_white, padx=15, pady=10)
            search_header.pack(anchor="w")
            
            search_frame = tk.Frame(search_card, bg=self.bg_white)
            search_frame.pack(fill="x", padx=15, pady=(0, 15))
            
            self.search_var = tk.StringVar()
            self.search_var.trace("w", lambda *args: self.filter_bookings())
            search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=50,
                                   font=("Arial", 11), bg=self.bg_light, fg=self.text_primary,
                                   insertbackground=self.accent_blue, borderwidth=1, relief="solid")
            search_entry.pack(side="left", padx=5, fill="x", expand=True)
            
            search_hint = tk.Label(search_frame, text="(Date, Department, User, Reason)",
                                  font=("Arial", 9), bg=self.bg_white, fg=self.text_secondary)
            search_hint.pack(side="left", padx=10)
            
            # Filter by Department
            filter_frame = tk.Frame(search_card, bg=self.bg_white)
            filter_frame.pack(fill="x", padx=15, pady=(0, 15))
            
            tk.Label(filter_frame, text="🏢 Filter by Department:", font=("Arial", 10, "bold"),
                    fg=self.accent_blue, bg=self.bg_white).pack(side="left", padx=(0, 10))
            
            self.dept_filter_var = tk.StringVar(value="All")
            self.dept_filter_var.trace("w", lambda *args: self.filter_bookings())
            dept_filter = ttk.Combobox(filter_frame, textvariable=self.dept_filter_var, width=20,
                                      font=("Arial", 10), values=["All", "Finance", "HR", "IT", "Marketing", 
                                                                  "Operations", "Sales", "Other"], state="readonly")
            dept_filter.pack(side="left", padx=5)
            
            clear_btn = tk.Button(filter_frame, text="🔄 Reset Filters", command=self.reset_filters,
                                 bg=self.accent_blue, fg="white", font=("Arial", 10, "bold"),
                                 relief="flat", bd=0, padx=15, pady=8, cursor="hand2",
                                 activebackground="#003db3")
            clear_btn.pack(side="left", padx=10)
            
            # Bookings Display Frame (Card-based)
            self.bookings_list_frame = tk.Frame(manage_scrollable, bg=self.bg_main)
            self.bookings_list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            # Create scrollable frame for booking cards
            bookings_canvas = tk.Canvas(self.bookings_list_frame, bg=self.bg_main, highlightthickness=0)
            bookings_scrollbar = ttk.Scrollbar(self.bookings_list_frame, orient="vertical", command=bookings_canvas.yview)
            self.bookings_scrollable = tk.Frame(bookings_canvas, bg=self.bg_main)
            
            self.bookings_scrollable.bind(
                "<Configure>",
                lambda e: bookings_canvas.configure(scrollregion=bookings_canvas.bbox("all"))
            )
            
            bookings_canvas.create_window((0, 0), window=self.bookings_scrollable, anchor="nw")
            bookings_canvas.configure(yscrollcommand=bookings_scrollbar.set)
            
            bookings_scrollbar.pack(side="right", fill="y")
            bookings_canvas.pack(side="left", fill="both", expand=True)
            
            # Store reference for loading bookings
            self.bookings_display_canvas = bookings_canvas
            
            # Action buttons
            action_frame = tk.Frame(manage_scrollable, bg=self.bg_white, relief="solid", bd=1,
                                   highlightthickness=1, highlightcolor=self.border_color, highlightbackground=self.border_color)
            action_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            action_inner = tk.Frame(action_frame, bg=self.bg_white)
            action_inner.pack(fill="x", padx=15, pady=15)
            
            self._create_button(action_inner, "🗑️  Delete Selected", self.delete_booking, self.danger_red, side="left")
            self._create_button(action_inner, "💾  Export CSV", self.export_to_csv, self.success_green, side="left")
            self._create_button(action_inner, "🔄  Refresh", self.load_bookings, self.accent_blue, side="left")
            
            # Initialize empty state
            self.tree = None  # For compatibility with filter_bookings
            self.manage_bookings_cards = []  # Store card references for filtering
        else:
            # For non-admin users, create a simple search variable (needed by filter_bookings method)
            self.search_var = tk.StringVar()
            self.tree = None  # Placeholder for non-admin users
            self.bookings_scrollable = None
        
        # ===== TAB 3: Calendar View =====
        calendar_tab = tk.Frame(self.notebook, bg=self.bg_main)
        self.notebook.add(calendar_tab, text="📆  Calendar View")
        
        # Main container for calendar tab with grid layout
        cal_main_frame = tk.Frame(calendar_tab, bg=self.bg_main)
        cal_main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configure grid weights for responsive layout
        cal_main_frame.grid_columnconfigure(0, weight=2, minsize=400)
        cal_main_frame.grid_columnconfigure(1, weight=1, minsize=350)
        cal_main_frame.grid_rowconfigure(0, weight=1)
        
        # Left side - Calendar Widget (Modern card style with shadow)
        cal_left_card = tk.Frame(cal_main_frame, bg=self.bg_white, relief="solid", bd=1,
                                highlightthickness=2, highlightcolor=self.border_color, 
                                highlightbackground=self.border_color)
        cal_left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        cal_left_title = tk.Label(cal_left_card, text="📅 Select a Date", font=("Arial", 13, "bold"), 
                                 fg=self.accent_blue, bg=self.bg_white, pady=12)
        cal_left_title.pack(anchor="w", padx=15, pady=(15, 0))
        
        cal_sep = tk.Frame(cal_left_card, bg=self.accent_blue, height=2)
        cal_sep.pack(fill="x", padx=15, pady=(8, 12))
        
        cal_left_frame = tk.Frame(cal_left_card, bg=self.bg_white)
        cal_left_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.calendar_widget = Calendar(cal_left_frame, selectmode='day', year=datetime.now().year, 
                                       month=datetime.now().month, day=datetime.now().day,
                                       cursor="hand2", font=("Arial", 10), headersformatvar="long",
                                       width=30, background=self.bg_white, foreground=self.text_primary,
                                       fieldbackground=self.bg_white, selectforeground=self.bg_white,
                                       selectbackground=self.accent_blue, normalbackground=self.bg_white,
                                       normalforeground=self.text_primary, othermonthforeground=self.text_secondary,
                                       othermonthweforeground=self.text_secondary, weekendforeground=self.accent_blue)
        self.calendar_widget.pack(fill="both", expand=True)
        self.calendar_widget.bind("<<CalendarSelected>>", self.on_calendar_selected)
        
        # Configure tag for dates with bookings
        self.calendar_widget.tag_config('booked', background=self.accent_blue, foreground=self.bg_white)
        
        # Right side - Bookings Details (Modern card style with shadow)
        cal_right_card = tk.Frame(cal_main_frame, bg=self.bg_white, relief="solid", bd=1,
                                 highlightthickness=2, highlightcolor=self.border_color,
                                 highlightbackground=self.border_color)
        cal_right_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        cal_right_title = tk.Label(cal_right_card, text="📋 Bookings", font=("Arial", 13, "bold"), 
                                  fg=self.accent_blue, bg=self.bg_white, pady=12)
        cal_right_title.pack(anchor="w", padx=15, pady=(15, 0))
        
        cal_sep2 = tk.Frame(cal_right_card, bg=self.accent_blue, height=2)
        cal_sep2.pack(fill="x", padx=15, pady=(8, 12))
        
        # Selected date label - Modern banner style
        self.selected_date_label = tk.Label(cal_right_card, text="", font=("Arial", 12, "bold"), 
                                           bg=self.accent_blue, fg="white", padx=15, pady=12, 
                                           relief="flat", anchor="w")
        self.selected_date_label.pack(fill="x", padx=15, pady=(0, 15))
        
        # Scrollable frame for booking cards
        scrollable_frame = tk.Frame(cal_right_card, bg=self.bg_white)
        scrollable_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Create a canvas with scrollbar for scrollable content
        self.calendar_canvas = tk.Canvas(scrollable_frame, bg=self.bg_white, highlightthickness=0, relief="flat")
        scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=self.calendar_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.calendar_canvas.configure(yscrollcommand=scrollbar.set)
        self.calendar_canvas.pack(side="left", fill="both", expand=True)
        
        # Frame inside canvas to hold booking cards
        self.booking_cards_frame = tk.Frame(self.calendar_canvas, bg=self.bg_white)
        self.canvas_window = self.calendar_canvas.create_window((0, 0), window=self.booking_cards_frame, anchor="nw")
        
        # Bind canvas resize to update window
        self.calendar_canvas.bind("<Configure>", self._on_canvas_configure)
        self.booking_cards_frame.bind("<Configure>", self._on_frame_configure)
        
        # Button Frame - Modern button styling
        cal_button_frame = tk.Frame(cal_right_card, bg=self.bg_white)
        cal_button_frame.pack(fill="x", padx=15, pady=15)
        
        today_btn = tk.Button(cal_button_frame, text="🏠 Today", command=self.calendar_goto_today,
                             bg=self.accent_blue, fg="white", font=("Arial", 11, "bold"),
                             relief="flat", bd=0, padx=20, pady=10, cursor="hand2",
                             activebackground="#003db3", activeforeground="white")
        today_btn.pack(side="left", padx=(0, 10), fill="y")
        
        refresh_btn = tk.Button(cal_button_frame, text="⟲ Refresh", command=self.calendar_refresh_display,
                               bg=self.success_green, fg="white", font=("Arial", 11, "bold"),
                               relief="flat", bd=0, padx=20, pady=10, cursor="hand2",
                               activebackground="#059669", activeforeground="white")
        refresh_btn.pack(side="left", fill="y")
        
        self.selected_date = None
        
        # Load initial data
        self.load_bookings()
        
        # Initialize calendar display after load_bookings
        self.on_calendar_selected(None)

    def on_time_spinbox_change(self):
        """Handle time spinbox value changes"""
        try:
            self.current_hour = self.hour_var.get()
            self.current_minute = self.minute_var.get()
            
            # Clamp values
            self.current_hour = max(0, min(23, self.current_hour))
            self.current_minute = max(0, min(59, self.current_minute))
            
            # Update variables with clamped values
            self.hour_var.set(self.current_hour)
            self.minute_var.set(self.current_minute)
        except:
            pass

    def _create_form_field(self, parent, label_text, row, col):
        """Helper to create form field labels"""
        label = tk.Label(parent, text=label_text, font=("Arial", 11, "bold"), 
                        fg=self.accent_blue, bg=self.bg_white)
        label.grid(row=row, column=col, sticky="w", pady=12, padx=15, columnspan=1)
        return label
    
    def _create_button(self, parent, text, command, color, side="left"):
        """Helper to create modern buttons"""
        btn = tk.Button(parent, text=text, command=command, bg=color, fg="white", 
                       font=("Arial", 10, "bold"), width=16, height=2, cursor="hand2", 
                       relief="flat", bd=0, activebackground=self.button_hover, activeforeground="white")
        btn.pack(side=side, padx=8)
        return btn

    def get_db_path(self):
        """Get database path - checks config.ini first for server path"""
        import sys
        import configparser
        
        # Check for config.ini with server database path
        config_file = None
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller bundle
            app_data = os.getenv('APPDATA')
            app_dir = os.path.join(app_data, 'TASMA')
            config_file = os.path.join(app_dir, 'config.ini')
            if not os.path.exists(app_dir):
                os.makedirs(app_dir)
        else:
            # Running as normal Python script
            app_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(app_dir, 'config.ini')
        
        # Try to read server database path from config
        try:
            if os.path.exists(config_file):
                config = configparser.ConfigParser()
                config.read(config_file)
                if config.has_option('Database', 'database_path'):
                    db_path = config.get('Database', 'database_path')
                    print(f"Using server database: {db_path}")
                    return db_path
        except Exception as e:
            print(f"Warning: Could not read config.ini: {e}")
        
        # Fallback to local database in AppData
        if getattr(sys, 'frozen', False):
            app_data = os.getenv('APPDATA')
            app_dir = os.path.join(app_data, 'TASMA')
            if not os.path.exists(app_dir):
                os.makedirs(app_dir)
        else:
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        local_db = os.path.join(app_dir, "bookings.db")
        print(f"Using local database: {local_db}")
        return local_db

    def init_database(self):
        """Create the database and table if they don't exist"""
        conn = sqlite3.connect(self.db_name, timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=30000")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_date TEXT NOT NULL,
                booking_time TEXT NOT NULL,
                duration_minutes INTEGER DEFAULT 60,
                department TEXT NOT NULL,
                user_name TEXT NOT NULL,
                reason TEXT,
                building TEXT DEFAULT 'Main Office',
                room TEXT DEFAULT 'Board Room A',
                attendees TEXT DEFAULT '5-10',
                floor TEXT DEFAULT '2nd Floor',
                priority TEXT DEFAULT 'Regular',
                setup TEXT DEFAULT 'None',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Migrate: Add new columns if they don't exist
        try:
            cursor.execute("ALTER TABLE bookings ADD COLUMN building TEXT DEFAULT 'Main Office'")
        except:
            pass
        try:
            cursor.execute("ALTER TABLE bookings ADD COLUMN room TEXT DEFAULT 'Board Room A'")
        except:
            pass
        try:
            cursor.execute("ALTER TABLE bookings ADD COLUMN attendees TEXT DEFAULT '5-10'")
        except:
            pass
        try:
            cursor.execute("ALTER TABLE bookings ADD COLUMN floor TEXT DEFAULT '2nd Floor'")
        except:
            pass
        try:
            cursor.execute("ALTER TABLE bookings ADD COLUMN priority TEXT DEFAULT 'Regular'")
        except:
            pass
        try:
            cursor.execute("ALTER TABLE bookings ADD COLUMN setup TEXT DEFAULT 'None'")
        except:
            pass
        try:
            cursor.execute("ALTER TABLE bookings ADD COLUMN notes TEXT")
        except:
            pass
        
        conn.commit()
        conn.close()

    def add_booking(self):
        """Insert new or update booking in database"""
        # Get the date from DateEntry popup
        try:
            date_obj = self.entry_date.get_date()  # Get as date object
            date = date_obj.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD
        except Exception as e:
            messagebox.showerror("Date Error", f"Please select a valid date")
            return
        
        # Get time from spinboxes - read directly from widget to capture typed values
        try:
            hour_text = self.hour_spinbox.get().strip()
            minute_text = self.minute_spinbox.get().strip()
            hour = int(hour_text) if hour_text else 0
            minute = int(minute_text) if minute_text else 0
        except ValueError:
            messagebox.showerror("Time Error", "Please enter valid hour (0-23) and minute (0-59) values")
            return
        
        # Validate values
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            messagebox.showerror("Time Error", f"Invalid time values: Hour must be 0-23, Minute must be 0-59 (got {hour}:{minute:02d})")
            return
        time = f"{hour:02d}:{minute:02d}"
        
        # Get all required and optional fields
        dept = str(self.entry_dept.get()).strip()
        user = str(self.entry_user.get()).strip()
        duration_str = str(self.entry_duration.get()).strip()
        reason = str(self.entry_reason.get("1.0", "end-1c")).strip()
        priority = str(self.entry_priority.get()).strip()
        setup = str(self.entry_setup.get()).strip()
        notes = str(self.entry_notes.get("1.0", "end-1c")).strip()
        
        # Parse duration to minutes
        duration_minutes = 60  # Default
        if "30" in duration_str:
            duration_minutes = 30
        elif "1.5" in duration_str:
            duration_minutes = 90
        elif "2.5" in duration_str:
            duration_minutes = 150
        elif "3" in duration_str:
            duration_minutes = 180
        elif "4" in duration_str:
            duration_minutes = 240
        elif "8" in duration_str:
            duration_minutes = 480
        elif "2" in duration_str:
            duration_minutes = 120
        elif "1" in duration_str:
            duration_minutes = 60
        
        # Ensure all values are strings and not empty
        date = str(date).strip() if date else ""
        time = str(time).strip() if time else ""
        dept = str(dept).strip() if dept else ""
        user = str(user).strip() if user else ""
        reason = str(reason).strip() if reason else ""
        
        # Validation
        if not all([date, time, dept, user]):
            messagebox.showerror("Validation Error", "Please fill in all required fields:\n- Date\n- Time\n- Department\n- User Name")
            self.update_status("Validation failed - incomplete booking details")
            return
        
        # Check for overlapping bookings
        if self._check_overlap(date, time, duration_minutes, self.selected_booking_id):
            messagebox.showerror("Booking Error", 
                "Another booking already exists at this time.\nPlease select a different time.")
            self.update_status("Booking failed - time slot already booked")
            return
        
        # Retry logic for database operations with exponential backoff
        max_retries = 10
        conn = None
        for attempt in range(max_retries):
            try:
                conn = sqlite3.connect(self.db_name, timeout=30.0)
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA busy_timeout=30000")
                cursor = conn.cursor()
                
                if self.is_edit_mode and self.selected_booking_id:
                    # Update existing booking
                    cursor.execute(
                        '''UPDATE bookings 
                           SET booking_date=?, booking_time=?, duration_minutes=?, department=?, user_name=?, reason=?,
                               priority=?, setup=?, notes=?
                           WHERE id=?''',
                        (date, time, duration_minutes, dept, user, reason, priority, setup, notes, int(self.selected_booking_id))
                    )
                    action_text = "updated"
                else:
                    # Insert new booking
                    cursor.execute(
                        '''INSERT INTO bookings (booking_date, booking_time, duration_minutes, department, user_name, reason, priority, setup, notes)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (date, time, duration_minutes, dept, user, reason, priority, setup, notes)
                    )
                    action_text = "created"
                
                conn.commit()
                conn.close()
                
                self.is_edit_mode = False
                self.selected_booking_id = None
                messagebox.showinfo("Success", f"Board Room Booking {action_text} Successfully!")
                self.update_status(f"Booking {action_text}: {dept} - {user} on {date} at {time}")
                self.clear_inputs()
                self.load_bookings()
                
                # Navigate to Calendar View tab and select the booked date
                self.notebook.select(2)  # Select Calendar View tab
                self.root.update()  # Force UI update
                try:
                    # Parse date and set calendar selection
                    if "-" in date:  # Format YYYY-MM-DD
                        parts = date.split("-")
                        booked_date = datetime(int(parts[0]), int(parts[1]), int(parts[2])).date()
                    else:  # Other formats
                        booked_date = datetime.strptime(date, "%Y-%m-%d").date()
                    
                    self.calendar_widget.selection_set(booked_date)
                    self.root.update()  # Force UI update again
                    # Add small delay to ensure calendar selection is processed before refreshing display
                    self.root.after(100, lambda: self.on_calendar_selected(None))
                except Exception as e:
                    self.update_status(f"Calendar display error: {str(e)}")
                    # Add small delay here too for consistency
                    self.root.after(100, lambda: self.on_calendar_selected(None))
                
                break  # Success, exit retry loop
                
            except sqlite3.OperationalError as e:
                if conn:
                    try:
                        conn.close()
                    except:
                        pass
                if attempt < max_retries - 1:
                    # Exponential backoff: 0.2s * 1.5^attempt, capped at 5s
                    wait_time = min(0.2 * (1.5 ** attempt), 5.0)
                    time.sleep(wait_time)
                else:
                    # Final attempt failed
                    messagebox.showerror("Database Error", f"Error saving booking:\n{str(e)}")
                    self.update_status(f"Booking save failed: {str(e)}")
                    return

    def edit_booking(self):
        """Edit selected booking"""
        # Only for admin users
        if not self.is_admin or self.tree is None:
            messagebox.showerror("Error", "Only admins can edit bookings")
            return
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to edit from the list.")
            self.update_status("No booking selected for editing")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        booking_id, date, time, dept, user, reason = values
        
        # Get duration from stored data
        duration_minutes = 60  # Default
        if hasattr(self, 'booking_data') and int(booking_id) in self.booking_data:
            duration_minutes = self.booking_data[int(booking_id)].get('duration_minutes', 60)
        
        self.is_edit_mode = True
        self.selected_booking_id = booking_id
        
        # Populate form with selected booking data
        self.entry_date.set_date(datetime.strptime(date, "%Y-%m-%d").date())
        # Parse time and update display
        try:
            hour, minute = time.split(":")
            self.current_hour = int(hour)
            self.current_minute = int(minute)
        except:
            self.current_hour = 0
            self.current_minute = 0
        self.hour_var.set(self.current_hour)
        self.minute_var.set(self.current_minute)
        self.entry_dept.set(dept)
        
        # Set duration
        if duration_minutes == 30:
            self.entry_duration.set("30 minutes")
        elif duration_minutes == 90:
            self.entry_duration.set("1.5 hours")
        elif duration_minutes == 120:
            self.entry_duration.set("2 hours")
        elif duration_minutes == 150:
            self.entry_duration.set("2.5 hours")
        elif duration_minutes == 180:
            self.entry_duration.set("3 hours")
        elif duration_minutes == 240:
            self.entry_duration.set("4 hours")
        elif duration_minutes == 480:
            self.entry_duration.set("Full day (8 hours)")
        else:
            self.entry_duration.set("1 hour")
        
        # Username field is read-only and always the logged-in user
        self.entry_reason.delete("1.0", tk.END)
        self.entry_reason.insert("1.0", reason)
        
        messagebox.showinfo("Edit Mode", 
            f"Editing booking #{booking_id}\nModify the details and click 'Book Room' to save changes.")
        self.update_status(f"Editing booking #{booking_id}")
    
    def _validate_time(self, time_str):
        """Validate time format HH:MM"""
        try:
            parts = time_str.split(":")
            if len(parts) != 2:
                return False
            hour = int(parts[0])
            minute = int(parts[1])
            return 0 <= hour <= 23 and 0 <= minute <= 59
        except:
            return False
    
    def _check_overlap(self, date, time, duration_minutes, exclude_id=None):
        """Check if time slot overlaps with existing bookings"""
        try:
            # Convert time string HH:MM to total minutes
            time_parts = time.split(":")
            start_minutes = int(time_parts[0]) * 60 + int(time_parts[1])
            end_minutes = start_minutes + duration_minutes
            
            conn = sqlite3.connect(self.db_name, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=30000")
            cursor = conn.cursor()
            
            # Get all bookings on the same date
            if exclude_id:
                cursor.execute("SELECT booking_time, duration_minutes FROM bookings WHERE booking_date=? AND id!=?", 
                             (date, exclude_id))
            else:
                cursor.execute("SELECT booking_time, duration_minutes FROM bookings WHERE booking_date=?", 
                             (date,))
            
            existing_bookings = cursor.fetchall()
            conn.close()
            
            # Check for overlaps with existing bookings
            for booking_time, booking_duration in existing_bookings:
                try:
                    time_parts = booking_time.split(":")
                    existing_start = int(time_parts[0]) * 60 + int(time_parts[1])
                    existing_end = existing_start + (booking_duration if booking_duration else 60)
                    
                    # Check if time ranges overlap: new_start < existing_end AND new_end > existing_start
                    if start_minutes < existing_end and end_minutes > existing_start:
                        return True
                except:
                    pass
            
            return False
        except:
            return False
    
    def load_bookings(self, bookings_list=None):
        """Fetch data from database and display as cards"""
        # Only load for admin users
        if not self.is_admin or not hasattr(self, 'bookings_scrollable') or self.bookings_scrollable is None:
            # For non-admin users, just update calendar dates
            self.highlight_booked_dates()
            self.on_calendar_selected(None)
            return
        
        # Clear existing cards
        for widget in self.bookings_scrollable.winfo_children():
            widget.destroy()
        self.manage_bookings_cards = []
        
        try:
            if bookings_list is None:
                conn = sqlite3.connect(self.db_name, timeout=30.0)
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA busy_timeout=30000")
                cursor = conn.cursor()
                cursor.execute("SELECT id, booking_date, booking_time, duration_minutes, department, user_name, reason, priority, setup, notes FROM bookings ORDER BY booking_date DESC, booking_time")
                bookings_list = cursor.fetchall()
                conn.close()
            
            # Update booking count
            self.booking_count_label.config(text=f"📊 Total Bookings: {len(bookings_list)}")
            
            # Display bookings as cards
            if len(bookings_list) == 0:
                empty_card = tk.Frame(self.bookings_scrollable, bg=self.bg_white, relief="solid", bd=1,
                                     highlightthickness=1, highlightcolor=self.border_color, highlightbackground=self.border_color)
                empty_card.pack(fill="x", pady=10, padx=0)
                
                empty_label = tk.Label(empty_card, text="✨ No bookings found", font=("Arial", 14, "bold"),
                                      fg=self.accent_blue, bg=self.bg_white, pady=20)
                empty_label.pack()
            else:
                for row in bookings_list:
                    self._create_booking_card(row)
            
            self.update_status(f"Loaded {len(bookings_list)} booking(s)")
            self.highlight_booked_dates()
            self.on_calendar_selected(None)
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not load bookings:\n{str(e)}")
            self.update_status(f"Error loading bookings: {str(e)}")
    
    def _create_booking_card(self, booking_data):
        """Create a modern card for a booking"""
        booking_id, date, time, duration_mins, dept, user, reason, priority, setup, notes = booking_data
        
        # Color mapping for departments
        dept_colors = {
            "Finance": "#ff6b6b",
            "HR": "#4ecdc4",
            "IT": "#0052cc",
            "Marketing": "#ffa502",
            "Operations": "#6c5ce7",
            "Sales": "#00b894",
            "Other": "#9b9b9b"
        }
        dept_color = dept_colors.get(dept, "#0052cc")
        
        # Priority colors
        priority_colors = {
            "Regular": "#95a5a6",
            "Important": "#f39c12",
            "Urgent": "#e74c3c",
            "Critical": "#c0392b"
        }
        priority_color = priority_colors.get(priority, "#95a5a6")
        
        # Card frame
        card = tk.Frame(self.bookings_scrollable, bg=self.bg_white, relief="solid", bd=1,
                       highlightthickness=1, highlightcolor=self.border_color, highlightbackground=self.border_color)
        card.pack(fill="x", pady=8, padx=0)
        self.manage_bookings_cards.append((card, booking_id, dept))
        
        # Left color bar
        color_bar = tk.Frame(card, bg=dept_color, width=5)
        color_bar.pack(side="left", fill="y", padx=0)
        color_bar.pack_propagate(False)
        
        # Main content
        content = tk.Frame(card, bg=self.bg_white)
        content.pack(side="left", fill="both", expand=True, padx=15, pady=12)
        
        # Header row: Date, Time, Department, Priority
        header_frame = tk.Frame(content, bg=self.bg_white)
        header_frame.pack(fill="x", pady=(0, 8))
        
        date_label = tk.Label(header_frame, text=f"📅 {date}", font=("Arial", 11, "bold"),
                             fg=self.text_primary, bg=self.bg_white)
        date_label.pack(side="left", padx=(0, 15))
        
        time_label = tk.Label(header_frame, text=f"⏰ {time}", font=("Arial", 11, "bold"),
                             fg=self.text_primary, bg=self.bg_white)
        time_label.pack(side="left", padx=(0, 15))
        
        dept_badge = tk.Label(header_frame, text=f"🏢 {dept}", font=("Arial", 10, "bold"),
                             fg="white", bg=dept_color, padx=10, pady=4, relief="solid", bd=1)
        dept_badge.pack(side="left", padx=(0, 15))
        
        priority_badge = tk.Label(header_frame, text=f"⭐ {priority}", font=("Arial", 10, "bold"),
                                 fg="white", bg=priority_color, padx=10, pady=4, relief="solid", bd=1)
        priority_badge.pack(side="left")
        
        # Details row: Organizer, Duration
        details_frame = tk.Frame(content, bg=self.bg_white)
        details_frame.pack(fill="x", pady=5)
        
        user_label = tk.Label(details_frame, text=f"👤 {user}", font=("Arial", 10),
                             fg=self.text_secondary, bg=self.bg_white)
        user_label.pack(side="left", padx=(0, 20))
        
        duration_text = f"{duration_mins} mins" if duration_mins < 60 else f"{duration_mins // 60}h {duration_mins % 60}m"
        duration_label = tk.Label(details_frame, text=f"⏱️ {duration_text}", font=("Arial", 10),
                                 fg=self.text_secondary, bg=self.bg_white)
        duration_label.pack(side="left", padx=(0, 20))
        
        if setup and setup != "None":
            setup_label = tk.Label(details_frame, text=f"🔧 {setup}", font=("Arial", 10),
                                  fg=self.text_secondary, bg=self.bg_white)
            setup_label.pack(side="left")
        
        # Reason/Notes
        if reason:
            reason_label = tk.Label(content, text=f"📝 {reason}", font=("Arial", 10),
                                   fg=self.text_secondary, bg=self.bg_white, wraplength=600, justify="left")
            reason_label.pack(fill="x", pady=5, anchor="w")
        
        # Action buttons
        button_frame = tk.Frame(card, bg=self.bg_white)
        button_frame.pack(side="right", padx=15, pady=12)
        
        edit_btn = tk.Button(button_frame, text="✎ Edit", font=("Arial", 9, "bold"),
                            bg="#f59e0b", fg="white", relief="flat", bd=0, padx=12, pady=6,
                            cursor="hand2", activebackground="#d97706",
                            command=lambda bid=booking_id: self.edit_booking_from_card(bid))
        edit_btn.pack(side="left", padx=5)
        
        delete_btn = tk.Button(button_frame, text="🗑️ Delete", font=("Arial", 9, "bold"),
                              bg="#ef4444", fg="white", relief="flat", bd=0, padx=12, pady=6,
                              cursor="hand2", activebackground="#dc2626",
                              command=lambda bid=booking_id: self.delete_booking_by_id(bid))
        delete_btn.pack(side="left", padx=5)
    
    def highlight_booked_dates(self):
        """Highlight dates with bookings in the calendar"""
        try:
            # Get all booking dates
            conn = sqlite3.connect(self.db_name, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=30000")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT booking_date FROM bookings ORDER BY booking_date")
            booked_dates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in cursor.fetchall()]
            conn.close()
            
            # Try to tag the dates if the method exists
            if hasattr(self.calendar_widget, 'tag_dates') and booked_dates:
                try:
                    self.calendar_widget.tag_dates(booked_dates, 'booked')
                except:
                    pass  # Method might not be available in this version
                
        except Exception as e:
            # Silently handle errors in highlighting
            pass

    def filter_bookings(self):
        """Filter bookings by search term and department"""
        # Only for admin users
        if not self.is_admin or not hasattr(self, 'bookings_scrollable') or self.bookings_scrollable is None:
            return
        
        search_term = self.search_var.get().lower()
        dept_filter = self.dept_filter_var.get() if hasattr(self, 'dept_filter_var') else "All"
        
        try:
            conn = sqlite3.connect(self.db_name, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=30000")
            cursor = conn.cursor()
            cursor.execute("SELECT id, booking_date, booking_time, duration_minutes, department, user_name, reason, priority, setup, notes FROM bookings ORDER BY booking_date DESC, booking_time")
            all_bookings = cursor.fetchall()
            conn.close()
            
            filtered = []
            for booking in all_bookings:
                # Check department filter
                if dept_filter != "All" and booking[4] != dept_filter:
                    continue
                
                # Check search term
                if search_term and not any(search_term in str(field).lower() for field in booking):
                    continue
                
                filtered.append(booking)
            
            self.load_bookings(filtered)
            self.update_status(f"Found {len(filtered)} booking(s)")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not filter bookings:\n{str(e)}")
    
    def reset_filters(self):
        """Reset all filters"""
        self.search_var.set("")
        if hasattr(self, 'dept_filter_var'):
            self.dept_filter_var.set("All")
        self.load_bookings()
    
    def edit_booking_from_card(self, booking_id):
        """Load booking into edit mode from card"""
        try:
            conn = sqlite3.connect(self.db_name, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=30000")
            cursor = conn.cursor()
            cursor.execute("SELECT booking_date, booking_time, duration_minutes, department, reason, priority, setup, notes FROM bookings WHERE id=?", (booking_id,))
            booking = cursor.fetchone()
            conn.close()
            
            if booking:
                self.is_edit_mode = True
                self.selected_booking_id = booking_id
                
                # Populate form
                date_obj = datetime.strptime(booking[0], "%Y-%m-%d").date()
                self.entry_date.set_date(date_obj)
                
                time_parts = booking[1].split(":")
                self.hour_var.set(int(time_parts[0]))
                self.minute_var.set(int(time_parts[1]))
                
                self.entry_dept.set(booking[3])
                
                # Parse duration
                duration = booking[2]
                if duration == 30:
                    self.entry_duration.set("30 minutes")
                elif duration == 90:
                    self.entry_duration.set("1.5 hours")
                elif duration == 150:
                    self.entry_duration.set("2.5 hours")
                elif duration == 180:
                    self.entry_duration.set("3 hours")
                elif duration == 240:
                    self.entry_duration.set("4 hours")
                elif duration == 480:
                    self.entry_duration.set("Full day (8 hours)")
                elif duration == 120:
                    self.entry_duration.set("2 hours")
                else:
                    self.entry_duration.set("1 hour")
                
                self.entry_reason.delete("1.0", tk.END)
                self.entry_reason.insert("1.0", booking[4] if booking[4] else "")
                
                self.entry_priority.set(booking[5] if booking[5] else "Regular")
                self.entry_setup.set(booking[6] if booking[6] else "None")
                
                self.entry_notes.delete("1.0", tk.END)
                self.entry_notes.insert("1.0", booking[7] if booking[7] else "")
                
                # Switch to booking tab
                self.notebook.select(0)
                self.update_status(f"Editing booking #{booking_id}")
                messagebox.showinfo("Edit Mode", f"Editing booking #{booking_id}. Click 'BOOK ROOM' to save changes.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load booking:\n{str(e)}")
    
    def delete_booking_by_id(self, booking_id):
        """Delete a specific booking by ID"""
        if not self.is_admin:
            messagebox.showerror("Error", "Only admins can delete bookings")
            return
        
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this booking?"):
            self.update_status("Deletion cancelled")
            return
        
        try:
            conn = sqlite3.connect(self.db_name, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=30000")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Booking deleted successfully!")
            self.update_status(f"Booking #{booking_id} deleted")
            self.load_bookings()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete booking:\n{str(e)}")
            self.update_status(f"Error: {str(e)}")

    def delete_booking(self):
        """Delete selected booking (for backward compatibility)"""
        # For new card-based interface, use delete_booking_by_id
        # This is kept for backward compatibility
        pass

    def export_to_csv(self):
        """Export bookings to CSV file"""
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if not file_path:
                return
            
            conn = sqlite3.connect(self.db_name, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=30000")
            cursor = conn.cursor()
            cursor.execute("SELECT id, booking_date, booking_time, department, user_name, reason FROM bookings ORDER BY booking_date")
            bookings = cursor.fetchall()
            conn.close()
            
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Date', 'Time', 'Department', 'User', 'Reason'])
                writer.writerows(bookings)
            
            messagebox.showinfo("Success", f"Bookings exported to {file_path}")
            self.update_status(f"Exported {len(bookings)} booking(s) to CSV")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not export bookings:\n{str(e)}")

    def clear_inputs(self):
        """Clear all form inputs but preserve department for logged-in user"""
        self.entry_date.set_date(datetime.now().date())
        self.current_hour = datetime.now().hour
        self.current_minute = 0
        self.hour_var.set(self.current_hour)
        self.minute_var.set(self.current_minute)
        # Preserve department if user is logged in
        if self.user_department:
            self.entry_dept.set(self.user_department)
        else:
            self.entry_dept.set('')
        # Don't clear username field - it's always the logged-in user
        self.entry_reason.delete("1.0", tk.END)
        self.entry_priority.set('Regular')
        self.entry_setup.set('None')
        self.entry_notes.delete("1.0", tk.END)
        self.entry_duration.set('1 hour')
        self.is_edit_mode = False
        self.selected_booking_id = None
        self.update_status("Form cleared")

    def on_calendar_selected(self, event):
        """Handle calendar date selection with card-based display"""
        try:
            selected_date = self.calendar_widget.selection_get()
            if not selected_date:
                selected_date = datetime.now().date()
            
            date_str = selected_date.strftime("%Y-%m-%d")
            self.selected_date = date_str
            
            # Update the date label
            formatted_date = selected_date.strftime("%A, %B %d, %Y")
            self.selected_date_label.config(text=f"📅 {formatted_date}")
            
            # Get bookings for this date
            conn = sqlite3.connect(self.db_name, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=30000")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, booking_time, duration_minutes, department, user_name, reason 
                FROM bookings 
                WHERE booking_date = ? 
                ORDER BY booking_time
            """, (date_str,))
            bookings = cursor.fetchall()
            conn.close()
            
            # Clear previous cards
            for widget in self.booking_cards_frame.winfo_children():
                widget.destroy()
            
            # Department color mapping
            dept_colors = {
                "Finance": "#ff6b6b",
                "HR": "#4ecdc4",
                "IT": "#45b7d1",
                "Marketing": "#ffa502",
                "Operations": "#95e1d3",
                "Sales": "#f38181",
                "Other": "#c0a0ff"
            }
            
            if bookings:
                # Modern title with count badge
                title_frame = tk.Frame(self.booking_cards_frame, bg=self.bg_white)
                title_frame.pack(fill="x", pady=(0, 20))
                
                title = tk.Label(title_frame, text=f"Bookings for This Date", 
                               font=("Arial", 14, "bold"), fg=self.accent_blue, bg=self.bg_white)
                title.pack(anchor="w", side="left")
                
                # Count badge
                badge = tk.Label(title_frame, text=f" {len(bookings)} ", 
                               font=("Arial", 11, "bold"), fg="white", bg=self.accent_blue, 
                               padx=8, pady=2, relief="flat")
                badge.pack(side="left", padx=(10, 0))
                
                # Create booking cards
                for booking in bookings:
                    booking_id, time, duration_minutes, dept, user, reason = booking
                    
                    # Convert duration
                    duration_map = {30: "30 min", 60: "1 hour", 90: "1.5 hrs", 120: "2 hours",
                                   150: "2.5 hrs", 180: "3 hours", 240: "4 hours", 480: "All day"}
                    duration_text = duration_map.get(duration_minutes, f"{duration_minutes} min")
                    
                    # Modern booking card with shadow effect
                    card_outer = tk.Frame(self.booking_cards_frame, bg=self.bg_white)
                    card_outer.pack(fill="x", pady=8, padx=0)
                    
                    card = tk.Frame(card_outer, bg="white", relief="solid", bd=1,
                                  highlightthickness=0)
                    card.pack(fill="x", padx=2, pady=2)
                    
                    # Left color bar (thicker, more modern)
                    color = dept_colors.get(dept, "#c0a0ff")
                    color_bar = tk.Frame(card, bg=color, width=6, height=100)
                    color_bar.pack(side="left", fill="y", padx=0)
                    
                    # Main content
                    content = tk.Frame(card, bg="white")
                    content.pack(side="left", fill="both", expand=True, padx=15, pady=14)
                    
                    # Header: Time and Department (modern layout)
                    header = tk.Frame(content, bg="white")
                    header.pack(fill="x", pady=(0, 10))
                    
                    # Time (larger, prominent)
                    time_label = tk.Label(header, text=f"⏰ {time}", font=("Arial", 13, "bold"),
                                         fg=self.text_primary, bg="white")
                    time_label.pack(side="left")
                    
                    # Department as badge
                    dept_label = tk.Label(header, text=f"  {dept}", font=("Arial", 11, "bold"),
                                         fg="white", bg=color, padx=8, pady=2, relief="flat")
                    dept_label.pack(side="left", padx=(15, 0))
                    
                    # Duration
                    duration_label = tk.Label(header, text=f"  ⏱ {duration_text}", 
                                            font=("Arial", 10), fg=self.text_secondary, bg="white")
                    duration_label.pack(side="left", padx=(15, 0))
                    
                    # Details section
                    details = tk.Frame(content, bg="white")
                    details.pack(fill="x", pady=(0, 0))
                    
                    # User
                    user_label = tk.Label(details, text=f"👤 Booked by: {user}", font=("Arial", 10),
                                         fg=self.text_primary, bg="white", justify="left")
                    user_label.pack(anchor="w", pady=(0, 6))
                    
                    # Reason (if exists)
                    if reason:
                        reason_text = reason
                        reason_label = tk.Label(details, text=f"📝 {reason_text}", font=("Arial", 9),
                                              fg=self.text_secondary, bg="white", justify="left", wraplength=280)
                        reason_label.pack(anchor="w", pady=(0, 3))
                    
                    # Booking ID footer
                    id_label = tk.Label(details, text=f"Booking ID: #{booking_id}", font=("Arial", 8),
                                       fg="#b0b0b0", bg="white")
                    id_label.pack(anchor="w")
                
                self.update_status(f"Showing {len(bookings)} booking(s) for {date_str}")
            else:
                # Modern empty state with gradient
                empty_frame = tk.Frame(self.booking_cards_frame, bg="white")
                empty_frame.pack(fill="both", expand=True, pady=40)
                
                # Icon with modern animation effect
                empty_icon_bg = tk.Frame(empty_frame, bg="#f0f4f8", width=120, height=120)
                empty_icon_bg.pack(pady=(20, 15))
                empty_icon_bg.pack_propagate(False)
                
                empty_icon = tk.Label(empty_icon_bg, text="✨", font=("Arial", 60), 
                                     bg="#f0f4f8", fg=self.accent_blue)
                empty_icon.place(relx=0.5, rely=0.5, anchor="center")
                
                # Title
                empty_title = tk.Label(empty_frame, text="No Bookings Today", font=("Arial", 16, "bold"),
                                      fg=self.accent_blue, bg="white")
                empty_title.pack(pady=(0, 8))
                
                # Message
                empty_msg = tk.Label(empty_frame, text="Great! The room is completely free on this date", 
                                    font=("Arial", 11), fg=self.text_secondary, bg="white")
                empty_msg.pack(pady=(0, 20))
                
                # Call-to-action button
                cta_btn = tk.Button(empty_frame, text="📅 Create Your First Booking",
                                   command=lambda: self.notebook.select(0),
                                   font=("Arial", 11, "bold"), fg="white", bg=self.accent_blue,
                                   relief="flat", bd=0, padx=25, pady=10, cursor="hand2",
                                   activebackground="#003db3", activeforeground="white")
                cta_btn.pack()
                
                self.update_status(f"No bookings for {date_str} ✓")
        except Exception as e:
            self.update_status(f"Error loading bookings: {str(e)}")
    
    def _on_canvas_configure(self, event):
        """Adjust canvas window width when canvas resizes"""
        canvas_width = event.width
        self.calendar_canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def _on_frame_configure(self, event):
        """Update canvas scroll region when frame changes"""
        self.calendar_canvas.configure(scrollregion=self.calendar_canvas.bbox("all"))

    def calendar_goto_today(self):
        """Navigate to today's date"""
        today = datetime.now()
        self.calendar_widget.selection_set(today)
        self.on_calendar_selected(None)
        self.update_status(f"Navigated to today: {today.strftime('%Y-%m-%d')}")
    
    def calendar_refresh_display(self):
        """Refresh calendar display"""
        selected_date = self.calendar_widget.selection_get()
        if selected_date:
            self.on_calendar_selected(None)
        self.update_status("Calendar refreshed")

    def update_status(self, message):
        """Update status bar with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_label.config(text=f"✓ [{timestamp}] {message}")
    
    def logout(self):
        """Logout current user and return to login screen"""
        if messagebox.askyesno("Logout", f"Are you sure you want to logout, {self.logged_in_user}?"):
            self.root.destroy()
            # Restart the application with login screen
            root = tk.Tk()
            login = LoginWindow(root)
            root.mainloop()
            
            if login.logged_in_user:
                if login.is_admin:
                    # Open Admin Panel
                    admin_root = tk.Tk()
                    admin = AdminPanel(admin_root, login.logged_in_user)
                    admin_root.mainloop()
                else:
                    # Open Regular User App
                    app_root = tk.Tk()
                    app = TasmaBookingApp(app_root, login.logged_in_user, is_admin=login.is_admin, user_department=login.user_department)
                    app_root.mainloop()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        login = LoginWindow(root)
        root.mainloop()
        
        # Only proceed if user successfully logged in
        if login.logged_in_user:
            if login.is_admin:
                # Open Admin Panel
                admin_root = tk.Tk()
                admin = AdminPanel(admin_root, login.logged_in_user)
                admin_root.mainloop()
            else:
                # Open Regular User App
                app_root = tk.Tk()
                app = TasmaBookingApp(app_root, login.logged_in_user, is_admin=login.is_admin, user_department=login.user_department)
                app_root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror("Fatal Error", f"Application error:\n{str(e)}")
