import sqlite3
from db import DB_NAME, TABLE_NAME

def cleardb():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {TABLE_NAME}")
        conn.commit()


if __name__ == '__main__':
    cleardb()
