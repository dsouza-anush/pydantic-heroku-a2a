"""
Simple calculator tool for demonstrating A2A tool usage.
"""
import math
from typing import Dict, Any, Optional
from a2a import Tool
from pydantic import BaseModel, Field

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

class CalculatorTool(Tool):
    """A basic calculator tool that can evaluate mathematical expressions."""
    
    name: str = "calculator"
    description: str = "Evaluates mathematical expressions"
    input_schema: type = CalculateInput
    output_schema: type = CalculateOutput
    
    async def execute(self, input_data: CalculateInput) -> CalculateOutput:
        """Execute the calculation.
        
        Args:
            input_data: The calculation input containing the expression to evaluate
            
        Returns:
            The calculation result
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
        expression = input_data.expression.replace('^', '**')
        
        try:
            # Evaluate the expression in a safe context
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            return CalculateOutput(result=float(result), expression=input_data.expression)
        except Exception as e:
            return CalculateOutput(
                result=float('nan'),
                expression=f"Error evaluating {input_data.expression}: {str(e)}"
            )