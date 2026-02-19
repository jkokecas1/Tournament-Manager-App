from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

    team = db.relationship('Team', backref='representatives', lazy=True)


class TournamentCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    tournaments = db.relationship('Tournament', backref='category_rel', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False) # Keep for compatibility
    category_id = db.Column(db.Integer, db.ForeignKey('tournament_category.id'), nullable=True)
    win_points = db.Column(db.Integer, default=3)
    draw_points = db.Column(db.Integer, default=1)
    loss_points = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    season = db.Column(db.String(50), nullable=True)
    teams = db.relationship('Team', backref='tournament', lazy=True, cascade="all, delete-orphan")
    matches = db.relationship('Match', backref='tournament', lazy=True, cascade="all, delete-orphan")

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(120), nullable=True) # Stores filename
    logo_data = db.Column(db.LargeBinary)
    logo_mimetype = db.Column(db.String(50))
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    players = db.relationship('Player', backref='team', lazy=True, cascade="all, delete-orphan")
    
    # Stats helpers (computed dynamically or could be cached columns)
    @property
    def stats(self):
        played = 0
        won = 0
        drawn = 0
        lost = 0
        gf = 0
        ga = 0
        
        # Home matches
        for m in Match.query.filter_by(home_team_id=self.id, played=True).all():
            played += 1
            gf += m.home_score
            ga += m.away_score
            if m.home_score > m.away_score: won += 1
            elif m.home_score == m.away_score: drawn += 1
            else: lost += 1
            
        # Away matches
        for m in Match.query.filter_by(away_team_id=self.id, played=True).all():
            played += 1
            gf += m.away_score
            ga += m.home_score
            if m.away_score > m.home_score: won += 1
            elif m.away_score == m.home_score: drawn += 1
            else: lost += 1
            
        points = (won * self.tournament.win_points) + (drawn * self.tournament.draw_points) + (lost * self.tournament.loss_points)
        gd = gf - ga
        
        return {
            "played": played, "won": won, "drawn": drawn, "lost": lost,
            "gf": gf, "ga": ga, "gd": gd, "points": points
        }

    def get_form(self, limit=5):
        # Fetch all matches for this team
        matches = Match.query.filter(
            db.or_(Match.home_team_id == self.id, Match.away_team_id == self.id),
            Match.played == True
        ).order_by(Match.matchday.desc()).limit(limit).all()
        
        form = []
        for m in matches:
            if m.home_team_id == self.id:
                if m.home_score > m.away_score: form.append('W')
                elif m.home_score == m.away_score: form.append('D')
                else: form.append('L')
            else: # Away
                if m.away_score > m.home_score: form.append('W')
                elif m.away_score == m.home_score: form.append('D')
                else: form.append('L')
        
        return form # Returns list like ['W', 'L', 'D'] (Most recent first)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, default=0)
    position = db.Column(db.String(50))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matchday = db.Column(db.Integer, nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    home_score = db.Column(db.Integer, default=0)
    away_score = db.Column(db.Integer, default=0)
    played = db.Column(db.Boolean, default=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False)
    referee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    
    events = db.relationship('MatchEvent', backref='match', lazy=True, cascade="all, delete-orphan")
    
    home_team = db.relationship('Team', foreign_keys=[home_team_id], backref='home_matches')
    away_team = db.relationship('Team', foreign_keys=[away_team_id], backref='away_matches')
    referee = db.relationship('User', foreign_keys=[referee_id], backref='refereed_matches')

class MatchEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False) # Denormalized for easier query
    minute = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False) # goal, yellow, red

class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Company / Site Settings
    company_name = db.Column(db.String(100), default="My Tournament Manager")
    company_logo = db.Column(db.String(120), nullable=True) 
    company_logo_data = db.Column(db.LargeBinary)
    company_logo_mimetype = db.Column(db.String(50))
    social_facebook = db.Column(db.String(200), nullable=True)
    social_twitter = db.Column(db.String(200), nullable=True)
    social_instagram = db.Column(db.String(200), nullable=True)
    default_language = db.Column(db.String(5), default='en')
    
    # Tournament specific? Or unused? Keeping for backward compat if needed but nullable
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

class PendingGoalAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    count = db.Column(db.Integer, default=3)
    assigned_count = db.Column(db.Integer, default=0)
    
    match = db.relationship('Match', backref='pending_goals')
    team = db.relationship('Team', backref='pending_goals')


class TournamentPrize(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False)
    rank = db.Column(db.String(50), nullable=False) # e.g., "1st Place", "Top Scorer"
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    reward_value = db.Column(db.String(100), nullable=True) # e.g., "$500", "Gold Trophy"

    tournament = db.relationship('Tournament', backref=db.backref('prizes', lazy=True, cascade="all, delete-orphan"))


class MarketingAsset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=True)
    type = db.Column(db.String(20), nullable=False) # 'image' or 'video'
    filename = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tournament = db.relationship('Tournament', backref=db.backref('marketing_assets', lazy=True, cascade="all, delete-orphan"))

