from db import db

class Blocks(db.Model):
    __tablename__ = 'blocks'
    block_id = db.Column(db.Integer, primary_key=True)
    block_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(3000), nullable = False)
    category = db.Column(db.String(255), nullable=False)

    def to_json(self):
        print("Encoding the json")
        return {
            "block_name": self.block_name,
            "description": self.description,
            "category": self.category
        }

    @staticmethod
    def create_new_block(app, new_block):
        with app.app_context():
            db.session.add(new_block)
            db.session.commit()
            print("Committed and added new block!")