import importlib

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.schema.messages import HumanMessage, AIMessage, SystemMessage

from models.ChatHistory import ChatHistory
from models.Block import Blocks
from models.UserBlock import UserBlocks


def write_to_csv(blocks):
    with open('all_blocks.csv', 'w') as o:
        o.write('AgentName;AgentDescription\n')
        for block in blocks:
            o.write(f"{block['block_name']};{block['description']}\n")
        o.write('MarketplaceQuery;This agent is useful when none of the rest of the agents can be used to help with the prompt\n')


def blockPicker(user_prompt):
    prompt_for_gateway = f"Which of the agents can be used for this prompt: '{user_prompt}'?"
    
    # Read blocks available from DB
    write_to_csv(Blocks.get_all_blocks())
    
    # Let language model decide which block to use
    loader = TextLoader('all_blocks.csv')
    index = VectorstoreIndexCreator().from_loaders([loader])
    
    return { "chosen_block": index.query(prompt_for_gateway) }, 200
    

def json_encode_chat_history(chat_history):
    result = []
    for msg in chat_history:
        msg_type = "SYSTEM"
        if type(msg) == HumanMessage:
            msg_type = "HUMAN"
        elif type(msg) == AIMessage:
            msg_type = "AI"
        result.append((msg_type, msg.content))
    return result


def new_chat_history(app, block_name, msg, msg_type):
    new_entry = ChatHistory(
        block_id = Blocks.query.filter_by(block_name=block_name).all()[0].block_id,
        user_id = 1,  ## HARDCODED
        message = msg,
        message_type = msg_type
    )
    ChatHistory.add_new_record(app, new_entry)


def querySpecificBlock(app, block_name: str, user_prompt: str):
    
    block_id = Blocks.get_block_id_by_block_name(block_name)
    
    if not UserBlocks.query.filter_by(user_id=1, block_id=block_id).all():
        return { "error": f"User is not subscribed to {block_name}" }, 403
    
    # Import the new block
    block = importlib.import_module('agents.' + block_name)
    
    # Execute the prompt using the chosen block
    response = block.new_block(user_prompt)
    
    # Persist chat history
    try:
        new_chat_history(app, block_name, response['input'], 'HUMAN')
        new_chat_history(app, block_name, response['output'], 'AI')
    except:
        return { "error": "Chat history not recorded" }, 400
    
    return {
        "input": response['input'],
        "output": response['output'],
        "chat_history": json_encode_chat_history(response['chat_history'])
    }, 201
