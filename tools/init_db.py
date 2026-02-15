from app import app, db
from app.models import User, Tournament, Team

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password='admin', role='admin')
        db.session.add(admin)
        db.session.commit()
        print("Database initialized and admin created.")
    else:
        print("Database already initialized.")

    # Create Premier League if not exists
    pl = Tournament.query.filter_by(name="Premier League").first()
    if not pl:
        print("Creating Premier League...")
        pl = Tournament(name="Premier League", category="Pro", win_points=3, draw_points=1, loss_points=0)
        db.session.add(pl)
        db.session.commit()
    
    # Add Teams if empty
    if not pl.teams:
        print("Adding Premier League Teams...")
        teams = [
            "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton",
            "Chelsea", "Crystal Palace", "Everton", "Fulham", "Ipswich Town",
            "Leicester City", "Liverpool", "Man City", "Man Utd", "Newcastle",
            "Nottm Forest", "Southampton", "Tottenham", "West Ham", "Wolves"
        ]
        for name in teams:
            t = Team(name=name, tournament=pl)
            db.session.add(t)
        db.session.commit()
        print("Premier League Teams Added.")

