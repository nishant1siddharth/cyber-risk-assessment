from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.business import Business
from utils.auth_utils import get_current_business
from models.asset import Asset
from models.assessment import Assessment
from models import db
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    business = get_current_business()
    
    if not business:
        return redirect(url_for('business.profile'))

    total_assets = Asset.query.filter_by(business_id=business.id).count()
    total_assessments = Assessment.query.filter_by(business_id=business.id).count()
    
    # Calculate risks
    assessments = Assessment.query.filter_by(business_id=business.id).all()
    risk_counts = {'Low': 0, 'Medium': 0, 'High': 0, 'Critical': 0}
    for a in assessments:
        if a.risk_level in risk_counts:
            risk_counts[a.risk_level] += 1
            
    # Get top 5 risks
    top_risks = Assessment.query.filter_by(business_id=business.id).order_by(Assessment.risk_score.desc()).limit(5).all()

    return render_template('dashboard.html', 
                           business=business, 
                           total_assets=total_assets, 
                           total_assessments=total_assessments,
                           risk_counts=risk_counts,
                           top_risks=top_risks)

@dashboard_bp.route('/matrix')
@login_required
def matrix():
    return render_template('matrix.html')
