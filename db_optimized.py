"""
Optimized Database Module for Server Deployment
Provides improved concurrent access, connection pooling, and caching
"""
import sqlite3
import os
import threading
from queue import Queue
from datetime import datetime, timedelta
import configparser
import logging

class DatabasePool:
    """Connection pool for optimized concurrent database access"""
    def __init__(self, db_path, pool_size=5, timeout=60):
        self.db_path = db_path
        self.pool_size = pool_size
        self.timeout = timeout
        self.connection_pool = Queue(maxsize=pool_size)
        self.lock = threading.Lock()
        self.connections = []
        
        # Initialize pool with connections
        for _ in range(pool_size):
            try:
                conn = sqlite3.connect(db_path, timeout=timeout, 
                                      check_same_thread=False,
                                      isolation_level='DEFERRED')
                conn.row_factory = sqlite3.Row
                self.connection_pool.put(conn)
                self.connections.append(conn)
            except Exception as e:
                logging.error(f"Failed to create connection: {e}")
    
    def get_connection(self):
        """Get a connection from the pool"""
        try:
            return self.connection_pool.get(timeout=self.timeout)
        except:
            # If pool is empty, create a new connection
            conn = sqlite3.connect(self.db_path, timeout=self.timeout,
                                  check_same_thread=False,
                                  isolation_level='DEFERRED')
            conn.row_factory = sqlite3.Row
            return conn
    
    def return_connection(self, conn):
        """Return a connection to the pool"""
        try:
            self.connection_pool.put(conn, block=False)
        except:
            # Pool is full, close the connection
            try:
                conn.close()
            except:
                pass
    
    def close_all(self):
        """Close all connections in pool"""
        while not self.connection_pool.empty():
            try:
                conn = self.connection_pool.get_nowait()
                conn.close()
            except:
                pass


class SimpleCache:
    """Simple in-memory cache with TTL"""
    def __init__(self, ttl_seconds=300):
        self.cache = {}
        self.ttl = ttl_seconds
        self.timestamps = {}
        self.lock = threading.Lock()
    
    def get(self, key):
        """Get value from cache if not expired"""
        with self.lock:
            if key in self.cache:
                if datetime.now() - self.timestamps[key] < timedelta(seconds=self.ttl):
                    return self.cache[key]
                else:
                    del self.cache[key]
                    del self.timestamps[key]
        return None
    
    def set(self, key, value):
        """Set value in cache"""
        with self.lock:
            self.cache[key] = value
            self.timestamps[key] = datetime.now()
    
    def clear(self):
        """Clear entire cache"""
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()


class OptimizedDatabase:
    """Optimized database wrapper for server deployment"""
    
    def __init__(self, config_file='config.ini'):
        self.config = self._load_config(config_file)
        self.db_path = self._get_db_path()
        self.pool = DatabasePool(
            self.db_path,
            pool_size=int(self.config.get('PERFORMANCE', 'connection_pool_size', fallback=5)),
            timeout=int(self.config.get('SERVER', 'db_timeout', fallback=60))
        )
        
        enable_cache = self.config.get('SERVER', 'enable_cache', fallback='true').lower() == 'true'
        cache_timeout = int(self.config.get('SERVER', 'cache_timeout', fallback=300))
        self.cache = SimpleCache(cache_timeout) if enable_cache else None
        
        # Setup logging
        self._setup_logging()
    
    def _load_config(self, config_file):
        """Load configuration from ini file"""
        config = configparser.ConfigParser()
        if os.path.exists(config_file):
            config.read(config_file)
        return config
    
    def _setup_logging(self):
        """Setup logging based on config"""
        debug_mode = self.config.get('LOGGING', 'debug_mode', fallback='false').lower() == 'true'
        log_file = self.config.get('LOGGING', 'log_file', fallback='tasma_app.log')
        
        level = logging.DEBUG if debug_mode else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def _get_db_path(self):
        """Get database path from config or default"""
        import sys
        
        config_path = self.config.get('SERVER', 'database_path', fallback=None)
        
        if config_path:
            # Handle UNC paths and environment variables
            config_path = os.path.expandvars(config_path)
            return config_path
        
        # Default: check deployment directory first, then AppData
        if getattr(sys, 'frozen', False):
            app_dir = os.path.dirname(sys.executable)
        else:
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        db_path = os.path.join(app_dir, 'bookings.db')
        if os.path.exists(db_path):
            return db_path
        
        # Fallback to AppData
        appdata = os.getenv('APPDATA', os.path.expanduser('~'))
        return os.path.join(appdata, 'TASMA', 'bookings.db')
    
    def execute_query(self, query, params=None, fetch='all', use_cache=False):
        """Execute a query with connection pooling"""
        cache_key = f"{query}:{params}" if use_cache else None
        
        # Check cache
        if use_cache and self.cache:
            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                return cached_result
        
        conn = self.pool.get_connection()
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch == 'all':
                result = cursor.fetchall()
            elif fetch == 'one':
                result = cursor.fetchone()
            else:
                result = None
            
            # Cache the result
            if use_cache and self.cache and result:
                self.cache.set(cache_key, result)
            
            return result
        finally:
            self.pool.return_connection(conn)
    
    def execute_update(self, query, params=None):
        """Execute an update/insert/delete query"""
        conn = self.pool.get_connection()
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                logging.warning(f"Database locked, retrying: {e}")
                conn.rollback()
                # Retry once
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
            else:
                conn.rollback()
                raise
        finally:
            self.pool.return_connection(conn)
    
    def close(self):
        """Close all database connections"""
        self.pool.close_all()
        if self.cache:
            self.cache.clear()


# Global database instance
_db_instance = None

def get_db():
    """Get or create database instance (singleton pattern)"""
    global _db_instance
    if _db_instance is None:
        _db_instance = OptimizedDatabase()
    return _db_instance
