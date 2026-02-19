import sqlite3
import os

db_path = 'fut.db'

if not os.path.exists(db_path):
    print(f"Error: Database {db_path} not found.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Checking schema...")
cursor.execute("PRAGMA table_info(match)")
columns = [info[1] for info in cursor.fetchall()]

try:
    if 'start_time' not in columns:
        print("Adding start_time column...")
        cursor.execute("ALTER TABLE match ADD COLUMN start_time TIME")
    else:
        print("start_time column already exists.")

    if 'end_time' not in columns:
        print("Adding end_time column...")
        cursor.execute("ALTER TABLE match ADD COLUMN end_time TIME")
    else:
        print("end_time column already exists.")

    # New updates for Tournament Categories
    print("Creating tournament_category table if not exists...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tournament_category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL UNIQUE
        )
    """)

    cursor.execute("PRAGMA table_info(tournament)")
    t_columns = [info[1] for info in cursor.fetchall()]

    if 'category_id' not in t_columns:
        print("Adding category_id column to tournament...")
        cursor.execute("ALTER TABLE tournament ADD COLUMN category_id INTEGER REFERENCES tournament_category(id)")
    else:
        print("category_id column already exists in tournament.")

    # Marketing & Prizes Updates
    print("Creating tournament_prize table if not exists...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tournament_prize (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER NOT NULL REFERENCES tournament(id),
            rank VARCHAR(50) NOT NULL,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            reward_value VARCHAR(100)
        )
    """)

    print("Creating marketing_asset table if not exists...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marketing_asset (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER REFERENCES tournament(id),
            type VARCHAR(20) NOT NULL,
            filename VARCHAR(200) NOT NULL,
            title VARCHAR(100),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    print("Database updated successfully.")
except Exception as e:
    print(f"Error updating database: {e}")
finally:
    conn.close()
