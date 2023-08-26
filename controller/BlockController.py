from models.Block import Blocks

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

    return f"created new block '{block_name}'", 201
