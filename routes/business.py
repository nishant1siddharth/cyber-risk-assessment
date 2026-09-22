from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.business import Business
from models.user import User
from utils.auth_utils import get_current_business, admin_required

business_bp = Blueprint('business', __name__, url_prefix='/business')

@business_bp.route('/', methods=['GET', 'POST'])
@admin_required
def profile():
    business = get_current_business()

    if request.method == 'POST':
        name = request.form.get('name')
        b_type = request.form.get('business_type')
        employees = request.form.get('number_of_employees')
        devices = request.form.get('number_of_devices')
        description = request.form.get('description')

        if not name or not b_type:
            flash('Business name and type are required.', 'danger')
            return redirect(url_for('business.profile'))

        if not business:
            business = Business(user_id=current_user.id)
            db.session.add(business)

        business.name = name
        business.business_type = b_type
        business.number_of_employees = int(employees) if employees else 0
        business.number_of_devices = int(devices) if devices else 0
        business.description = description

        db.session.commit()
        flash('Business profile saved successfully.', 'success')
        return redirect(url_for('business.profile'))

    return render_template('business.html', business=business)

@business_bp.route('/employee_access', methods=['GET', 'POST'])
@admin_required
def employee_access():
    employee = User.query.filter_by(employer_id=current_user.id, role='employee').first()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('business.employee_access'))

        # Check if username exists and belongs to someone else
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != (employee.id if employee else -1):
            flash('Username already exists.', 'danger')
            return redirect(url_for('business.employee_access'))

        if not employee:
            employee = User(username=username, email=f'{username}@employee.local', role='employee', employer_id=current_user.id)
            db.session.add(employee)
        else:
            employee.username = username
            employee.email = f'{username}@employee.local'
        
        employee.set_password(password)
        db.session.commit()
        flash('Employee access updated successfully.', 'success')
        return redirect(url_for('business.employee_access'))

    return render_template('employee_access.html', employee=employee)

@business_bp.route('/employee_access/delete', methods=['POST'])
@admin_required
def employee_access_delete():
    employee = User.query.filter_by(employer_id=current_user.id, role='employee').first()
    if employee:
        db.session.delete(employee)
        db.session.commit()
        flash('Employee access has been completely revoked and removed.', 'success')
    return redirect(url_for('business.employee_access'))
