import sqlite3
import logging
import os

# Set up logging
logger = logging.getLogger(__name__)

# Database file name
DB_FILE = os.environ.get("DB_FILE", "shape_bot.db")

def init_db():
    """
    Initialize the database with the required tables.
    """
    logger.info("Initializing database...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create users table with user_id and api_key
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            api_key TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully!")

def store_api_key(user_id, api_key):
    """
    Store a user's API key in the database.
    
    Args:
        user_id (int): The Telegram user ID
        api_key (str): The user's Shapes API key
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Insert or replace the user's API key
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, api_key)
        VALUES (?, ?)
    ''', (user_id, api_key))
    
    conn.commit()
    conn.close()
    logger.info(f"Stored API key for user {user_id}")

def get_api_key(user_id):
    """
    Retrieve a user's API key from the database.
    
    Args:
        user_id (int): The Telegram user ID
        
    Returns:
        str or None: The API key if found, None otherwise
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT api_key FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result[0]
    return None

def delete_api_key(user_id):
    """
    Delete a user's API key from the database.
    
    Args:
        user_id (int): The Telegram user ID
        
    Returns:
        bool: True if a key was deleted, False otherwise
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    rows_affected = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    if rows_affected > 0:
        logger.info(f"Deleted API key for user {user_id}")
        return True
    return False
