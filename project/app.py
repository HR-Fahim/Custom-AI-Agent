# Imports
import os
import openai
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain.prompts import PromptTemplate
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

# Template for the system prompt
template = PromptTemplate(
    template="""
    You are a smart AI assistant to help user according to their preferences.
    Users may ask questions based on a specific topic that they want to know in detail.
    Users may provide information about the topic such as location, budget, food preference, and more.
    You should recommend best suggestions based on the user's preferences, explaining its choices along the way.
    You should remember the user's previous requests and adjust the information if the user changes decisions or adds new requirements.
    You should also ask questions wheather the user wants to know anything more.
    User: {user_input}
    Assistant:
    """
)

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

    prompt = template.format(user_input=body_text.get('user_input'))

    # @TODO: Syncronus streaming (check for debugging and can be impelemented only if needed)
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
            {"messages": [HumanMessage(content=prompt)]}, config=config, version="v1"
        ):
            kind = event["event"]

            print(kind) # debug
            
            # Each node traversal
            if kind == "on_chain_start" and event["name"] == "Agent":
                print("Starting agent: {event['name']} with input: {event['data'].get('input')}") # debug

            elif kind == "on_chain_end" and event["name"] == "Agent":
                print("Done agent: {event['name']} with output: {event['data'].get('output')['output']}") # debug

            elif kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                generated_text += content  

            elif kind == "on_tool_start":
                print("Starting tool: {event['name']} with inputs: {event['data'].get('input')}") # debug

            elif kind == "on_tool_end":
                print("Done tool: {event['name']} with output: {event['data'].get('output')}") # debug
        
        # Response output
        return jsonify({"response": generated_text})
        
    return asyncio.run(main())

if __name__ == '__main__':
    app.run(debug=True)