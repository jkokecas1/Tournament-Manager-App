import unittest
import os
from app import app, db
from app.models import User, Tournament, Team, Player, Match, MatchEvent

class TestDBMigration(unittest.TestCase):
    def setUp(self):
        # We try to use memory, but if it falls back to file, be safe
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        # Create Admin safely
        if not User.query.filter_by(username='admin').first():
            self.admin = User(username='admin', password='password', role='admin')
            db.session.add(self.admin)
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_full_flow(self):
        # 1. Create Tournament
        import time
        name = f"Champions Cup {time.time()}"
        t = Tournament(name=name, category="A")
        db.session.add(t)
        db.session.commit()
        self.assertIsNotNone(t.id)

        # 2. Add Teams
        t1 = Team(name="Team A", tournament=t)
        t2 = Team(name="Team B", tournament=t)
        db.session.add_all([t1, t2])
        db.session.commit()
        
        # 3. Add Players
        p1 = Player(name="Messi", number=10, position="FW", team=t1)
        db.session.add(p1)
        db.session.commit()

        # 4. Generate Schedule (Manual logic for test)
        match = Match(matchday=1, home_team=t1, away_team=t2, tournament=t)
        db.session.add(match)
        db.session.commit()

        # 5. Play Match
        match.home_score = 2
        match.away_score = 1
        match.played = True
        
        # 6. Add Event
        event = MatchEvent(match_id=match.id, player_id=p1.id, team_id=t1.id, minute=90, type="goal")
        db.session.add(event)
        db.session.commit()

        # Queries to verify
        saved_match = Match.query.filter_by(home_score=2).first()
        self.assertIsNotNone(saved_match)
        self.assertEqual(len(saved_match.events), 1)
        self.assertEqual(saved_match.events[0].type, "goal")
        
        # Check Team Stats property
        stats = t1.stats
        self.assertEqual(stats['points'], 3)
        self.assertEqual(stats['gf'], 2)

if __name__ == '__main__':
    unittest.main()
