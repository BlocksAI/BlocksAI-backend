import sys

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool

# INDIV FILE TESTING ONLY
if __name__ == '__main__':
    load_dotenv()


'''
THESE ARE THE BASE TEMPLATE CODE FOR DEVELOPERS:
'''
llm = ChatOpenAI(
    temperature=0,
    model_name='gpt-3.5-turbo'
)

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

# Function for backend to inject data for the ai-chatbot to learn from
def inject_dataset(form):
    # for i in range(0, len(chat_history), 2):
    #     human_msg = chat_history[i]
    #     ai_msg = chat_history[i + 1]
    #     memory.save_context({"input": human_msg}, {"output": ai_msg})
    print("Injected chat history from DB")


'''
DEVELOPERS WILL WRITE CUSTOM FUNCTIONS FOR CUSTOM TOOLS BELOW:
'''

# In-built search tool
search = DuckDuckGoSearchRun()

# Custom tool 1
def solve_question(input=""):
    agent_executor = create_python_agent(
    llm=llm,
    tool=PythonREPLTool(),
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    agent_executor_kwargs={"handle_parsing_errors": True},
)

    return agent_executor.run(input)

# Creating a list of tool objects
tools = [
    Tool(
        name='search',
        func=search.run,
        description='useful for when you need to answer questions about current events, or to search the web for the answers'
    ),
    Tool(
        name='solve question',
        func=solve_question,
        description='useful solving math questions for instance fibonacci numbers or training a neural network'
    )
]


'''
THESE ARE THE BASE TEMPLATE CODE FOR DEVELOPERS:
'''
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

Assistant would be specifically writing python codes to solve math questions, for instance fibonacci numbers or training a neural network. Assistant would be perfect for solving math questions.

Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
'''
new_block.agent.llm_chain.prompt.messages[0].prompt.template = FIXED_PROMPT

# FOR INDIV FILE TESTING ONLY
if __name__ == '__main__':
    while True:
        new_block(input("> "))