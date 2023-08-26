from models.User import Users
from models.Block import Blocks
from models.UserBlock import UserBlocks

def get_all_blocks():
    return [block.to_json() for block in Blocks.query.all()], 200


def create_new_block(app, block_name: str, description: str, category: str):
    # If block name already taken, do not create
    if Blocks.query.filter_by(block_name=block_name).all():
        return { "error": "Block name already taken!" }, 400
    
    # Create a new block object
    new_block = Blocks(
        block_name=block_name,
        description=description,
        category=category
    )
    
    # Try to add it to DB
    try:
        Blocks.create_new_block(app, new_block)
    except:
        return { "error": "Unable to create block" }, 500

    return { "status": f"created new block '{block_name}'" }, 201


def manufacture_new_block(agent_file):
    # Download file to /agents directory
    file_path = f"agents/{agent_file.filename}"
    agent_file.save(file_path)
    return { "status": "Block successfully manufactured!" }, 201


def subscribe_to_block(app, block_id: int, username: str):
    # If user already subscribed to block, exit
    if UserBlocks.query.filter_by(block_id=block_id, user_id=1).all():
        return { "error": "User already subscribed to this block!" }, 400
    
    # Query for user_id by username
    user_id = Users.get_user_id_by_username(username)
    
    # Create a new user_block object
    new_user_block = UserBlocks(
        block_id=block_id,
        user_id=user_id,
    )
    
    # Try to add it to DB
    try:
        UserBlocks.add_new_record(app, new_user_block)
    except:
        return { "error": "Unable to create user-block entry" }, 500

    return { "status": "Successfully subscribed to block" }, 201


def unsubscribe_to_block(block_id: int, username: str):
    # Query for user_id by username
    user_id = Users.get_user_id_by_username(username)
    
    # If user is not subscribed to the block, exit
    if not UserBlocks.query.filter_by(block_id=block_id, user_id=user_id).all():
        return { "error": "User is not subscribed to this block!" }, 400
    
    # Try to delete the user-block record
    try:
        UserBlocks.delete_by_block_id_user_id(block_id, user_id)
    except:
        return { "error": "Unable to delete user-block entry" }, 500

    return { "status": "Successfully unsubscribed to block" }, 204