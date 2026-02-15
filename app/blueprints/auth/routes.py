from flask import render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['role'] = user.role
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash("Invalid username or password.")
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
