from main import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=True, unique=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=True)

    # create record 
    def create_record(self):
        db.session.add(self)
        db.session.commit()


    