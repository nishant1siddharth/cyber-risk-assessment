from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from models.business import Business

def get_current_business():
    if not current_user.is_authenticated:
        return None
    
    admin_id = current_user.id if current_user.role == 'admin' else current_user.employer_id
    return Business.query.filter_by(user_id=admin_id).first()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            # Redirect based on whether they have a business setup
            business = get_current_business()
            if business:
                return redirect(url_for('dashboard.index'))
            else:
                return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
