import importlib
import json

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.schema.messages import HumanMessage, AIMessage, SystemMessage


def blockPicker(user_prompt: str) -> tuple[str, int]:
    prompt_for_gateway = f"Which of the agents can be used for this prompt: '{user_prompt}'?"
    
    loader = TextLoader('DB.csv')
    index = VectorstoreIndexCreator().from_loaders([loader])
    
    return index.query(prompt_for_gateway), 200
    

def json_encode_chat_history(chat_history):
    result = []
    for msg in chat_history:
        print(f"TYPE: {type(msg)}")
        print(f"MSG : {msg}")
        print()
        msg_type = "SYSTEM"
        if type(msg) == HumanMessage:
            msg_type = "HUMAN"
        elif type(msg) == AIMessage:
            msg_type = "AI"
        result.append((msg_type, msg.content))
    return result
    

def querySpecificBlock(block_name: str, user_prompt: str):
    
    # TODO: Check if the user has subscribed to the block
    
    # Import the new block
    block = importlib.import_module('agents.' + block_name)
    
    # Execute the prompt using the chosen block
    response = block.new_block(user_prompt)
    
    # TODO: Check if need to delete the import
    # del sys.modules[block]
    
    return {
            "input": response['input'],
            "output": response['output'],
            "chat_history": json_encode_chat_history(response['chat_history'])
        }, 200