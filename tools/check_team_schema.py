import sqlite3
import os

def check_team_schema():
    # Target the root database
    db_path = os.path.join(os.getcwd(), 'fut.db')
    print(f"Checking database at: {db_path}")
    
    if not os.path.exists(db_path):
        print("Database not found!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("Checking Team table...")
        cursor.execute("PRAGMA table_info(team)")
        columns = [info[1] for info in cursor.fetchall()]
        print(f"Current Team columns: {columns}")
        
        new_columns = {
            'logo_data': 'BLOB',
            'logo_mimetype': 'TEXT',
            'is_active': 'BOOLEAN DEFAULT 1'
        }
        
        for col, definition in new_columns.items():
            if col not in columns:
                print(f"Adding missing column to Team: {col}")
                try:
                    cursor.execute(f"ALTER TABLE team ADD COLUMN {col} {definition}")
                except Exception as e:
                    print(f"Error adding {col}: {e}")
            else:
                print(f"Column {col} already exists in Team.")

        conn.commit()
        print("Team schema check/update completed.")

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    check_team_schema()
