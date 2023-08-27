import sys

from dotenv import load_dotenv
import pandas as pd
from langchain import OpenAI, LLMMathChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool, initialize_agent
from langchain.tools import BaseTool
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Chroma

# INDIV FILE TESTING ONLY
if __name__ == '__main__':
    load_dotenv()

llm = ChatOpenAI(
    temperature=0,
    model_name='gpt-3.5-turbo'
)

# In-built search tool
search = DuckDuckGoSearchRun()

# =========================================================
# Creating Vector Store for Carbon Emission Supply Factors
# =========================================================
# Loading Dataset from https://catalog.data.gov/dataset/supply-chain-greenhouse-gas-emission-factors-v1-2-by-naics-6
emissions_set = pd.read_csv("https://pasteur.epa.gov/uploads/10.23719/1528686/SupplyChainGHGEmissionFactors_v1.2_NAICS_CO2e_USD2021.csv")
emissions_set.to_csv("emissions_dataset.csv", index = None)

loader = CSVLoader(file_path = "emissions_dataset.csv", encoding="utf-8", csv_args={
                'delimiter': ','})
data = loader.load()

embeddings = OpenAIEmbeddings()
vector_store = Chroma.from_documents(data, embeddings)

# =========================================================
# Creating Math Tool
# =========================================================
llm_math = LLMMathChain.from_llm(llm, verbose=True)

# Creating a list of tool objects
tools = [
    Tool(
        name='search',
        func=search.run,
        description='useful for when you need to answer questions about current events, or to search the web for the answers'
    ),
    Tool(
        name='Carbon Emission Factors',
        func=vector_store.similarity_search,
        description='useful for when you need to find the carbon emissions supply factors for a company. You want to return the most relevant industry for the specified company. After you get the data, find the revenue for the company and multiply the Supply Chain Emission Factors with the Revenue'
    ),
    Tool(
        name='Math Calculator',
        func=llm_math.run,
        description='useful for when you need to perform mathematical calculations'
    )
]

# Create agent memory
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    return_messages=True
)

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

When asked about the carbon emission or footprint for a certain company or industry, follow the steps listed below:
Do not use DuckDuckGo to search directly for carbon footprint of companies, just use it to find the revenue.
Do not use DuckDuckGo to search for carbon footprint report statistics or carbon emission report statistics, use Carbon Emissions Factors instead.
First, use DuckDuckGo to find the only last available revenue for the Company.
Second, use Carbon Emissions Factors to find the Supply Chain Emission Factors with Margins that is closest to that for the company.
Third, use Math Calculator to multiply the emissions factor with the revenue. If revenue is not provided, generate a random number instead.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
'''
new_block.agent.llm_chain.prompt.messages[0].prompt.template = FIXED_PROMPT

# FOR INDIV FILE TESTING ONLY
if __name__ == '__main__':
    # print(data)
    # st.write(data)
    while True:
        new_block(input("> "))