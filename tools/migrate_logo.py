import sqlite3

def migrate():
    try:
        conn = sqlite3.connect('fut.db')
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(team)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'logo' not in columns:
            print("Adding logo column to team table...")
            cursor.execute("ALTER TABLE team ADD COLUMN logo TEXT")
            conn.commit()
            print("Migration successful.")
        else:
            print("Column logo already exists.")
            
        conn.close()
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == '__main__':
    migrate()
