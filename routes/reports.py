from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.business import Business
from models.asset import Asset
from models.assessment import Assessment
from services.recommendation_engine import get_recommendations
from utils.auth_utils import get_current_business
from datetime import datetime

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/')
@login_required
def executive_report():
    business = get_current_business()
    if not business:
        return redirect(url_for('business.profile'))

    assets = Asset.query.filter_by(business_id=business.id).all()
    assessments = Assessment.query.filter_by(business_id=business.id).order_by(Assessment.risk_score.desc()).all()
    
    # Calculate summary stats
    risk_counts = {'Low': 0, 'Medium': 0, 'High': 0, 'Critical': 0}
    for a in assessments:
        if a.risk_level in risk_counts:
            risk_counts[a.risk_level] += 1
            
    # Gather mitigations for High/Critical risks
    critical_assessments = [a for a in assessments if a.risk_level in ['High', 'Critical']]
    action_plan = []
    seen_threats = set()
    
    for a in critical_assessments:
        if a.threat_id not in seen_threats:
            mitigations = get_recommendations(a.threat_id, a.risk_level)
            action_plan.append({
                'threat_name': a.threat.name,
                'mitigations': mitigations
            })
            seen_threats.add(a.threat_id)

    return render_template('report.html', 
                           business=business, 
                           assets=assets, 
                           assessments=assessments,
                           risk_counts=risk_counts,
                           action_plan=action_plan,
                           date=datetime.utcnow().strftime('%Y-%m-%d'))
