from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models import Tournament, TournamentPrize, MarketingAsset
from app.utils.decorators import admin_required
from . import marketing_bp
import os
from werkzeug.utils import secure_filename

@marketing_bp.route('/admin/marketing')
@admin_required
def dashboard():
    tournaments = Tournament.query.all()
    assets = MarketingAsset.query.order_by(MarketingAsset.created_at.desc()).all()
    prizes = TournamentPrize.query.all()
    return render_template('marketing_dashboard.html', 
                           tournaments=tournaments, 
                           assets=assets, 
                           prizes=prizes)

@marketing_bp.route('/admin/marketing/prizes/add', methods=['POST'])
@admin_required
def add_prize():
    t_id = request.form.get('tournament_id')
    rank = request.form.get('rank')
    title = request.form.get('title')
    description = request.form.get('description')
    reward = request.form.get('reward_value')
    
    if t_id and rank and title:
        prize = TournamentPrize(tournament_id=t_id, rank=rank, title=title, 
                                 description=description, reward_value=reward)
        db.session.add(prize)
        db.session.commit()
        flash("Premio añadido con éxito.")
    return redirect(url_for('marketing.dashboard'))

@marketing_bp.route('/admin/marketing/prizes/<int:p_id>/delete', methods=['POST'])
@admin_required
def delete_prize(p_id):
    prize = db.session.get(TournamentPrize, p_id)
    if prize:
        db.session.delete(prize)
        db.session.commit()
        flash("Premio eliminado.")
    return redirect(url_for('marketing.dashboard'))

@marketing_bp.route('/admin/marketing/assets/upload', methods=['POST'])
@admin_required
def upload_asset():
    t_id = request.form.get('tournament_id')
    asset_type = request.form.get('type', 'image')
    title = request.form.get('title')
    
    if 'file' not in request.files:
        flash("No hay archivo.")
        return redirect(url_for('marketing.dashboard'))
        
    file = request.files['file']
    if file.filename == '':
        flash("No se seleccionó ningún archivo.")
        return redirect(url_for('marketing.dashboard'))
        
    if file:
        filename = secure_filename(file.filename)
        # Ensure directory exists
        upload_path = os.path.join('app', 'static', 'uploads', 'marketing')
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
            
        file.save(os.path.join(upload_path, filename))
        
        asset = MarketingAsset(tournament_id=t_id if t_id else None,
                               type=asset_type,
                               filename=filename,
                               title=title)
        db.session.add(asset)
        db.session.commit()
        flash("Archivo de marketing subido con éxito.")
        
    return redirect(url_for('marketing.dashboard'))

@marketing_bp.route('/admin/marketing/assets/<int:a_id>/delete', methods=['POST'])
@admin_required
def delete_asset(a_id):
    asset = db.session.get(MarketingAsset, a_id)
    if asset:
        # Delete file
        try:
            os.remove(os.path.join('app', 'static', 'uploads', 'marketing', asset.filename))
        except:
            pass
        db.session.delete(asset)
        db.session.commit()
        flash("Archivo eliminado.")
    return redirect(url_for('marketing.dashboard'))

@marketing_bp.route('/admin/marketing/ai/generate', methods=['POST'])
@admin_required
def request_ai_generation():
    prompt = request.form.get('prompt')

    if prompt:
        # In a real app, this would call an AI API like DALL-E or Imagen.
        # For this demo, we simulate the request being sent to the AI Engine.
        flash(f"Solicitud enviada al Motor AI: '{prompt[:50]}...'. "
              "Las imágenes se generarán en breve.")

        # We can add a placeholder or wait for the agent to provide the real image.
        # For now, we just redirect back to the dashboard.
    return redirect(url_for('marketing.dashboard'))
