"""
Tests for the tool implementations.
"""
import pytest
import asyncio
from unittest.mock import patch, MagicMock

from app.tools.calculator import CalculatorTool, CalculateInput, CalculateOutput
from app.tools.search import SearchTool, SearchInput, SearchOutput

class TestCalculatorTool:
    """Tests for the calculator tool."""
    
    @pytest.mark.asyncio
    async def test_calculator_addition(self):
        """Test calculator addition."""
        calculator = CalculatorTool()
        result = await calculator.execute(CalculateInput(expression="2 + 2"))
        assert isinstance(result, CalculateOutput)
        assert result.result == 4
        assert result.expression == "2 + 2"
    
    @pytest.mark.asyncio
    async def test_calculator_complex_expression(self):
        """Test calculator with a more complex expression."""
        calculator = CalculatorTool()
        result = await calculator.execute(CalculateInput(expression="sqrt(16) + 5 * 2"))
        assert isinstance(result, CalculateOutput)
        assert result.result == 14
        assert result.expression == "sqrt(16) + 5 * 2"
    
    @pytest.mark.asyncio
    async def test_calculator_error_handling(self):
        """Test calculator error handling."""
        calculator = CalculatorTool()
        result = await calculator.execute(CalculateInput(expression="1 / 0"))
        assert isinstance(result, CalculateOutput)
        assert "Error" in result.expression
        assert "division by zero" in result.expression.lower()

class TestSearchTool:
    """Tests for the search tool."""
    
    @pytest.mark.asyncio
    async def test_search_basic_query(self):
        """Test search with a basic query."""
        search = SearchTool()
        result = await search.execute(SearchInput(query="python"))
        
        assert isinstance(result, SearchOutput)
        assert len(result.results) > 0
        assert result.query == "python"
        assert result.total_results_found > 0
    
    @pytest.mark.asyncio
    async def test_search_max_results(self):
        """Test search with max_results parameter."""
        search = SearchTool()
        result = await search.execute(SearchInput(query="python", max_results=1))
        
        assert isinstance(result, SearchOutput)
        assert len(result.results) <= 1
        assert result.query == "python"
    
    @pytest.mark.asyncio
    async def test_search_no_results(self):
        """Test search with a query that has no results."""
        search = SearchTool()
        result = await search.execute(SearchInput(query="xyzabc123nonexistent"))
        
        assert isinstance(result, SearchOutput)
        assert len(result.results) == 0
        assert result.query == "xyzabc123nonexistent"
        assert result.total_results_found == 0