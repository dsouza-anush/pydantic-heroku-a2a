"""
Mock search tool for demonstrating Pydantic AI tool usage.
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from pydantic_ai.tools import Tool

class SearchInput(BaseModel):
    """Input model for the search tool."""
    query: str = Field(..., description="The search query to execute")
    max_results: int = Field(default=5, description="Maximum number of results to return")

class SearchResult(BaseModel):
    """Model for a single search result."""
    title: str = Field(..., description="Title of the search result")
    url: str = Field(..., description="URL of the search result")
    snippet: str = Field(..., description="Snippet from the search result")

class SearchOutput(BaseModel):
    """Output model for the search tool."""
    results: List[SearchResult] = Field(..., description="List of search results")
    query: str = Field(..., description="The original search query")
    total_results_found: int = Field(..., description="Total number of results found")

# Mock database of search results
mock_results = {
    "python": [
        {
            "title": "Python (programming language) - Wikipedia",
            "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
            "snippet": "Python is a high-level, interpreted, general-purpose programming language."
        },
        {
            "title": "Python.org",
            "url": "https://www.python.org/",
            "snippet": "The official home of the Python Programming Language."
        },
        {
            "title": "Learn Python - Free Interactive Python Tutorial",
            "url": "https://www.learnpython.org/",
            "snippet": "Learn Python, a powerful programming language used for many different applications."
        }
    ],
    "agent": [
        {
            "title": "Agent Protocol",
            "url": "https://agentprotocol.ai/",
            "snippet": "A common interface for AI agents."
        },
        {
            "title": "A2A Protocol",
            "url": "https://github.com/a2aproject/a2a-python",
            "snippet": "Official Python SDK for the Agent-to-Agent (A2A) protocol."
        }
    ],
    "heroku": [
        {
            "title": "Heroku: Cloud Application Platform",
            "url": "https://www.heroku.com/",
            "snippet": "Heroku is a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud."
        },
        {
            "title": "Heroku Inference",
            "url": "https://elements.heroku.com/addons/heroku-inference",
            "snippet": "Add-on for accessing AI inference capabilities within your Heroku application."
        }
    ]
}

def search_function(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Search for information based on the query.
    
    Args:
        query: The search query to execute
        max_results: Maximum number of results to return
        
    Returns:
        Dictionary with search results, query, and total results found
    """
    query_terms = query.lower().split()
    all_results = []
    
    # Find results that match any of the query terms
    for term in query_terms:
        for key, results in mock_results.items():
            if term in key:
                all_results.extend(results)
    
    # Deduplicate results based on URL
    unique_results = {}
    for result in all_results:
        if result["url"] not in unique_results:
            unique_results[result["url"]] = result
    
    results_list = list(unique_results.values())[:max_results]
    
    return {
        "results": results_list,
        "query": query,
        "total_results_found": len(results_list)
    }

# Create a Tool from the function
search_tool = Tool(
    name="search",
    description="Search for information on the web",
    function=search_function,
    input=SearchInput,
    output=SearchOutput
)