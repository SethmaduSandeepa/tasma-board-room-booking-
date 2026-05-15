import sqlite3
from datetime import datetime

conn = sqlite3.connect('bookings.db')
cursor = conn.cursor()

# Add test bookings
test_bookings = [
    ('2026-02-28', '10:30', 'HR', 'kasun', 'meeting of monthly pay'),
    ('2026-02-28', '14:00', 'IT', 'john', 'system maintenance'),
    ('2026-03-01', '09:00', 'Finance', 'sarah', 'quarterly review'),
    ('2026-03-05', '15:30', 'Marketing', 'mike', 'campaign planning'),
]

for date, time, dept, user, reason in test_bookings:
    cursor.execute('''
        INSERT INTO bookings (booking_date, booking_time, department, user_name, reason)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, time, dept, user, reason))
    print(f"Added: {date} {time} - {dept} - {user}")

conn.commit()
conn.close()
print("\nTest bookings added successfully!")
