import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ManuPiyu90@",
        database="youtube_sentiment"
    )

def create_user_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password VARCHAR(100)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def create_analysis_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            comment TEXT,
            sentiment VARCHAR(10),
            video_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def register_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cur.close()
    conn.close()

def save_analysis(username, comments, sentiments, video_url):
    conn = get_connection()
    cur = conn.cursor()
    for comment, sentiment in zip(comments, sentiments):
        cur.execute("INSERT INTO analyses (username, comment, sentiment, video_url) VALUES (%s, %s, %s, %s)",
                    (username, comment, sentiment, video_url))
    conn.commit()
    cur.close()
    conn.close()

def fetch_user_history(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT video_url, sentiment, COUNT(*) 
        FROM analyses 
        WHERE username=%s 
        GROUP BY video_url, sentiment
    """, (username,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows