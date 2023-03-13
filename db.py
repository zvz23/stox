import sqlite3

DB_NAME = 'stox.db'
TABLE_NAME = 'leads'

def is_stox_exists(stox_id: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT ID FROM {TABLE_NAME} WHERE STOX_ID=?", [stox_id])
        result = cursor.fetchone()
        if result is None:
            return False
        return True
    
def save_stox(stox_id: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT OR IGNORE INTO {TABLE_NAME}(STOX_ID) VALUES(?)", [stox_id])