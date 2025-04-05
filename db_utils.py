import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stylist.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS preferences
                 (username TEXT PRIMARY KEY,
                  age INTEGER,
                  gender TEXT,
                  style_preferences TEXT,
                  favorite_colors TEXT,
                  image_path TEXT)''')
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    result = c.fetchone()
    conn.close()
    return bool(result)

def save_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO users VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def save_preferences(username, preferences, image_path=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO preferences VALUES (?, ?, ?, ?, ?, ?)',
              (username, preferences['age'], preferences['gender'],
               ','.join(preferences['style_preferences']),
               ','.join(preferences['favorite_colors']),
               image_path))
    conn.commit()
    conn.close()

def get_preferences(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM preferences WHERE username=?', (username,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return {
            'age': result[1],
            'gender': result[2],
            'style_preferences': result[3].split(',') if result[3] else [],
            'favorite_colors': result[4].split(',') if result[4] else [],
            'image_path': result[5]
        }
    return None