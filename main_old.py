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
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Set style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Database Configuration
        self.db_name = "bookings.db"
        self.init_database()
        
        self.selected_booking_id = None
        self.is_edit_mode = False
        
        # --- Main Container ---
        main_container = tk.Frame(root, bg="#f5f5f5")
        main_container.pack(fill="both", expand=True)
        
        # --- Status Bar (Create Early) ---
        status_frame = tk.Frame(main_container, bg="#333", height=30)
        status_frame.pack(fill="x", side="bottom")
        self.status_label = tk.Label(status_frame, text="Ready", font=("Arial", 9), 
                                    fg="white", bg="#333", justify="left", padx=10)
        self.status_label.pack(side="left", fill="both", expand=True)
        
        # --- Header/Title ---
        title_frame = tk.Frame(main_container, bg="#1976D2", height=60)
        title_frame.pack(fill="x")
        title_label = tk.Label(title_frame, text="TASMA Board Room Booking System", 
                              font=("Helvetica", 22, "bold"), fg="white", bg="#1976D2", pady=15)
        title_label.pack()
        
        # --- Content Frame ---
        content_frame = tk.Frame(main_container, bg="#f5f5f5")
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # --- Notebook (Tabs) ---
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab 1: New Booking
        book_tab = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(book_tab, text="New Booking")
        
        # Form Frame
        form_frame = tk.LabelFrame(book_tab, text="Booking Details", font=("Arial", 12, "bold"), 
                                   padx=20, pady=20, bg="#f5f5f5", fg="#333")
        form_frame.pack(fill="x", padx=10, pady=10)
        
        # Row 1: Date and Time
        tk.Label(form_frame, text="Date:", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, sticky="w", pady=8)
        self.entry_date = DateEntry(form_frame, width=25, background='darkblue', foreground='white', 
                                    borderwidth=2, year=datetime.now().year, month=datetime.now().month, 
                                    day=datetime.now().day)
        self.entry_date.grid(row=0, column=1, pady=8, padx=10, sticky="w")
        
        tk.Label(form_frame, text="Time (HH:MM):", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=2, sticky="w", pady=8, padx=(20,0))
        self.entry_time = tk.Entry(form_frame, width=20, font=("Arial", 10))
        self.entry_time.grid(row=0, column=3, pady=8, padx=10, sticky="w")
        
        # Row 2: Department and User
        tk.Label(form_frame, text="Department:", font=("Arial", 10), bg="#f5f5f5").grid(row=1, column=0, sticky="w", pady=8)
        self.entry_dept = ttk.Combobox(form_frame, width=22, font=("Arial", 10), 
                                       values=["Finance", "HR", "IT", "Marketing", "Operations", "Sales", "Other"])
        self.entry_dept.grid(row=1, column=1, pady=8, padx=10, sticky="w")
        
        tk.Label(form_frame, text="User Name:", font=("Arial", 10), bg="#f5f5f5").grid(row=1, column=2, sticky="w", pady=8, padx=(20,0))
        self.entry_user = tk.Entry(form_frame, width=20, font=("Arial", 10))
        self.entry_user.grid(row=1, column=3, pady=8, padx=10, sticky="w")
        
        # Row 3: Reason
        tk.Label(form_frame, text="Reason:", font=("Arial", 10), bg="#f5f5f5").grid(row=2, column=0, sticky="nw", pady=8)
        self.entry_reason = tk.Text(form_frame, width=60, height=3, font=("Arial", 10))
        self.entry_reason.grid(row=2, column=1, columnspan=3, pady=8, padx=10, sticky="w")
        
        # Buttons Frame
        btn_frame = tk.Frame(form_frame, bg="#f5f5f5")
        btn_frame.grid(row=3, column=0, columnspan=4, pady=15)
        
        tk.Button(btn_frame, text="Book Room", command=self.add_booking, bg="#4CAF50", fg="white", 
                 font=("Arial", 10, "bold"), width=15, height=2, cursor="hand2").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Edit Selected", command=self.edit_booking, bg="#FF9800", fg="white",
                 font=("Arial", 10, "bold"), width=15, height=2, cursor="hand2").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Clear Form", command=self.clear_inputs, bg="#9C27B0", fg="white",
                 font=("Arial", 10, "bold"), width=15, height=2, cursor="hand2").pack(side="left", padx=10)
        
        # Tab 2: Manage Bookings
        manage_tab = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(manage_tab, text="Manage Bookings")
        
        # Search Frame
        search_frame = tk.Frame(manage_tab, bg="#f5f5f5")
        search_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(search_frame, text="Search:", font=("Arial", 10, "bold"), bg="#f5f5f5").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_bookings())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40, font=("Arial", 10))
        search_entry.pack(side="left", padx=5)
        
        tk.Label(search_frame, text="(Search by Date, Department, User, or Reason)", 
                font=("Arial", 9, "italic"), bg="#f5f5f5", fg="#666").pack(side="left", padx=5)
        
        # Bookings List Frame
        list_frame = tk.LabelFrame(manage_tab, text="Current Bookings", font=("Arial", 12, "bold"), 
                                  padx=10, pady=10, bg="#f5f5f5", fg="#333")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview with better styling
        columns = ("ID", "Date", "Time", "Department", "User", "Reason")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=18)
        
        # Define Headings and widths
        col_widths = {"ID": 40, "Date": 90, "Time": 60, "Department": 100, "User": 100, "Reason": 300}
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=col_widths[col])
        
        # Add alternating row colors
        self.tree.tag_configure('oddrow', background='white')
        self.tree.tag_configure('evenrow', background='#f9f9f9')
        self.tree.tag_configure('selected', background='#1976D2', foreground='white')
        
        # Configure treeview style
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
        # Scrollbars
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Action Buttons Frame
        action_frame = tk.Frame(manage_tab, bg="#f5f5f5")
        action_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(action_frame, text="Refresh List", command=self.load_bookings, bg="#2196F3", 
                 fg="white", font=("Arial", 10, "bold"), width=15, height=2, cursor="hand2").pack(side="left", padx=10)
        tk.Button(action_frame, text="Delete Selected", command=self.delete_booking, bg="#f44336",
                 fg="white", font=("Arial", 10, "bold"), width=15, height=2, cursor="hand2").pack(side="left", padx=10)
        tk.Button(action_frame, text="Export to CSV", command=self.export_to_csv, bg="#00BCD4",
                 fg="white", font=("Arial", 10, "bold"), width=15, height=2, cursor="hand2").pack(side="left", padx=10)
        
        # Tab 3: Calendar View
        calendar_tab = tk.Frame(self.notebook, bg="#f5f5f5")
        self.notebook.add(calendar_tab, text="Calendar View")
        
        # Main container for calendar tab with grid layout
        cal_main_frame = tk.Frame(calendar_tab, bg="#f5f5f5")
        cal_main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid weights for responsive layout
        cal_main_frame.grid_columnconfigure(0, weight=2, minsize=400)  # Calendar takes more space
        cal_main_frame.grid_columnconfigure(1, weight=1, minsize=300)  # Details area
        cal_main_frame.grid_rowconfigure(0, weight=1)
        
        # Left side - Calendar Widget (now using grid)
        cal_left_frame = tk.LabelFrame(cal_main_frame, text="Select a Date", font=("Arial", 12, "bold"),
                                       padx=10, pady=10, bg="#f5f5f5", fg="#333")
        cal_left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.calendar_widget = Calendar(cal_left_frame, selectmode='day', year=datetime.now().year, 
                                       month=datetime.now().month, day=datetime.now().day,
                                       cursor="hand2", font=("Arial", 11), headersformatvar="long",
                                       width=30)  # Make calendar wider
        self.calendar_widget.pack(fill="both", expand=True)
        self.calendar_widget.bind("<<CalendarSelected>>", self.on_calendar_selected)
        
        # Configure tag for dates with bookings
        self.calendar_widget.tag_config('booked', background='#4CAF50', foreground='white')
        
        # Right side - Bookings Details (using grid)
        cal_right_frame = tk.LabelFrame(cal_main_frame, text="Bookings for Selected Date", font=("Arial", 12, "bold"),
                                       padx=10, pady=10, bg="#f5f5f5", fg="#333")
        cal_right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Selected date label
        self.selected_date_label = tk.Label(cal_right_frame, text="", font=("Arial", 11, "bold"), 
                                           bg="#E3F2FD", fg="#1976D2", padx=10, pady=5, relief="solid", borderwidth=1)
        self.selected_date_label.pack(fill="x", pady=(0, 10))
        
        # Scrollable text area for bookings
        scrollable_frame = tk.Frame(cal_right_frame)
        scrollable_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(scrollable_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.calendar_details_text = tk.Text(scrollable_frame, height=20, font=("Arial", 10), 
                                            wrap="word", yscrollcommand=scrollbar.set)
        self.calendar_details_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.calendar_details_text.yview)
        
        # Button Frame
        button_frame = tk.Frame(cal_right_frame, bg="#f5f5f5")
        button_frame.pack(fill="x", pady=(10, 0))
        
        tk.Button(button_frame, text="Today", command=self.calendar_goto_today, bg="#4CAF50",
                 fg="white", font=("Arial", 10, "bold"), width=15, cursor="hand2").pack(side="left", padx=5)
        tk.Button(button_frame, text="Refresh", command=self.calendar_refresh_display, bg="#2196F3",
                 fg="white", font=("Arial", 10, "bold"), width=15, cursor="hand2").pack(side="left", padx=5)
        
        self.selected_date = None
        
        # Load initial data
        self.load_bookings()
        
        # Initialize calendar display after load_bookings
        self.on_calendar_selected(None)

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
        """Check if there's already a booking at this time"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            if exclude_id:
                cursor.execute("SELECT COUNT(*) FROM bookings WHERE booking_date=? AND booking_time=? AND id!=?",
                             (date, time, exclude_id))
            else:
                cursor.execute("SELECT COUNT(*) FROM bookings WHERE booking_date=? AND booking_time=?",
                             (date, time))
            result = cursor.fetchone()
            conn.close()
            return result[0] > 0
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
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a booking to delete.")
            self.update_status("No booking selected for deletion")
            return
        
        item_values = self.tree.item(selected_item)['values']
        item_id = item_values[0]
        dept = item_values[3]
        date = item_values[1]
        
        confirm = messagebox.askyesno("Confirm Deletion", 
            f"Delete booking #{item_id}?\n{dept} - {date}\n\nThis action cannot be undone.")
        
        if confirm:
            try:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM bookings WHERE id=?", (item_id,))
                conn.commit()
                conn.close()
                self.update_status(f"Booking #{item_id} deleted successfully")
                self.load_bookings()
                messagebox.showinfo("Success", "Booking cancelled successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete booking:\n{str(e)}")
                self.update_status(f"Error deleting booking: {str(e)}")

    def clear_inputs(self):
        """Clear input fields"""
        self.entry_date.set_date(datetime.now().date())
        self.entry_time.delete(0, tk.END)
        self.entry_dept.set("")
        self.entry_user.delete(0, tk.END)
        self.entry_reason.delete("1.0", tk.END)
        self.is_edit_mode = False
        self.selected_booking_id = None
        self.update_status("Form cleared")
    
    def filter_bookings(self):
        """Filter bookings based on search query"""
        search_term = self.search_var.get().lower().strip()
        
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
                if (search_term in str(booking[1]).lower() or  # date
                    search_term in str(booking[2]).lower() or  # time
                    search_term in booking[3].lower() or       # department
                    search_term in booking[4].lower() or       # user
                    search_term in booking[5].lower()):        # reason
                    filtered.append(booking)
            
            self.load_bookings(filtered)
            self.update_status(f"Found {len(filtered)} matching booking(s)")
        except Exception as e:
            self.update_status(f"Search error: {str(e)}")
    
    def sort_by_column(self, col):
        """Sort treeview by column"""
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        items.sort(reverse=False)
        
        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)
        
        self.update_status(f"Sorted by {col}")
    
    def export_to_csv(self):
        """Export bookings to CSV file"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"bookings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if not file_path:
                return
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT id, booking_date, booking_time, department, user_name, reason, created_at FROM bookings ORDER BY booking_date DESC")
            bookings = cursor.fetchall()
            conn.close()
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Date', 'Time', 'Department', 'User', 'Reason', 'Created At'])
                writer.writerows(bookings)
            
            messagebox.showinfo("Success", f"Exported {len(bookings)} booking(s) to:\n{file_path}")
            self.update_status(f"Exported {len(bookings)} bookings to CSV")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export bookings:\n{str(e)}")
            self.update_status(f"Export error: {str(e)}")
    
    def update_status(self, message):
        """Update status bar message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_label.config(text=f"[{timestamp}] {message}")
    
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

if __name__ == "__main__":
    root = tk.Tk()
    app = TasmaBookingApp(root)
    root.mainloop()
