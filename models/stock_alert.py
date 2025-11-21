# File models/stock_alert.py
from datetime import datetime
from . import db

class StockAlert(db.Model):
    __tablename__ = 'stock_alerts'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    actual_stock = db.Column(db.Numeric(10,2))
    alert_date = db.Column(db.DateTime, default=datetime.utcnow)
    resolved = db.Column(db.Boolean, default=False)

    product = db.relationship('Product')

    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.name if self.product else 'N/A',
            'actual_stock': float(self.actual_stock),
            'date': self.alert_date.isoformat(),
            'resolved': self.resolved
        }