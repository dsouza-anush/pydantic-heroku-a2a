"""
Implementation of a research assistant agent for A2A demo.
"""
from typing import List, Optional
from a2a import Agent, OpenAI, Tool
from app.config import INFERENCE_API_KEY, MODEL_ID, INFERENCE_URL

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
        
        # Create the OpenAI client for Heroku
        self.client = OpenAI(
            api_key=self.api_key,
            model=MODEL_ID,
            base_url=f"{INFERENCE_URL}/v1"
        )
        
        # Create the agent
        self.agent = Agent(
            name=self.name,
            llm=self.client,
            tools=[]  # No tools for the assistant agent
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