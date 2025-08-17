"""
FastAPI application for serving the Heroku agent via a REST API.
"""
import os
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel

from app.config import INFERENCE_API_KEY
from app.agents.heroku_agent import create_heroku_agent
from app.tools.registry import tool_registry
from app.agents.a2a_communication import demonstrate_a2a_communication

app = FastAPI(
    title="Heroku Pydantic AI Demo",
    description="A demonstration of Pydantic AI with Heroku Inference",
    version="0.1.0",
)

class QueryRequest(BaseModel):
    """Request model for querying the agent."""
    query: str
    tools: Optional[List[str]] = None

class QueryResponse(BaseModel):
    """Response model for agent queries."""
    response: str
    tools_used: Optional[List[str]] = None

class A2ARequest(BaseModel):
    """Request model for agent-to-agent communication."""
    query: str
    context: Optional[str] = None

class A2AResponse(BaseModel):
    """Response model for agent-to-agent communication."""
    query: str
    context: Optional[str]
    response: str

async def verify_api_key(x_api_key: str = Header(None)):
    """Verify the API key.
    
    Args:
        x_api_key: The API key from the request header
        
    Returns:
        True if the API key is valid
        
    Raises:
        HTTPException: If the API key is invalid
    """
    expected_key = os.environ.get("API_KEY")
    if expected_key and expected_key != x_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Heroku Pydantic AI Demo API",
        "available_tools": tool_registry.get_tool_names()
    }

@app.get("/tools")
async def list_tools():
    """List available tools."""
    return {
        "tools": tool_registry.get_tool_names()
    }

@app.post("/query", response_model=QueryResponse)
async def query_agent(
    request: QueryRequest,
    _: bool = Depends(verify_api_key)
):
    """Query the agent.
    
    Args:
        request: The query request
        
    Returns:
        The agent's response
    """
    try:
        # Create an agent with the requested tools
        requested_tools = []
        if request.tools:
            for tool_name in request.tools:
                tool = tool_registry.get_tool_by_name(tool_name)
                if tool:
                    requested_tools.append(tool)
            
            # Create an agent with only the requested tools
            agent = create_heroku_agent(
                tools=requested_tools,
                use_registry_tools=False
            )
        else:
            # Create an agent with all tools
            agent = create_heroku_agent()
        
        # Process the query
        result = await agent.run(request.query)
        
        # Extract the response string from the result
        if hasattr(result, 'output'):
            response = result.output
        else:
            response = str(result)
        
        # Return the response
        tools_used = []
        if hasattr(agent, 'tools'):
            tools_used = [tool.name for tool in agent.tools]
        
        return QueryResponse(
            response=response,
            tools_used=tools_used
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@app.post("/a2a", response_model=A2AResponse)
async def agent_to_agent(
    request: A2ARequest,
    _: bool = Depends(verify_api_key)
):
    """Demonstrate agent-to-agent communication.
    
    Args:
        request: The a2a request
        
    Returns:
        The result of agent-to-agent communication
    """
    try:
        # Call the a2a demonstration function
        result = await demonstrate_a2a_communication(request.query, request.context)
        
        return A2AResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing A2A request: {str(e)}"
        )