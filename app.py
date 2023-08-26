import os

from dotenv import load_dotenv
from datetime import datetime
from flask import Flask
from db import db

from routes.GatewayRoutes import gateway_bp
from routes.UserRoutes import user_bp


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


# Health Check route
@app.route('/')
def index():
    return "BlocksAI is running!"

# Register the rest of the blueprints (routes)
app.register_blueprint(gateway_bp, url_prefix='/blocks-gateway')
app.register_blueprint(user_bp, url_prefix='/users')


if __name__ == '__main__':
    app.run(debug=True, port=5001)