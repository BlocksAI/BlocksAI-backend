import sys

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool, initialize_agent,create_csv_agent
from langchain.chains.question_answering import load_qa_chain
from langchain.agents.agent_types import AgentType
import PyPDF2
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
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


'''
DEVELOPERS WILL WRITE CUSTOM FUNCTIONS FOR CUSTOM TOOLS BELOW:
'''

# In-built search tool
search = DuckDuckGoSearchRun()


# Custom tool 1
def parse_csv(input=""):
    csv_files=[file for file in files if ".csv" in file]
    
    agent=create_csv_agent(
        llm,
        csv_files,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )
    
    # output=agent.run(input)
    return agent.run(input)

def process_text(text):
    # Split the text into chunks using Langchain's CharacterTextSplitter
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    # Convert the chunks of text into embeddings to form a knowledge base
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    return knowledge_base
    
def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader=PyPDF2.PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return text

def parse_pdf(input="",**kwargs):
    
    pdf_files=[file for file in files if ".pdf" in file]

    if len(pdf_files)==0:
        return parse_csv(input)
    
    text=get_pdf_text(pdf_files)
    knowledge_base=process_text(text)
    docs=knowledge_base.similarity_search(input)
    chain = load_qa_chain(llm=llm, chain_type="stuff")
    
    return chain({"input_documents": docs, "question": input},return_only_outputs=True)["output_text"]

files=[]

# Creating a list of tool objects
tools = [
    Tool(
        name='search',
        func=search.run,
        description='useful for when you need to answer questions about current events, or to search the web for the answers'
    ),
    Tool(
        name='csv parsing tool',
        func=parse_csv,
        description='useful when the user is asking questions and specifies that they need to gather insights from the csv uploaded',
        # args_schema=
    ),
    Tool(
        name='pdf parsing tool',
        func=parse_pdf,
        description='useful when the user is asking questions and specifies that they need to gather insights from the pdf uploaded'
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
    memory=memory,
    max_iterations=2,
)

# Fine-tuning of agent prompt template (AS REQUIRED)
FIXED_PROMPT = '''
Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

When asked about a certain term, assistant should try to look for the grades of that subject for that term using the grade history display, instead of searching the web. If the results/grades for that term is not recorded, you can answer by saying that there are no records for that term.

Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
'''
new_block.agent.llm_chain.prompt.messages[0].prompt.template = FIXED_PROMPT

# FOR INDIV FILE TESTING ONLY
if __name__ == '__main__':
    while True:
        new_block(input("> "))