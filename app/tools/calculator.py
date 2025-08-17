"""
Simple calculator tool for demonstrating Pydantic AI tool usage.
"""
import math
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from pydantic_ai.tools import Tool

class CalculateInput(BaseModel):
    """Input model for the calculator tool."""
    expression: str = Field(
        ...,
        description="The mathematical expression to evaluate. Supports basic operators (+, -, *, /, ^) and functions (sin, cos, tan, sqrt)."
    )

class CalculateOutput(BaseModel):
    """Output model for the calculator tool."""
    result: float = Field(..., description="The result of the calculation")
    expression: str = Field(..., description="The original expression")

def calculator_function(expression: str) -> Dict[str, Any]:
    """
    Calculate the result of a mathematical expression.
    
    Args:
        expression: The expression to evaluate
        
    Returns:
        Dictionary with result and original expression
    """
    # Define safe operations
    safe_dict = {
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'sqrt': math.sqrt,
        'pi': math.pi,
        'e': math.e,
    }
    
    # Replace ^ with ** for exponentiation
    expr = expression.replace('^', '**')
    
    try:
        # Evaluate the expression in a safe context
        result = eval(expr, {"__builtins__": {}}, safe_dict)
        return {"result": float(result), "expression": expression}
    except Exception as e:
        return {"result": float('nan'), "expression": f"Error evaluating {expression}: {str(e)}"}

# Create a Tool from the function
calculator_tool = Tool(
    name="calculator",
    description="Evaluates mathematical expressions",
    function=calculator_function,
    input=CalculateInput,
    output=CalculateOutput
)