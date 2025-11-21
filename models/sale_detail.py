# File models/sale_detail.py
from . import db

class SaleDetail(db.Model):
    __tablename__ = 'sales_detail'

    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    # Cantidades
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    # Relacion
    product = db.relationship('Product')

    def to_dict(self):
        return {
            'id': self.id,
            'sale_id': self.sale_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else 'Producto Desconocido',
            'amount': float(self.amount),
            'unit_price': float(self.unit_price),
            'subtotal': float(self.subtotal)
        }