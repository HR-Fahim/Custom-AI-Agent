# Imports
import os
import openai
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from flask import Flask, render_template, request, jsonify

# Loaded .env
load_dotenv() 

# Initization of .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Model initialization
model = ChatOpenAI(model="gpt-3.5-turbo")

# Search tool initialization
search = TavilySearchResults(max_results=2, api_key=os.getenv("TAVILY_API_KEY"))

# Flask initialization
app = Flask(__name__)

# Flask routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    tools = [search]

    memory = MemorySaver()

    agent_executor = create_react_agent(model, tools, checkpointer=memory)

    user_input = request.get_json()

    print(user_input) # debug

    # response = query_ai_agent(user_input)

    config = {"configurable": {"thread_id": "abc123"}} # Will modify to track user session

    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content=user_input)]}, config
    ):
        print(chunk)
        return jsonify({"response": chunk})

if __name__ == '__main__':
    app.run(debug=True)