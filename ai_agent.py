import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

load_dotenv()

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

# openai_llm=ChatOpenAI(model="gpt-4o-mini")
# groq_llm=ChatGroq(model="llama-3.3-70b-versatile")
# system_prompt="Act as an AI chatbot who is smart and friendly."

def get_response_from_agent(model,query,allow_search,system_prompt,provider):

    if provider=="Groq":
        llm=ChatGroq(model=model)
    elif provider=="OpenAI":
        llm=ChatOpenAI(model=model)  
    else:
        raise ValueError("Unsupposted model provider {provider}, choose correct model provider.")

    tools=[TavilySearchResults(max_results=2)] if allow_search else[]
   
    agent=create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt
    )
    # query="Tell me about the trends in crypto market."
    state={"messages":query}
    response=agent.invoke(state)
    messages=response["messages"]
    # messages=response.get("messages", [])

    if messages is not None: 
        #   messages: Any | None - Object of type "None" cannot be used as iterable value
        ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
        return ai_messages[-1]
    else:
        print("No response from agent found!")
    
    # ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
    # return ai_messages[-1]





