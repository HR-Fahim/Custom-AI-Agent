# Imports
import os
import openai
import asyncio
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
tools = [search]

# Memory to save user responses
memory = MemorySaver()
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Flask initialization
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    

    body_text = request.get_json()

    print(body_text.get('thread_id')) # debug
    print(body_text.get('user_input')) # debug

    # Syncronus streaming check for debugging
    # for chunk in agent_executor.stream(
    #     {"messages": [HumanMessage(content=body_text.get('user_input'))]}, config
    # ):
    #     print(str(chunk)) # debug

    #     return jsonify({"response": str(chunk)})

    # Asyncronus streaming
    async def main():

        # Empty string initialization
        generated_text = "" 

        config = {"configurable": {"thread_id": body_text.get('thread_id')}} # threadID to track user

        async for event in agent_executor.astream_events(
            {"messages": [HumanMessage(content=body_text.get('user_input'))]}, config=config, version="v1"
        ):
            kind = event["event"]
            
            # Each node traversal
            if kind == "on_chain_start" and event["name"] == "Agent":
                print(f"Starting agent: {event['name']} with input: {event['data'].get('input')}")

            elif kind == "on_chain_end" and event["name"] == "Agent":
                print(f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}")

            elif kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                generated_text += content  

            elif kind == "on_tool_start":
                print(f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}")

            elif kind == "on_tool_end":
                print(f"Done tool: {event['name']} with output: {event['data'].get('output')}")
        
        # Response output
        return jsonify({"response": generated_text})
        
    return asyncio.run(main())

if __name__ == '__main__':
    app.run(debug=True)