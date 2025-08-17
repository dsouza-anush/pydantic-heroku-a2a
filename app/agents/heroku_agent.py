"""
Implementation of a Heroku-backed agent using Pydantic AI.
"""
import os
from typing import List, Dict, Any, Optional

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.heroku import HerokuProvider
from pydantic_ai.tools import Tool

from app.config import INFERENCE_API_KEY, MODEL_ID, DEFAULT_AGENT_NAME
from app.tools.registry import tool_registry

def create_heroku_agent(
    name: str = DEFAULT_AGENT_NAME,
    tools: Optional[List[Tool]] = None,
    use_registry_tools: bool = True
) -> Agent:
    """Create a new Pydantic AI agent powered by Heroku Inference.
    
    Args:
        name: The name of the agent
        tools: Optional list of additional tools for the agent
        use_registry_tools: Whether to include tools from the tool registry
        
    Returns:
        An initialized Pydantic AI Agent
    """
    # Check if we have an API key
    if not INFERENCE_API_KEY:
        raise ValueError("INFERENCE_API_KEY must be provided")
    
    # Create the Heroku OpenAI model
    model = OpenAIModel(
        MODEL_ID,
        provider=HerokuProvider(api_key=INFERENCE_API_KEY),
    )
    
    # Collect all tools
    all_tools = []
    
    # Add registry tools if specified
    if use_registry_tools:
        all_tools.extend(tool_registry.get_all_tools())
    
    # Add any additional tools provided
    if tools:
        all_tools.extend(tools)
    
    # Create and configure the agent
    agent = Agent(
        model=model,
        tools=all_tools
    )
    
    return agent