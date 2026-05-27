"""
TASMA User Data Sync Module
Synchronizes all user data with server database
Ensures users see consistent data across all devices
"""

import sqlite3
from datetime import datetime
import logging
from typing import Dict, List, Tuple, Optional
import json

class UserDataSync:
    """Manages user data synchronization with server database"""
    
    def __init__(self, db):
        """
        Initialize user data sync
        
        Args:
            db: Database instance from db_optimized.py
        """
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def init_user_tables(self):
        """Create or verify user-related tables in database"""
        try:
            # Users table
            self.db.execute_update('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT,
                    email TEXT,
                    department TEXT,
                    role TEXT DEFAULT 'user',
                    phone TEXT,
                    is_active INTEGER DEFAULT 1,
                    last_login TIMESTAMP,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User preferences table
            self.db.execute_update('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    theme TEXT DEFAULT 'light',
                    auto_refresh BOOLEAN DEFAULT 1,
                    notifications_enabled BOOLEAN DEFAULT 1,
                    default_department TEXT,
                    preferred_rooms TEXT,
                    settings_json TEXT,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # Bookings table
            self.db.execute_update('''
                CREATE TABLE IF NOT EXISTS bookings (
                    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    booking_date DATE NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'confirmed',
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_by INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (created_by) REFERENCES users(user_id)
                )
            ''')
            
            # Rooms table
            self.db.execute_update('''
                CREATE TABLE IF NOT EXISTS rooms (
                    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_name TEXT UNIQUE NOT NULL,
                    capacity INTEGER,
                    location TEXT,
                    amenities TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User activity log
            self.db.execute_update('''
                CREATE TABLE IF NOT EXISTS user_activity_log (
                    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    action TEXT,
                    details TEXT,
                    ip_address TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            self.logger.info("User tables initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize user tables: {e}")
            return False
    
    def create_user(self, username: str, password: str, full_name: str, 
                   email: str, department: str, role: str = 'user') -> Optional[int]:
        """
        Create new user in server database
        
        Args:
            username: Username (unique)
            password: Hashed password
            full_name: User's full name
            email: User email
            department: User department
            role: User role (user, admin, manager)
            
        Returns:
            user_id if successful, None otherwise
        """
        try:
            result = self.db.execute_update('''
                INSERT INTO users 
                (username, password, full_name, email, department, role, created_date, updated_date)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''', (username, password, full_name, email, department, role))
            
            if result > 0:
                # Get the inserted user_id
                user = self.get_user_by_username(username)
                if user:
                    self.logger.info(f"User created: {username} (ID: {user['user_id']})")
                    # Create default preferences for user
                    self.create_user_preferences(user['user_id'])
                    return user['user_id']
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to create user {username}: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user data from server by username"""
        try:
            result = self.db.execute_query(
                'SELECT * FROM users WHERE username = ?',
                (username,),
                fetch='one'
            )
            
            if result:
                return dict(result)
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get user {username}: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user data from server by user_id"""
        try:
            result = self.db.execute_query(
                'SELECT * FROM users WHERE user_id = ?',
                (user_id,),
                fetch='one'
            )
            
            if result:
                return dict(result)
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get user {user_id}: {e}")
            return None
    
    def verify_user_password(self, username: str, password: str) -> bool:
        """Verify user credentials against server database"""
        user = self.get_user_by_username(username)
        if not user:
            return False
        
        # Hash comparison (assumes password is already hashed)
        return user.get('password') == password
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        """
        Update user information in server database
        
        Args:
            user_id: User ID
            **kwargs: Fields to update (e.g., full_name='John', email='john@example.com')
        """
        try:
            if not kwargs:
                return True
            
            # Build update query
            fields = [f"{k} = ?" for k in kwargs.keys()]
            values = list(kwargs.values())
            values.append(user_id)
            
            query = f'''
                UPDATE users 
                SET {', '.join(fields)}, updated_date = CURRENT_TIMESTAMP
                WHERE user_id = ?
            '''
            
            result = self.db.execute_update(query, values)
            return result > 0
            
        except Exception as e:
            self.logger.error(f"Failed to update user {user_id}: {e}")
            return False
    
    def create_user_preferences(self, user_id: int) -> bool:
        """Create default preferences for new user"""
        try:
            self.db.execute_update('''
                INSERT INTO user_preferences 
                (user_id, theme, auto_refresh, notifications_enabled, updated_date)
                VALUES (?, 'light', 1, 1, CURRENT_TIMESTAMP)
            ''', (user_id,))
            return True
        except Exception as e:
            self.logger.error(f"Failed to create preferences for user {user_id}: {e}")
            return False
    
    def get_user_preferences(self, user_id: int) -> Optional[Dict]:
        """Get user preferences from server"""
        try:
            result = self.db.execute_query(
                'SELECT * FROM user_preferences WHERE user_id = ?',
                (user_id,),
                fetch='one'
            )
            
            if result:
                return dict(result)
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get preferences for user {user_id}: {e}")
            return None
    
    def update_user_preferences(self, user_id: int, **kwargs) -> bool:
        """Update user preferences in server"""
        try:
            if not kwargs:
                return True
            
            fields = [f"{k} = ?" for k in kwargs.keys()]
            values = list(kwargs.values())
            values.append(user_id)
            
            query = f'''
                UPDATE user_preferences 
                SET {', '.join(fields)}, updated_date = CURRENT_TIMESTAMP
                WHERE user_id = ?
            '''
            
            result = self.db.execute_update(query, values)
            return result > 0
            
        except Exception as e:
            self.logger.error(f"Failed to update preferences for user {user_id}: {e}")
            return False
    
    def create_booking(self, room_id: int, user_id: int, booking_date: str,
                      start_time: str, end_time: str, title: str, 
                      description: str = "") -> Optional[int]:
        """
        Create booking in server database
        
        Returns:
            booking_id if successful, None otherwise
        """
        try:
            result = self.db.execute_update('''
                INSERT INTO bookings 
                (room_id, user_id, booking_date, start_time, end_time, 
                 title, description, status, created_date, updated_date, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'confirmed', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)
            ''', (room_id, user_id, booking_date, start_time, end_time, title, description, user_id))
            
            if result > 0:
                self.logger.info(f"Booking created for user {user_id}")
                self.log_activity(user_id, "CREATE_BOOKING", f"Room {room_id} on {booking_date}")
                return result
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to create booking: {e}")
            return None
    
    def get_user_bookings(self, user_id: int, date_from: str = None, 
                         date_to: str = None) -> List[Dict]:
        """Get all bookings for a user from server"""
        try:
            if date_from and date_to:
                query = '''
                    SELECT * FROM bookings 
                    WHERE user_id = ? AND booking_date BETWEEN ? AND ?
                    ORDER BY booking_date, start_time
                '''
                results = self.db.execute_query(query, (user_id, date_from, date_to), fetch='all')
            else:
                query = '''
                    SELECT * FROM bookings 
                    WHERE user_id = ?
                    ORDER BY booking_date DESC
                '''
                results = self.db.execute_query(query, (user_id,), fetch='all')
            
            return [dict(row) for row in results] if results else []
            
        except Exception as e:
            self.logger.error(f"Failed to get bookings for user {user_id}: {e}")
            return []
    
    def get_all_bookings(self, date_from: str = None, date_to: str = None) -> List[Dict]:
        """Get all bookings from server (for admin view)"""
        try:
            if date_from and date_to:
                query = '''
                    SELECT b.*, u.full_name, r.room_name
                    FROM bookings b
                    JOIN users u ON b.user_id = u.user_id
                    JOIN rooms r ON b.room_id = r.room_id
                    WHERE b.booking_date BETWEEN ? AND ?
                    ORDER BY b.booking_date, b.start_time
                '''
                results = self.db.execute_query(query, (date_from, date_to), fetch='all')
            else:
                query = '''
                    SELECT b.*, u.full_name, r.room_name
                    FROM bookings b
                    JOIN users u ON b.user_id = u.user_id
                    JOIN rooms r ON b.room_id = r.room_id
                    ORDER BY b.booking_date DESC
                '''
                results = self.db.execute_query(query, fetch='all')
            
            return [dict(row) for row in results] if results else []
            
        except Exception as e:
            self.logger.error(f"Failed to get all bookings: {e}")
            return []
    
    def delete_booking(self, booking_id: int, user_id: int) -> bool:
        """Delete a booking (user can only delete own bookings)"""
        try:
            result = self.db.execute_update(
                'DELETE FROM bookings WHERE booking_id = ? AND user_id = ?',
                (booking_id, user_id)
            )
            
            if result > 0:
                self.log_activity(user_id, "DELETE_BOOKING", f"Booking {booking_id} deleted")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to delete booking {booking_id}: {e}")
            return False
    
    def update_last_login(self, user_id: int) -> bool:
        """Update user's last login timestamp on server"""
        try:
            result = self.db.execute_update(
                'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?',
                (user_id,)
            )
            return result > 0
        except Exception as e:
            self.logger.error(f"Failed to update last login for user {user_id}: {e}")
            return False
    
    def log_activity(self, user_id: int, action: str, details: str = "", 
                    ip_address: str = "") -> bool:
        """Log user activity on server"""
        try:
            self.db.execute_update('''
                INSERT INTO user_activity_log 
                (user_id, action, details, ip_address, timestamp)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, action, details, ip_address))
            return True
        except Exception as e:
            self.logger.warning(f"Failed to log activity: {e}")
            return False
    
    def get_user_activity(self, user_id: int, limit: int = 100) -> List[Dict]:
        """Get user activity log from server"""
        try:
            results = self.db.execute_query('''
                SELECT * FROM user_activity_log 
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit), fetch='all')
            
            return [dict(row) for row in results] if results else []
            
        except Exception as e:
            self.logger.error(f"Failed to get activity log: {e}")
            return []
    
    def get_all_users(self, active_only: bool = True) -> List[Dict]:
        """Get all users from server"""
        try:
            if active_only:
                query = 'SELECT * FROM users WHERE is_active = 1 ORDER BY full_name'
                results = self.db.execute_query(query, fetch='all')
            else:
                query = 'SELECT * FROM users ORDER BY full_name'
                results = self.db.execute_query(query, fetch='all')
            
            return [dict(row) for row in results] if results else []
            
        except Exception as e:
            self.logger.error(f"Failed to get users: {e}")
            return []


# Global instance
_user_sync = None

def get_user_sync(db):
    """Get or create user data sync instance"""
    global _user_sync
    if _user_sync is None:
        _user_sync = UserDataSync(db)
    return _user_sync
