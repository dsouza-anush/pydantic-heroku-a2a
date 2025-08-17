"""
Tool registry for managing available tools.
"""
from typing import Dict, List, Type, Optional

from pydantic_ai.tools import Tool
from app.tools.calculator import CalculatorTool
from app.tools.search import SearchTool

class ToolRegistry:
    """Registry for managing available tools."""
    
    def __init__(self):
        """Initialize the tool registry."""
        self._tools: Dict[str, Type[Tool]] = {}
        
        # Register built-in tools
        self.register_tool(CalculatorTool)
        self.register_tool(SearchTool)
    
    def register_tool(self, tool_class: Type[Tool]) -> None:
        """Register a tool with the registry.
        
        Args:
            tool_class: The tool class to register
        """
        tool_instance = tool_class()
        self._tools[tool_instance.name] = tool_class
    
    def get_tool_by_name(self, name: str) -> Optional[Type[Tool]]:
        """Get a tool class by its name.
        
        Args:
            name: The name of the tool to retrieve
            
        Returns:
            The tool class if found, None otherwise
        """
        return self._tools.get(name)
    
    def get_all_tools(self) -> List[Tool]:
        """Get instances of all registered tools.
        
        Returns:
            List of tool instances
        """
        return [tool_cls() for tool_cls in self._tools.values()]
    
    def get_tool_names(self) -> List[str]:
        """Get the names of all registered tools.
        
        Returns:
            List of tool names
        """
        return list(self._tools.keys())

# Create a global tool registry instance
tool_registry = ToolRegistry()