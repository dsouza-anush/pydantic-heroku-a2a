"""
Tests for the Heroku agent functionality.
"""
import os
import pytest
import asyncio
from unittest.mock import patch, MagicMock

from app.agents.heroku_agent import HerokuOpenAI, create_heroku_agent
from app.tools.registry import tool_registry
from app.tools.calculator import CalculatorTool
from app.tools.search import SearchTool

# Skip tests if API key is not set
pytestmark = pytest.mark.skipif(
    os.environ.get("HEROKU_API_KEY") is None,
    reason="HEROKU_API_KEY environment variable not set"
)

class TestHerokuAgent:
    """Tests for the Heroku agent."""
    
    def test_heroku_openai_init_missing_api_key(self):
        """Test that HerokuOpenAI raises an error when API key is missing."""
        with patch.dict(os.environ, {"HEROKU_API_KEY": ""}):
            with patch('app.config.HEROKU_API_KEY', None):
                with pytest.raises(ValueError, match="HEROKU_API_KEY must be provided"):
                    HerokuOpenAI()
    
    def test_create_heroku_agent_with_tools(self):
        """Test creating a Heroku agent with tools."""
        # Mock the HerokuOpenAI client
        with patch('app.agents.heroku_agent.HerokuOpenAI') as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            
            # Create the agent
            agent = create_heroku_agent()
            
            # Check that the client was created with the correct parameters
            mock_client_class.assert_called_once()
            
            # Check that the agent has tools
            assert len(agent.tools) > 0
    
    def test_create_heroku_agent_without_registry_tools(self):
        """Test creating a Heroku agent without registry tools."""
        # Mock the HerokuOpenAI client
        with patch('app.agents.heroku_agent.HerokuOpenAI') as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            
            # Create a custom tool
            custom_tool = MagicMock()
            
            # Create the agent with no registry tools
            agent = create_heroku_agent(use_registry_tools=False, tools=[custom_tool])
            
            # Check that the agent has only the custom tool
            assert len(agent.tools) == 1
            assert custom_tool in agent.tools

class TestToolRegistry:
    """Tests for the tool registry."""
    
    def test_tool_registry_initialization(self):
        """Test that the tool registry is initialized with the correct tools."""
        # Check that the registry has the expected tools
        assert "calculator" in tool_registry.get_tool_names()
        assert "search" in tool_registry.get_tool_names()
        
        # Check that we can get all tools
        all_tools = tool_registry.get_all_tools()
        assert len(all_tools) == 2
        
        # Check that the tools are of the correct types
        tool_types = [type(tool) for tool in all_tools]
        assert CalculatorTool in tool_types
        assert SearchTool in tool_types
    
    def test_get_tool_by_name(self):
        """Test getting a tool by name."""
        calculator_tool = tool_registry.get_tool_by_name("calculator")
        assert calculator_tool is not None
        assert calculator_tool().name == "calculator"
        
        search_tool = tool_registry.get_tool_by_name("search")
        assert search_tool is not None
        assert search_tool().name == "search"
        
        # Test with a non-existent tool
        assert tool_registry.get_tool_by_name("nonexistent") is None