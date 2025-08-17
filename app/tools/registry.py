"""
Tool registry for managing available tools.
"""
from typing import Dict, List, Any

from pydantic_ai.tools import Tool
from app.tools.calculator import calculator_tool
from app.tools.search import search_tool

class ToolRegistry:
    """Registry for managing available tools."""
    
    def __init__(self):
        """Initialize the tool registry."""
        self._tools: Dict[str, Tool] = {}
        
        # Register built-in tools
        self.register_tool(calculator_tool)
        self.register_tool(search_tool)
    
    def register_tool(self, tool: Tool) -> None:
        """Register a tool with the registry.
        
        Args:
            tool: The tool to register
        """
        self._tools[tool.name] = tool
    
    def get_tool_by_name(self, name: str) -> Tool:
        """Get a tool by its name.
        
        Args:
            name: The name of the tool to retrieve
            
        Returns:
            The tool if found, None otherwise
        """
        return self._tools.get(name)
    
    def get_all_tools(self) -> List[Tool]:
        """Get all registered tools.
        
        Returns:
            List of all registered tools
        """
        return list(self._tools.values())
    
    def get_tool_names(self) -> List[str]:
        """Get the names of all registered tools.
        
        Returns:
            List of tool names
        """
        return list(self._tools.keys())

# Create a global tool registry instance
tool_registry = ToolRegistry()