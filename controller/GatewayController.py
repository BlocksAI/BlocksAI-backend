import importlib

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.schema.messages import HumanMessage, AIMessage, SystemMessage

from models.ChatHistory import ChatHistory
from models.Block import Blocks


def blockPicker(user_prompt):
    prompt_for_gateway = f"Which of the agents can be used for this prompt: '{user_prompt}'?"
    
    # TODO: Read blocks available from DB
    loader = TextLoader('DB.csv')
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
    # TODO: Check if the user has subscribed to the block
    
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
