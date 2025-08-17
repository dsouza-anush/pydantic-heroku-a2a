# Pydantic Heroku A2A Demo Project

## Goal
Build a sample demo app to test the Agent 2 Agent (A2A) protocol using Heroku for inference. The app will:
- Use the official A2A Python SDK to implement agent communication
- Leverage Heroku's OpenAI-compatible chat completions API
- Implement a composable design that can be extended with additional tools
- Demonstrate how to provision A2A protocol for inter-agent communication
- Provide a reference implementation for Heroku users building agents

## Important References

### Heroku Inference API
- Heroku has an OpenAI-compatible chat completions API: https://devcenter.heroku.com/articles/heroku-inference-api-v1-chat-completions
- Heroku Inference add-on: https://elements.heroku.com/addons/heroku-inference
- Add-on creation: `heroku addons:create heroku-inference:claude-4-sonnet -a $APP_NAME`

### A2A Protocol
- Official A2A Python SDK: https://github.com/a2aproject/a2a-python
- Will be used for implementing agent communication

### Pydantic Integration
- Pydantic AI: https://ai.pydantic.dev/a2a/
- OpenAI model with Heroku provider: https://ai.pydantic.dev/models/openai/#heroku-ai
- Sample code:
```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.heroku import HerokuProvider

model = OpenAIModel(
    'claude-3-4-sonnet',
    provider=HerokuProvider(api_key='your-heroku-inference-key'),
)
agent = Agent(model)
```

## Implementation Strategy
The project will primarily focus on using the official A2A Python SDK while incorporating Pydantic for data validation where appropriate. This approach will ensure we follow the official A2A protocol specification while leveraging Heroku's inference capabilities.