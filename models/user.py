# File BackendStore/models/user.py
from datetime import datetime
from enum import unique

from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(100))
    role = db.Column(db.Enum('admin', 'cashier'), default='cashier')
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'role': self.role,
            'active': self.active,
            'created_at': self.created_at
        }
