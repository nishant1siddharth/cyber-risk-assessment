from datetime import datetime
from . import db

class Asset(db.Model):
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    importance = db.Column(db.Integer, nullable=False) # 1 to 5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    assessments = db.relationship('Assessment', backref='asset', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Asset {self.name}>'
