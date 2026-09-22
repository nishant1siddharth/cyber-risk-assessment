from . import db

class Mitigation(db.Model):
    __tablename__ = 'mitigations'
    
    id = db.Column(db.Integer, primary_key=True)
    threat_id = db.Column(db.Integer, db.ForeignKey('threats.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(50)) # e.g., 'High', 'Medium', 'Low'

    def __repr__(self):
        return f'<Mitigation {self.title}>'
