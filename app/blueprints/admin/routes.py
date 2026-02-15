from flask import render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User, Tournament, Team, Configuration
from app.utils.decorators import admin_required
from . import admin_bp
import os
from werkzeug.utils import secure_filename
from flask import current_app

@admin_bp.route('/admin')
@admin_required
def admin_panel():
    stats = {
        'user_count': User.query.count(),
        'tournament_count': Tournament.query.count(),
        'team_count': Team.query.count(),
        'match_count': Match.query.count() if 'Match' in globals() else 0 # Need to import Match
    }
    # Fix: need model imports
    from app.models import Match
    stats['match_count'] = Match.query.count()
    
    tournaments = Tournament.query.all()
    return render_template('admin.html', tournaments=tournaments, stats=stats)

@admin_bp.route('/admin/users', methods=['GET', 'POST'])
@admin_required
def manage_users():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        team_id = request.form.get('team_id')
        
        if team_id: team_id = int(team_id)
        else: team_id = None
        
        if username and password:
            existing = User.query.filter_by(username=username).first()
            if existing:
                flash("Username already taken.")
            else:
                user = User(username=username, password=password, role=role, team_id=team_id)
                db.session.add(user)
                db.session.commit()
                flash(f"User {username} created.")
        return redirect(url_for('admin.manage_users'))

    users = User.query.all()
    teams = Team.query.join(Tournament).order_by(Tournament.name, Team.name).all()
    return render_template('users.html', users=users, teams=teams)

@admin_bp.route('/admin/users/generate_reps', methods=['POST'])
@admin_required
def generate_reps():
    teams = Team.query.all()
    created_count = 0
    skipped_count = 0
    
    for team in teams:
        clean_name = "".join(c for c in team.name if c.isalnum()).lower()
        username = f"rep_{clean_name}"
        
        existing = User.query.filter_by(username=username).first()
        if not existing:
            new_user = User(
                username=username, 
                password="password123", 
                role='rep',
                team_id=team.id
            )
            db.session.add(new_user)
            created_count += 1
        else:
            skipped_count += 1
            
    db.session.commit()
    flash(f"Generated {created_count} representative users. Skipped {skipped_count} existing.")
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/admin/settings', methods=['POST'])
@admin_required
def update_settings():
    config = Configuration.query.first()
    if not config:
        config = Configuration()
        db.session.add(config)
    
    config.company_name = request.form.get('company_name')
    config.social_facebook = request.form.get('social_facebook')
    config.social_twitter = request.form.get('social_twitter')
    config.social_instagram = request.form.get('social_instagram')
    
    if 'company_logo' in request.files:
        file = request.files['company_logo']
        if file.filename != '':
            # Save to DB
            config.company_logo_data = file.read()
            config.company_logo_mimetype = file.mimetype
            config.company_logo = file.filename # Fallback
            
    db.session.commit()
    flash("Settings updated successfully.")
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/admin/company_logo')
def company_logo():
    config = Configuration.query.first()
    if config and config.company_logo_data:
        from io import BytesIO
        from flask import send_file
        return send_file(BytesIO(config.company_logo_data), mimetype=config.company_logo_mimetype)
    else:
        # Return default image or 404
        return redirect(url_for('static', filename='img/default_logo.png'))

@admin_bp.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'es']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))
