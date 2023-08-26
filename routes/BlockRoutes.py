from flask import Blueprint, request, current_app
from controller.BlockController import *


block_bp = Blueprint('block', __name__)

@block_bp.route('/', methods=['GET'])
def all_blocks():
    return get_all_blocks()


@block_bp.route('/create', methods=['POST'])
def new_block():
    data = request.get_json()
    return create_new_block(
        current_app,
        data['block_name'],
        data['description'],
        data['category']
    )
    

@block_bp.route('/manufacture', methods=['POST'])
def new_agent():
    return manufacture_new_block(request.files['block_file'])


@block_bp.route('/subscribe/<block_id>', methods=['POST'])
def user_subscribe_to_block(block_id):
    data = request.get_json()
    return subscribe_to_block(current_app, block_id, data['username'])


@block_bp.route('/unsubscribe/<block_id>', methods=['DELETE'])
def user_unsubscribe_to_block(block_id):
    data = request.get_json()
    return unsubscribe_to_block(block_id, data['username'])