import sqlite3

def create_db():
    conn = sqlite3.connect('lyrics.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            output_text TEXT,
            order_val INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rating INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    return conn, cursor

def insert_history(conn, cursor, input_text, output_text, order_val):
    cursor.execute('''
        INSERT INTO history (input_text, output_text, order_val) 
        VALUES (?, ?, ?)
    ''', (input_text, output_text, order_val))
    conn.commit()
