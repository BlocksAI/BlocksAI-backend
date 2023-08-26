from db import db

class UserBlocks(db.Model):
    __tablename__ = 'user_blocks'
    user_block_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    block_id = db.Column(db.Integer, db.ForeignKey('blocks.block_id'), nullable=False)
    
    @staticmethod
    def add_new_record(app, new_user_block):
        with app.app_context():
            db.session.add(new_user_block)
            db.session.commit()
            print("Committed and added new user block")
            
    @staticmethod
    def delete_by_block_id_user_id(block_id, user_id):
        db.session.query(UserBlocks).filter_by(block_id=block_id, user_id=user_id).delete()
        db.session.commit()