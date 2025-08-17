"""
Tests for the Agent-to-Agent (A2A) communication functionality.
"""
import os
import pytest
import asyncio
from unittest.mock import patch, MagicMock

from app.agents.a2a_communication import ResearchTool, ResearchInput, ResearchOutput
from app.agents.a2a_communication import demonstrate_a2a_communication
from app.agents.assistant_agent import ResearchAssistantAgent

# Skip tests if API key is not set
pytestmark = pytest.mark.skipif(
    os.environ.get("HEROKU_API_KEY") is None,
    reason="HEROKU_API_KEY environment variable not set"
)

class TestResearchTool:
    """Tests for the research tool."""
    
    @pytest.mark.asyncio
    async def test_research_tool_execution(self):
        """Test the research tool execution with a mocked research agent."""
        # Create a mock research agent
        mock_research_agent = MagicMock()
        mock_research_agent.agent = MagicMock()
        mock_research_agent.name = "mock_research_agent"
        mock_research_agent.agent.a_run = MagicMock()
        mock_research_agent.agent.a_run.return_value = "Mock research results"
        
        # Create the research tool with the mocked agent
        research_tool = ResearchTool()
        research_tool.research_agent = mock_research_agent
        
        # Execute the tool
        result = await research_tool.execute(
            ResearchInput(topic="test topic", context="test context")
        )
        
        # Verify the result
        assert isinstance(result, ResearchOutput)
        assert result.summary == "Mock research results"
        assert result.source_agent == "mock_research_agent"
        
        # Verify the agent was called correctly
        mock_research_agent.agent.a_run.assert_called_once()
        call_args = mock_research_agent.agent.a_run.call_args[0][0]
        assert "test topic" in call_args
        assert "test context" in call_args

class TestA2ACommunication:
    """Tests for the A2A communication functionality."""
    
    @pytest.mark.asyncio
    async def test_demonstrate_a2a_communication(self):
        """Test the A2A communication demonstration with mocked agents."""
        # Mock the main agent
        mock_main_agent = MagicMock()
        mock_main_agent.a_run = MagicMock()
        mock_main_agent.a_run.return_value = "Mock main agent response"
        
        # Mock the create_heroku_agent function
        with patch('app.agents.a2a_communication.create_heroku_agent', return_value=mock_main_agent):
            # Mock the ResearchTool
            with patch('app.agents.a2a_communication.ResearchTool') as mock_research_tool_class:
                mock_research_tool = MagicMock()
                mock_research_tool_class.return_value = mock_research_tool
                
                # Call the demonstration function
                result = await demonstrate_a2a_communication("test query", "test context")
                
                # Verify the result
                assert "query" in result
                assert result["query"] == "test query"
                assert "context" in result
                assert result["context"] == "test context"
                assert "response" in result
                assert result["response"] == "Mock main agent response"
                
                # Verify the main agent was called correctly
                mock_main_agent.a_run.assert_called_once()
                call_args = mock_main_agent.a_run.call_args[0][0]
                assert "test query" in call_args
                assert "test context" in call_args