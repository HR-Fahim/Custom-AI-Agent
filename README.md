## Custom AI Agent

This project demonstrates a custom AI agent that responds to user inputs based on preferences and searches. Flask is used as the backend, JavaScript is used for client-side interaction, and the LangChain framework is used for the assistant. Also here used a thread ID that allows the AI agent to track user sessions and manage asynchronous requests.

#### Visit Custom AI Page: [Click Here](https://custom-ai-agent.onrender.com)

_<sub>**Note:** As here used Render for free deployment, it may get idle after few moments. Implemented here continuous intergration to on Git actions to keep the Render service alive. If it still shows inactive please let me know.</sub>_

![screenshot](image.png)

## Key Features

**Thread ID Management:** To keep track of the context of the conversation, a unique thread ID is generated for every session. As a result, the AI agent is able to retain user preferences throughout the session.

**Asynchronous Processing:** The AI assistant is effective for lengthy or complicated queries because it handles streaming responses using asynchronous techniques.

**Tavily Search API:** To improve the assistant's functionality, this project incorporates a search tool (TavilySearchResults).
