from datetime import datetime
import sqlite3
import os
from bot.config import DATABASE_PATH

def log_interaction(telegram_id, action):
    interactions_db_path = os.path.join(DATABASE_PATH, "interactions.db")
    conn = sqlite3.connect(interactions_db_path)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO interactions (telegram_id, action, timestamp) VALUES (?, ?, ?)",
                   (telegram_id, action, timestamp))
    conn.commit()
    conn.close()
