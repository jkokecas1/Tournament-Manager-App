import unittest
import os
import json
from app.models import Tournament, Team, Match
from app import app

class TestTournament(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_data.json"
        self.tournament = Tournament("Test Tournament", data_file=self.test_file)
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_team_persistence(self):
        self.tournament.add_team("Team A")
        self.tournament.add_team("Team B")
        
        # Reload
        new_tournament = Tournament("Test Tournament", data_file=self.test_file)
        self.assertEqual(len(new_tournament.teams), 2)
        self.assertEqual(new_tournament.teams[0].name, "Team A")

    def test_generate_schedule(self):
        self.tournament.add_team("Team A")
        self.tournament.add_team("Team B")
        success, msg = self.tournament.generate_schedule()
        self.assertTrue(success)
        self.assertEqual(len(self.tournament.matches), 2) # 2 rounds? No, 2 teams -> 1 round -> 1 match. 
        # Wait, my logic: num_teams=2. rounds=1. matches_per_round=1. loops 1 time. 
        # range(1) -> matchday 1. 
        # match added.
        # len(matches) should be 1.
        self.assertEqual(len(self.tournament.matches), 1)

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
