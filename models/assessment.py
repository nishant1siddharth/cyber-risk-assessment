from datetime import datetime
from . import db

class Assessment(db.Model):
    __tablename__ = 'assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    threat_id = db.Column(db.Integer, db.ForeignKey('threats.id'), nullable=False)
    likelihood = db.Column(db.Integer, nullable=False) # 1-5
    impact = db.Column(db.Integer, nullable=False) # 1-5
    risk_score = db.Column(db.Integer, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False) # Low, Medium, High, Critical
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Assessment {self.id} for Asset {self.asset_id}>'
