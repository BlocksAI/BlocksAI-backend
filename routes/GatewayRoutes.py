from flask import Blueprint, request
from controller.GatewayController import *


gateway_bp = Blueprint('gateway', __name__)

# Gateway route to pick out suitable block
@gateway_bp.route('/gateway', methods=["POST"])
def blocks_gateway():
    return blockPicker(request.get_json()['user_prompt'])


# This endpoint is to run the chosen block
@gateway_bp.route('/chosen-block', methods=['POST'])
def run_chosen_block():
    data = request.get_json()
    block_name = data['block_name']
    user_prompt = data['user_prompt']
    return querySpecificBlock(block_name, user_prompt)
