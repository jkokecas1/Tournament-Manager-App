from app import app, db
from app.models import Configuration
import sqlalchemy

def migrate():
    with app.app_context():
        # Create table if not exists
        engine = db.engine
        inspector = sqlalchemy.inspect(engine)
        if not inspector.has_table("configuration"):
            print("Creating configuration table...")
            db.create_all() # This creates all missing tables
            
            # Initialize default config
            if not Configuration.query.first():
                print("Initializing default configuration...")
                default_config = Configuration(company_name="Football Tournament Manager")
                db.session.add(default_config)
                db.session.commit()
                print("Default configuration created.")
        else:
            print("Configuration table already exists.")
            
if __name__ == "__main__":
    migrate()
