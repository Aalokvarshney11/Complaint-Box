import sqlite3
import hashlib

def get_all_complaints():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints ORDER BY created_at DESC")
    complaints = cursor.fetchall()
    conn.close()
    return complaints

def get_unsolved_complaints():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE status='unsolved' ORDER BY created_at DESC")
    complaints = cursor.fetchall()
    conn.close()
    return complaints

def get_solved_complaints():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE status='solved' ORDER BY created_at DESC")
    complaints = cursor.fetchall()
    conn.close()
    return complaints

def mark_solved(complaint_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status='solved' WHERE id=?", (complaint_id,))
    conn.commit()
    conn.close()

def login_user(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Pehle manager check
    cursor.execute("SELECT * FROM managers WHERE username=? AND password=?", (username, hashed))
    manager = cursor.fetchone()
    if manager:
        conn.close()
        return "manager"
    
    # Phir client check
    cursor.execute("SELECT * FROM clients WHERE username=? AND password=?", (username, hashed))
    client = cursor.fetchone()
    if client:
        conn.close()
        return "client"
    
    conn.close()
    return None

def register_client(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO clients (username, password) VALUES (?,?)", 
                      (username, hashed))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def get_connection():
    conn = sqlite3.connect("complaintbox.db")
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            house_number TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            problem TEXT NOT NULL,
            status TEXT DEFAULT 'unsolved',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Managers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS managers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # Clients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()