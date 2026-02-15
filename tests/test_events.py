import unittest
import os
import json
from app.models import System, Tournament, Team, MatchEvent

class TestMatchEvents(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_events.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.system = System(data_file=self.test_file)
        
        # Setup basic data
        self.t = self.system.create_tournament("Cup", "A")
        self.t.add_team("Home")
        self.t.add_team("Away")
        self.t.add_player(self.t.teams[0].id, "P1", 1, "F")
        self.t.generate_schedule()

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_match_event(self):
        match = self.t.matches[0]
        player_id = self.t.teams[0].players[0].id
        team_id = self.t.teams[0].id
        
        # Add Goal
        event = MatchEvent(player_id, team_id, 10, "goal")
        match.events.append(event)
        
        # Add Yellow
        event2 = MatchEvent(player_id, team_id, 45, "yellow")
        match.events.append(event2)
        
        self.assertEqual(len(match.events), 2)
        
        # Save and Reload
        self.system.save_data()
        new_sys = System(data_file=self.test_file)
        loaded_match = new_sys.tournaments[0].matches[0]
        
        self.assertEqual(len(loaded_match.events), 2)
        self.assertEqual(loaded_match.events[0].type, "goal")

if __name__ == '__main__':
    unittest.main()
