from app import app, db
import sqlalchemy

def migrate():
    with app.app_context():
        # Add default_language column
        with db.engine.connect() as conn:
            try:
                conn.execute(sqlalchemy.text("ALTER TABLE configuration ADD COLUMN default_language VARCHAR(5) DEFAULT 'en'"))
                print("Added default_language column.")
            except Exception as e:
                print(f"Column might already exist: {e}")

if __name__ == "__main__":
    migrate()
