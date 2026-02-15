from app import app, db
from app.models import Team, Player
import random

def add_players():
    with app.app_context():
        teams = Team.query.all()
        positions = ['GK', 'DF', 'DF', 'DF', 'DF', 'MF', 'MF', 'MF', 'FW', 'FW', 'FW'] # 11 positions
        
        for team in teams:
            current_count = len(team.players)
            print(f"Team {team.name} has {current_count} players.")
            
            # Target: Add 10 players (or ensure 11?)
            # User said "add 10 players". Let's add 10 new ones.
            # Names will be realistic-ish or generic
            
            first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"]
            last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
            
            for i in range(10):
                # Unique-ish name
                name = f"{random.choice(first_names)} {random.choice(last_names)}"
                # Fallback if name exists? simpler to just append number if needed, but for now simple random is fine.
                # Actually, "Team Player X" is clearer for testing.
                
                # Check if number exists
                existing_numbers = [p.number for p in team.players]
                number = 1
                while number in existing_numbers:
                    number += 1
                    
                # Position
                pos = random.choice(['DP', 'MF', 'FW', 'GK'])
                
                player = Player(name=name, number=number, position=pos, team_id=team.id)
                db.session.add(player)
                
            print(f"Added 10 players to {team.name}")
        
        db.session.commit()
        print("Done!")

if __name__ == '__main__':
    add_players()
