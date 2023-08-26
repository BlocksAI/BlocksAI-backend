from db import db


class ChatHistory(db.Model):
    __tablename__ = 'chat_history'
    message_id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, db.ForeignKey('blocks.block_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(10), nullable=False)
    
    @staticmethod
    def get_history_by_block_id_user_id(block_id, user_id):
        history = ChatHistory.query.filter_by(user_id=user_id, block_id=block_id).all()
        return [msg.message for msg in history]

    @staticmethod
    def add_new_record(app, new_chat_history):
        with app.app_context():
            db.session.add(new_chat_history)
            db.session.commit()
            print("Committed and added new chat history")