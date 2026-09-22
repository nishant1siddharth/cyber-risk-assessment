from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.asset import Asset
from utils.auth_utils import get_current_business, admin_required

assets_bp = Blueprint('assets', __name__, url_prefix='/assets')

@assets_bp.route('/')
@login_required
def index():
    business = get_current_business()
    if not business:
        flash('Please complete your business profile first.', 'warning')
        return redirect(url_for('business.profile'))
    
    assets = Asset.query.filter_by(business_id=business.id).all()
    return render_template('assets.html', assets=assets)

@assets_bp.route('/add', methods=['POST'])
@admin_required
def add():
    business = get_current_business()
    if not business:
        return redirect(url_for('business.profile'))

    name = request.form.get('name')
    category = request.form.get('category')
    importance = request.form.get('importance')
    description = request.form.get('description')

    if not name or not category or not importance:
        flash('Name, Category, and Importance are required.', 'danger')
        return redirect(url_for('assets.index'))

    try:
        importance = int(importance)
        if not (1 <= importance <= 5):
            raise ValueError
    except ValueError:
        flash('Importance must be a number between 1 and 5.', 'danger')
        return redirect(url_for('assets.index'))

    asset = Asset(
        business_id=business.id,
        name=name,
        category=category,
        description=description,
        importance=importance
    )
    db.session.add(asset)
    db.session.commit()
    
    flash(f'Asset "{name}" added successfully.', 'success')
    return redirect(url_for('assets.index'))

@assets_bp.route('/delete/<int:asset_id>', methods=['POST'])
@admin_required
def delete(asset_id):
    business = get_current_business()
    if not business:
        return redirect(url_for('business.profile'))
        
    asset = Asset.query.filter_by(id=asset_id, business_id=business.id).first()
    if asset:
        db.session.delete(asset)
        db.session.commit()
        flash('Asset deleted successfully.', 'success')
    else:
        flash('Asset not found or unauthorized.', 'danger')
        
    return redirect(url_for('assets.index'))
