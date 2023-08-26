from db import db

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    