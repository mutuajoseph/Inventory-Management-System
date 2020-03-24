from main import db
from datetime import datetime

class Stock(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String(100), default=datetime.now())


    def create_record(self):
        db.session.add(self)
        db.session.commit()