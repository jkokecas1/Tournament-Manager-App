import sqlite3

def migrate():
    try:
        conn = sqlite3.connect('fut.db')
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(match)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'referee_id' not in columns:
            print("Adding referee_id column to match table...")
            cursor.execute("ALTER TABLE match ADD COLUMN referee_id INTEGER REFERENCES user(id)")
            conn.commit()
            print("Migration successful.")
        else:
            print("Column referee_id already exists.")
            
        conn.close()
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == '__main__':
    migrate()
