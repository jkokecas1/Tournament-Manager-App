"""
Authorization decorators for route protection
"""
from functools import wraps
from flask import session, redirect, url_for, abort, flash
from flask_babel import gettext as _

def login_required(f):
    """
    Decorator to require user to be logged in
    Redirects to login page if not authenticated
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash(_('Please log in to access this page.'), 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to require admin role
    Returns 403 if user is not admin
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash(_('Please log in to access this page.'), 'warning')
            return redirect(url_for('login'))
        
        if session.get('role') != 'admin':
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def referee_required(f):
    """
    Decorator to require referee role
    Returns 403 if user is not referee
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash(_('Please log in to access this page.'), 'warning')
            return redirect(url_for('login'))
        
        if session.get('role') != 'referee':
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def rep_required(f):
    """
    Decorator to require representative role
    Returns 403 if user is not representative
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash(_('Please log in to access this page.'), 'warning')
            return redirect(url_for('login'))
        
        if session.get('role') != 'rep':
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def admin_or_rep_required(f):
    """
    Decorator to require admin OR representative role
    Returns 403 if user is neither admin nor representative
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash(_('Please log in to access this page.'), 'warning')
            return redirect(url_for('login'))
        
        role = session.get('role')
        if role not in ['admin', 'rep']:
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def admin_or_referee_required(f):
    """
    Decorator to require admin OR referee role
    Returns 403 if user is neither admin nor referee
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash(_('Please log in to access this page.'), 'warning')
            return redirect(url_for('login'))
        
        role = session.get('role')
        if role not in ['admin', 'referee']:
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function
