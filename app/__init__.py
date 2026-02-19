import os
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

pass  # dummy pass to keep imports if needed, though usually not

basedir = os.path.abspath(os.path.dirname(__file__))

def get_locale():
    # 1. Check URL param (optional, usually handled by route but good for forcing)
    lang = request.args.get('lang')
    if lang in ['en', 'es']:
        return lang
    
    # 2. Check Session
    if 'lang' in session:
        return session['lang']
        
    # 3. Check Database Config (if available and not in session)
    # Note: Accessing DB here might be circular if not careful, 
    # but strictly speaking we are inside request context.
    # For simplicity, we skip DB here to avoid overhead on every request 
    # and rely on session being set from DB at login/start.
    
    # 4. Best Match - prioritize Spanish, fallback to Spanish if no match
    return request.accept_languages.best_match(['es', 'en']) or 'es'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'fut.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.secret_key = 'super_secret_key_for_demo'
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

db = SQLAlchemy(app)
babel = Babel(app, locale_selector=get_locale)

# Register Blueprints
from app.blueprints.main import main_bp
from app.blueprints.auth import auth_bp
from app.blueprints.admin import admin_bp
from app.blueprints.tournaments import tournaments_bp
from app.blueprints.teams import teams_bp
from app.blueprints.marketing import marketing_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(tournaments_bp)
app.register_blueprint(teams_bp)
app.register_blueprint(marketing_bp)

from app import models # Keep models import for DB initialization if needed
