# Pydantic Heroku A2A Demo

A demonstration project showing how to build agents using the Agent-to-Agent (A2A) protocol with Heroku Inference for LLM capabilities.

## Features

- Uses the official [A2A Python SDK](https://github.com/a2aproject/a2a-python) for agent communication
- Integrates with Heroku Inference API for LLM capabilities
- Implements custom tools (calculator, search)
- Demonstrates agent-to-agent communication
- Provides tests and examples

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
heroku addons:create heroku-inference:claude-3-4-sonnet -a your-app-name
```

3. Get your Heroku Inference API key:

```bash
heroku config:get HEROKU_INFERENCE_KEY -a your-app-name
```

4. Add this key to your `.env` file:

```
HEROKU_API_KEY=your-key-here
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

Note: Tests that require the Heroku API key will be skipped if the `HEROKU_API_KEY` environment variable is not set.

## Deploying to Heroku

1. Create a `Procfile` (already included in the repository):

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Create a `runtime.txt` file:

```
python-3.9.15
```

3. Deploy to Heroku:

```bash
git add .
git commit -m "Initial commit"
git push heroku main
```

4. Scale the dyno:

```bash
heroku ps:scale web=1
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
├── tests/                  # Test code
│   ├── __init__.py
│   ├── test_heroku_agent.py
│   ├── test_tools.py
│   └── test_a2a_communication.py
├── .env.example            # Example environment file
├── .gitignore              # Git ignore file
├── main.py                 # Main entry point
├── a2a_demo.py             # A2A demo entry point
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Dependencies
├── PROJECT_REFERENCE.md    # Project reference document
└── README.md               # Documentation
```

## Further Development

- Add more tools to enhance agent capabilities
- Implement more complex agent-to-agent communication patterns
- Create a web interface for interacting with the agents
- Add monitoring and logging for agent interactions
- Support additional LLM providers