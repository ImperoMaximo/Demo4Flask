from datetime import datetime
from .db import db


class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
