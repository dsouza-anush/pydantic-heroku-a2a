"""
Simplified implementation of agent-to-agent communication.
"""
from typing import Dict, Any, Optional

from app.agents.heroku_agent import create_heroku_agent

async def demonstrate_a2a_communication(query: str, context: Optional[str] = None) -> Dict[str, Any]:
    """Demonstrate a simple agent-to-agent communication pattern.
    
    Args:
        query: The query to process
        context: Optional context for the query
        
    Returns:
        A dictionary with the results of the communication
    """
    # Create the first agent
    first_agent = create_heroku_agent(name="primary_agent")
    
    # Process the query with the first agent
    first_prompt = f"Please research the following topic: {query}"
    if context:
        first_prompt += f"\n\nContext: {context}"
    
    # Get response from first agent
    result = await first_agent.run(first_prompt)
    
    # Extract the response string from the result
    if hasattr(result, 'output'):
        first_response = result.output
    else:
        first_response = str(result)
    
    # Create a second agent with knowledge of the first response
    second_agent = create_heroku_agent(name="secondary_agent")
    
    # Have the second agent review and enhance the first agent's response
    second_prompt = f"""You are reviewing another AI assistant's response about '{query}'. 
    Please enhance this response by adding more details, correcting any errors, and making it more comprehensive.
    
    Original response: 
    {first_response}
    
    Your improved response:"""
    
    # Get enhanced response from second agent
    result = await second_agent.run(second_prompt)
    
    # Extract the response string from the result
    if hasattr(result, 'output'):
        final_response = result.output
    else:
        final_response = str(result)
    
    return {
        "query": query,
        "context": context,
        "response": final_response
    }