from main import db
from datetime import datetime

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.String(100), default=datetime.now())
    

    def create_record(self):
        db.session.add(self)
        db.session.commit()