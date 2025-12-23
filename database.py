import sqlite3

def init_db():
    conn = sqlite3.connect("game.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        coins INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def add_coins(user_id, amount):
    conn = sqlite3.connect("game.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, coins) VALUES (?, 0)", (user_id,))
    c.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = sqlite3.connect("game.db")
    c = conn.cursor()
    c.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0
  
