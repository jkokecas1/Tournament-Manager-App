import unittest
import os
import json
from app.models import System, Tournament, Team, Player

class TestPhase2(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_phase2.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.system = System(data_file=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_full_flow(self):
        # 1. Create Tournament
        t = self.system.create_tournament("Summer Cup", "U-18")
        self.assertEqual(t.name, "Summer Cup")
        self.assertEqual(len(self.system.tournaments), 1)

        # 2. Add Teams
        t.add_team("Lions")
        t.add_team("Tigers")
        self.assertEqual(len(t.teams), 2)

        # 3. Add Players
        p1 = t.add_player(t.teams[0].id, "Leo", 10, "FW")
        self.assertIsNotNone(p1)
        self.assertEqual(p1.name, "Leo")
        self.assertEqual(len(t.teams[0].players), 1)

        # 4. Generate Schedule
        t.generate_schedule()
        self.assertEqual(len(t.matches), 1) # 2 teams = 1 match

        # 5. Play Match
        match = t.matches[0]
        match.home_score = 2
        match.away_score = 1
        match.played = True
        
        # 6. Check Standings
        standings = t.get_standings()
        # Winner (Lions/Home) should be first
        self.assertEqual(standings[0].name, "Lions")
        self.assertEqual(standings[0].points, 3)
        self.assertEqual(standings[0].won, 1)
        
        # Loser (Tigers/Away) should be second
        self.assertEqual(standings[1].name, "Tigers")
        self.assertEqual(standings[1].points, 0)
        
        # 7. Persistence
        self.system.save_data()
        new_system = System(data_file=self.test_file)
        t_loaded = new_system.tournaments[0]
        self.assertEqual(len(t_loaded.teams), 2)
        self.assertEqual(t_loaded.teams[0].players[0].name, "Leo")
        self.assertTrue(t_loaded.matches[0].played)

if __name__ == '__main__':
    unittest.main()
