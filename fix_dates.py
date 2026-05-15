import sqlite3
from datetime import datetime

conn = sqlite3.connect('bookings.db')
cursor = conn.cursor()

# Get all bookings
cursor.execute('SELECT id, booking_date FROM bookings')
bookings = cursor.fetchall()

# Update each booking with properly formatted date
for booking_id, date_str in bookings:
    try:
        # Try to parse the current format (M/D/YY or M/DD/YY)
        if '/' in date_str:
            parsed = datetime.strptime(date_str, "%m/%d/%y")
            new_date = parsed.strftime("%Y-%m-%d")
            cursor.execute('UPDATE bookings SET booking_date = ? WHERE id = ?', (new_date, booking_id))
            print(f"Updated ID {booking_id}: {date_str} → {new_date}")
    except Exception as e:
        print(f"Error updating ID {booking_id}: {e}")

conn.commit()
conn.close()
print("Database updated successfully!")
