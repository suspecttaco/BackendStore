# File models/sale.py
from datetime import datetime
from . import db


class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'), nullable=True)

    total = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum('cash', 'card', 'credit'), default='cash')
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    user = db.relationship('User', backref='sales')
    customer = db.relationship('Customer', backref='purchases')
    details = db.relationship('SaleDetail', backref='sale', cascade="all, delete-orphan")


class SaleDetail(db.Model):
    __tablename__ = 'sale_details'

    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotions.id'), nullable=True)

    amount = db.Column(db.Numeric(10, 3), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), default=0)

    # Relaciones
    product = db.relationship('Product')


class Return(db.Model):
    __tablename__ = 'returns'
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    authorized_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    reason = db.Column(db.Text)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    details = db.relationship('ReturnDetail', backref='return_obj', cascade="all, delete-orphan")


class ReturnDetail(db.Model):
    __tablename__ = 'return_details'
    id = db.Column(db.Integer, primary_key=True)
    return_id = db.Column(db.Integer, db.ForeignKey('returns.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 3), nullable=False)
    refund_amount = db.Column(db.Numeric(10, 2), nullable=False)