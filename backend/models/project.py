from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    client = db.Column(db.String(200), nullable=False)
    delivery_method = db.Column(db.String(100), nullable=False)  # Design-Bid-Build, Design-Build, etc.
    description = db.Column(db.Text)
    status = db.Column(db.String(50), index=True, default='active')  # active, completed, on-hold
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    goals = db.relationship('Goal', backref='project', lazy=True, cascade='all, delete-orphan')
    tidp_entries = db.relationship('TIDP', backref='project', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'client': self.client,
            'delivery_method': self.delivery_method,
            'description': self.description,
            'status': self.status,
            'owner_id': self.owner_id,
            'owner_name': self.owner.name if self.owner else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Counts may cause N+1; consider denormalization or subqueries for large datasets
            'goals_count': len(self.goals),
            'tidp_count': len(self.tidp_entries),
            'comments_count': len(self.comments)
        }
