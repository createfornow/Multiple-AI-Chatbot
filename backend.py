from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from ai_agent import get_response_from_agent

class RequestState(BaseModel):
    model_name: str
    model_provider:str
    system_prompt:str
    messages:List[str]
    allow_search:bool


app=FastAPI(title="Langgraph AI Agent")

ALLOWED_MODEL_LIST=["llama3-70b-8192","mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-4o-mini"]
@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API Endpoint to interact with the chatbot using LangGraph and search tool.
    It dynamically select the model specified in the request.
    """
    if request.model_name not in ALLOWED_MODEL_LIST:
        return {"Error": "Invalid model name. Kindly select a valid model."}
    
    model=request.model_name
    query=request.messages
    allow_search=request.allow_search
    system_prompt=request.system_prompt
    provider=request.model_provider
    
    response=get_response_from_agent(model,query,allow_search,system_prompt,provider)
    return response

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)

    