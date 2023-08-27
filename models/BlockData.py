from db import db

class BlockData(db.Model):
    __tablename__ = 'blocks_data'
    block_id = db.Column(db.Integer, db.ForeignKey('blocks.block_id'),primary_key=True,)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'), primary_key=True)
    block_file = db.Column(db.String(255), primary_key=True)
        
    @staticmethod
    def add_new_record(app, block_data):
        with app.app_context():
            db.session.add(block_data)
            db.session.commit()
            print("Committed and added new chat history")

    @staticmethod
    def get_block_by_block_id_user_id(user_id,block_id):
        return BlockData.query.filter_by(user_id=1, block_id=block_id).all()