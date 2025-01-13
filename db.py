import sqlite3

def create_tables():
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            username TEXT,
            victories INTEGER DEFAULT 0,
            defeats INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_player(player_id, username):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO players (id, username)
        VALUES (?, ?)
    """, (player_id, username))
    conn.commit()
    conn.close()
