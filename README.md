# Pydantic Heroku A2A Demo

A demonstration project showing how to build agents using Pydantic AI with Heroku Inference for LLM capabilities, enabling agent-to-agent communication.

## Features

- Uses Pydantic AI for agent implementation
- Integrates with Heroku Inference API for LLM capabilities
- Implements custom tools (calculator, search)
- Demonstrates agent-to-agent communication
- Provides tests and examples

## Agent-to-Agent Communication

The agent-to-agent (A2A) protocol is implemented in `app/agents/a2a_communication.py` and demonstrates how agents can collaborate and delegate tasks to each other.

### Implementation Details

We've implemented a simple but effective agent-to-agent communication pattern:

1. **Primary Agent**: Acts as the first point of contact and processes the initial user query
2. **Secondary Agent**: Reviews and enhances the primary agent's output

This implementation showcases the core concept of agent collaboration:

```python
async def demonstrate_a2a_communication(query: str, context: Optional[str] = None) -> Dict[str, Any]:
    # Create the first agent
    first_agent = create_heroku_agent(name="primary_agent")
    
    # Process the query with the first agent
    first_prompt = f"Please research the following topic: {query}"
    if context:
        first_prompt += f"\n\nContext: {context}"
    
    # Get response from first agent
    result = await first_agent.run(first_prompt)
    first_response = extract_response_text(result)
    
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
    final_response = extract_response_text(result)
    
    return {
        "query": query,
        "context": context,
        "response": final_response
    }
```

### Testing A2A Communication

You can test the A2A communication using the `/a2a` endpoint:

```bash
curl -X POST https://pydantic-heroku-a2a-10c8e5734aae.herokuapp.com/a2a \
    -H "Content-Type: application/json" \
    -H "X-API-Key: demo-api-key-123" \
    -d '{"query": "What is the Agent to Agent protocol?", "context": "I need a brief explanation."}'
```

This demonstrates the core principle of the A2A protocol where agents can collaborate to produce better results than they could individually.

### Benefits of A2A Communication

- **Enhanced Outputs**: The second agent can expand on, correct, or refine the first agent's response
- **Specialization**: Each agent can focus on a specific aspect of the problem
- **Improved Reliability**: Multiple agents working together can produce more reliable results

## Prerequisites

- Python 3.8+
- A Heroku account
- Heroku CLI installed
- Heroku Inference add-on

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/pydantic-heroku-a2a.git
cd pydantic-heroku-a2a
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:

```bash
cp .env.example .env
```

5. Edit the `.env` file and add your Heroku Inference API key.

## Setting Up Heroku

1. Create a new Heroku application:

```bash
heroku create your-app-name
```

2. Add the Heroku Inference add-on:

```bash
heroku addons:create heroku-inference:claude-4-sonnet -a your-app-name -- --region us
```

3. Get your Heroku Inference API key:

```bash
heroku config -a your-app-name
```

4. Add this key to your `.env` file:

```
INFERENCE_API_KEY=your-key-here
MODEL_ID=claude-4-sonnet
API_KEY=your-app-api-key
INFERENCE_URL=https://us.inference.heroku.com
```

## Running the Demo

To run the basic agent demo:

```bash
python main.py
```

To run the Agent-to-Agent communication demo:

```bash
python a2a_demo.py
```

## Running Tests

Run the tests with:

```bash
pytest
```

Note: Tests that require the Heroku API key will be skipped if the `INFERENCE_API_KEY` environment variable is not set.

## Deploying to Heroku

1. Create a `.python-version` file (already included in the repository):

```
3.9
```

2. Create a `Procfile` (already included in the repository):

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

3. Deploy to Heroku:

```bash
git add .
git commit -m "Initial commit"
git push heroku main
```

4. Set environment variables on Heroku:

```bash
heroku config:set INFERENCE_API_KEY=your-inference-key MODEL_ID=claude-4-sonnet API_KEY=your-api-key -a your-app-name
```

5. Open the application:

```bash
heroku open
```

## Project Structure

```
├── app/                    # Main application code
│   ├── agents/             # Agent implementations
│   │   ├── __init__.py
│   │   ├── heroku_agent.py          # Heroku agent implementation
│   │   ├── assistant_agent.py       # Research assistant agent 
│   │   └── a2a_communication.py     # A2A communication module
│   ├── tools/              # Tool implementations
│   │   ├── __init__.py
│   │   ├── calculator.py            # Calculator tool
│   │   ├── search.py                # Search tool
│   │   └── registry.py              # Tool registry
│   ├── __init__.py
│   └── config.py           # Configuration settings
│   └── main.py             # FastAPI application
├── tests/                  # Test code
│   ├── __init__.py
│   ├── test_heroku_agent.py
│   ├── test_tools.py
│   └── test_a2a_communication.py
├── .env.example            # Example environment file
├── .python-version         # Python version for Heroku
├── .gitignore              # Git ignore file
├── main.py                 # Main entry point
├── a2a_demo.py             # A2A demo entry point
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Dependencies
├── Procfile                # Heroku Procfile
├── PROJECT_REFERENCE.md    # Project reference document
└── README.md               # Documentation
```

## Further Development

- Add more tools to enhance agent capabilities
- Implement more complex agent-to-agent communication patterns
- Create a web interface for interacting with the agents
- Add monitoring and logging for agent interactions
- Support additional LLM providers