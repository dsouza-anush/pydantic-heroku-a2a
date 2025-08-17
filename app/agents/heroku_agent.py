"""
Implementation of a Heroku-backed agent using the A2A Python SDK.
"""
import os
from typing import List, Dict, Any, Optional

from a2a import Agent, OpenAI, Tool
from app.config import HEROKU_API_KEY, MODEL_ID, INFERENCE_URL, DEFAULT_AGENT_NAME
from app.tools.registry import tool_registry

class HerokuOpenAI(OpenAI):
    """Custom OpenAI client that connects to Heroku Inference API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = MODEL_ID):
        """Initialize the Heroku OpenAI client.
        
        Args:
            api_key: The Heroku Inference API key
            model: The model ID to use (defaults to config.MODEL_ID)
        """
        api_key = api_key or HEROKU_API_KEY
        if not api_key:
            raise ValueError("HEROKU_API_KEY must be provided")
            
        # Initialize with the Heroku Inference API endpoint
        super().__init__(
            api_key=api_key,
            model=model,
            base_url=f"{INFERENCE_URL}/v1"
        )

def create_heroku_agent(
    name: str = DEFAULT_AGENT_NAME,
    tools: Optional[List[Tool]] = None,
    use_registry_tools: bool = True
) -> Agent:
    """Create a new A2A agent powered by Heroku Inference.
    
    Args:
        name: The name of the agent
        tools: Optional list of additional tools for the agent
        use_registry_tools: Whether to include tools from the tool registry
        
    Returns:
        An initialized A2A Agent
    """
    # Create the Heroku OpenAI client
    client = HerokuOpenAI()
    
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
        name=name,
        llm=client,
        tools=all_tools
    )
    
    return agent