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
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

# Search tool initialization
search = TavilySearchResults(max_results=2, api_key=os.getenv("TAVILY_API_KEY"))

# Flask initialization
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    tools = [search]

    memory = MemorySaver()

    agent_executor = create_react_agent(model, tools, checkpointer=memory)

    body_text = request.get_json()

    print(body_text.get('thread_id')) # debug
    print(body_text.get('user_input')) # debug

    # response = query_ai_agent(user_input)

    config = {"configurable": {"thread_id": body_text.get('thread_id')}} # threadID to track user

    # @TODO: Syncronus streaming check
    # for chunk in agent_executor.stream(
    #     {"messages": [HumanMessage(content=body_text.get('user_input'))]}, config
    # ):
    #     print(str(chunk)) # debug

    #     return jsonify({"response": str(chunk)})

if __name__ == '__main__':
    app.run(debug=True)