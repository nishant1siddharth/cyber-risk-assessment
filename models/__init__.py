from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

# Import models so they are registered with SQLAlchemy
from models.user import User
from models.business import Business
from models.asset import Asset
from models.threat import Threat
from models.assessment import Assessment
from models.mitigation import Mitigation
