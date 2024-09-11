"""
    Test Code to check API interrogation
    
"""
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Loaded .env
load_dotenv()  

# Model initialization
model = ChatOpenAI(model="gpt-3.5-turbo")

# Test Code to check API interrogation
from langchain_core.messages import HumanMessage

response = model.invoke([HumanMessage(content="How are you?")])
print(response.content)
