from app import app, db
from app.models import User, Tournament, Team, Player, Match, MatchEvent, Configuration

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created.")
        
        # specific seeding if needed (e.g. default config)
        if not Configuration.query.first():
            print("Creating default configuration...")
            default_config = Configuration(company_name="My Tournament Manager")
            db.session.add(default_config)
            db.session.commit()
            print("Default configuration added.")
            
        print("Initialization complete.")

if __name__ == "__main__":
    init_db()
