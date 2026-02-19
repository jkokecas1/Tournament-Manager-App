from flask import render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User, Tournament, Team, Player, Match, MatchEvent, PendingGoalAssignment, TournamentCategory
from app.utils.decorators import admin_required, admin_or_rep_required, admin_or_referee_required, login_required
from . import tournaments_bp
import os
from werkzeug.utils import secure_filename
from flask import current_app
from app.utils.image_utils import resize_image

@tournaments_bp.route('/create_tournament', methods=['POST'])
@admin_required
def create_tournament():
    name = request.form.get('name')
    category_name = request.form.get('category') # Legacy or custom
    category_id = request.form.get('category_id') # From selector
    win = int(request.form.get('win_points', 3))
    draw = int(request.form.get('draw_points', 1))
    loss = int(request.form.get('loss_points', 0))
    
    if name:
        t = Tournament(name=name, win_points=win, draw_points=draw, loss_points=loss)
        if category_id:
            t.category_id = int(category_id)
            cat = db.session.get(TournamentCategory, category_id)
            t.category = cat.name if cat else "General"
        else:
            t.category = category_name or "General"
            
        db.session.add(t)
        db.session.commit()
    return redirect(url_for('tournaments.tournaments_management'))

@tournaments_bp.route('/t/<int:t_id>/archive', methods=['POST'])
@admin_required
def archive_tournament(t_id):
    t = db.session.get(Tournament, t_id)
    if not t: return redirect(url_for('main.index'))
    
    # 1. Mark current as inactive
    t.is_active = False
    
    # 2. Check if we want to create a new season
    create_new = request.form.get('create_new_season') == 'yes'
    
    if create_new:
        new_season_name = request.form.get('new_season_name')
        # Create new tournament
        new_t = Tournament(
            name=t.name, 
            category=t.category,
            win_points=t.win_points,
            draw_points=t.draw_points,
            loss_points=t.loss_points,
            season=new_season_name,
            is_active=True
        )
        db.session.add(new_t)
        db.session.flush() # Get ID for new_t
        
        # Clone teams
        for team in t.teams:
            # Only active teams? Or all? Let's clone all for history sake or just active.
            # Assuming we clone all.
            new_team = Team(
                name=team.name,
                logo=team.logo,
                logo_data=team.logo_data,
                logo_mimetype=team.logo_mimetype,
                tournament_id=new_t.id,
                is_active=True # Reset to active in new season
            )
            db.session.add(new_team)
            
            # Clone players? Usually yes.
            for player in team.players:
                new_player = Player(
                    name=player.name,
                    number=player.number,
                    position=player.position,
                    team=new_team # Link to new team object (SQLAlchemy handles ID)
                )
                db.session.add(new_player)
                
        db.session.commit()
        flash(f"Tournament archived. New season '{new_season_name}' created!")
        return redirect(url_for('tournaments.tournament_dashboard', t_id=new_t.id))
        
    db.session.commit()
    flash("Tournament archived.")
    return redirect(url_for('main.index'))

@tournaments_bp.route('/t/<int:t_id>/')
def tournament_dashboard(t_id):
    t = db.session.get(Tournament, t_id)
    if not t: return redirect(url_for('main.index'))
    return render_template('tournament_dashboard.html', t=t)

@tournaments_bp.route('/t/<int:t_id>/teams')
def tournament_teams(t_id):
    t = db.session.get(Tournament, t_id)
    if not t: return redirect(url_for('main.index'))
    return render_template('teams.html', t=t)

@tournaments_bp.route('/t/<int:t_id>/team/<int:team_id>/delete', methods=['POST'])
@admin_required
def delete_team(t_id, team_id):
    team = db.session.get(Team, team_id)
    if not team:
        flash("Team not found.")
        return redirect(url_for('tournaments.tournament_teams', t_id=t_id))
        
    # Check for matches
    match_count = Match.query.filter(
        (Match.home_team_id == team_id) | (Match.away_team_id == team_id)
    ).count()
    
    if match_count > 0:
        flash(f"Cannot delete team: It has {match_count} scheduled or played matches. Remove matches first or withdraw the team.")
        return redirect(url_for('tournaments.tournament_teams', t_id=t_id))
        
    try:
        db.session.delete(team)
        db.session.commit()
        flash("Team deleted successfully.")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting team: {e}")
        
    return redirect(url_for('tournaments.tournament_teams', t_id=t_id))

@tournaments_bp.route('/t/<int:t_id>/simulate_season', methods=['POST'])
@admin_required
def simulate_season(t_id):
    import random
    
    t = db.session.get(Tournament, t_id)
    if not t:
        flash("Tournament not found.")
        return redirect(url_for('main.index'))
    
    # Get all unplayed matches
    matches = Match.query.filter_by(tournament_id=t_id, played=False).all()
    
    if not matches:
        flash("No unplayed matches to simulate.")
        return redirect(url_for('tournaments.tournament_dashboard', t_id=t_id))
    
    # Simulate each match with random scores
    for match in matches:
        match.home_score = random.randint(0, 5)
        match.away_score = random.randint(0, 5)
        match.played = True
    
    db.session.commit()
    flash(f"Season simulated! {len(matches)} matches completed with random scores.")
    return redirect(url_for('tournaments.tournament_dashboard', t_id=t_id))


@tournaments_bp.route('/t/<int:t_id>/match/<int:match_id>/walkover', methods=['POST'])
@admin_required
def mark_walkover(t_id, match_id):
    match = db.session.get(Match, match_id)
    if not match or match.tournament_id != t_id:
        flash("Match not found.")
        return redirect(url_for('tournaments.tournament_schedule', t_id=t_id))
    
    if match.played:
        flash("Cannot mark played match as walkover.")
        return redirect(url_for('tournaments.tournament_schedule', t_id=t_id))
    
    # Get winning team from form (home or away)
    winner = request.form.get('winner')  # 'home' or 'away'
    
    if winner == 'home':
        match.home_score = 3
        match.away_score = 0
        winning_team_id = match.home_team_id
    elif winner == 'away':
        match.home_score = 0
        match.away_score = 3
        winning_team_id = match.away_team_id
    else:
        flash("Invalid winner selection.")
        return redirect(url_for('tournaments.tournament_schedule', t_id=t_id))
    
    match.played = True
    db.session.commit()
    
    flash(f"Match marked as walkover (3-0). Assign goals to players if needed.")
    return redirect(url_for('tournaments.tournament_schedule', t_id=t_id))




@tournaments_bp.route('/upload_logo', methods=['POST'])
@admin_or_rep_required
def upload_logo():
    team_id = request.form.get('team_id')
    t_id = request.form.get('t_id')
    
    if not team_id or not t_id:
        flash("Missing ID parameters.")
        return redirect(url_for('main.index'))
        
    team_id = int(team_id)
    t_id = int(t_id)

    user = db.session.get(User, session['user_id'])
    
    if user.role != 'admin':
         if user.role != 'rep' or user.team_id != team_id:
             flash("Permission denied")
             return redirect(url_for('tournaments.tournament_teams', t_id=t_id))
             
    if 'logo' not in request.files:
        flash("No file part")
        return redirect(url_for('tournaments.tournament_teams', t_id=t_id))
        
    file = request.files['logo']
    if file.filename == '':
        flash("No selected file")
        return redirect(url_for('tournaments.tournament_teams', t_id=t_id))
        
    if file:
        try:
            # Resize image to 25x25
            file_data, mimetype = resize_image(file, size=(25, 25))
            
            if not file_data:
                flash("Empty file uploaded")
                return redirect(url_for('tournaments.tournament_teams', t_id=t_id))

            team = db.session.get(Team, team_id)
            if team:
                team.logo_data = file_data
                team.logo_mimetype = mimetype
                team.logo = secure_filename(file.filename) # Keep filename as fallback/reference
                db.session.commit()
                flash("Logo uploaded successfully (resized to 25x25)!")
            else:
                flash("Team not found")
        except Exception as e:
            flash(f"Error uploading logo: {str(e)}")
            db.session.rollback()
        
    return redirect(url_for('tournaments.tournament_teams', t_id=t_id))

@tournaments_bp.route('/t/<int:t_id>/team/<int:team_id>/logo')
def team_logo(t_id, team_id):
    team = db.session.get(Team, team_id)
    if team and team.logo_data:
        from io import BytesIO
        from flask import send_file
        return send_file(BytesIO(team.logo_data), mimetype=team.logo_mimetype)
    else:
        # Return default image or 404
        return redirect(url_for('static', filename='img/default_team.png'))

@tournaments_bp.route('/t/<int:t_id>/team/<int:team_id>/withdraw', methods=['POST'])
@admin_required
def withdraw_team(t_id, team_id):
    team = db.session.get(Team, team_id)
    if not team:
        flash("Team not found.")
        return redirect(url_for('tournaments.tournament_teams', t_id=t_id))
    
    team.is_active = False
    
    # Update all matches involving this team
    matches = Match.query.filter(
        db.and_(Match.tournament_id == t_id, 
                db.or_(Match.home_team_id == team_id, Match.away_team_id == team_id))
    ).all()
    
    from app.models import PendingGoalAssignment
    
    for m in matches:
        # Determine opponent
        if m.home_team_id == team_id:
            opponent_id = m.away_team_id
            m.home_score = 0
            m.away_score = 3
        else:
            opponent_id = m.home_team_id
            m.home_score = 3
            m.away_score = 0
            
        m.played = True
        
        # Create pending goal assignment for opponent
        pending = PendingGoalAssignment(
            match_id=m.id,
            team_id=opponent_id,
            count=3,
            assigned_count=0
        )
        db.session.add(pending)
        
    db.session.commit()
    flash(f"Team {team.name} has been withdrawn. All matches set to 3-0.")
    return redirect(url_for('tournaments.tournament_teams', t_id=t_id))

@tournaments_bp.route('/t/<int:t_id>/add_team', methods=['POST'])
@admin_or_rep_required
def add_team(t_id):
    t = db.session.get(Tournament, t_id)
    if t:
        name = request.form.get('name')
        if name:
            team = Team(name=name, tournament=t)
            db.session.add(team)
            db.session.commit()
    return redirect(url_for('tournaments.tournament_teams', t_id=t_id))

@tournaments_bp.route('/t/<int:t_id>/add_player', methods=['POST'])
@admin_or_rep_required
def add_player(t_id):
    user = db.session.get(User, session['user_id'])
    team_id = int(request.form.get('team_id'))
    
    if user.role != 'admin':
        if user.role != 'rep' or user.team_id != team_id:
             flash("You can only add players to your own team.")
             return redirect(url_for('tournaments.tournament_teams', t_id=t_id))

    t = db.session.get(Tournament, t_id)
    if t:
        name = request.form.get('name')
        number = int(request.form.get('number') or 0)
        position = request.form.get('position')
        
        player = Player(name=name, number=number, position=position, team_id=team_id)
        db.session.add(player)
        db.session.commit()
    return redirect(url_for('tournaments.tournament_teams', t_id=t_id))

@tournaments_bp.route('/t/<int:t_id>/schedule')
def tournament_schedule(t_id):
    t = db.session.get(Tournament, t_id)
    if not t: return redirect(url_for('main.index'))
    
    query = Match.query.filter_by(tournament_id=t_id)
    all_md_query = Match.query.with_entities(Match.matchday).filter_by(tournament_id=t_id).distinct().order_by(Match.matchday).all()
    matchdays = [m.matchday for m in all_md_query]
    
    min_matchday = min(matchdays) if matchdays else 1
    max_matchday = max(matchdays) if matchdays else 1

    matchday_filter = request.args.get('matchday')
    if matchday_filter is None:
        # Default to min_matchday on first load
        matchday_filter = min_matchday
        query = query.filter_by(matchday=matchday_filter)
    elif matchday_filter.isdigit():
        matchday_filter = int(matchday_filter)
        query = query.filter_by(matchday=matchday_filter)
    else:
        # User explicitly selected "All Matchdays" (empty string)
        matchday_filter = None
        
    team_filter = request.args.get('team_id')
    if team_filter and team_filter.isdigit():
        team_id = int(team_filter)
        query = query.filter(db.or_(Match.home_team_id == team_id, Match.away_team_id == team_id))

    matches = query.order_by(Match.matchday).all()
    
    return render_template('schedule.html', t=t, matches=matches, matchdays=matchdays, teams=t.teams, 
                           selected_matchday=matchday_filter, selected_team=team_filter,
                           min_matchday=min_matchday, max_matchday=max_matchday)

@tournaments_bp.route('/t/<int:t_id>/generate_schedule', methods=['POST'])
@admin_or_rep_required
def generate_schedule(t_id):
    t = db.session.get(Tournament, t_id)
    if not t: return redirect(url_for('main.index'))
    
    Match.query.filter_by(tournament_id=t_id).delete()
    
    teams = t.teams
    team_ids = [team.id for team in teams]
    if len(team_ids) % 2 != 0:
        team_ids.append(None) # Bye
    
    n = len(team_ids)
    rounds = n - 1
    half = n // 2
    
    for r in range(rounds):
        for i in range(half):
            t1 = team_ids[i]
            t2 = team_ids[n - 1 - i]
            
            if t1 is not None and t2 is not None:
                match = Match(matchday=r+1, home_team_id=t1, away_team_id=t2, tournament_id=t.id)
                db.session.add(match)
        
        team_ids.insert(1, team_ids.pop())

    db.session.commit()
    return redirect(url_for('tournaments.tournament_schedule', t_id=t_id))

@tournaments_bp.route('/t/<int:t_id>/match/<int:m_id>', methods=['GET', 'POST'])
@login_required
def match_detail(t_id, m_id):
    t = db.session.get(Tournament, t_id)
    if not t: return redirect(url_for('main.index'))
    match = db.session.get(Match, m_id)
    if not match: return redirect(url_for('tournaments.tournament_schedule', t_id=t_id))

    home_team = match.home_team
    away_team = match.away_team
    player_map = {p.id: p for team in t.teams for p in team.players} 
    referees = User.query.filter_by(role='referee').all()

    if request.method == 'POST':
        user = db.session.get(User, session.get('user_id'))
        if not user: return redirect(url_for('auth.login'))

        if user.role == 'admin' and 'referee_id' in request.form:
            try:
                ref_id = request.form.get('referee_id')
                match.referee_id = int(ref_id) if ref_id else None
                
                # Update times if provided by admin
                from datetime import datetime
                start_time_str = request.form.get('start_time')
                end_time_str = request.form.get('end_time')
                
                if start_time_str:
                    match.start_time = datetime.strptime(start_time_str, '%H:%M').time()
                else:
                    match.start_time = None
                    
                if end_time_str:
                    match.end_time = datetime.strptime(end_time_str, '%H:%M').time()
                else:
                    match.end_time = None
                
                db.session.commit()
                flash("Match updated.")
            except (ValueError, TypeError):
                flash("Invalid time format.")
                pass

        if user.role == 'admin' or user.role == 'referee':
            if 'home_score' in request.form: 
                try:
                    home_score = int(request.form.get('home_score'))
                    away_score = int(request.form.get('away_score'))
                    match.home_score = home_score
                    match.away_score = away_score
                    match.played = True
                    db.session.commit()
                except ValueError:
                    pass
        
        return redirect(url_for('tournaments.match_detail', t_id=t.id, m_id=m_id))

    return render_template('match_detail.html', t=t, match=match, home_team=home_team, away_team=away_team, players=player_map, referees=referees)

@tournaments_bp.route('/t/<int:t_id>/match/<int:m_id>/event', methods=['POST'])
@admin_or_referee_required
def add_match_event(t_id, m_id):
    user = db.session.get(User, session['user_id'])
    if user.role != 'admin' and user.role != 'referee':
        flash("Only referees and admins can add events.")
        return redirect(url_for('tournaments.match_detail', t_id=t_id, m_id=m_id))
    
    try:
        player_id = int(request.form.get('player_id'))
        team_id = int(request.form.get('team_id'))
        minute = int(request.form.get('minute'))
        event_type = request.form.get('type')
        
        event = MatchEvent(match_id=m_id, player_id=player_id, team_id=team_id, minute=minute, type=event_type)
        db.session.add(event)
        db.session.commit()
    except (ValueError, TypeError):
        pass
    return redirect(url_for('tournaments.match_detail', t_id=t_id, m_id=m_id))

@tournaments_bp.route('/t/<int:t_id>/standings')
def tournament_standings(t_id):
    t = db.session.get(Tournament, t_id)
    if not t: return redirect(url_for('main.index'))
    
    teams_stats = []
    for team in t.teams:
        s = team.stats
        s['team'] = team
        s['name'] = team.name 
        s['form'] = team.get_form()
        teams_stats.append(s)
        
    teams_stats.sort(key=lambda x: (x['points'], x['gd'], x['gf']), reverse=True)
    return render_template('standings.html', t=t, standings=teams_stats)

@tournaments_bp.route('/t/<int:t_id>/metrics')
def tournament_metrics(t_id):
    t = db.session.get(Tournament, t_id)
    if not t: return redirect(url_for('main.index'))
    
    teams_stats = []
    for team in t.teams:
        s = team.stats
        s['team'] = team
        teams_stats.append(s)
        
    if not teams_stats:
        return render_template('metrics.html', t=t, error="No data available")

    most_wins = sorted(teams_stats, key=lambda x: x['won'], reverse=True)[:3]
    best_attack = sorted(teams_stats, key=lambda x: x['gf'], reverse=True)[:3]
    most_conceded = sorted(teams_stats, key=lambda x: x['ga'], reverse=True)[:3]
    
    top_scorers = db.session.query(
        Player.name, Team.name, db.func.count(MatchEvent.id).label('goals')
    ).join(Team, Team.id == Player.team_id)\
     .join(MatchEvent, MatchEvent.player_id == Player.id)\
     .join(Match, Match.id == MatchEvent.match_id).filter(
        Match.tournament_id == t_id,
        MatchEvent.type == 'goal'
    ).group_by(Player.id).order_by(db.desc('goals')).limit(10).all()

    single_match_record = db.session.query(
        Player.name, Team.name, Match.matchday, db.func.count(MatchEvent.id).label('goals')
    ).join(Team, Team.id == Player.team_id)\
     .join(MatchEvent, MatchEvent.player_id == Player.id)\
     .join(Match, Match.id == MatchEvent.match_id).filter(
        Match.tournament_id == t_id,
        MatchEvent.type == 'goal'
    ).group_by(Match.id, Player.id).order_by(db.desc('goals')).limit(5).all()

    team_cards = db.session.query(
        Team.name, db.func.count(MatchEvent.id).label('cards')
    ).join(MatchEvent, MatchEvent.team_id == Team.id)\
     .join(Match, Match.id == MatchEvent.match_id).filter(
        Match.tournament_id == t_id,
        MatchEvent.type.in_(['yellow', 'red'])
    ).group_by(Team.id).order_by('cards').limit(5).all()

    return render_template('metrics.html', t=t, 
                           most_wins=most_wins, 
                           best_attack=best_attack, 
                           most_conceded=most_conceded,
                           top_scorers=top_scorers,
                           single_match_record=single_match_record,
                           team_cards=team_cards)

@tournaments_bp.route('/pending_goals')
@tournaments_bp.route('/tournament/<int:t_id>/pending_goals')
@login_required
def pending_goals(t_id=None):
    user = db.session.get(User, session['user_id'])
    if user.role != 'admin' and not (user.role == 'rep' and user.team_id):
        flash("Access denied.")
        return redirect(url_for('main.index'))
    
    query = PendingGoalAssignment.query.filter(PendingGoalAssignment.assigned_count < PendingGoalAssignment.count)
    
    current_tournament = None
    if t_id:
        current_tournament = db.session.get(Tournament, t_id)
        if not current_tournament:
            t_id = None

    if user.role == 'rep':
        query = query.filter_by(team_id=user.team_id)

    all_pending = query.all()
    
    # Use application-level filter for tournament context to ensure consistency with sidebar badges
    if t_id:
        pending = [p for p in all_pending if p.match.tournament_id == t_id]
    else:
        pending = all_pending
    return render_template('pending_goals.html', pending=pending, t=current_tournament)

    return render_template('pending_goals.html', pending=pending, t=current_tournament)

@tournaments_bp.route('/assign_goal', methods=['POST'])
@login_required
def assign_goal():
    user = db.session.get(User, session['user_id'])
    pending_id = int(request.form.get('pending_id'))
    player_id = int(request.form.get('player_id'))
    
    from app.models import PendingGoalAssignment, Player, MatchEvent
    pending = db.session.get(PendingGoalAssignment, pending_id)
    
    if not pending:
        flash("Assignment not found.")
        return redirect(url_for('tournaments.pending_goals'))
    
    if user.role != 'admin' and (user.role != 'rep' or user.team_id != pending.team_id):
        flash("Permission denied.")
        return redirect(url_for('tournaments.pending_goals'))
    
    if pending.assigned_count < pending.count:
        event = MatchEvent(
            match_id=pending.match_id,
            player_id=player_id,
            team_id=pending.team_id,
            minute=0, # Auto-assigned goals have no specific minute
            type='goal'
        )
        db.session.add(event)
        pending.assigned_count += 1
        db.session.commit()
        flash("Goal assigned successfully.")
    t_id = request.form.get('t_id')
    return redirect(url_for('tournaments.pending_goals', t_id=t_id))

@tournaments_bp.route('/t/<int:t_id>/match/<int:m_id>/change_matchday', methods=['POST'])
@admin_required
def change_matchday(t_id, m_id):
    match = db.session.get(Match, m_id)
    
    if not match:
        flash("Match not found.")
        return redirect(url_for('tournaments.tournament_schedule', t_id=t_id))
    
    # Validate match belongs to tournament
    if match.tournament_id != t_id:
        flash("Invalid match.")
        return redirect(url_for('tournaments.tournament_schedule', t_id=t_id))
    
    # Don't allow changing played matches
    if match.played:
        flash("Cannot reschedule a match that has already been played.")
        return redirect(url_for('tournaments.tournament_schedule', t_id=t_id))
    
    new_matchday = request.form.get('new_matchday', type=int)
    
    if new_matchday and new_matchday > 0:
        old_matchday = match.matchday
        
        # SMART SWAP: Find matches in the destination matchday involving these teams
        conflicting_matches = Match.query.filter(
            Match.tournament_id == t_id,
            Match.matchday == new_matchday,
            (Match.home_team_id.in_([match.home_team_id, match.away_team_id])) |
            (Match.away_team_id.in_([match.home_team_id, match.away_team_id]))
        ).all()
        
        swapped_count = 0
        # Move conflicting matches to the old matchday
        for conflict in conflicting_matches:
            if not conflict.played and conflict.id != match.id:
                conflict.matchday = old_matchday
                swapped_count += 1
        
        # Move the requested match to the new matchday
        match.matchday = new_matchday
        db.session.commit()
        
        if swapped_count > 0:
            flash(f"Match rescheduled to Matchday {new_matchday}. {swapped_count} conflicting matches moved to Matchday {old_matchday}.")
        else:
            flash(f"Match rescheduled to Matchday {new_matchday} successfully.")
    else:
        flash("Invalid matchday number.")
    
    return redirect(url_for('tournaments.tournament_schedule', t_id=t_id))
