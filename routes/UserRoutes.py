from flask import Blueprint, request
from controller.UserController import (
    login,
    register
)

# Create a blueprint for app to register
user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    return login(data['username'], data['password'])


@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    return register(data['username'], data['password'], data['role'])
