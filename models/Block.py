from db import db

class Blocks(db.Model):
    __tablename__ = 'blocks'
    block_id = db.Column(db.Integer, primary_key=True)
    block_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(3000), nullable = False)
    category = db.Column(db.String(255), nullable=False)

    def to_json(self):
        print("Encoding the json")
        return {
            "block_id": self.block_id,
            "block_name": self.block_name,
            "description": self.description,
            "category": self.category
        }
        
    @staticmethod
    def get_all_blocks():
        return [block.to_json() for block in Blocks.query.all()]
        
    @staticmethod
    def get_block_id_by_block_name(block_name):
        return Blocks.query.filter_by(block_name=block_name).all()[0].block_id

    @staticmethod
    def create_new_block(app, new_block):
        with app.app_context():
            db.session.add(new_block)
            db.session.commit()
            print("Committed and added new block!")