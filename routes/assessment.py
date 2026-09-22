from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.asset import Asset
from models.threat import Threat
from models.assessment import Assessment
from services.risk_engine import calculate_risk
from services.recommendation_engine import get_recommendations
from utils.auth_utils import get_current_business, admin_required

assessment_bp = Blueprint('assessment', __name__, url_prefix='/assessment')

@assessment_bp.route('/new', methods=['GET', 'POST'])
@admin_required
def new():
    business = get_current_business()
    if not business:
        flash('Please complete your business profile first.', 'warning')
        return redirect(url_for('business.profile'))

    assets = Asset.query.filter_by(business_id=business.id).all()
    if not assets:
        flash('You need to add at least one asset before performing an assessment.', 'warning')
        return redirect(url_for('assets.index'))

    threats = Threat.query.all()

    if request.method == 'POST':
        asset_id = request.form.get('asset_id')
        threat_id = request.form.get('threat_id')
        likelihood = request.form.get('likelihood')
        impact = request.form.get('impact')
        notes = request.form.get('notes')

        if not asset_id or not threat_id or not likelihood or not impact:
            flash('All assessment fields are required.', 'danger')
            return redirect(url_for('assessment.new'))

        try:
            risk_data = calculate_risk(likelihood, impact)
            
            assessment = Assessment(
                business_id=business.id,
                asset_id=int(asset_id),
                threat_id=int(threat_id),
                likelihood=risk_data['likelihood'],
                impact=risk_data['impact'],
                risk_score=risk_data['score'],
                risk_level=risk_data['level'],
                notes=notes
            )
            db.session.add(assessment)
            db.session.commit()
            
            flash('Risk assessment completed successfully.', 'success')
            return redirect(url_for('assessment.results', assessment_id=assessment.id))
            
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('assessment.new'))

    return render_template('assessment.html', assets=assets, threats=threats)

@assessment_bp.route('/results/<int:assessment_id>')
@login_required
def results(assessment_id):
    business = get_current_business()
    if not business:
        return redirect(url_for('business.profile'))

    assessment = Assessment.query.filter_by(id=assessment_id, business_id=business.id).first_or_404()
    mitigations = get_recommendations(assessment.threat_id, assessment.risk_level)
    
    return render_template('results.html', assessment=assessment, mitigations=mitigations)

@assessment_bp.route('/history')
@login_required
def history():
    business = get_current_business()
    if not business:
        return redirect(url_for('business.profile'))

    assessments = Assessment.query.filter_by(business_id=business.id).order_by(Assessment.created_at.desc()).all()
    return render_template('history.html', assessments=assessments)
