import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
from datetime import datetime
import csv
import hashlib
import time
from tkcalendar import DateEntry, Calendar
from PIL import Image, ImageTk

class SimpleBookingApp:
    """Simplified, user-friendly booking app"""
    def __init__(self, root, logged_in_user, user_department=None):
        self.root = root
        self.logged_in_user = logged_in_user
        self.user_department = user_department
        self.root.title("TASMA Board Room Booking System")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Colors
        self.bg_main = "#ffffff"
        self.accent_blue = "#0052cc"
        self.accent_blue_light = "#e0eaff"
        self.text_primary = "#1f2937"
        self.text_secondary = "#6b7280"
        self.border_gray = "#e5e7eb"
        self.success_green = "#10b981"
        
        self.root.configure(bg=self.bg_main)
        self.db_name = "bookings.db"
        self.init_database()
        
        # ===== HEADER =====
        header = tk.Frame(self.root, bg=self.accent_blue, height=80)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        # Logo/Title
        title_frame = tk.Frame(header, bg=self.accent_blue)
        title_frame.pack(side="left", padx=25, pady=20)
        
        title = tk.Label(title_frame, text="📅 TASMA Booking System", 
                        font=("Arial", 20, "bold"), fg="white", bg=self.accent_blue)
        title.pack(anchor="w")
        
        subtitle = tk.Label(title_frame, text="Book your room in seconds", 
                           font=("Arial", 11), fg="#cce5ff", bg=self.accent_blue)
        subtitle.pack(anchor="w")
        
        # User info
        user_frame = tk.Frame(header, bg=self.accent_blue)
        user_frame.pack(side="right", padx=25, pady=20)
        
        tk.Label(user_frame, text=f"👤 {logged_in_user}", 
                font=("Arial", 11, "bold"), fg="white", bg=self.accent_blue).pack()
        
        tk.Button(user_frame, text="Logout", command=self.logout, 
                 bg="white", fg=self.accent_blue, font=("Arial", 9, "bold"),
                 relief="flat", bd=0, padx=15, pady=5, cursor="hand2").pack(pady=(8, 0))
        
        # ===== MAIN CONTENT =====
        main = tk.Frame(self.root, bg=self.bg_main)
        main.pack(fill="both", expand=True, padx=30, pady=30)
        
        # ===== SECTION 1: QUICK BOOKING FORM =====
        form_title = tk.Label(main, text="Create a Booking", 
                             font=("Arial", 18, "bold"), fg=self.accent_blue, bg=self.bg_main)
        form_title.pack(anchor="w", pady=(0, 20))
        
        # Form container
        form_box = tk.Frame(main, bg=self.border_gray, relief="solid", bd=1)
        form_box.pack(fill="x", padx=0, pady=(0, 30))
        
        form_inner = tk.Frame(form_box, bg=self.bg_main)
        form_inner.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Row 1: Date and Time
        row1 = tk.Frame(form_inner, bg=self.bg_main)
        row1.pack(fill="x", pady=(0, 15))
        
        tk.Label(row1, text="Date", font=("Arial", 12, "bold"), fg=self.text_primary, bg=self.bg_main).pack(side="left", padx=(0, 10))
        self.date_entry = DateEntry(row1, width=20, background=self.accent_blue, foreground="white", 
                                   borderwidth=2, font=("Arial", 11))
        self.date_entry.pack(side="left", padx=(0, 30))
        
        tk.Label(row1, text="Time (HH:MM)", font=("Arial", 12, "bold"), fg=self.text_primary, bg=self.bg_main).pack(side="left", padx=(0, 10))
        time_frame = tk.Frame(row1, bg=self.bg_main)
        time_frame.pack(side="left")
        
        self.hour_var = tk.StringVar(value="09")
        self.minute_var = tk.StringVar(value="00")
        
        tk.Spinbox(time_frame, from_=0, to=23, width=4, font=("Arial", 13, "bold"), 
                  textvariable=self.hour_var, justify="center").pack(side="left", padx=3)
        tk.Label(time_frame, text=":", font=("Arial", 13, "bold"), bg=self.bg_main).pack(side="left", padx=3)
        tk.Spinbox(time_frame, from_=0, to=59, width=4, font=("Arial", 13, "bold"),
                  textvariable=self.minute_var, justify="center").pack(side="left", padx=3)
        
        # Row 2: Department and Duration
        row2 = tk.Frame(form_inner, bg=self.bg_main)
        row2.pack(fill="x", pady=(0, 15))
        
        tk.Label(row2, text="Department", font=("Arial", 12, "bold"), fg=self.text_primary, bg=self.bg_main).pack(side="left", padx=(0, 10))
        self.dept_combo = ttk.Combobox(row2, width=20, font=("Arial", 11),
                                      values=["Finance", "HR", "IT", "Marketing", "Operations", "Sales", "Other"],
                                      state="readonly")
        if user_department:
            self.dept_combo.set(user_department)
        else:
            self.dept_combo.set("IT")
        self.dept_combo.pack(side="left", padx=(0, 30))
        
        tk.Label(row2, text="Duration", font=("Arial", 12, "bold"), fg=self.text_primary, bg=self.bg_main).pack(side="left", padx=(0, 10))
        self.duration_combo = ttk.Combobox(row2, width=20, font=("Arial", 11),
                                          values=["30 min", "1 hour", "1.5 hours", "2 hours", "3 hours", "Full day"],
                                          state="readonly")
        self.duration_combo.set("1 hour")
        self.duration_combo.pack(side="left")
        
        # Row 3: Reason
        row3 = tk.Frame(form_inner, bg=self.bg_main)
        row3.pack(fill="x", pady=(0, 15))
        
        tk.Label(row3, text="Reason for booking", font=("Arial", 12, "bold"), fg=self.text_primary, bg=self.bg_main).pack(anchor="w", pady=(0, 8))
        self.reason_text = tk.Text(row3, width=80, height=4, font=("Arial", 11),
                                  bg=self.border_gray, fg=self.text_primary, relief="solid", bd=1)
        self.reason_text.pack(fill="x")
        
        # Buttons
        btn_row = tk.Frame(form_inner, bg=self.bg_main)
        btn_row.pack(fill="x", pady=(15, 0))
        
        book_btn = tk.Button(btn_row, text="✓ BOOK ROOM", command=self.book_room,
                            bg=self.success_green, fg="white", font=("Arial", 13, "bold"),
                            relief="flat", bd=0, padx=30, pady=12, cursor="hand2",
                            activebackground="#059669")
        book_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = tk.Button(btn_row, text="Clear", command=self.clear_form,
                             bg="#f3f4f6", fg=self.text_secondary, font=("Arial", 11),
                             relief="flat", bd=0, padx=20, pady=10, cursor="hand2")
        clear_btn.pack(side="left")
        
        # ===== SECTION 2: YOUR BOOKINGS =====
        bookings_title = tk.Label(main, text="Your Bookings Today", 
                                 font=("Arial", 16, "bold"), fg=self.accent_blue, bg=self.bg_main)
        bookings_title.pack(anchor="w", pady=(20, 15))
        
        # Bookings list
        list_box = tk.Frame(main, bg=self.border_gray, relief="solid", bd=1)
        list_box.pack(fill="both", expand=True)
        
        list_inner = tk.Frame(list_box, bg=self.bg_main)
        list_inner.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Scrollable canvas for bookings
        canvas = tk.Canvas(list_inner, bg=self.bg_main, highlightthickness=0, relief="flat")
        scrollbar = ttk.Scrollbar(list_inner, orient="vertical", command=canvas.yview)
        
        self.bookings_frame = tk.Frame(canvas, bg=self.bg_main)
        canvas.create_window((0, 0), window=self.bookings_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.bookings_frame.bind("<Configure>", on_frame_configure)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Status bar
        status = tk.Label(main, text="Ready to book", font=("Arial", 10), 
                         fg=self.text_secondary, bg=self.bg_main)
        status.pack(anchor="w", pady=(20, 0))
        
        self.status_label = status
        self.canvas = canvas
        
        # Load bookings
        self.load_today_bookings()
    
    def clear_form(self):
        """Clear the form"""
        self.date_entry.set_date(datetime.now().date())
        self.hour_var.set("09")
        self.minute_var.set("00")
        self.duration_combo.set("1 hour")
        self.reason_text.delete("1.0", "end")
    
    def book_room(self):
        """Add booking to database"""
        date = str(self.date_entry.get_date()).strip()
        time = f"{self.hour_var.get()}:{self.minute_var.get()}"
        dept = self.dept_combo.get().strip()
        duration_str = self.duration_combo.get().strip()
        reason = self.reason_text.get("1.0", "end-1c").strip()
        
        if not all([date, time, dept, duration_str]):
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        # Parse duration
        duration_map = {"30 min": 30, "1 hour": 60, "1.5 hours": 90, "2 hours": 120, "3 hours": 180, "Full day": 480}
        duration_mins = duration_map.get(duration_str, 60)
        
        try:
            conn = sqlite3.connect(self.db_name, timeout=30.0)
            cursor = conn.cursor()
            
            cursor.execute("""INSERT INTO bookings 
                           (booking_date, booking_time, duration_minutes, department, user_name, reason)
                           VALUES (?, ?, ?, ?, ?, ?)""",
                         (date, time, duration_mins, dept, self.logged_in_user, reason))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Room booked for {time} on {date}!")
            self.clear_form()
            self.load_today_bookings()
        except Exception as e:
            messagebox.showerror("Error", f"Booking failed: {str(e)}")
    
    def load_today_bookings(self):
        """Load and display today's bookings"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Clear previous bookings
        for widget in self.bookings_frame.winfo_children():
            widget.destroy()
        
        try:
            conn = sqlite3.connect(self.db_name, timeout=30.0)
            cursor = conn.cursor()
            cursor.execute("""SELECT id, booking_time, duration_minutes, department, user_name, reason 
                            FROM bookings WHERE booking_date = ? ORDER BY booking_time""", (today,))
            bookings = cursor.fetchall()
            conn.close()
            
            if not bookings:
                empty = tk.Label(self.bookings_frame, text="No bookings yet today 🎉", 
                               font=("Arial", 12), fg=self.text_secondary, bg=self.bg_main)
                empty.pack(pady=20)
                self.status_label.config(text=f"No bookings for {today}")
                return
            
            for booking in bookings:
                booking_id, time, duration_mins, dept, user, reason = booking
                
                # Booking card
                card = tk.Frame(self.bookings_frame, bg="#f9fafb", relief="solid", bd=1)
                card.pack(fill="x", pady=8)
                
                card_content = tk.Frame(card, bg="#f9fafb")
                card_content.pack(fill="x", padx=15, pady=12)
                
                # Header
                header_text = f"⏰ {time} • {dept} • {user}"
                tk.Label(card_content, text=header_text, font=("Arial", 12, "bold"), 
                        fg=self.text_primary, bg="#f9fafb").pack(anchor="w")
                
                # Reason
                if reason:
                    tk.Label(card_content, text=f"📝 {reason}", font=("Arial", 10), 
                            fg=self.text_secondary, bg="#f9fafb", wraplength=300).pack(anchor="w", pady=(5, 0))
                
                # Duration
                dur_text = f"{duration_mins} min" if duration_mins < 60 else f"{duration_mins//60}h"
                tk.Label(card_content, text=f"⏱ {dur_text}", font=("Arial", 9), 
                        fg=self.text_secondary, bg="#f9fafb").pack(anchor="w")
            
            self.status_label.config(text=f"Showing {len(bookings)} booking(s) for {today}")
        except Exception as e:
            error_label = tk.Label(self.bookings_frame, text=f"Error loading bookings: {str(e)}", 
                                  font=("Arial", 11), fg="red", bg=self.bg_main)
            error_label.pack(pady=20)
    
    def init_database(self):
        """Create database if needed"""
        conn = sqlite3.connect(self.db_name, timeout=30.0)
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def logout(self):
        """Logout user"""
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleBookingApp(root, "demo_user", "IT")
    root.mainloop()
