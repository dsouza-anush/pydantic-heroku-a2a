"""
Main entry point for the Pydantic Heroku A2A demo application.
"""
import os
from dotenv import load_dotenv
from app.agents.heroku_agent import create_heroku_agent
from app.tools.registry import tool_registry

# Load environment variables
load_dotenv()

def main():
    """Main function to demonstrate agent capabilities."""
    print("Creating Heroku Agent with tools...")
    agent = create_heroku_agent()
    
    print(f"Agent created with tools: {tool_registry.get_tool_names()}")
    
    # Example usage
    print("\nExample 1: Basic query")
    response = agent.run(
        "What is the capital of France and what's the weather like there today?"
    )
    print(f"Response: {response}")
    
    print("\nExample 2: Calculator tool usage")
    response = agent.run(
        "Can you calculate the square root of 256 plus 42?"
    )
    print(f"Response: {response}")
    
    print("\nExample 3: Search tool usage")
    response = agent.run(
        "Find me some information about the A2A protocol"
    )
    print(f"Response: {response}")

if __name__ == "__main__":
    main()