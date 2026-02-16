from flask import render_template, request, session
from app import db
from app.models import User, Tournament, Team, Configuration
from . import main_bp

@main_bp.app_context_processor
def inject_context():
    user = None
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
    
    config = Configuration.query.first()
    return dict(current_user=user, site_config=config)

@main_bp.app_errorhandler(403)
def forbidden(e):
    return render_template('error_403.html'), 403

@main_bp.app_errorhandler(401)
def unauthorized(e):
    return render_template('error_401.html'), 401

@main_bp.route('/')
def index():
    search_query = request.args.get('q', '')
    show_history = request.args.get('history') == 'true'
    page = request.args.get('page', 1, type=int)
    per_page = 6
    
    query = Tournament.query
    
    if search_query:
        query = query.filter(Tournament.name.contains(search_query))
        
    if show_history:
        query = query.filter(Tournament.is_active == False)
    else:
        query = query.filter(Tournament.is_active == True)
        
    pagination = query.order_by(Tournament.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    tournaments = pagination.items
    
    return render_template('index.html', tournaments=tournaments, pagination=pagination, search_query=search_query, show_history=show_history)
    

