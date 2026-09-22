from . import db

class Threat(db.Model):
    __tablename__ = 'threats'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    likelihood_default = db.Column(db.Integer)
    impact_default = db.Column(db.Integer)

    # Relationships
    mitigations = db.relationship('Mitigation', backref='threat', lazy='dynamic', cascade='all, delete-orphan')
    assessments = db.relationship('Assessment', backref='threat', lazy='dynamic')

    def __repr__(self):
        return f'<Threat {self.name}>'
