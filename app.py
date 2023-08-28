import os
import pymysql
pymysql.install_as_MySQLdb()

from dotenv import load_dotenv
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from db import db
from models.Block import Blocks
from models.User import Users
from models.UserBlock import UserBlocks
from models.ChatHistory import ChatHistory

from routes.GatewayRoutes import gateway_bp
from routes.UserRoutes import user_bp
from routes.BlockRoutes import block_bp

load_dotenv()

# DB env variables
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOSTNAME = os.environ.get('DB_HOSTNAME')
DB_SCHEMA = os.environ.get('DB_SCHEMA')

# Set up server
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_SCHEMA}"

# Set up connection to DB
db.init_app(app)
print(f"[{datetime.now()} SERVER] Connected to DB!")

# Enable CORS
CORS(app)

# Health Check route
@app.route('/')
def index():
    return "BlocksAI is running!"

# Register the rest of the blueprints (routes)
app.register_blueprint(gateway_bp, url_prefix='/blocks-gateway')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(block_bp, url_prefix='/blocks')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tables created!")
        
        # Seed user (1, "bobby", "123456")
        if not Users.query.filter_by(username="bobby").all():
            db.session.add(Users(username="bobby", password="123456"))
            db.session.commit()
            print(f"[{datetime.now()} SERVER] User 'bobby' seeded")
            
        # Seed default block (1, "OnlineSearch", "This agent is useful when none of the rest of the agents can be used to help with the prompt", "Misc")
        if not Blocks.query.filter_by(block_name="OnlineSearch").all():
            db.session.add(Blocks(block_id=1,block_name="OnlineSearch", description="This agent is useful when none of the rest of the agents can be used to help with the prompt", category="Misc"))
            db.session.commit()
            print(f"[{datetime.now()} SERVER] Block 'OnlineSearch' created")
            
    app.run(host = "0.0.0.0", debug=False, port=5001)
