# File models/product.py
from datetime import datetime
from . import db

# Tabla asociación para promociones
product_promotions = db.Table('product_promotions',
                              db.Column('promotion_id', db.Integer, db.ForeignKey('promotions.id'), primary_key=True),
                              db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
                              )


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    buy_price = db.Column(db.Numeric(10, 2))
    sell_price = db.Column(db.Numeric(10, 2), nullable=False)

    actual_stock = db.Column(db.Numeric(10, 3), default=0)
    minimum_stock = db.Column(db.Numeric(10, 3), default=5)

    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'sell_price': float(self.sell_price),
            'stock': float(self.actual_stock),
            'category_id': self.category_id
        }


class StockAlert(db.Model):
    __tablename__ = 'stock_alerts'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    actual_stock = db.Column(db.Numeric(10, 3))
    alert_date = db.Column(db.DateTime, default=datetime.utcnow)
    resolved = db.Column(db.Boolean, default=False)

    product = db.relationship('Product')


class Promotion(db.Model):
    __tablename__ = 'promotions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    type = db.Column(db.Enum('percentage', 'fixed_amount', 'buy_x_get_y'), nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    active = db.Column(db.Boolean, default=True)

    products = db.relationship('Product', secondary=product_promotions, backref='promotions')