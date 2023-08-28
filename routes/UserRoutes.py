from flask import Blueprint, request
from controller.UserController import (
    login,
    register,
    get_chat_history,
    upload_user_file
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


@user_bp.route('/<user_id>/chat-history', methods=['GET'])
def user_chat_history(user_id):
    return get_chat_history(user_id)


@user_bp.route('/file-upload', methods=['POST'])
def upload_file():
    return upload_user_file(request.files['user_file'])