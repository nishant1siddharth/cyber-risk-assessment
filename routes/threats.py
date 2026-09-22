from flask import Blueprint, render_template
from flask_login import login_required
from models.threat import Threat

threats_bp = Blueprint('threats', __name__, url_prefix='/threats')

@threats_bp.route('/')
@login_required
def index():
    threats = Threat.query.all()
    return render_template('threats.html', threats=threats)
