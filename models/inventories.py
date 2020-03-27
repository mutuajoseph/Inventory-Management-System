from main import db

class Inventories(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    type = db.Column(db.String(100), nullable=False)
    buying_price = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer, nullable=False)
    sales = db.relationship('Sale', backref='inventory', lazy=True)
    stocks = db.relationship('Stock', backref='inventory', lazy=True)
    

    # create record 
    def create_record(self):
        db.session.add(self)
        db.session.commit()
    
    # fetch all records from database 
    @classmethod
    def fetch_records(cls):
        inventory = cls.query.all()
        return inventory
    
    # fetch records id
    @classmethod
    def fetch_by_id(cls,id):
        delete_record = cls.query.filter_by(id=id)
        
        if delete_record.first():

            delete_record.delete()
            db.session.commit()
            return True
        else:
            return False
