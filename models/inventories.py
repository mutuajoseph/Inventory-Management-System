from main import db

class Inventories(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    type = db.Column(db.String(100), nullable=False)
    buying_price = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer, nullable=False)
    

    # create record 
    def create_record(self):
        db.session.add(self)
        db.session.commit()
    
    # fetch all records from database 
    @classmethod
    def fetch_records(cls):
        inventory = cls.query.all()
        return inventory
