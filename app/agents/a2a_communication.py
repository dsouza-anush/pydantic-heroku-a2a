"""
Demonstration of communication between agents using Pydantic AI.
"""
import asyncio
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

class ResearchTool(Tool):
    """A tool that delegates research tasks to a research assistant agent."""
    
    name: str = "research"
    description: str = "Delegate research tasks to a specialized research agent"
    input_model: type = ResearchInput
    output_model: type = ResearchOutput
    
    def __init__(self):
        """Initialize the research tool."""
        super().__init__()
        # Create the research assistant agent
        self.research_agent = ResearchAssistantAgent()
    
    def execute(self, input_data: ResearchInput) -> ResearchOutput:
        """Execute the research task.
        
        Args:
            input_data: The research input containing the topic to research
            
        Returns:
            The research results
        """
        # Construct the prompt for the research agent
        prompt = f"Please research the following topic: {input_data.topic}"
        if input_data.context:
            prompt += f"\n\nContext: {input_data.context}"
        
        # Send the prompt to the research agent
        response = self.research_agent.agent.run(prompt)
        
        # Return the research results
        return ResearchOutput(
            summary=response,
            source_agent=self.research_agent.name
        )

def demonstrate_a2a_communication(query: str, context: Optional[str] = None) -> Dict[str, Any]:
    """Demonstrate communication between a main agent and a research agent.
    
    Args:
        query: The query to process
        context: Optional context for the query
        
    Returns:
        A dictionary with the results of the communication
    """
    # Create the main agent with the research tool
    research_tool = ResearchTool()
    main_agent = create_heroku_agent(
        name="main_agent",
        tools=[research_tool],
        use_registry_tools=True
    )
    
    # Process the query with the main agent
    # This will potentially invoke the research tool, which will communicate with the research agent
    response = main_agent.run(
        f"I need information about '{query}'. {context or ''} Use the research tool if needed."
    )
    
    return {
        "query": query,
        "context": context,
        "response": response
    }