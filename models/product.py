# File BackendStore/models/product.py
from datetime import datetime
from . import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    buy_price = db.Column(db.Numeric(10,2))
    sell_price = db.Column(db.Numeric(10,2), nullable=False)
    actual_stock = db.Column(db.Numeric(10,2), default=0)
    minimum_stock = db.Column(db.Numeric(10,2), default=5)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'buy_price': self.buy_price,
            'sell_price': self.sell_price,
            'actual_stock': self.actual_stock,
            'minimum_stock': self.minimum_stock,
            'active': self.active,
            'created_at': self.created_at
        }