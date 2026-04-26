import sqlite3

def init_db():
    conn = sqlite3.connect('logs_database.db')
    cursor = conn.cursor()
    # Table banana (Timestamp, Severity, Message ke liye)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            severity TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_logs_to_db(parsed_data):
    conn = sqlite3.connect('logs_database.db')
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO system_logs (timestamp, severity, message) VALUES (?, ?, ?)', parsed_data)
    conn.commit()
    conn.close()