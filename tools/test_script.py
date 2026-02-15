
from core import Tournament

def test_tournament():
    print("--- Starting Verification ---")
    t = Tournament("Test Cup")
    
    # 1. Add Teams
    teams = ["Team A", "Team B", "Team C", "Team D"]
    for name in teams:
        t.add_team(name)
    print(f"Added {len(t.teams)} teams.")

    # 2. Generate Schedule
    t.generate_schedule()
    matches = t.get_schedule()
    print(f"Generated {len(matches)} matches.")
    
    # Verify matchdays (4 teams -> 3 rounds * 2 matches/round = 6 matches)
    assert len(matches) == 6
    print("Match count correct.")

    # 3. Move Match
    m1 = matches[0]
    original_day = m1.matchday
    new_day = 10
    print(f"Moving Match {m1.id} from Day {original_day} to Day {new_day}...")
    t.move_match(m1.id, new_day)
    assert m1.matchday == new_day
    print("Match moved successfully.")

    # 4. Replace Team
    team_a = t.teams[0]
    print(f"Replacing {team_a.name} with 'Team Z'...")
    new_team = t.replace_team(team_a.id, "Team Z")
    
    # Verify in matches
    updated_count = 0
    for match in t.matches:
        if match.home_team.id == new_team.id or match.away_team.id == new_team.id:
            updated_count += 1
    
    # Team A played in 3 matches (one per round). All should be updated.
    print(f"Team Z found in {updated_count} matches.")
    assert updated_count == 3
    print("Team replacement verified.")

    print("\n--- Verification Complete & Successful ---")

if __name__ == "__main__":
    test_tournament()
