from app import db
from datetime import datetime

class TIDP(db.Model):
    __tablename__ = 'tidp'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    responsible_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    due_date = db.Column(db.Date, nullable=False, index=True)
    file_format = db.Column(db.String(100), nullable=False)  # e.g., "IFC", "DWG", "PDF"
    status = db.Column(db.String(20), default='pending', index=True)  # pending, in-progress, completed, overdue
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'description': self.description,
            'responsible_user_id': self.responsible_user_id,
            'responsible_user_name': self.responsible_user.name if self.responsible_user else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'file_format': self.file_format,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def is_overdue(self):
        if self.due_date and self.status != 'completed':
            return self.due_date < datetime.now().date()
        return False
