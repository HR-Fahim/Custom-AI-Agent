# Necessary imports
import os
import openai

from langchain import OpenAI, ConversationChain
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory

# Initization of .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Memory to save data
memory = ConversationBufferMemory()

# Prompt template
prompt_template = """
You are a smart AI assistant to help the user to plan a birthday party.
Users may provide deatils about the party such as location, number of guests, food preference, and more.
You should recommand suggestions to book the best veneues, caterers, and entertainment options for the party, explaining its choices along the way.
You should remember the user's previous requests and adjust the party plan if the user changes their mind or adds new requirements.
User: {user_input}
Assistant:
"""
template = ChatPromptTemplate.from_template(template=prompt_template)

# Initialization model with memory
model = OpenAI(model_name="gpt-3.5-turbo", temperature=0.5)

conversation = ConversationChain(
    llm=model, memory=memory, prompt_template=template
)