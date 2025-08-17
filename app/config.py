"""
Configuration settings for the application.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Heroku API settings
INFERENCE_API_KEY = os.getenv("INFERENCE_API_KEY") or os.getenv("INFERENCE_KEY")
MODEL_ID = os.getenv("MODEL_ID", "claude-4-sonnet")
INFERENCE_URL = os.getenv("INFERENCE_URL", "https://us.inference.heroku.com")

# A2A Protocol settings
DEFAULT_AGENT_NAME = "heroku_demo_agent"