"""
Implementation of a research assistant agent using Pydantic AI.
"""
from typing import List, Optional
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.heroku import HerokuProvider
from app.config import INFERENCE_API_KEY, MODEL_ID

class ResearchAssistantAgent:
    """A research assistant agent that can communicate with our main agent."""
    
    def __init__(self, name: str = "research_assistant", api_key: Optional[str] = None):
        """Initialize the research assistant agent.
        
        Args:
            name: The name of the agent
            api_key: The Heroku Inference API key
        """
        self.name = name
        self.api_key = api_key or INFERENCE_API_KEY
        
        if not self.api_key:
            raise ValueError("INFERENCE_API_KEY must be provided")
        
        # Create the OpenAI model with Heroku provider
        self.model = OpenAIModel(
            MODEL_ID,
            provider=HerokuProvider(api_key=self.api_key),
        )
        
        # Create the agent
        self.agent = Agent(
            model=self.model,
        )
        
        # Set system instructions
        self._set_system_instructions()
    
    def _set_system_instructions(self):
        """Set the system instructions for the research assistant agent."""
        system_prompt = """
        You are a research assistant agent that helps the main agent with research tasks.
        When asked to research a topic:
        1. Consider what's likely already known about the topic
        2. Focus on filling knowledge gaps or providing deeper context
        3. Structure your response with clear sections and bullet points for readability
        4. Include key facts, figures, and definitions relevant to the topic
        5. If the query is ambiguous, clarify what specific aspect you're addressing
        
        Your response should be comprehensive yet concise, focusing on quality information
        rather than excessive detail. Always maintain a professional, informative tone.
        """
        
        self.agent.system_prompt = system_prompt