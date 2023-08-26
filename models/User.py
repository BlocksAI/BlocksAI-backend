from db import db

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @staticmethod
    def get_user_id_by_username(username):
        return Users.query.filter_by(username=username).all()[0].user_id