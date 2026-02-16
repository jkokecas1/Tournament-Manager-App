import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fut.db')

def migrate():
    print(f"Connecting to database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check and add is_active column
        try:
            cursor.execute("SELECT is_active FROM tournament LIMIT 1")
            print("Column 'is_active' already exists in 'tournament'.")
        except sqlite3.OperationalError:
            print("Adding 'is_active' column to 'tournament'...")
            cursor.execute("ALTER TABLE tournament ADD COLUMN is_active BOOLEAN DEFAULT 1")
            print("Column 'is_active' added.")

        # Check and add season column
        try:
            cursor.execute("SELECT season FROM tournament LIMIT 1")
            print("Column 'season' already exists in 'tournament'.")
        except sqlite3.OperationalError:
            print("Adding 'season' column to 'tournament'...")
            cursor.execute("ALTER TABLE tournament ADD COLUMN season TEXT")
            print("Column 'season' added.")

        conn.commit()
        print("Migration complete.")
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
