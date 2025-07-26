import sqlite3

DB_NAME = "mkulima_soko.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crop_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop TEXT NOT NULL,
            region TEXT NOT NULL,
            price INTEGER NOT NULL,
            category TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_price(crop, region, price, category):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO crop_prices (crop, region, price, category)
        VALUES (?, ?, ?, ?)
    """, (crop, region, price, category))
    conn.commit()
    conn.close()


def get_prices_by_crop_and_region(crop, region):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT price FROM crop_prices
        WHERE crop = ? AND region = ?
    """, (crop, region))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
