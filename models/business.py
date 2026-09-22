from datetime import datetime
from . import db

class Business(db.Model):
    __tablename__ = 'businesses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    business_type = db.Column(db.String(50), nullable=False)
    number_of_employees = db.Column(db.Integer)
    number_of_devices = db.Column(db.Integer)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    assets = db.relationship('Asset', backref='business', lazy='dynamic', cascade='all, delete-orphan')
    assessments = db.relationship('Assessment', backref='business', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Business {self.name}>'
