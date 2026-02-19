from flask import render_template, request, redirect, url_for, flash, session, current_app
from app.blueprints.teams import teams_bp
from app.models import Team, Player, User
from app import db
from app.utils.decorators import admin_or_rep_required
from app.utils.image_utils import resize_image
from werkzeug.utils import secure_filename
import os

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return db.session.get(User, user_id)
    return None

@teams_bp.route('/my_team')
@admin_or_rep_required
def my_team():
    user = get_current_user()
    if not user or (user.role == 'rep' and not user.team_id):
        flash("No tienes un equipo asignado.")
        return redirect(url_for('main.index'))
    
    team = user.team
    return render_template('my_team.html', team=team)

@teams_bp.route('/my_team/update_logo', methods=['POST'])
@admin_or_rep_required
def update_logo():
    user = get_current_user()
    if not user or not user.team:
        flash("Equipo no encontrado.")
        return redirect(url_for('main.index'))
        
    team = user.team
    logo = request.files.get('logo')
    if logo and logo.filename:
        try:
            # Resize image to 150x150 for team profile
            file_data, mimetype = resize_image(logo, size=(150, 150))
            
            if file_data:
                team.logo_data = file_data
                team.logo_mimetype = mimetype
                team.logo = secure_filename(logo.filename)
                db.session.commit()
                flash("Logo actualizado con éxito.")
            else:
                flash("Error al procesar la imagen.")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar el logo: {str(e)}")
    return redirect(url_for('teams.my_team'))


@teams_bp.route('/my_team/add_player', methods=['POST'])
@admin_or_rep_required
def add_player():
    user = get_current_user()
    if not user or not user.team:
        flash("Equipo no encontrado.")
        return redirect(url_for('main.index'))
        
    team = user.team
    name = request.form.get('name')
    number = request.form.get('number', 0)
    position = request.form.get('position')
    
    if name:
        new_player = Player(name=name, number=number, position=position, team_id=team.id)
        db.session.add(new_player)
        db.session.commit()
        flash(f"Jugador {name} añadido.")
    return redirect(url_for('teams.my_team'))


@teams_bp.route('/my_team/player/<int:p_id>/update', methods=['POST'])
@admin_or_rep_required
def update_player(p_id):
    user = get_current_user()
    if not user or not user.team:
        return redirect(url_for('main.index'))
        
    team = user.team
    player = db.session.get(Player, p_id)
    if player and player.team_id == team.id:
        player.name = request.form.get('name', player.name)
        player.number = request.form.get('number', player.number)
        player.position = request.form.get('position', player.position)
        db.session.commit()
        flash("Datos del jugador actualizados.")
    return redirect(url_for('teams.my_team'))


@teams_bp.route('/my_team/player/<int:p_id>/delete', methods=['POST'])
@admin_or_rep_required
def delete_player(p_id):
    user = get_current_user()
    if not user or not user.team:
        return redirect(url_for('main.index'))
        
    team = user.team
    player = db.session.get(Player, p_id)
    if player and player.team_id == team.id:
        db.session.delete(player)
        db.session.commit()
        flash("Jugador eliminado.")
    return redirect(url_for('teams.my_team'))
