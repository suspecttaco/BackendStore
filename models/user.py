# File models/user.py
from datetime import datetime
from . import db

# Tabla N:N para permisos
user_permissions = db.Table('user_permissions',
                            db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                            db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
                            )


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    role = db.Column(db.Enum('admin', 'cashier', 'manager'), default='cashier')
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    permissions = db.relationship('Permission', secondary=user_permissions, lazy='subquery',
                                  backref=db.backref('users', lazy=True))
    shifts = db.relationship('Shift', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'role': self.role,
            'active': self.active
        }


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    table_affected = db.Column(db.String(50))
    record_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Shift(db.Model):
    __tablename__ = 'shifts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_amount = db.Column(db.Numeric(10, 2), nullable=False)
    end_amount = db.Column(db.Numeric(10, 2))
    expected_amount = db.Column(db.Numeric(10, 2))
    difference = db.Column(db.Numeric(10, 2))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    closed = db.Column(db.Boolean, default=False)

    # Relación para retiros parciales
    withdrawals = db.relationship('CashWithdrawal', backref='shift', lazy=True)


class CashWithdrawal(db.Model):
    __tablename__ = 'cash_withdrawals'
    id = db.Column(db.Integer, primary_key=True)
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    concept = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)