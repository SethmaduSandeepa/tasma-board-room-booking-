import sqlite3

conn = sqlite3.connect('bookings.db')
cursor = conn.cursor()

# Check bookings
cursor.execute('SELECT COUNT(*) FROM bookings')
count = cursor.fetchone()[0]
print(f'Total bookings: {count}')

if count > 0:
    cursor.execute('SELECT id, booking_date, booking_time, department, user_name FROM bookings')
    rows = cursor.fetchall()
    print('\nBookings:')
    for row in rows:
        print(f'  ID: {row[0]}, Date: {row[1]}, Time: {row[2]}, Dept: {row[3]}, User: {row[4]}')
else:
    print('No bookings found')

conn.close()
