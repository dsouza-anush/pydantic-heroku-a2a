"""
Demonstration of communication between agents using Pydantic AI.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from pydantic_ai.tools import Tool

from app.agents.heroku_agent import create_heroku_agent
from app.agents.assistant_agent import ResearchAssistantAgent

class ResearchInput(BaseModel):
    """Input model for the research tool."""
    topic: str = Field(..., description="The topic to research")
    context: Optional[str] = Field(None, description="Additional context or specific questions about the topic")

class ResearchOutput(BaseModel):
    """Output model for the research tool."""
    summary: str = Field(..., description="Summary of the research findings")
    source_agent: str = Field(..., description="Name of the agent that provided the research")

async def research_function(topic: str, context: Optional[str] = None) -> Dict[str, Any]:
    """
    Research a topic using a specialized research agent.
    
    Args:
        topic: The topic to research
        context: Additional context or specific questions about the topic
        
    Returns:
        Dictionary with research summary and source agent name
    """
    # Create the research assistant agent
    research_agent = ResearchAssistantAgent()
    
    # Construct the prompt for the research agent
    prompt = f"Please research the following topic: {topic}"
    if context:
        prompt += f"\n\nContext: {context}"
    
    # Send the prompt to the research agent
    result = await research_agent.agent.run(prompt)
    
    # Extract the response string from the result
    if hasattr(result, 'output'):
        response = result.output
    else:
        response = str(result)
    
    # Return the research results
    return {
        "summary": response,
        "source_agent": research_agent.name
    }

# Create a Tool from the function
research_tool = Tool(
    name="research",
    description="Delegate research tasks to a specialized research agent",
    function=research_function
)

async def demonstrate_a2a_communication(query: str, context: Optional[str] = None) -> Dict[str, Any]:
    """Demonstrate communication between a main agent and a research agent.
    
    Args:
        query: The query to process
        context: Optional context for the query
        
    Returns:
        A dictionary with the results of the communication
    """
    # Create the main agent with the research tool
    main_agent = create_heroku_agent(
        name="main_agent",
        tools=[research_tool],
        use_registry_tools=True
    )
    
    # Process the query with the main agent
    # This will potentially invoke the research tool, which will communicate with the research agent
    result = await main_agent.run(
        f"I need information about '{query}'. {context or ''} Use the research tool if needed."
    )
    
    # Extract the response string from the result
    if hasattr(result, 'output'):
        response = result.output
    else:
        response = str(result)
    
    return {
        "query": query,
        "context": context,
        "response": response
    }