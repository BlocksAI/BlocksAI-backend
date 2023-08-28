import sys

from dotenv import load_dotenv
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool, initialize_agent
from langchain.tools import BaseTool

# INDIV FILE TESTING ONLY
if __name__ == '__main__':
    load_dotenv()

llm = ChatOpenAI(
    temperature=0,
    model_name='gpt-3.5-turbo'
)

# In-built search tool
search = DuckDuckGoSearchRun()


# Creating a list of tool objects
tools = [
    Tool(
        name='search',
        func=search.run,
        description='useful for when you need to answer questions about current events, or to search the web for the answers'
    )
]

# Create agent memory
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    return_messages=True
)

# Function for backend to inject persisted chat-memory
def inject_chat_history(chat_history):
    for i in range(0, len(chat_history), 2):
        human_msg = chat_history[i]
        ai_msg = chat_history[i + 1]
        memory.save_context({"input": human_msg}, {"output": ai_msg})
    print("Injected chat history from DB")


# Initialise agent
new_block = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools,
    llm=llm,
    verbose=True,
    memory=memory
)

# Fine-tuning of agent prompt template (AS REQUIRED)
FIXED_PROMPT = '''
Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
'''
new_block.agent.llm_chain.prompt.messages[0].prompt.template = FIXED_PROMPT

# FOR INDIV FILE TESTING ONLY
if __name__ == '__main__':
    while True:
        new_block(input("> "))