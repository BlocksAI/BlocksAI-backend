from db import db

class Blocks(db.Model):
    __tablename__ = 'blocks'
    block_id = db.Column(db.Integer, primary_key=True)
    block_name = db.Column(db.String(100), nullable=False)
    block_description = db.Column(db.String(3000), nullable = False)
