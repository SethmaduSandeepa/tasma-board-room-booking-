import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
from datetime import datetime
import csv
from tkcalendar import DateEntry, Calendar

class TasmaBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TASMA Board Room Booking System")
        self.root.geometry("1400x850")
        self.root.resizable(True, True)
        
        # Modern Dark Theme Colors
        self.bg_dark = "#1a1a1a"
        self.bg_darker = "#0f0f0f"
        self.bg_card = "#2a2a2a"
        self.accent_teal = "#00d4d4"
        self.accent_cyan = "#00e5ff"
        self.text_primary = "#ffffff"
        self.text_secondary = "#b0b0b0"
        self.border_color = "#404040"
        
        # Set root background
        self.root.configure(bg=self.bg_dark)
        
        # Database Configuration
        self.db_name = "bookings.db"
        self.init_database()
        
        self.selected_booking_id = None
        self.is_edit_mode = False
        
        # --- Main Container ---
        main_container = tk.Frame(root, bg=self.bg_dark)
        main_container.pack(fill="both", expand=True)
        
        # --- Header/Title ---
        title_frame = tk.Frame(main_container, bg=self.bg_darker, height=80)
        title_frame.pack(fill="x")
        
        # Logo/Title on the left with accent
        title_label = tk.Label(title_frame, text="🏢 TASMA", 
                              font=("Helvetica", 28, "bold"), fg=self.accent_teal, 
                              bg=self.bg_darker, pady=15)
        title_label.pack(side="left", padx=30)
        
        subtitle_label = tk.Label(title_frame, text="Board Room Booking System", 
                                 font=("Helvetica", 14), fg=self.text_secondary, 
                                 bg=self.bg_darker)
        subtitle_label.pack(side="left", padx=5)
        
        # --- Status Bar (Create Early) ---
        status_frame = tk.Frame(main_container, bg=self.bg_card, height=35)
        status_frame.pack(fill="x", side="bottom", padx=15, pady=10)
        self.status_label = tk.Label(status_frame, text="✓ Ready", font=("Arial", 10), 
                                    fg=self.accent_teal, bg=self.bg_card, justify="left", padx=15)
        self.status_label.pack(side="left", fill="both", expand=True)
        
        # --- Content Frame ---
        content_frame = tk.Frame(main_container, bg=self.bg_dark)
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Configure style for tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.bg_dark, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 12], font=("Arial", 11, "bold"))
        style.map('TNotebook.Tab', 
                  background=[('selected', self.accent_teal)],
                  foreground=[('selected', self.bg_dark)])
        
        # --- Notebook (Tabs) ---
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # ===== TAB 1: New Booking =====
        book_tab = tk.Frame(self.notebook, bg=self.bg_dark)
        self.notebook.add(book_tab, text="📅 New Booking")
        
        # Scroll frame for form
        scroll_frame = tk.Frame(book_tab, bg=self.bg_dark)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form Card
        form_card = tk.Frame(scroll_frame, bg=self.bg_card, relief="flat", bd=0)
        form_card.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Card title
        card_title = tk.Label(form_card, text="Booking Details", font=("Arial", 16, "bold"), 
                             fg=self.accent_teal, bg=self.bg_card, pady=15)
        card_title.pack(fill="x", padx=20)
        
        # Separator line
        separator = tk.Frame(form_card, bg=self.border_color, height=1)
        separator.pack(fill="x", padx=20, pady=(0, 20))
        
        form_frame = tk.Frame(form_card, bg=self.bg_card)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Row 1: Date and Time
        self._create_form_field(form_frame, "📅 Date:", 0, 0)
        self.entry_date = DateEntry(form_frame, width=25, background=self.accent_teal, 
                                   foreground=self.bg_dark, borderwidth=1, 
                                   year=datetime.now().year, month=datetime.now().month, 
                                   day=datetime.now().day)
        self.entry_date.grid(row=0, column=1, pady=12, padx=15, sticky="w")
        
        self._create_form_field(form_frame, "⏰ Time (HH:MM):", 0, 2)
        self.entry_time = tk.Entry(form_frame, width=15, font=("Arial", 11), 
                                  bg=self.bg_darker, fg=self.text_primary, 
                                  insertbackground=self.accent_teal, borderwidth=1, relief="solid")
        self.entry_time.grid(row=0, column=3, pady=12, padx=15, sticky="w")
        
        # Row 2: Department and User
        self._create_form_field(form_frame, "🏢 Department:", 1, 0)
        self.entry_dept = ttk.Combobox(form_frame, width=22, font=("Arial", 11), 
                                       values=["Finance", "HR", "IT", "Marketing", "Operations", "Sales", "Other"],
                                       state="readonly")
        self.entry_dept.grid(row=1, column=1, pady=12, padx=15, sticky="w")
        
        self._create_form_field(form_frame, "👤 User Name:", 1, 2)
        self.entry_user = tk.Entry(form_frame, width=15, font=("Arial", 11), 
                                  bg=self.bg_darker, fg=self.text_primary, 
                                  insertbackground=self.accent_teal, borderwidth=1, relief="solid")
        self.entry_user.grid(row=1, column=3, pady=12, padx=15, sticky="w")
        
        # Row 3: Reason
        self._create_form_field(form_frame, "📝 Reason:", 2, 0)
        self.entry_reason = tk.Text(form_frame, width=60, height=3, font=("Arial", 11),
                                    bg=self.bg_darker, fg=self.text_primary, 
                                    insertbackground=self.accent_teal, borderwidth=1, relief="solid")
        self.entry_reason.grid(row=2, column=1, columnspan=3, pady=12, padx=15, sticky="nsew")
        
        # Buttons Frame
        btn_frame = tk.Frame(form_card, bg=self.bg_card)
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        self._create_button(btn_frame, "✓ Book Room", self.add_booking, self.accent_teal, side="left")
        self._create_button(btn_frame, "✎ Edit Selected", self.edit_booking, "#ff9800", side="left")
        self._create_button(btn_frame, "⟲ Clear Form", self.clear_inputs, "#9C27B0", side="left")
        
        # ===== TAB 2: Manage Bookings =====
        manage_tab = tk.Frame(self.notebook, bg=self.bg_dark)
        self.notebook.add(manage_tab, text="📋 Manage Bookings")
        
        # Search Frame (Card style)
        search_card = tk.Frame(manage_tab, bg=self.bg_card, relief="flat", bd=0)
        search_card.pack(fill="x", padx=15, pady=15)
        
        search_label = tk.Label(search_card, text="🔍 Search Bookings", font=("Arial", 12, "bold"), 
                               fg=self.accent_teal, bg=self.bg_card, padx=15, pady=10)
        search_label.pack(anchor="w")
        
        search_frame = tk.Frame(search_card, bg=self.bg_card)
        search_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_bookings())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40, 
                               font=("Arial", 11), bg=self.bg_darker, fg=self.text_primary,
                               insertbackground=self.accent_teal, borderwidth=1, relief="solid")
        search_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        search_hint = tk.Label(search_frame, text="(Date, Department, User, Reason)", 
                              font=("Arial", 9), bg=self.bg_card, fg=self.text_secondary)
        search_hint.pack(side="left", padx=10)
        
        # Bookings List Frame (Card style)
        list_card = tk.Frame(manage_tab, bg=self.bg_card, relief="flat", bd=0)
        list_card.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        list_label = tk.Label(list_card, text="📅 Current Bookings", font=("Arial", 12, "bold"), 
                             fg=self.accent_teal, bg=self.bg_card, padx=15, pady=10)
        list_label.pack(anchor="w")
        
        # Separator
        sep = tk.Frame(list_card, bg=self.border_color, height=1)
        sep.pack(fill="x", padx=15)
        
        list_frame = tk.Frame(list_card, bg=self.bg_card)
        list_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Treeview with modern styling
        columns = ("ID", "Date", "Time", "Department", "User", "Reason")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=18)
        
        # Define Headings and widths
        col_widths = {"ID": 40, "Date": 90, "Time": 60, "Department": 110, "User": 110, "Reason": 350}
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=col_widths[col])
        
        # Configure treeview appearance
        style.configure("Treeview", font=("Arial", 10), rowheight=26, background=self.bg_darker, 
                       foreground=self.text_primary, fieldbackground=self.bg_darker, borderwidth=0)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background=self.bg_card, 
                       foreground=self.accent_teal, borderwidth=0)
        style.map('Treeview', background=[('selected', self.accent_teal)], 
                 foreground=[('selected', self.bg_dark)])
        
        # Add row colors
        self.tree.tag_configure('oddrow', background=self.bg_darker, foreground=self.text_primary)
        self.tree.tag_configure('evenrow', background='#252525', foreground=self.text_primary)
        self.tree.tag_configure('selected', background=self.accent_teal, foreground=self.bg_dark)
        
        # Scrollbars
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Action buttons
        action_frame = tk.Frame(list_card, bg=self.bg_card)
        action_frame.pack(fill="x", padx=15, pady=15)
        
        self._create_button(action_frame, "🗑️ Delete", self.delete_booking, "#ff5252", side="left")
        self._create_button(action_frame, "💾 Export CSV", self.export_to_csv, "#4CAF50", side="left")
        
        # ===== TAB 3: Calendar View =====
        calendar_tab = tk.Frame(self.notebook, bg=self.bg_dark)
        self.notebook.add(calendar_tab, text="📆 Calendar View")
        
        # Main container for calendar tab with grid layout
        cal_main_frame = tk.Frame(calendar_tab, bg=self.bg_dark)
        cal_main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Configure grid weights for responsive layout
        cal_main_frame.grid_columnconfigure(0, weight=2, minsize=400)
        cal_main_frame.grid_columnconfigure(1, weight=1, minsize=350)
        cal_main_frame.grid_rowconfigure(0, weight=1)
        
        # Left side - Calendar Widget (Card style)
        cal_left_card = tk.Frame(cal_main_frame, bg=self.bg_card, relief="flat", bd=0)
        cal_left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        cal_left_title = tk.Label(cal_left_card, text="📅 Select a Date", font=("Arial", 12, "bold"), 
                                 fg=self.accent_teal, bg=self.bg_card, pady=12)
        cal_left_title.pack(anchor="w", padx=15, pady=(15, 0))
        
        cal_sep = tk.Frame(cal_left_card, bg=self.border_color, height=1)
        cal_sep.pack(fill="x", padx=15, pady=12)
        
        cal_left_frame = tk.Frame(cal_left_card, bg=self.bg_card)
        cal_left_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.calendar_widget = Calendar(cal_left_frame, selectmode='day', year=datetime.now().year, 
                                       month=datetime.now().month, day=datetime.now().day,
                                       cursor="hand2", font=("Arial", 10), headersformatvar="long",
                                       width=30, background=self.bg_darker, foreground=self.text_primary,
                                       fieldbackground=self.bg_darker, selectforeground=self.bg_dark,
                                       selectbackground=self.accent_teal, normalbackground=self.bg_darker,
                                       normalforeground=self.text_primary, othermonthforeground=self.text_secondary,
                                       othermonthweforeground=self.text_secondary, weekendforeground=self.accent_teal)
        self.calendar_widget.pack(fill="both", expand=True)
        self.calendar_widget.bind("<<CalendarSelected>>", self.on_calendar_selected)
        
        # Configure tag for dates with bookings
        self.calendar_widget.tag_config('booked', background=self.accent_teal, foreground=self.bg_dark)
        
        # Right side - Bookings Details (Card style)
        cal_right_card = tk.Frame(cal_main_frame, bg=self.bg_card, relief="flat", bd=0)
        cal_right_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        cal_right_title = tk.Label(cal_right_card, text="📋 Bookings", font=("Arial", 12, "bold"), 
                                  fg=self.accent_teal, bg=self.bg_card, pady=12)
        cal_right_title.pack(anchor="w", padx=15, pady=(15, 0))
        
        cal_sep2 = tk.Frame(cal_right_card, bg=self.border_color, height=1)
        cal_sep2.pack(fill="x", padx=15, pady=12)
        
        # Selected date label
        self.selected_date_label = tk.Label(cal_right_card, text="", font=("Arial", 11, "bold"), 
                                           bg=self.bg_darker, fg=self.accent_teal, padx=15, pady=10, 
                                           relief="flat", anchor="w")
        self.selected_date_label.pack(fill="x", padx=15, pady=(0, 10))
        
        # Scrollable text area for bookings
        scrollable_frame = tk.Frame(cal_right_card, bg=self.bg_card)
        scrollable_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        scrollbar = ttk.Scrollbar(scrollable_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.calendar_details_text = tk.Text(scrollable_frame, height=20, font=("Arial", 10), 
                                            wrap="word", yscrollcommand=scrollbar.set,
                                            bg=self.bg_darker, fg=self.text_primary, 
                                            insertbackground=self.accent_teal, borderwidth=0, relief="flat")
        self.calendar_details_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.calendar_details_text.yview)
        
        # Button Frame
        cal_button_frame = tk.Frame(cal_right_card, bg=self.bg_card)
        cal_button_frame.pack(fill="x", padx=15, pady=15)
        
        self._create_button(cal_button_frame, "🏠 Today", self.calendar_goto_today, self.accent_teal, side="left")
        self._create_button(cal_button_frame, "⟲ Refresh", self.calendar_refresh_display, "#4CAF50", side="left")
        
        self.selected_date = None
        
        # Load initial data
        self.load_bookings()
        
        # Initialize calendar display after load_bookings
        self.on_calendar_selected(None)

    def _create_form_field(self, parent, label_text, row, col):
        """Helper to create form field labels"""
        label = tk.Label(parent, text=label_text, font=("Arial", 11, "bold"), 
                        fg=self.accent_teal, bg=self.bg_card)
        label.grid(row=row, column=col, sticky="w", pady=12, padx=15, columnspan=1)
        return label
    
    def _create_button(self, parent, text, command, color, side="left"):
        """Helper to create modern buttons"""
        btn = tk.Button(parent, text=text, command=command, bg=color, fg="#000000" if color == self.accent_teal else "white", 
                       font=("Arial", 10, "bold"), width=16, height=2, cursor="hand2", 
                       relief="flat", bd=0, activebackground=color, activeforeground="#000000" if color == self.accent_teal else "white")
        btn.pack(side=side, padx=8)
        return btn

    def init_database(self):
        """Create the database and table if they don't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_date TEXT NOT NULL,
                booking_time TEXT NOT NULL,
                department TEXT NOT NULL,
                user_name TEXT NOT NULL,
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def add_booking(self):
        """Insert new or update booking in database"""
        # Get the date from DateEntry - it returns a date object or string
        try:
            date_obj = self.entry_date.get_date()  # Get as date object
            date = date_obj.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD
        except:
            # Fallback: try to get and parse the value
            date_input = self.entry_date.get()
            if hasattr(date_input, 'strftime'):
                date = date_input.strftime("%Y-%m-%d")
            else:
                date = str(date_input).strip()
        
        time = self.entry_time.get().strip()
        dept = self.entry_dept.get().strip()
        user = self.entry_user.get().strip()
        reason = self.entry_reason.get("1.0", "end-1c").strip()
        
        # Validation
        if not all([date, time, dept, user]):
            messagebox.showerror("Validation Error", "Please fill in all required fields:\n- Date\n- Time\n- Department\n- User Name")
            self.update_status("Validation failed - incomplete booking details")
            return
        
        # Validate time format
        if not self._validate_time(time):
            messagebox.showerror("Time Format Error", "Please enter time in HH:MM format (e.g., 14:30)")
            self.update_status("Validation failed - invalid time format")
            return
        
        # Check for overlapping bookings
        if self._check_overlap(date, time, self.selected_booking_id):
            if not messagebox.askyesno("Overlap Warning", 
                "Another booking exists at this time.\nContinue anyway?"):
                self.update_status("Booking cancelled")
                return
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            if self.is_edit_mode and self.selected_booking_id:
                # Update existing booking
                cursor.execute('''
                    UPDATE bookings 
                    SET booking_date=?, booking_time=?, department=?, user_name=?, reason=?
                    WHERE id=?
                ''', (date, time, dept, user, reason, self.selected_booking_id))
                action_text = "updated"
            else:
                # Insert new booking
                cursor.execute('''
                    INSERT INTO bookings (booking_date, booking_time, department, user_name, reason)
                    VALUES (?, ?, ?, ?, ?)
                ''', (date, time, dept, user, reason))
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
                self.on_calendar_selected(None)
            except Exception as e:
                self.update_status(f"Calendar display error: {str(e)}")
                self.on_calendar_selected(None)
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Error saving booking:\n{str(e)}")
            self.update_status(f"Error: {str(e)}")

    def edit_booking(self):
        """Edit selected booking"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to edit from the list.")
            self.update_status("No booking selected for editing")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        booking_id, date, time, dept, user, reason = values
        
        self.is_edit_mode = True
        self.selected_booking_id = booking_id
        
        # Populate form with selected booking data
        self.entry_date.set_date(datetime.strptime(date, "%Y-%m-%d").date())
        self.entry_time.delete(0, tk.END)
        self.entry_time.insert(0, time)
        self.entry_dept.set(dept)
        self.entry_user.delete(0, tk.END)
        self.entry_user.insert(0, user)
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
    
    def _check_overlap(self, date, time, exclude_id=None):
        """Check if time slot is already booked"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            if exclude_id:
                cursor.execute("SELECT COUNT(*) FROM bookings WHERE booking_date=? AND booking_time=? AND id!=?", 
                             (date, time, exclude_id))
            else:
                cursor.execute("SELECT COUNT(*) FROM bookings WHERE booking_date=? AND booking_time=?", 
                             (date, time))
            result = cursor.fetchone()[0]
            conn.close()
            return result > 0
        except:
            return False
    
    def load_bookings(self, bookings_list=None):
        """Fetch data from database and display in Treeview"""
        # Clear existing list
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            if bookings_list is None:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute("SELECT id, booking_date, booking_time, department, user_name, reason FROM bookings ORDER BY booking_date DESC, booking_time")
                bookings_list = cursor.fetchall()
                conn.close()
            
            # Add rows with alternating colors
            for idx, row in enumerate(bookings_list):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=row, tags=(tag,))
            
            self.update_status(f"Loaded {len(bookings_list)} booking(s)")
            
            # Update calendar highlights with booked dates
            self.highlight_booked_dates()
            
            # Refresh calendar display
            self.on_calendar_selected(None)
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not load bookings:\n{str(e)}")
            self.update_status(f"Error loading bookings: {str(e)}")
    
    def highlight_booked_dates(self):
        """Highlight dates with bookings in the calendar"""
        try:
            # Get all booking dates
            conn = sqlite3.connect(self.db_name)
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

    def delete_booking(self):
        """Delete selected booking"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to delete.")
            self.update_status("No booking selected for deletion")
            return
        
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this booking?"):
            self.update_status("Deletion cancelled")
            return
        
        try:
            item = self.tree.item(selected[0])
            booking_id = item['values'][0]
            
            conn = sqlite3.connect(self.db_name)
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

    def filter_bookings(self):
        """Filter bookings by search term"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.load_bookings()
            return
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT id, booking_date, booking_time, department, user_name, reason FROM bookings")
            all_bookings = cursor.fetchall()
            conn.close()
            
            filtered = []
            for booking in all_bookings:
                if any(search_term in str(field).lower() for field in booking):
                    filtered.append(booking)
            
            self.load_bookings(filtered)
            self.update_status(f"Found {len(filtered)} booking(s) matching '{search_term}'")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not filter bookings:\n{str(e)}")

    def sort_by_column(self, col):
        """Sort bookings by selected column"""
        try:
            items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
            items.sort()
            for index, (val, k) in enumerate(items):
                self.tree.move(k, '', index)
            self.update_status(f"Sorted by {col}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not sort:\n{str(e)}")

    def export_to_csv(self):
        """Export bookings to CSV file"""
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if not file_path:
                return
            
            conn = sqlite3.connect(self.db_name)
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
        """Clear all form inputs"""
        self.entry_date.set_date(datetime.now().date())
        self.entry_time.delete(0, tk.END)
        self.entry_dept.set('')
        self.entry_user.delete(0, tk.END)
        self.entry_reason.delete("1.0", tk.END)
        self.is_edit_mode = False
        self.selected_booking_id = None
        self.update_status("Form cleared")

    def on_calendar_selected(self, event):
        """Handle calendar date selection"""
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
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, booking_time, department, user_name, reason 
                FROM bookings 
                WHERE booking_date = ? 
                ORDER BY booking_time
            """, (date_str,))
            bookings = cursor.fetchall()
            conn.close()
            
            # Display bookings
            self.calendar_details_text.config(state="normal")
            self.calendar_details_text.delete("1.0", tk.END)
            
            if bookings:
                header = f"Found {len(bookings)} booking(s):\n{'='*60}\n\n"
                self.calendar_details_text.insert("1.0", header)
                
                for booking in bookings:
                    booking_id, time, dept, user, reason = booking
                    details = f"ID: #{booking_id}\n"
                    details += f"⏰ Time: {time}\n"
                    details += f"🏢 Department: {dept}\n"
                    details += f"👤 User: {user}\n"
                    details += f"📝 Reason: {reason}\n"
                    details += f"{'-'*60}\n\n"
                    self.calendar_details_text.insert(tk.END, details)
                
                self.update_status(f"Showing {len(bookings)} booking(s) for {date_str}")
            else:
                empty_msg = "No bookings for this date ✓\n\n"
                empty_msg += "This date is available! 🎉\n\n"
                empty_msg += "Click the 'New Booking' tab to create a new booking."
                self.calendar_details_text.insert("1.0", empty_msg)
                self.update_status(f"No bookings for {date_str}")
            
            self.calendar_details_text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch bookings:\n{str(e)}")
            self.update_status(f"Error: {str(e)}")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = TasmaBookingApp(root)
    root.mainloop()
