import importlib
import json

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator


def blockPicker(user_prompt: str) -> tuple[str, int]:
    prompt_for_gateway = f"Which of the agents can be used for this prompt: '{user_prompt}'?"
    
    loader = TextLoader('DB.csv')
    index = VectorstoreIndexCreator().from_loaders([loader])
    
    return index.query(prompt_for_gateway), 200
    

def querySpecificBlock(block_name: str, user_prompt: str):
    
    # TODO: Check if the user has subscribed to the block
    
    # Import the new block
    block = importlib.import_module('agents.' + block_name)
    
    # Execute the prompt using the chosen block
    response = block.new_block(user_prompt)
    print("RES:", response)
    print("JSON:", json.dumps(response))
    
    # TODO: Encode chat history to json format
    
    # TODO: Check if need to delete the import
    # del sys.modules[block]
    
    return json.dumps(response), 200