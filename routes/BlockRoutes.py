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
